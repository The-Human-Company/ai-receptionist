---
name: deploy-pipeline
description: Deploy or update a VectorShift pipeline
argument-hint: <pipeline-id or "new">
---

# Deploy or Update a VectorShift Pipeline

You are helping the user deploy or update a VectorShift pipeline.

## If updating an existing pipeline:

1. Ask for the pipeline ID (or help them find it in the registry)
2. Fetch the existing pipeline: `Pipeline.fetch(id="...")`
3. Create updated nodes with **strings, not bytes** (critical: use `""` not `b""`)
4. Replace nodes: `pipeline.nodes = [...]`
5. Save: `pipeline.save()` - this DOES work when done correctly!

## If creating a new pipeline:

1. Use `Pipeline.new(name="...", nodes=[...])`
2. Update `vs_pipelines/registry.py` with the new ID
3. Mark previous version as DEPRECATED if applicable

## Critical Checklist:

- [ ] All node parameters use strings (`""`) not bytes (`b""`)
- [ ] Prompt templates have escaped curly braces (`{{` and `}}`)
- [ ] Test syntax locally before deploying
- [ ] Verify on VectorShift after deployment

## Common Error Fixes:

- **TypeError: bytes not JSON serializable** → Replace `b""` with `""`
- **KeyError on deploy** → Escape curly braces in prompts
- **500 on save** → Try creating new pipeline instead

Read `.claude/skills/vectorshift-pipeline-deployment.md` for the full deployment guide.
