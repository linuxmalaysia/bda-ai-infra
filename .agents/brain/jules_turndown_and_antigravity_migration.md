---
okf_version: "0.2"
type: spatial_memory
title: "Google Jules Turndown, Data Export & Google Antigravity Migration Guide"
description: "Master migration reference in DSOM spatial memory detailing the Google Jules turndown timeline, export procedures, backend API architecture, and transition roadmap to Google Antigravity."
status: active
timestamp: "2026-10-31T00:00:00Z"
stale_after: "2027-10-31T00:00:00Z"
generated: false
verified: true
sources:
  - id: "jules_changelog_turndown"
    url: "https://jules.google.com/changelog"
  - id: "antigravity_platform"
    url: "https://antigravity.google/"
topics:
  - jules
  - turndown
  - antigravity
  - data-export
  - migration
  - spatial-memory
---

# 🛸 Google Jules Turndown & Google Antigravity Migration Guide

## 1. Executive Summary & Turndown Timeline

As part of Google's unification of its agentic coding efforts into next-generation, agent-first platforms like **Google Antigravity**, Google Jules is scheduled for deprecation and turndown.

- **Announcement Date:** 29 October 2026
- **Read-Only Transition Date:** 11 November 2026
  - Sessions can no longer be initiated or executed.
  - Existing sessions and historical logs remain accessible in read-only mode until year-end.
- **Decommissioning Date:** 31 December 2026
  - Complete wind-down of backend services and endpoints.

---

## 2. Migration and Data Export Protocol

Users and autonomous systems can extract complete historical context, memories, configuration, and code patches from Jules into a structured local directory (`~/jules-export`).

### 2.1 Scope of Exported Data

- **Account Settings:** `user-settings.json` (GetUserSettings)
- **Environment Variables:** `env-variables.json` (ListEnvironmentVariables)
- **Scheduled Tasks:** `scheduled-tasks.json` (ListScheduledTasks)
- **Connected Repositories & Memories:** `sources.json` and per-repo `memories.json` / `memories.md`
- **Session Archives:** Full per-session bundles under `sessions/<id>/` containing:
  - `session.json` (task definition, prompts, suggested titles)
  - `activities.json` (activity steps and tool executions)
  - `summary.md` (human-readable executive summary)
  - `patch-<n>.diff` (Git unidiff patches)
  - `setup.sh` & `test-command.txt` (environment setup and verification scripts)

### 2.2 CLI Authentication & Keychain Storage Mechanics

The Jules CLI (`@google/jules`) manages user authentication via OAuth2:

- **macOS Keychain:**
  - Service: `jules-cli`
  - Account: `default`
  - Format: `go-keyring-base64:<base64-json>`
- **Linux Secret Service:**
  - Service: `jules-cli`
  - Username: `default`
- **Local Fallback:**
  - Cache file: `~/.jules/cache/oauth_creds.json`
- **Token Validity:**
  - Access tokens expire approximately 60 minutes after generation. Running any `jules` command or refreshing via `jules login` re-authenticates.
- **GitHub Target Association:**
  - If `ListSources` returns HTTP 401 ("missing required authentication credential"), authorization is required at:
    `https://github.com/apps/google-labs-jules/installations/select_target`

---

## 3. Backend Endpoints Architecture

Data retrieval connects directly to Google's backend APIs:

1. **Protobuf RPC Gateway:**
   - URL: `https://aida.googleapis.com/$rpc/language_labs.aida.swebot.proto.SweBotService`
   - Operations: `GetUserSettings`, `ListEnvironmentVariables`, `ListScheduledTasks`, `ListSources`, `ListMemories`
2. **REST SweBot Gateway:**
   - Base URL: `https://aida.googleapis.com/v1/swebot`
   - Operations:
     - `/tasks` (list tasks)
     - `/tasks/{id}` (task details & code output metadata)
     - `/tasks/{id}/activities` (full chronological activity log)

---

## 4. Standalone Export Script Specification

Below is the verified standalone Python exporter for reference:

```python
import base64, json, pathlib, re, subprocess, sys, urllib.error, urllib.parse, urllib.request

def get_token():
    for cmd in [["security", "find-generic-password", "-s", "jules-cli", "-a", "default", "-w"],
                ["secret-tool", "lookup", "service", "jules-cli", "username", "default"]]:
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
            if out.startswith("go-keyring-base64:"):
                out = base64.b64decode(out.split(":", 1)[1]).decode()
            if out: return json.loads(out)["access_token"]
        except Exception: pass
    p = pathlib.Path.home() / ".jules/cache/oauth_creds.json"
    if p.exists(): return json.loads(p.read_text())["access_token"]
    sys.exit("Run `jules login` first.")

TOKEN = get_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
RPC = "https://aida.googleapis.com/$rpc/language_labs.aida.swebot.proto.SweBotService"
REST = "https://aida.googleapis.com/v1/swebot"
OUT = pathlib.Path("./jules-export"); OUT.mkdir(exist_ok=True)
errors = []

def rpc(m, b=None):
    req = urllib.request.Request(f"{RPC}/{m}", data=json.dumps(b or {}).encode(), headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode() or "{}")

def get(path, **params):
    q = ("?" + urllib.parse.urlencode(params)) if params else ""
    with urllib.request.urlopen(urllib.request.Request(f"{REST}{path}{q}", headers=HEADERS), timeout=60) as r:
        return json.loads(r.read().decode() or "{}")

def paged(fetch, key):
    items, token = [], None
    while True:
        resp = fetch(token)
        items += resp.get(key, [])
        token = resp.get("nextPageToken")
        if not token: return items

def safe(s): return re.sub(r"[^a-zA-Z0-9._-]", "_", s)
def dump(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, indent=2))

# Account-level data
dump(OUT / "user-settings.json", rpc("GetUserSettings"))
dump(OUT / "env-variables.json", rpc("ListEnvironmentVariables"))
dump(OUT / "scheduled-tasks.json", rpc("ListScheduledTasks"))

# Repos (sources) and their memories
sources = paged(lambda t: rpc("ListSources", {"pageSize": 100, **({"pageToken": t} if t else {})}), "sources")
dump(OUT / "sources.json", sources)
mem_repos = 0
for src in sources:
    sid = src.get("sourceId") or src.get("id") or src.get("name", "").removeprefix("sources/")
    try:
        mems = paged(lambda t: rpc("ListMemories", {"sourceId": sid, "pageSize": 100, **({"pageToken": t} if t else {})}), "memories")
    except urllib.error.HTTPError as e:
        errors.append(f"memories {sid}: HTTP {e.code}"); continue
    if mems:
        mem_repos += 1
        d = OUT / "repos" / safe(sid)
        dump(d / "memories.json", mems)
        (d / "memories.md").write_text("# Memories\n\n" + "\n".join(
            f"- {m.get('Fact') or m.get('fact') or m.get('content')}" for m in mems if not m.get("archived")) + "\n")

# Sessions: full detail, activity log, patches, and a readable summary
sessions = paged(lambda t: get("/tasks", pageSize=100, **({"pageToken": t} if t else {})), "tasks")
dump(OUT / "sessions.json", sessions)
setup = {}
patches = 0
for s in sorted(sessions, key=lambda s: s.get("createdAt", "")):
    tid = s["id"]; d = OUT / "sessions" / tid
    try:
        task = get(f"/tasks/{tid}").get("task", {})
        acts = paged(lambda t: get(f"/tasks/{tid}/activities", pageSize=100, **({"pageToken": t} if t else {})), "activitySteps")
    except urllib.error.HTTPError as e:
        errors.append(f"session {tid}: HTTP {e.code}"); continue
    dump(d / "session.json", task)
    dump(d / "activities.json", acts)
    commits = [o["gitCommit"] for o in task.get("outputs", []) if "gitCommit" in o]
    for i, c in enumerate(commits, 1):
        if c.get("patch", {}).get("unidiff"):
            (d / f"patch-{i}.diff").write_text(c["patch"]["unidiff"]); patches += 1
        meta = c.get("repoMetadata", {})
        if meta.get("environmentSetupScript") or meta.get("testCommand"):
            setup[task.get("sourceId") or meta.get("name") or tid] = meta
    plan = task.get("latestPlan", {}).get("steps", [])
    kinds = {}
    for a in acts:
        for actor, v in a.items():
            if isinstance(v, dict):
                for k in v: kinds[f"{actor}.{k}"] = kinds.get(f"{actor}.{k}", 0) + 1
    lines = [f"# {task.get('title') or s.get('suggestedTitle') or tid}", "",
             f"- **ID:** {tid}", f"- **Repo:** {task.get('sourceId', '')}",
             f"- **Status:** {task.get('taskStatus', '')}", f"- **Created:** {task.get('createdAt', '')}",
             f"- **Completed:** {task.get('completedAt', '')}", "", "## Prompt", "", task.get("description", ""), ""]
    if plan: lines += ["## Latest plan", ""] + [f"{p.get('index', 0) + 1}. {p.get('title', '')}" for p in plan] + [""]
    if commits: lines += ["## Code outputs", ""] + [
        f"- `patch-{i}.diff`: {c.get('title') or (c.get('commitMessage') or '').split(chr(10))[0]} (branch `{c.get('gitBranchName', '')}`)"
        for i, c in enumerate(commits, 1)] + [""]
    if pub := task.get("latestPublish", {}).get("commitInfo"):
        lines += ["## Published", "", f"- Commit `{pub.get('commitId', '')}` on `{pub.get('branchName', '')}`", ""]
    lines += ["## Activity", "", f"{len(acts)} steps (full log in `activities.json`):", ""] + [f"- {k}: {n}" for k, n in sorted(kinds.items())]
    (d / "summary.md").write_text("\n".join(lines) + "\n")

for sid, meta in setup.items():
    d = OUT / "repos" / safe(sid); d.mkdir(parents=True, exist_ok=True)
    if meta.get("environmentSetupScript"): (d / "setup.sh").write_text(meta["environmentSetupScript"] + "\n")
    if meta.get("testCommand"): (d / "test-command.txt").write_text(meta["testCommand"] + "\n")

print(json.dumps({"repos": len(sources), "repos_with_memories": mem_repos, "sessions": len(sessions),
                  "patches": patches, "repos_with_setup_or_test": len(setup),
                  "error_count": len(errors), "errors": errors[:10]}, indent=2))
print(f"Exported all Jules data to {OUT.resolve()}")
```

---

## 5. Transition Runway to Google Antigravity & Sovereign Coding Agents

1. **Ingestion into Google Antigravity:**
   - Antigravity consumes agentic configurations and project context natively. The recovered memories and setup commands can be supplied directly to initialize Antigravity task graphs.
2. **Sovereign Repository Self-Containment:**
   - Core guidelines, skills, and memory palace registries persist inside `.agents/brain/` and `.agents/skills/`.
   - Claude Code, Cursor, and OpenViking CLI agents can read `.agents/` configurations seamlessly without reliance on central external agent hosts.
3. **Branch & Code Continuity:**
   - Because all code patches and pull requests reside on GitHub (`origin`), project branches and commit histories remain unaffected by the turndown.
