---
okf_version: "0.2"
type: reference
title: "BDA AI Infra :: Enterprise Big Data & AI Architecture"
description: "Enterprise Big Data Analytics & AI Lakehouse Architecture Blueprint & Documentation"
status: active
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://linuxmalaysia.github.io/bda-ai-infra/"
    description: "Documentation homepage."
topics:
  - bda
  - ai-infra
  - homepage
layout: default
---

{% capture raw_readme %}{% include_relative README.md %}{% endcapture %}
{% assign parts = raw_readme | split: "---" %}
{% for part in parts offset: 2 %}{% if forloop.first == false %}---{% endif %}{{ part }}{% endfor %}
