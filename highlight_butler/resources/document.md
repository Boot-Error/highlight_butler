---
title: {{doc.title}}
created: {{doc.created}}
author: {{doc.author}}
tags: {{doc.tags}}
category: {{doc.category}}
url: {{doc.url}}
---

## Summary

## Content
  {% for highlight in doc.highlights %}
  - {{highlight.text}}
    {% if highlight.annotation %}
    - {{highlight.annotation}}
    {% endif %}
    - #ref {{highlight.location.value}}
  {% endfor %}