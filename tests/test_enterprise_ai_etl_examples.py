"""Unit tests for the enterprise AI ETL and multi-tenant RLS examples."""

import ast
import asyncio
import copy
import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any

import pytest
import yaml

from tests.test_dual_render_diagrams import (
    extract_mermaid_blocks,
    extract_routing_tables,
    extract_svg_blocks,
)


REPO_ROOT = Path(__file__).parent.parent
ETL_SPEC = REPO_ROOT / "docs/reference/enterprise-ai-etl-lifecycle-and-multi-tenancy.md"
CONSUMPTION_SPEC = REPO_ROOT / "docs/reference/consumption-and-integration-layer.md"
POSTGRES_SPEC = REPO_ROOT / "docs/reference/postgresql-pgvector-enterprise-strategy.md"
ALLOWED_ROLES = {"INTERNAL_STAFF", "EXTERNAL_CLIENT"}


def _extract_fence(path: Path, language: str, marker: str) -> str:
    """Return the fenced example in ``path`` containing ``marker``."""
    content = path.read_text(encoding="utf-8")
    blocks = re.findall(rf"```{re.escape(language)}\n([\s\S]*?)\n```", content)
    matches = [block for block in blocks if marker in block]
    assert len(matches) == 1, f"Expected one {language} block containing {marker!r} in {path}"
    return matches[0]


def _load_definition(
    source: str,
    name: str,
    namespace: dict[str, Any],
    *,
    drop_defaults: bool = False,
) -> Any:
    """Compile one class or function from a documented Python example."""
    tree = ast.parse(source)
    definition = next(
        node
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == name
    )
    definition = copy.deepcopy(definition)
    definition.decorator_list = []
    if drop_defaults and isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef)):
        definition.args.defaults = []
        definition.args.kw_defaults = [None] * len(definition.args.kwonlyargs)

    module = ast.Module(
        body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), definition],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)
    exec(compile(module, str(name), "exec"), namespace)
    return namespace[name]


class _CharacterTokenizer:
    """Provide deterministic character-level tokenisation for chunking tests."""

    @staticmethod
    def encode(text: str) -> list[str]:
        """Represent each character as one token."""
        return list(text)

    @staticmethod
    def decode(tokens: list[str]) -> str:
        """Convert character tokens back into text."""
        return "".join(tokens)


class _FlowFileTransformResult:
    """Capture a documented NiFi transform result without requiring NiFi."""

    def __init__(self, **kwargs: Any) -> None:
        """Retain result fields for assertions."""
        self.__dict__.update(kwargs)


class _FlowFile:
    """Expose the subset of the NiFi FlowFile API used by the example."""

    def __init__(self, content: str, attributes: dict[str, Any]) -> None:
        """Store synthetic contents and attributes."""
        self.content = content
        self.attributes = attributes

    def getContentsAsBytes(self) -> bytes:  # noqa: N802
        """Return UTF-8 encoded synthetic contents."""
        return self.content.encode("utf-8")

    def getAttribute(self, name: str) -> Any:  # noqa: N802
        """Return one synthetic FlowFile attribute."""
        return self.attributes.get(name)


class _Vector(list[float]):
    """Mimic a model vector exposing ``tolist``."""

    def tolist(self) -> list[float]:
        """Return a plain list representation."""
        return list(self)


class _Model:
    """Record embedding input and return a deterministic vector."""

    def __init__(self) -> None:
        """Initialise an empty call ledger."""
        self.calls: list[str] = []

    def encode(self, value: str) -> _Vector:
        """Record the value and return a fixed vector."""
        self.calls.append(value)
        return _Vector([0.25, 0.75])


class _AsyncContext:
    """Provide a reusable asynchronous context manager."""

    def __init__(self, value: Any) -> None:
        """Store the value returned on entry."""
        self.value = value
        self.entered = False
        self.exited = False

    async def __aenter__(self) -> Any:
        """Mark entry and return the configured value."""
        self.entered = True
        return self.value

    async def __aexit__(self, *args: Any) -> None:
        """Mark context exit."""
        self.exited = True


class _AsyncConnection:
    """Capture asyncpg-style execute and fetch calls."""

    def __init__(self, records: list[dict[str, Any]]) -> None:
        """Store query results and initialise call ledgers."""
        self.records = records
        self.execute_calls: list[tuple[Any, ...]] = []
        self.fetch_calls: list[tuple[Any, ...]] = []
        self.transaction_context = _AsyncContext(None)

    def transaction(self) -> _AsyncContext:
        """Return the transaction context used by the example."""
        return self.transaction_context

    async def execute(self, *args: Any) -> None:
        """Record a session context statement."""
        self.execute_calls.append(args)

    async def fetch(self, *args: Any) -> list[dict[str, Any]]:
        """Record a query and return configured rows."""
        self.fetch_calls.append(args)
        return self.records


class _AsyncPool:
    """Expose one asyncpg-style connection acquisition context."""

    def __init__(self, connection: _AsyncConnection) -> None:
        """Wrap the supplied connection."""
        self.acquire_context = _AsyncContext(connection)

    def acquire(self) -> _AsyncContext:
        """Return the connection acquisition context."""
        return self.acquire_context


def _load_chunker() -> type:
    """Load the documented token-aware chunker with local NiFi substitutes."""
    source = _extract_fence(ETL_SPEC, "python", "class TokenAwareChunker")
    namespace = {
        "json": json,
        "tiktoken": SimpleNamespace(get_encoding=lambda _name: _CharacterTokenizer()),
        "FlowFileTransform": object,
        "FlowFileTransformResult": _FlowFileTransformResult,
    }
    return _load_definition(source, "TokenAwareChunker", namespace)


@pytest.mark.parametrize(
    ("text", "max_tokens", "overlap", "expected"),
    [
        ("", 4, 1, []),
        ("abcd", 4, 1, ["abcd"]),
        ("abcdefghij", 4, 1, ["abcd", "defg", "ghij"]),
        ("abcdefgh", 4, 0, ["abcd", "efgh"]),
    ],
)
def test_token_aware_chunker_boundaries(
    text: str, max_tokens: int, overlap: int, expected: list[str]
) -> None:
    """Verify empty, exact, overlapping, and non-overlapping chunk boundaries."""
    chunker = _load_chunker()()

    assert chunker.chunk_by_tokens(text, max_tokens=max_tokens, overlap=overlap) == expected


def test_token_aware_transform_enriches_every_chunk() -> None:
    """Verify chunk overlap and parent metadata survive NiFi transformation."""
    chunker = _load_chunker()()
    flowfile = _FlowFile(
        "a" * 600,
        {
            "filename": "s3://tenant-a/manual.pdf",
            "page.number": "7",
            "custom.metadata": json.dumps(
                {"author": "A. Writer", "creation_date": "2026-09-11"}
            ),
        },
    )

    result = chunker.transform(None, flowfile)
    records = json.loads(result.contents)

    assert result.relationship == "success"
    assert result.attributes == {"mime.type": "application/json"}
    assert [record["chunk_index"] for record in records] == [0, 1]
    assert [len(record["payload_content"]) for record in records] == [512, 152]
    assert [record["metadata"]["token_count"] for record in records] == [512, 152]
    assert all(record["metadata"]["document_source_url"] == "s3://tenant-a/manual.pdf" for record in records)
    assert all(record["metadata"]["page_number"] == "7" for record in records)
    assert records[0]["metadata"]["author"] == "A. Writer"
    assert records[0]["metadata"]["creation_date"] == "2026-09-11"
    assert records[0]["payload_content"][-64:] == records[1]["payload_content"][:64]


def test_token_aware_transform_uses_safe_metadata_defaults() -> None:
    """Verify absent optional FlowFile metadata produces documented defaults."""
    chunker = _load_chunker()()

    result = chunker.transform(None, _FlowFile("healthy content", {"filename": "input.txt"}))
    metadata = json.loads(result.contents)[0]["metadata"]

    assert metadata == {
        "document_source_url": "input.txt",
        "page_number": 1,
        "author": "unknown",
        "creation_date": "",
        "token_count": 15,
    }


@pytest.mark.parametrize(
    ("text", "language", "expected"),
    [
        (" " * 10, "en", (False, "REJECTED_TOO_SHORT: Content under 50 characters.")),
        ("a" * 49, "en", (False, "REJECTED_TOO_SHORT: Content under 50 characters.")),
        ("a" * 50, "en", (True, "PASSED")),
        ("a" * 50, "ms", (True, "PASSED")),
        ("a" * 50, "fr", (False, "REJECTED_UNSUPPORTED_LANG: Detected fr.")),
        ("é" * 35 + "a" * 65, "en", (True, "PASSED")),
        (
            "é" * 36 + "a" * 64,
            "en",
            (False, "REJECTED_CORRUPTED_ENCODING: High non-ASCII symbol ratio."),
        ),
    ],
)
def test_content_health_validation_boundaries(
    text: str, language: str, expected: tuple[bool, str]
) -> None:
    """Verify minimum length, supported languages, and corruption threshold edges."""
    source = _extract_fence(ETL_SPEC, "python", "def validate_content_health")
    function = _load_definition(
        source,
        "validate_content_health",
        {"detect_language": lambda _text: language},
    )

    assert function(text) == expected


def test_etl_navigation_and_dynamic_parser_inventory() -> None:
    """Verify the new reference is discoverable and every promised parser route exists."""
    navigation = yaml.safe_load((REPO_ROOT / "_data/navigation.yml").read_text(encoding="utf-8"))
    reference = next(section for section in navigation if section["title"] == "Reference")
    item = next(
        item
        for item in reference["items"]
        if item["url"] == "/docs/reference/enterprise-ai-etl-lifecycle-and-multi-tenancy.html"
    )
    summary = (REPO_ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    content = ETL_SPEC.read_text(encoding="utf-8")

    assert item["title"] == "Enterprise AI ETL Lifecycle, Dynamic Multi-Modal Parsing, & Multi-Tenant RLS Specification"
    assert "(docs/reference/enterprise-ai-etl-lifecycle-and-multi-tenancy.md)" in summary
    for route in (
        "Apache Tika / PyPDF",
        "Record Path Parser",
        "AST Parser (Native Python)",
        "GeoJSON Spatial Agent",
    ):
        assert route in content


def test_etl_dual_render_views_describe_the_same_security_flow() -> None:
    """Verify SVG, Mermaid, and routing table retain the core ETL security path."""
    content = ETL_SPEC.read_text(encoding="utf-8")
    svg_blocks = extract_svg_blocks(content)
    mermaid_blocks = extract_mermaid_blocks(content)
    routing_tables = extract_routing_tables(content)

    assert len(svg_blocks) == len(mermaid_blocks) == 1
    routing_table = next(
        table
        for table in routing_tables
        if any(row["source"] == "FastAPI / MCP Server" for row in table)
    )
    for term in ("CDC", "MIME", "PostgreSQL", "RLS", "set_config"):
        assert term.lower() in svg_blocks[0].lower()
    for edge in ("CDCEngine -->", "MimeRouter --> Splitter", "ContextInject -->"):
        assert edge in mermaid_blocks[0]
    routes = {(row["source"], row["target"]) for row in routing_table}
    assert ("`DetectMimeType` Router", "Native Python Worker") in routes
    assert ("FastAPI / MCP Server", "PostgreSQL Master Hub") in routes


def test_sql_examples_enforce_tenant_isolation_and_classification() -> None:
    """Verify deletion, RLS, and DDL examples preserve tenant security boundaries."""
    tombstone = _extract_fence(ETL_SPEC, "sql", "DELETE FROM secure_ai_lakehouse")
    etl_rls = _extract_fence(ETL_SPEC, "sql", "CREATE POLICY internal_staff_policy")
    postgres_ddl = _extract_fence(POSTGRES_SPEC, "sql", "CREATE TABLE enterprise_knowledge_base")

    assert re.search(r"WHERE\s+source_origin\s*=\s*:document_source_url", tombstone)
    assert re.search(r"AND\s+tenant_id\s*=\s*:tenant_id", tombstone)
    assert "ALTER TABLE secure_ai_lakehouse ENABLE ROW LEVEL SECURITY" in etl_rls
    assert "tenant_id = current_setting('app.current_tenant_id', true)" in etl_rls
    assert "access_classification = 'PUBLIC'" in etl_rls
    assert "ALTER TABLE enterprise_knowledge_base ENABLE ROW LEVEL SECURITY" in postgres_ddl
    assert "CHECK (access_classification IN ('PUBLIC', 'RESTRICTED', 'INTERNAL_ONLY'))" in postgres_ddl


def test_secure_tenant_search_injects_context_inside_transaction() -> None:
    """Verify the MCP example binds trusted identity before fetching tenant data."""
    source = _extract_fence(ETL_SPEC, "python", "async def secure_tenant_vector_search")
    connection = _AsyncConnection(
        [{"source_origin": "manual.pdf", "payload_content": "safe", "access_classification": "PUBLIC"}]
    )
    model = _Model()
    namespace = {
        "mcp": SimpleNamespace(
            get_context=lambda: SimpleNamespace(
                user_role="EXTERNAL_CLIENT", tenant_id="tenant-a"
            )
        ),
        "os": SimpleNamespace(getenv=lambda _name: None),
        "ALLOWED_ROLES": ALLOWED_ROLES,
        "model": model,
        "db_pool": _AsyncPool(connection),
        "json": json,
    }
    search = _load_definition(source, "secure_tenant_vector_search", namespace)

    result = json.loads(asyncio.run(search("flood report", 101.7, 2.9, 750.0)))

    assert result == connection.records
    assert model.calls == ["flood report"]
    assert connection.transaction_context.entered and connection.transaction_context.exited
    assert connection.execute_calls == [
        ("SELECT set_config('app.current_user_role', $1, true);", "EXTERNAL_CLIENT"),
        ("SELECT set_config('app.current_tenant_id', $1, true);", "tenant-a"),
    ]
    query, longitude, latitude, radius, vector = connection.fetch_calls[0]
    assert "ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography" in query
    assert (longitude, latitude, radius, vector) == (101.7, 2.9, 750.0, "[0.25, 0.75]")


@pytest.mark.parametrize(
    ("role", "tenant", "message"),
    [
        (None, "tenant-a", "Unauthorised or missing user_role"),
        ("ADMIN", "tenant-a", "Unauthorised or missing user_role"),
        ("EXTERNAL_CLIENT", None, "Missing tenant_id"),
    ],
)
def test_secure_tenant_search_rejects_untrusted_context(
    role: str | None, tenant: str | None, message: str
) -> None:
    """Verify missing or unauthorised MCP identity fails before database access."""
    source = _extract_fence(ETL_SPEC, "python", "async def secure_tenant_vector_search")
    connection = _AsyncConnection([])
    namespace = {
        "mcp": SimpleNamespace(get_context=lambda: SimpleNamespace(user_role=role, tenant_id=tenant)),
        "os": SimpleNamespace(getenv=lambda _name: None),
        "ALLOWED_ROLES": ALLOWED_ROLES,
        "model": _Model(),
        "db_pool": _AsyncPool(connection),
        "json": json,
    }
    search = _load_definition(source, "secure_tenant_vector_search", namespace)

    with pytest.raises(ValueError, match=message):
        asyncio.run(search("query", 0.0, 0.0))

    assert connection.execute_calls == []
    assert connection.fetch_calls == []


def _load_semantic_search(namespace: dict[str, Any]) -> Any:
    """Load the consumption-layer MCP search example."""
    source = _extract_fence(CONSUMPTION_SPEC, "python", "async def semantic_spatial_search")
    return _load_definition(source, "semantic_spatial_search", namespace)


def test_semantic_spatial_search_returns_uninitialised_error() -> None:
    """Verify the MCP search reports startup state before consulting identity context."""
    namespace = {
        "db_pool": None,
        "embedding_model": None,
        "json": json,
        "mcp": SimpleNamespace(get_context=lambda: pytest.fail("context must not be read")),
    }
    search = _load_semantic_search(namespace)

    assert json.loads(asyncio.run(search("query", 1.0, 2.0))) == {
        "error": "Server not initialized"
    }


def test_semantic_spatial_search_uses_environment_identity_fallback() -> None:
    """Verify RLS context, query parameters, rounding, and context cleanup."""
    records = [
        {
            "uuid": 42,
            "source_origin": "sensor.csv",
            "payload_content": "reading",
            "location_wkt": "POINT(101.7 2.9)",
            "distance_meters": 12.345,
            "cosine_similarity": 0.98765,
        }
    ]
    connection = _AsyncConnection(records)
    environment = {
        "MCP_CLIENT_ROLE": "EXTERNAL_CLIENT",
        "MCP_CLIENT_TENANT_ID": "tenant-b",
    }
    model = _Model()
    namespace = {
        "db_pool": _AsyncPool(connection),
        "embedding_model": model,
        "json": json,
        "mcp": SimpleNamespace(get_context=lambda: SimpleNamespace()),
        "os": SimpleNamespace(getenv=environment.get),
        "ALLOWED_ROLES": ALLOWED_ROLES,
    }
    search = _load_semantic_search(namespace)

    result = json.loads(asyncio.run(search("sensor", 101.7, 2.9, 250.0, 3)))

    assert result == [
        {
            "uuid": "42",
            "source_origin": "sensor.csv",
            "content": "reading",
            "location_wkt": "POINT(101.7 2.9)",
            "distance_meters": 12.35,
            "similarity_score": 0.9877,
        }
    ]
    assert connection.execute_calls == [
        ("SELECT set_config('app.current_user_role', $1, true);", "EXTERNAL_CLIENT"),
        ("SELECT set_config('app.current_tenant_id', $1, true);", "tenant-b"),
    ]
    query, *parameters = connection.fetch_calls[0]
    assert "LIMIT $5" in query
    assert parameters == [101.7, 2.9, "[0.25,0.75]", 250.0, 3]
    assert connection.transaction_context.exited


@pytest.mark.parametrize(
    ("role", "tenant", "message"),
    [
        ("ROOT", "tenant-a", "Invalid or missing user_role"),
        ("EXTERNAL_CLIENT", None, "Missing or invalid tenant_id"),
        ("EXTERNAL_CLIENT", 123, "Missing or invalid tenant_id"),
    ],
)
def test_semantic_spatial_search_rejects_invalid_identity(
    role: str, tenant: Any, message: str
) -> None:
    """Verify the consumption example rejects invalid role and tenant values."""
    connection = _AsyncConnection([])
    namespace = {
        "db_pool": _AsyncPool(connection),
        "embedding_model": _Model(),
        "json": json,
        "mcp": SimpleNamespace(
            get_context=lambda: SimpleNamespace(user_role=role, tenant_id=tenant)
        ),
        "os": SimpleNamespace(getenv=lambda _name: None),
        "ALLOWED_ROLES": ALLOWED_ROLES,
    }
    search = _load_semantic_search(namespace)

    with pytest.raises(ValueError, match=message):
        asyncio.run(search("query", 0.0, 0.0))

    assert connection.fetch_calls == []


class _HTTPException(Exception):
    """Capture FastAPI HTTP exception fields for isolated example tests."""

    def __init__(self, status_code: int, detail: str, headers: dict[str, str]) -> None:
        """Store FastAPI-compatible exception details."""
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class _JWT:
    """Provide controllable JWT decoding results and errors."""

    class PyJWTError(Exception):
        """Represent a PyJWT validation failure."""

    def __init__(self, payload: dict[str, Any] | None = None, error: str | None = None) -> None:
        """Configure the decoder result or failure."""
        self.payload = payload
        self.error = error
        self.calls: list[tuple[Any, ...]] = []

    def decode(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Record verification arguments and return or raise."""
        self.calls.append((args, kwargs))
        if self.error:
            raise self.PyJWTError(self.error)
        assert self.payload is not None
        return self.payload


def _load_verify_jwt(jwt_decoder: _JWT, public_key: str | None = "public-key") -> Any:
    """Load the documented JWT verifier with local FastAPI substitutes."""
    source = _extract_fence(CONSUMPTION_SPEC, "python", "def verify_jwt_token")
    namespace = {
        "jwt": jwt_decoder,
        "KEYCLOAK_PUBLIC_KEY": public_key,
        "OIDC_AUDIENCE": "bda-api-service",
        "OIDC_ISSUER": "https://issuer.example/realm",
        "ALLOWED_ROLES": ALLOWED_ROLES,
        "HTTPException": _HTTPException,
        "status": SimpleNamespace(HTTP_401_UNAUTHORIZED=401),
    }
    return _load_definition(source, "verify_jwt_token", namespace, drop_defaults=True)


def test_verify_jwt_token_validates_signature_and_identity_claims() -> None:
    """Verify a valid JWT returns claims after strict RS256 verification."""
    payload = {"sub": "user-1", "user_role": "EXTERNAL_CLIENT", "tenant_id": "tenant-a"}
    decoder = _JWT(payload=payload)
    verify = _load_verify_jwt(decoder)

    assert verify(SimpleNamespace(credentials="signed-token")) is payload
    args, kwargs = decoder.calls[0]
    assert args == ("signed-token", "public-key")
    assert kwargs == {
        "algorithms": ["RS256"],
        "audience": "bda-api-service",
        "issuer": "https://issuer.example/realm",
    }


@pytest.mark.parametrize(
    ("payload", "detail"),
    [
        ({"tenant_id": "tenant-a"}, "Missing or invalid user_role claim"),
        ({"user_role": "ADMIN", "tenant_id": "tenant-a"}, "Missing or invalid user_role claim"),
        ({"user_role": "EXTERNAL_CLIENT"}, "Missing or invalid tenant_id claim"),
        ({"user_role": "EXTERNAL_CLIENT", "tenant_id": 42}, "Missing or invalid tenant_id claim"),
    ],
)
def test_verify_jwt_token_rejects_invalid_security_claims(
    payload: dict[str, Any], detail: str
) -> None:
    """Verify missing, unauthorised, and mistyped security claims return 401."""
    verify = _load_verify_jwt(_JWT(payload=payload))

    with pytest.raises(_HTTPException, match=detail) as error:
        verify(SimpleNamespace(credentials="signed-token"))

    assert error.value.status_code == 401
    assert error.value.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.parametrize(("token", "key"), [("", "public-key"), ("signed-token", None)])
def test_verify_jwt_token_rejects_missing_authentication_configuration(
    token: str, key: str | None
) -> None:
    """Verify absent bearer tokens and public keys fail before decoding."""
    decoder = _JWT(payload={})
    verify = _load_verify_jwt(decoder, public_key=key)

    with pytest.raises(_HTTPException, match="Authentication token or Keycloak key"):
        verify(SimpleNamespace(credentials=token))

    assert decoder.calls == []


def test_verify_jwt_token_maps_decoder_errors_to_unauthorised() -> None:
    """Verify signature, issuer, audience, or expiry errors become bearer 401 responses."""
    verify = _load_verify_jwt(_JWT(error="token expired"))

    with pytest.raises(_HTTPException, match="Invalid JWT Token: token expired") as error:
        verify(SimpleNamespace(credentials="expired-token"))

    assert error.value.status_code == 401


class _Cursor:
    """Capture psycopg2 cursor operations."""

    def __init__(self, rows: list[dict[str, Any]], fetch_error: Exception | None = None) -> None:
        """Configure fetched rows or an injected failure."""
        self.rows = rows
        self.fetch_error = fetch_error
        self.execute_calls: list[tuple[str, Any]] = []

    def __enter__(self) -> "_Cursor":
        """Return the cursor from its context."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit the cursor context."""

    def execute(self, query: str, parameters: Any) -> None:
        """Record one SQL execution."""
        self.execute_calls.append((query, parameters))

    def fetchall(self) -> list[dict[str, Any]]:
        """Return configured rows or raise the configured failure."""
        if self.fetch_error:
            raise self.fetch_error
        return self.rows


class _Connection:
    """Capture psycopg2 transaction and close behaviour."""

    def __init__(self, cursor: _Cursor) -> None:
        """Wrap the supplied cursor."""
        self.cursor_value = cursor
        self.entered = False
        self.exited = False
        self.closed = False

    def __enter__(self) -> "_Connection":
        """Mark transaction entry."""
        self.entered = True
        return self

    def __exit__(self, *args: Any) -> None:
        """Mark transaction exit."""
        self.exited = True

    def cursor(self, **_kwargs: Any) -> _Cursor:
        """Return the configured cursor."""
        return self.cursor_value

    def close(self) -> None:
        """Mark connection closure."""
        self.closed = True


def _load_hybrid_search(connection: _Connection, model: _Model | None = None) -> Any:
    """Load the documented FastAPI hybrid search function."""
    source = _extract_fence(CONSUMPTION_SPEC, "python", "def hybrid_search")
    namespace = {
        "model": model or _Model(),
        "get_db_connection": lambda: connection,
        "RealDictCursor": object,
    }
    return _load_definition(source, "hybrid_search", namespace, drop_defaults=True)


def test_hybrid_search_binds_rls_context_and_query_parameters() -> None:
    """Verify FastAPI search uses JWT identity and a transactional database context."""
    rows = [{"uuid": "id-1", "payload_content": "safe"}]
    cursor = _Cursor(rows)
    connection = _Connection(cursor)
    model = _Model()
    search = _load_hybrid_search(connection, model)
    request = SimpleNamespace(
        query_text="rainfall",
        longitude=101.7,
        latitude=2.9,
        radius_meters=500.0,
        limit=4,
    )

    result = search(
        request,
        {"user_role": "EXTERNAL_CLIENT", "tenant_id": "tenant-a"},
    )

    assert result == {"status": "success", "count": 1, "data": rows}
    assert model.calls == ["rainfall"]
    assert connection.entered and connection.exited and connection.closed
    assert cursor.execute_calls[:2] == [
        ("SELECT set_config('app.current_user_role', %s, true);", ("EXTERNAL_CLIENT",)),
        ("SELECT set_config('app.current_tenant_id', %s, true);", ("tenant-a",)),
    ]
    query, parameters = cursor.execute_calls[2]
    assert "ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography" in query
    assert parameters == (101.7, 2.9, [0.25, 0.75], 101.7, 2.9, 500.0, [0.25, 0.75], 4)


def test_hybrid_search_closes_connection_when_query_fails() -> None:
    """Verify the FastAPI example closes database connections after query failures."""
    connection = _Connection(_Cursor([], fetch_error=RuntimeError("database unavailable")))
    search = _load_hybrid_search(connection)
    request = SimpleNamespace(
        query_text="query",
        longitude=0.0,
        latitude=0.0,
        radius_meters=1.0,
        limit=1,
    )

    with pytest.raises(RuntimeError, match="database unavailable"):
        search(request, {"user_role": "INTERNAL_STAFF", "tenant_id": "internal"})

    assert connection.exited and connection.closed
