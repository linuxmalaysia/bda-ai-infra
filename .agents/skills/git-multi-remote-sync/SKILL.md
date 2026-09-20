---
okf_version: "0.2"
name: git-multi-remote-sync
type: skill
title: "Git Multi-Remote Dual-Sync and Credential Isolation Protocol"
description: "Runbook for synchronizing independent or divergent remotes (GitHub and GitLab), preserving commit histories, merging CI pipelines, and isolating local authentication tokens."
status: active
timestamp: "2026-09-20T00:00:00Z"
stale_after: "2027-09-20T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://git-scm.com/docs/git-remote"
    description: "Official Git Remote reference documentation."
topics:
  - dsom
  - skill
  - git
  - gitops
  - multi-remote
  - security
---

# Git Multi-Remote Dual-Sync & Credential Isolation Skill

## Context & Purpose
When operating repositories that must synchronize across multiple independent git remotes (e.g. GitHub and GitLab) without losing history or leaking credentials:
1. Local secrets must be stored outside git tracking.
2. Distinct branch lineages must be reconciled using `--allow-unrelated-histories`.
3. CI/CD pipelines (e.g. GitLab CI security templates and Pages) must be merged cleanly.
4. Both endpoints must be verified and kept in lockstep.

---

## Operational Workflow

### 1. Credential Isolation & Gitignore Verification
Before writing any access tokens or sensitive local configs:
- Inspect `.gitignore` and ensure `.credentials`, `.env`, and `.env.*` are explicitly listed.
- Verify using `git check-ignore -v .credentials`.
- Store credentials in `.credentials` with restrictive permissions. Never stage or commit this file.

### 2. Remote Configuration
Add or inspect the second remote endpoint:
```bash
git remote add <remote_name> <authenticated_or_ssh_url>
git remote -v
```

### 3. Fetch and Merge Unrelated Histories
Fetch remote objects and merge with lineage preservation:
```bash
git fetch <remote_name>
git merge <remote_name>/main --allow-unrelated-histories -m "chore: merge <remote_name>/main history"
```

### 4. Conflict Resolution & Pipeline Unification
- For duplicate READMEs or documentation, prefer local authoritative architecture docs (`git checkout --ours README.md`).
- For CI configuration files (e.g. `.gitlab-ci.yml`), merge platform-native scanning templates (SAST, Secret Detection) with application deployment stages (Jekyll Pages, containers).

### 5. Dual-Target Push & Lineage Confirmation
Push synchronized commits to both endpoints:
```bash
git push <remote_name> main
git push origin main
git remote -v && git status
```
