---
okf_version: "0.2"
type: tutorial
title: "GitHub Pages Setup & Deployment Guide"
description: "Step-by-step instructions for configuring GitHub Pages with automated Jekyll CI/CD workflow."
status: active
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll"
    description: "Official GitHub Pages Jekyll documentation."
topics:
  - github-pages
  - jekyll
  - ci-cd
  - deployment
---

# 🚀 GitHub Pages Setup & Deployment Guide

This guide details how to configure GitHub Pages for automated building and publishing of documentation using Jekyll.

## Overview

GitHub Pages is configured using the official GitHub Actions workflow `.github/workflows/jekyll-gh-pages.yml`. On every push to the `main` branch, GitHub Actions builds the static site using Jekyll and deploys it to the `github-pages` environment.

## Step-by-Step Configuration

1. **Repository Settings**:
   - Navigate to **Settings > Pages** in your GitHub repository.
   - Under **Build and deployment > Source**, select **GitHub Actions**.

2. **Jekyll Configuration (`_config.yml`)**:
   - Ensure `_config.yml` at root specifies `url` and `baseurl`:
     ```yaml
     title: "BDA AI Infra :: Enterprise Big Data & AI Architecture"
     baseurl: "/bda-ai-infra"
     url: "https://linuxmalaysia.github.io"
     ```

3. **Workflow Verification**:
   - The workflow `.github/workflows/jekyll-gh-pages.yml` executes:
     - `actions/checkout@v4`
     - `actions/configure-pages@v5`
     - `actions/jekyll-build-pages@v1`
     - `actions/deploy-pages@v5`

4. **Automated Publishing**:
   - The site is automatically published at `https://linuxmalaysia.github.io/bda-ai-infra/`.
