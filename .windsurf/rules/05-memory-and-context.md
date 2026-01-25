---
trigger: always_on
---

# Memory & Context Management Rules

Act as if you have perfect memory of the entire repo.

When starting work:
1. First, read AGENTS.md in root
2. Read relevant service/AGENTS.md if editing a specific service
3. Scan .windsurf/rules/ for all numbered rules
4. If task involves pipeline flow, mentally trace: upload → transcriber → analyzer → exporter

Memory update protocol:
- If you discover/implement something important (new convention, bug pattern, performance trick), propose adding it to AGENTS.md "Detailed Architecture & Decision Log"
- Never assume previous context is lost — reference past decisions explicitly
- When user says "continue from last change", assume you remember everything unless contradicted

Context trimming strategy:
- Prioritize: rules > AGENTS.md > current file > related files
- Avoid dumping full files unless asked; summarize diffs or intent