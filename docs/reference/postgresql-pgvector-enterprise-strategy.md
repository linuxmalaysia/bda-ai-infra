---
okf_version: "0.2"
title: "PostgreSQL & pgvector Enterprise Strategy Specification"
description: "Master architectural specification establishing PostgreSQL and pgvector as the core primary database foundation for Big Data Analytics (BDA) and Enterprise AI infrastructure."
type: "reference"
status: "verified"
timestamp: "2026-09-08T00:00:00Z"
stale_after: "2027-09-08T00:00:00Z"
topics:
  - postgresql
  - pgvector
  - bda
  - ai-infrastructure
  - vector-search
  - rag
  - percona
  - openmetadata
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
  - url: "https://www.percona.com/blog/create-an-ai-expert-with-open-source-tools-and-pgvector/"
    description: "Percona Technical Guide: Create an AI Expert With Open Source Tools and pgvector."
  - url: "https://www.percona.com/blog/pgvector-the-critical-postgresql-component-for-your-enterprise-ai-strategy/"
    description: "Percona Enterprise Strategy: pgvector - The Critical PostgreSQL Component for Your Enterprise AI Strategy."
---

# PostgreSQL & pgvector Enterprise Strategy Specification

This master specification establishes **PostgreSQL** and its native **`pgvector`** extension as the primary, master operational database and vector processing backbone for the entire **Big Data Analytics (BDA) and Artificial Intelligence (AI)** infrastructure.

By anchoring enterprise AI strategy around PostgreSQL, the platform eliminates unnecessary database sprawl, avoids proprietary cloud SaaS vector lock-in, and guarantees strict data sovereignty, ACID transactional consistency, and enterprise-grade security across relational, spatial, and vector workloads.

---

## 1. Master Strategic Rationale: Unified Database Architecture

### The Problem of Vector Database Sprawl
Many enterprise AI implementations default to introducing specialized standalone vector databases (e.g., Pinecone, Qdrant Cloud, Milvus, Weaviate). This practice introduces severe operational hazards:
- **Infrastructure Sprawl & Multi-Database Overhead:** Operations teams must deploy, monitor, backup, and patch separate distributed vector stores alongside existing relational databases.
- **Data Synchronization & Consistency Risks:** Syncing operational relational records to external vector stores requires complex Change Data Capture (CDC) or ETL pipelines, introducing replication lag, eventual consistency bugs, and orphaned vector embeddings.
- **Security & WAN Data Egress Risks:** Cloud SaaS vector databases require transmitting sensitive enterprise records and vector embeddings over public WAN links, violating zero-trust sovereignty mandates.
- **Licensing & Vendor Lock-In:** Specialized vector SaaS vendors often introduce tier-based API pricing, usage-based pricing spikes, and proprietary indexing APIs.

### The PostgreSQL Solution
PostgreSQL is the world's most trusted open-source relational database engine. With the `pgvector` extension, PostgreSQL handles high-dimensional vector similarity search natively within standard SQL tables.

```
+-----------------------------------------------------------------------------------+
|               POSTGRESQL OPERATIONAL & SEMANTIC SERVING BACKBONE                 |
+-----------------------------------------------------------------------------------+
|  [ Structured OLTP Data ] + [ Spatial Geometries (PostGIS) ]                      |
|  [ Operational Cache ]    + [ Operational Vector Search (pgvector) ]               |
|                                                                                   |
|  * Iceberg REST Catalog Authority: Apache Polaris                                 |
|  * Enterprise Metadata & Lineage: OpenMetadata (backed by PostgreSQL & OpenSearch)|
|  * Embedded Analytical Vectors: DuckDB vss (In-process Parquet ARRAY HNSW)        |
+-----------------------------------------------------------------------------------+
```

### Strategic Benefits Matrix

| Strategic Dimension | Standalone Vector SaaS / DBs | PostgreSQL + `pgvector` Master Strategy | Business & Operational Impact |
| :--- | :--- | :--- | :--- |
| **Architectural Footprint** | Fragmented (Separate DB cluster or cloud SaaS) | **Unified** (Single PostgreSQL engine for OLTP, GIS, and Vectors) | Eliminates database sprawl and reduces infrastructure licensing costs by **60%–70%**. |
| **Data Consistency** | Dual-write ETL lag; eventual consistency risk | **ACID Serialized Transactions** across relational, GIS, & vector data | Guarantees zero orphaned embeddings and instant transactional consistency. |
| **Security & Governance** | Separate RBAC, custom API tokens, WAN egress risks | **Native PostgreSQL Security** (Keycloak OIDC, RBAC, TLS, Audit Logging) | Ensures 100% data sovereignty with zero WAN data egress under zero-trust mandates. |
| **Hybrid Query Capabilities** | API-level post-filtering across disconnected systems | **Single-Query SQL Joins** combining relational, PostGIS, & vector predicates | Sub-10ms query execution combining spatial bounds, role filters, and semantic search. |
| **High Availability & Disaster Recovery** | Custom cluster HA setups or third-party cloud dependency | **Battle-tested HA** (Patroni, etcd, `pg_backrest`, Percona Operator) | Leverages proven enterprise PITR backups and sub-120s automated failover. |

---

## 2. Technical Capabilities & Indexing Mechanics of `pgvector`

### Vector Data Types & Distance Operators
`pgvector` adds a native `vector(dimensions)` data type to PostgreSQL (e.g., `vector(1024)` or `vector(1536)`). It supports three primary vector distance operators:

1. **Cosine Distance (`<=>`):** $1 - \cos(\theta)$, measuring the angle between vectors regardless of magnitude. This is the industry standard for text semantic similarity.
2. **Euclidean / L2 Distance (`<->`):** $\sqrt{\sum (u_i - v_i)^2}$, measuring straight-line distance in vector space.
3. **Negative Inner Product (`<#>`):** $- (u \cdot v)$, optimized for dot-product similarity when vectors are normalized.

### Indexing Strategies: HNSW vs. IVFFlat
Without an index, vector search executes an exact k-Nearest Neighbors (kNN) sequential scan (`ORDER BY embedding <=> query_embedding LIMIT k`), guaranteeing 100% recall but scaling $O(N)$ with dataset size. For large-scale datasets, `pgvector` provides two high-performance indexing mechanisms:

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 360" width="100%" height="100%">
  <defs>
    <marker id="arrow-pg" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B" />
    </marker>
  </defs>

  <rect width="900" height="360" fill="#0F172A" rx="10"/>

  <rect x="20" y="20" width="410" height="320" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="410" height="36" fill="#0F172A" rx="8"/>
  <text x="35" y="43" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#60A5FA">HNSW (HIERARCHICAL NAVIGABLE SMALL WORLD)</text>

  <rect x="40" y="75" width="370" height="60" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="50" y="98" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#F8FAFC">Layer 2: Top Sparse Layer</text>
  <text x="50" y="118" font-family="Consolas, Monaco, monospace" font-size="11" fill="#60A5FA">Express skip links across graph</text>

  <line x1="225" y1="135" x2="225" y2="160" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-pg)"/>

  <rect x="40" y="160" width="370" height="60" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="50" y="183" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#F8FAFC">Layer 1: Middle Layer</text>
  <text x="50" y="203" font-family="Consolas, Monaco, monospace" font-size="11" fill="#94A3B8">Medium-density graph connections</text>

  <line x1="225" y1="220" x2="225" y2="245" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-pg)"/>

  <rect x="40" y="245" width="370" height="70" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="50" y="268" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#F8FAFC">Layer 0: Base Dense Layer</text>
  <text x="50" y="288" font-family="Consolas, Monaco, monospace" font-size="11" fill="#4ADE80">Full k-NN vector node neighborhood</text>

  <rect x="470" y="20" width="410" height="320" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8"/>
  <rect x="470" y="20" width="410" height="36" fill="#0F172A" rx="8"/>
  <text x="485" y="43" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#94A3B8">IVFFLAT (INVERTED FILE FLAT)</text>

  <rect x="490" y="75" width="370" height="60" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="500" y="98" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#F8FAFC">Voronoi Centroids</text>
  <text x="500" y="118" font-family="Consolas, Monaco, monospace" font-size="11" fill="#FBBF24">K-Means spatial vector partitioning</text>

  <line x1="560" y1="135" x2="540" y2="180" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-pg)"/>
  <line x1="675" y1="135" x2="675" y2="180" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-pg)"/>
  <line x1="790" y1="135" x2="810" y2="180" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-pg)"/>

  <rect x="490" y="180" width="110" height="135" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="500" y="203" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#F8FAFC">Cluster A</text>
  <text x="500" y="223" font-family="Consolas, Monaco, monospace" font-size="10" fill="#94A3B8">Inverted List</text>

  <rect x="620" y="180" width="110" height="135" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="630" y="203" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#F8FAFC">Cluster B</text>
  <text x="630" y="223" font-family="Consolas, Monaco, monospace" font-size="10" fill="#94A3B8">Inverted List</text>

  <rect x="750" y="180" width="110" height="135" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="760" y="203" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#F8FAFC">Cluster C</text>
  <text x="760" y="223" font-family="Consolas, Monaco, monospace" font-size="10" fill="#94A3B8">Inverted List</text>
</svg>

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart LR
    subgraph HNSW ["HNSW (Hierarchical Navigable Small World)"]
        Layer2["Top Layer: Sparse Express Links"] -->|"hnsw.ef_search / Graph Traversal"| Layer1["Middle Layer: Medium Links"]
        Layer1 -->|"Local Neighbor Traversal"| Layer0["Base Layer: Dense Local Graph"]
    end

    subgraph IVFFlat ["IVFFlat (Inverted File Flat)"]
        Centroids["Voronoi Centroids (Lists)"] -->|"k-Means Centroid Probing"| ClusterA["Cluster A Embeddings"]
        Centroids -->|"k-Means Centroid Probing"| ClusterB["Cluster B Embeddings"]
        Centroids -->|"k-Means Centroid Probing"| ClusterC["Cluster C Embeddings"]
    end
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Top Express Layer 2** | **Middle Layer 1** | In-Memory Graph Pointers | Internal PostgreSQL Shared Memory | Traverses sparse multi-layer skip connections to quickly narrow candidate vector region. |
| **Middle Layer 1** | **Base Dense Layer 0** | In-Memory Graph Pointers | Internal PostgreSQL Shared Memory | Drills down into high-density local vector neighborhood for sub-10ms nearest neighbor search. |
| **Voronoi Centroids** | **Inverted Cluster Lists** | In-Memory Index Search | Internal PostgreSQL Shared Memory | Probes closest centroid lists during IVFFlat search; fast build time but lower recall under dynamic updates. |

| Dimension / Index Type | HNSW Index (Hierarchical Navigable Small World) | IVFFlat Index (Inverted File Flat) |
| :--- | :--- | :--- |
| **Primary Algorithm** | Multi-layer graph structure linking nearest vector neighbors. | K-means clustering dividing vector space into Voronoi cells. |
| **Search Performance** | **Ultra-Fast (Sub-10ms)** with exceptionally high recall. | Fast, but speed/recall depends on number of probed lists. |
| **Build Time & Memory** | Higher memory footprint and longer build time. | Low build memory and faster initial build time. |
| **Dataset Dynamic Updates** | **Excellent.** Vectors can be inserted without rebuilding the index. | **Requires Warm Dataset.** Index quality degrades if built before vectors are inserted. |
| **Recommended Usage** | **Primary Choice for Enterprise BDA AI Production.** | Secondary choice for memory-constrained historical archives. |

#### HNSW Index Tuning Parameters
```sql
CREATE INDEX ON perconavec USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```
- **`m` (default 16):** Maximum number of bidirectional connections per node in the graph. Higher values improve recall for high-dimensional vectors at the cost of index build memory.
- **`ef_construction` (default 64):** Size of the dynamic candidate list evaluated during index construction.
- **`hnsw.ef_search` (runtime parameter, default 40):** Size of the candidate list evaluated during queries (`SET hnsw.ef_search = 100;`).

---

## 3. Unified Single-Query Hybrid Search

A major architectural advantage of PostgreSQL + `pgvector` over standalone vector databases is the ability to execute **Hybrid Search** (Relational SQL + Spatial PostGIS + Full-Text Search + Vector Distance) in a single unified, transactional query.

### Hybrid SQL Example
To leverage the HNSW index efficiently, the query first performs vector distance ordering to pull an oversized candidate pool (e.g. `LIMIT 100`) before combining text search ranking (`websearch_to_tsquery` to avoid syntax errors on raw user strings) and spatial predicates (`ST_SetSRID` with SRID 4326 for WGS84 coordinates).

```sql
-- 2-Stage Hybrid Search: Stage 1 HNSW Candidate Selection -> Stage 2 Reciprocal / Combined Reranking
-- 2-Stage Hybrid Search: Stage 1 HNSW Candidate Scan with Predicate Filtering -> Stage 2 Combined Reranking
WITH vector_candidates AS (
    SELECT
        d.id,
        d.document_uri,
        d.chunk_content,
        d.geom_location,
        d.classification_level,
        d.text_search_vector,
        d.embedding,
        (1 - (d.embedding <=> :query_vector)) AS vector_similarity
    FROM enterprise_knowledge_base d
    WHERE
        d.classification_level <= :user_clearance_level
        AND ST_DWithin(d.geom_location, ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography, 50000) -- 50km spatial buffer
        AND d.text_search_vector @@ websearch_to_tsquery('english', :keyword)
    ORDER BY d.embedding <=> :query_vector
    LIMIT 100 -- Oversample candidate pool satisfying clearance, spatial, and text predicates
)
SELECT
    c.id,
    c.document_uri,
    c.chunk_content,
    c.vector_similarity,
    ts_rank(c.text_search_vector, websearch_to_tsquery('english', :keyword)) AS text_rank
FROM vector_candidates c
ORDER BY
    (c.vector_similarity * 0.7) +
    (ts_rank(c.text_search_vector, websearch_to_tsquery('english', :keyword)) * 0.3) DESC
LIMIT 5;
```

> **Iterative Scans & Index Plan Diagnostics:**
> Production queries using HNSW with selective filters require **pgvector 0.8.0 or later** to utilize `SET hnsw.iterative_scan = 'relaxed_order';` (or `strict_order` when exact distance ordering must be preserved during graph traversal). Note that `hnsw.iterative_scan` allows pgvector to dynamically continue scanning the index graph until the requested candidate `LIMIT` is fulfilled after predicate filtering. In contrast, `hnsw.ef_search` only expands the initial candidate list evaluated during graph exploration without continuing to scan after clearance, spatial, or text filters remove rows; highly selective queries relying solely on `hnsw.ef_search` may return fewer than five rows. Validate query plans with `EXPLAIN (ANALYZE, BUFFERS)` against an exact kNN baseline (`SET enable_indexscan = off;`) to measure recall.

---

## 4. End-to-End Enterprise AI Expert & RAG Production Blueprint

Following the research patterns established in Percona's technical guidance (*Create an AI Expert With Open Source Tools and pgvector*), the BDA platform implements an end-to-end, 100% open-source AI Expert RAG pipeline.

### Dual-Render Architecture Specification: Enterprise AI Expert & RAG Pipeline

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B" />
    </marker>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Canvas Background -->
  <rect width="1000" height="580" fill="#0F172A" rx="12"/>

  <!-- Header Banner -->
  <rect x="20" y="20" width="960" height="40" fill="#1E293B" stroke="#334155" rx="6"/>
  <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#F8FAFC">
    POSTGRESQL &amp; PGVECTOR ENTERPRISE AI EXPERT RAG PIPELINE ARCHITECTURE
  </text>
  <text x="820" y="45" font-family="Consolas, Monaco, monospace" font-size="12" fill="#38BDF8">
    ZONE: TRUSTED-DMZ
  </text>

  <!-- Zone 1: Document Ingestion & Chunking -->
  <rect x="20" y="80" width="220" height="470" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow)"/>
  <rect x="20" y="80" width="220" height="32" fill="#0F172A" rx="8"/>
  <text x="30" y="101" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#60A5FA">
    1. INGESTION &amp; CHUNKING
  </text>

  <rect x="35" y="130" width="190" height="90" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="45" y="150" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">Enterprise Docs</text>
  <text x="45" y="170" font-family="Consolas, Monaco, monospace" font-size="11" fill="#38BDF8">s3://bda-docs/</text>
  <text x="45" y="190" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#94A3B8">Markdown &amp; ODCS Contracts</text>

  <rect x="35" y="250" width="190" height="90" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="45" y="270" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">MarkdownSplitter</text>
  <text x="45" y="290" font-family="Consolas, Monaco, monospace" font-size="11" fill="#60A5FA">chunk_size=1000</text>
  <text x="45" y="310" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#94A3B8">Overlap: 100 tokens</text>

  <!-- Zone 2: Local Vector Embedding -->
  <rect x="260" y="80" width="220" height="470" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow)"/>
  <rect x="260" y="80" width="220" height="32" fill="#0F172A" rx="8"/>
  <text x="270" y="101" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#94A3B8">
    2. LOCAL EMBEDDING
  </text>

  <rect x="275" y="180" width="190" height="110" fill="#0F172A" stroke="#3B82F6" stroke-width="1" rx="6"/>
  <text x="285" y="202" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">SentenceTransformer</text>
  <text x="285" y="222" font-family="Consolas, Monaco, monospace" font-size="10" fill="#60A5FA">/opt/models/WhereIsAI/UAE-Large-V1</text>
  <text x="285" y="242" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#E2E8F0">1024-dim Vector Output</text>
  <text x="285" y="262" font-family="Consolas, Monaco, monospace" font-size="10" fill="#4ADE80">local_files_only=True</text>

  <!-- Zone 3: Master PostgreSQL Store -->
  <rect x="500" y="80" width="240" height="470" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow)"/>
  <rect x="500" y="80" width="240" height="32" fill="#0F172A" rx="8"/>
  <text x="510" y="101" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#4ADE80">
    3. MASTER POSTGRESQL STORE
  </text>

  <rect x="515" y="130" width="210" height="120" fill="#0F172A" stroke="#22C55E" stroke-width="1" rx="6"/>
  <text x="525" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#86EFAC">PostgreSQL 17 Cluster</text>
  <text x="525" y="172" font-family="Consolas, Monaco, monospace" font-size="10" fill="#E2E8F0">bda-pgvector-master:5432</text>
  <text x="525" y="192" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#4ADE80">Patroni HA + PostGIS + pgvector</text>
  <text x="525" y="212" font-family="Consolas, Monaco, monospace" font-size="10" fill="#94A3B8">sslmode=verify-full</text>

  <rect x="515" y="270" width="210" height="100" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="525" y="292" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">HNSW Vector Index</text>
  <text x="525" y="312" font-family="Consolas, Monaco, monospace" font-size="10" fill="#60A5FA">m=16, ef_construction=64</text>
  <text x="525" y="332" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#94A3B8">vector_cosine_ops</text>

  <!-- Zone 4: Sandboxed RAG Inference -->
  <rect x="760" y="80" width="220" height="470" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow)"/>
  <rect x="760" y="80" width="220" height="32" fill="#0F172A" rx="8"/>
  <text x="770" y="101" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#FBBF24">
    4. SANDBOXED INFERENCE
  </text>

  <rect x="775" y="130" width="190" height="80" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="785" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">User / AI Agent</text>
  <text x="785" y="172" font-family="Consolas, Monaco, monospace" font-size="10" fill="#94A3B8">APISIX / Keycloak OIDC</text>

  <rect x="775" y="230" width="190" height="90" fill="#0F172A" stroke="#334155" stroke-width="1" rx="6"/>
  <text x="785" y="252" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">match_documents()</text>
  <text x="785" y="272" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#94A3B8">2-Stage CTE Oversampling</text>
  <text x="785" y="292" font-family="Consolas, Monaco, monospace" font-size="10" fill="#60A5FA">websearch_to_tsquery</text>

  <rect x="775" y="340" width="190" height="100" fill="#0F172A" stroke="#F59E0B" stroke-width="1" rx="6"/>
  <text x="785" y="362" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#F8FAFC">vLLM / Ollama GPU</text>
  <text x="785" y="382" font-family="Consolas, Monaco, monospace" font-size="10" fill="#FBBF24">http://localhost:8000</text>
  <text x="785" y="402" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" fill="#4ADE80">Grounded Output</text>

  <!-- Connection Paths & Protocol Badges -->
  <!-- Ingestion -> Embedding -->
  <line x1="225" y1="295" x2="275" y2="235" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow)"/>
  <rect x="230" y="250" width="45" height="18" fill="#1E3A8A" rx="3"/>
  <text x="233" y="262" font-family="Consolas, Monaco, monospace" font-size="9" fill="#93C5FD">IPC</text>

  <!-- Embedding -> Postgres Insert -->
  <line x1="465" y1="235" x2="515" y2="190" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow)"/>
  <rect x="460" y="195" width="60" height="18" fill="#065F46" rx="3"/>
  <text x="463" y="207" font-family="Consolas, Monaco, monospace" font-size="9" fill="#86EFAC">TCP 5432</text>

  <!-- User -> Match documents -->
  <line x1="870" y1="210" x2="870" y2="230" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Match documents -> Postgres query -->
  <line x1="775" y1="275" x2="725" y2="210" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Match documents -> Local LLM -->
  <line x1="870" y1="320" x2="870" y2="340" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow)"/>
  <rect x="880" y="322" width="60" height="18" fill="#78350F" rx="3"/>
  <text x="883" y="334" font-family="Consolas, Monaco, monospace" font-size="9" fill="#FDE68A">Context</text>
</svg>

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    subgraph DataIngestion ["1. Enterprise Ingestion & Chunking"]
        Docs["Enterprise Markdown &amp; ODCS Contracts<br/>s3://bda-docs/"] --> Splitter["MarkdownTextSplitter<br/>(chunk_size=1000, overlap=100)"]
    end

    subgraph EmbeddingPipeline ["2. Local Vector Embedding Pipeline"]
        Splitter -->|"Local IPC / CUDA"| LocalEmbed["SentenceTransformer Model<br/>/opt/models/WhereIsAI/UAE-Large-V1<br/>(1024-dim, local_files_only=True)"]
    end

    subgraph PgVectorStore ["3. Master Operational Database Store"]
        LocalEmbed -->|"TCP 5432 / TLS (sslmode=verify-full)"| PgDB[("PostgreSQL 17 HA Cluster<br/>bda-pgvector-master:5432<br/>(Patroni + pgvector + PostGIS)")]
        PgDB --> HNSWIdx["HNSW Index<br/>(m=16, ef_construction=64, cosine)"]
    end

    subgraph RAGInference ["4. Zero-Trust Local RAG Inference"]
        UserQ["User / AI Agent Question<br/>(Keycloak OIDC / APISIX Gateway)"] --> QEmbed["Convert Question to Vector<br/>(Local SentenceTransformer)"]
        QEmbed -->|"2-Stage CTE Match Query"| MatchFunc["match_documents() SQL Search<br/>(ST_DWithin + websearch_to_tsquery)"]
        MatchFunc -->|"SQL Read Query"| PgDB
        PgDB -->|"Top K Context Chunks"| PromptBuilder["Prompt Context Builder"]
        UserQ --> PromptBuilder
        PromptBuilder -->|"Augmented Prompt"| LocalLLM["Local Sandboxed Inference<br/>(vLLM / Ollama on Local GPUs)"]
        LocalLLM --> GroundedAnswer["Grounded Hallucination-Free Answer"]
    end
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **MarkdownTextSplitter** | **SentenceTransformer** | Local Memory IPC / CUDA | Zone 1 -> Zone 2 (Local Container Memory) | Transforms 1000-character document chunks into dense 1024-dimensional floating-point vectors. |
| **SentenceTransformer** | **PostgreSQL Cluster (`bda-pgvector-master`)** | `TCP 5432` / PostgreSQL Protocol | Zone 2 -> Zone 3 (`sslmode=verify-full`, Secret Manager TLS Password) | Executes idempotent `INSERT INTO enterprise_knowledge_base ... ON CONFLICT DO UPDATE` storing embeddings. |
| **APISIX Gateway** | **`match_documents()` Query Handler** | `TCP 443` (HTTPS / OIDC) | Public DMZ -> Zone 4 (Keycloak RBAC JWT Token) | Authenticates user request and delegates semantic similarity search. |
| **`match_documents()` Handler** | **PostgreSQL Cluster** | `TCP 5432` / SQL Session | Zone 4 -> Zone 3 (`sslmode=verify-full`, Read-Only DB Role) | Executes 2-stage CTE oversampling vector scan combining PostGIS `ST_DWithin` and `websearch_to_tsquery`. |
| **Prompt Context Builder** | **vLLM / Ollama Local Inference** | `TCP 8000` / HTTP REST API | Zone 4 Internal (Local Host GPU Passthrough) | Feeds grounded document context chunks and user prompt to local LLM for hallucination-free generation. |

### Production Implementation Steps

#### Step 1: Provisioning HA PostgreSQL with `pgvector`
Deploy enterprise PostgreSQL via **Percona Operator for PostgreSQL** or **Patroni HA** on Kubernetes (RKE2 / Proxmox VE). The operator loads custom extension packages from S3/Ceph object storage without requiring custom container image rebuilds.

```yaml
# Percona PostgreSQL Operator Custom Resource Snippet
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: bda-pgvector-master
spec:
  instances: 3
  extensions:
    storage:
      type: s3
      bucket: bda-pg-extensions
      region: us-east-1
      secret:
        name: ext-s3-secret
    custom:
      - name: pgvector
        version: 0.8.0
```

#### Step 2: Database Table & Match Function DDL
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Operational AI Knowledge Base Table
CREATE TABLE enterprise_knowledge_base (
    id BIGSERIAL PRIMARY KEY,
    document_uri TEXT NOT NULL,
    chunk_index INT NOT NULL,
    chunk_content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(1024), -- UAE-Large-V1 1024-dimension embedding
    tenant_id VARCHAR(50) NOT NULL DEFAULT 'INTERNAL',
    access_classification VARCHAR(20) NOT NULL DEFAULT 'RESTRICTED' CHECK (access_classification IN ('PUBLIC', 'RESTRICTED', 'INTERNAL_ONLY')),
    organizational_unit VARCHAR(50) DEFAULT 'GENERAL',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_doc_chunk UNIQUE (document_uri, chunk_index)
);

-- Construct HNSW Index over vector column
CREATE INDEX idx_knowledge_embedding_hnsw
ON enterprise_knowledge_base
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Configure Multi-Tenant Row-Level Security (RLS)
ALTER TABLE enterprise_knowledge_base ENABLE ROW LEVEL SECURITY;

-- Internal Staff Policy: Can read all internal and public tenant data
CREATE POLICY internal_staff_policy ON enterprise_knowledge_base
    FOR SELECT
    USING (
        current_setting('app.current_user_role', true) = 'INTERNAL_STAFF'
    );

-- External Client Policy: Hard-locked to their specific tenant ID and public classification
CREATE POLICY external_client_policy ON enterprise_knowledge_base
    FOR SELECT
    USING (
        current_setting('app.current_user_role', true) = 'EXTERNAL_CLIENT'
        AND tenant_id = current_setting('app.current_tenant_id', true)
        AND access_classification = 'PUBLIC'
    );

-- Similarity Match Function
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding vector(1024),
    match_threshold FLOAT,
    match_count INT
)
RETURNS TABLE (
    id BIGINT,
    document_uri TEXT,
    chunk_content TEXT,
    similarity FLOAT
)
LANGUAGE sql STABLE
AS $$
    SELECT
        id,
        document_uri,
        chunk_content,
        1 - (embedding <=> query_embedding) AS similarity
    FROM enterprise_knowledge_base
    WHERE 1 - (embedding <=> query_embedding) > match_threshold
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
```

#### Step 3: Python Chunking & Idempotent Vector Insertion Script
```python
import os
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import MarkdownTextSplitter

# 1. Initialize pre-staged local embedding model (Zero WAN Egress & Local Cache Only)
# Staged model directory integrity verified via SHA-256 checksum manifest prior to load
LOCAL_MODEL_DIR = os.getenv("EMBEDDING_MODEL_PATH", "/opt/models/WhereIsAI/UAE-Large-V1")
model = SentenceTransformer(LOCAL_MODEL_DIR, device='cuda', local_files_only=True)

# 2. Connect to Master PostgreSQL DB using verified TLS and Secret Manager credentials
db_password = os.getenv("DB_PASSWORD") # Loaded from Kubernetes Secret
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "bda-pgvector-master"),
    dbname=os.getenv("DB_NAME", "bdadb"),
    user=os.getenv("DB_USER", "vector"),
    password=db_password,
    sslmode="verify-full",
    sslrootcert="/etc/ssl/certs/pg-ca.crt"
)
register_vector(conn)
cur = conn.cursor()

# 3. Chunk Document & Perform Idempotent Insertion
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_text(raw_document_markdown)

for idx, chunk in enumerate(chunks):
    embedding = model.encode(chunk, device='cuda').tolist()
    cur.execute("""
        INSERT INTO enterprise_knowledge_base
        (document_uri, chunk_index, chunk_content, embedding)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (document_uri, chunk_index) DO UPDATE SET
            chunk_content = EXCLUDED.chunk_content,
            embedding = EXCLUDED.embedding,
            created_at = CURRENT_TIMESTAMP
    """, ("s3://bda-docs/ref-01.md", idx, chunk, embedding))

conn.commit()
```

#### Step 4: Context Augmentation & Local LLM Generation
```python
# Query semantic similarity match function
cur.execute("SELECT chunk_content, similarity FROM match_documents(%s, 0.7, 5)", (query_vector,))
context_chunks = cur.fetchall()

context_str = "\n---\n".join([c[0] for c in context_chunks])
prompt = f"""
You are an enterprise BDA AI Expert. Answer the question using ONLY the context provided below.

Context:
{context_str}

Question: {user_question}
Answer:
"""

# Send prompt to local sandboxed vLLM / Ollama instance
```

---

## 5. Summary Architectural Governance Principles

1. **PostgreSQL as Master Anchor:** PostgreSQL with `pgvector` and `PostGIS` serves as the primary master database for all operational relational tables, metadata catalogs, spatial indexes, and vector embeddings across the BDA platform.
2. **Zero Third-Party Vector SaaS:** Standalone vector SaaS services (Pinecone, Qdrant Cloud, etc.) are strictly prohibited to prevent WAN data egress, high recurring API costs, and vendor lock-in.
3. **Local Embedding Execution:** Vector embeddings must be generated using local open-source transformer models (`SentenceTransformers` / `vLLM` / `Ollama` on local GPUs) to maintain 100% data sovereignty.
4. **HNSW Index Default:** HNSW graph indexing (`m=16`, `ef_construction=64`) is the mandatory default index type for production `pgvector` tables containing more than 10,000 vector records.
5. **OpenMetadata Lineage Integration:** All vector-indexed knowledge bases and database schemas must be registered in OpenMetadata with automated column-level lineage and governance tags.
