---
okf_version: "0.2"
type: how-to-guide
title: "Multi-Platform Hosting Guide (GitLab, GitBook, ReadTheDocs)"
description: "Comprehensive guide for configuring cross-platform documentation deployment across GitLab Pages, GitBook, and ReadTheDocs."
status: active
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://docs.gitlab.com/ee/user/project/pages/"
    description: "GitLab Pages documentation."
  - url: "https://docs.gitbook.com/"
    description: "GitBook documentation."
  - url: "https://docs.readthedocs.io/en/stable/config-file/v2.html"
    description: "ReadTheDocs v2 configuration specification."
topics:
  - multi-platform
  - gitlab-pages
  - gitbook
  - readthedocs
---

# 🌐 Multi-Platform Documentation Hosting Guide

This project supports seamless multi-platform hosting across GitHub Pages, GitLab Pages, GitBook, and ReadTheDocs.

## Supported Platforms

### 1. GitLab Pages (`.gitlab-ci.yml`)
- Deploys automatically via GitLab CI/CD using Ruby 3.2 and Jekyll.
- Output directory: `public/`.

### 2. GitBook (`.gitbook.yaml`)
- Native GitBook integration reading `README.md` as home and `SUMMARY.md` as table of contents structure.

### 3. ReadTheDocs.org (`.readthedocs.yaml`)
- ReadTheDocs v2 configuration using Python 3.12 and MkDocs dependencies listed in `docs/requirements.txt`.

### 4. Dynamic Markdown Navigation
- All documentation files under `docs/` and root files (`README.md`, `CHANGELOG.md`, `SUMMARY.md`, `HISTORY.md`) are automatically indexed by `tools/generate_summary.py`.
