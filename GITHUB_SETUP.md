# GitHub Repository Setup

## Repository name
project-memory-skill

## Description (one-line, for GitHub repo settings)
Durable project memory across chat loss, model switches, and multi-session research. Promotion rules prevent hypotheses from silently becoming facts. Works with Claude Code, Codex, Gemini CLI, Cursor.

## Topics (add these in repo Settings > Topics)
agent-skills
skill-md
project-memory
context-engineering
claude-code
codex
gemini-cli
cursor
research
decision-log
hypothesis

## Before you push
1. Update `metadata.author` in SKILL.md with your GitHub username
2. Run: git init && git add . && git commit -m "Release v2.0"
3. Create repo: gh repo create project-memory-skill --public --source=. --push
4. Add topics in GitHub repo Settings

## After publishing
1. Submit to awesome-agent-skills:
   https://github.com/VoltAgent/awesome-agent-skills
   → Add your repo under an appropriate category via PR

2. Submit to anthropics/skills:
   https://github.com/anthropics/skills
   → Fork, add your skill folder, submit PR

3. Optional — submit to LobeHub Skills Marketplace:
   https://lobehub.com/skills

4. Optional — submit to skills.sh / agentskill.sh
