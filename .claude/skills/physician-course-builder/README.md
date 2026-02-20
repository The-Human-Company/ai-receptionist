# Physician Course Builder Skill

Build JSON-based lectures for the physician course preview system.

## Quick Start

1. **Create lecture JSON**: `content/physician-courses/{physician}/{course}/lecture-N.json`
2. **Register**: Add to `content/physician-courses/registry.ts`
3. **Test**: Visit `/preview/courses/{physician}/{course}-N`

## Key Files

- `content/lectures/schema.ts` - TypeScript types for lecture JSON
- `content/physician-courses/registry.ts` - Course registration
- `src/views/preview/*` - Preview components
- `src/components/lectures/UniversalLecture.tsx` - Lecture renderer

## Common Issues

### Nested Anchor Tags
Never nest `<a>` inside `<Link>`. Use `<Link className="..." style={{...}}>Content</Link>`.

### Missing Keys in Lists
Always provide unique `key` props when rendering arrays.

### Network Diagram Property
Use `edges` (not `links`) for network diagram connections.

## Schema Reference

See `SKILL.md` for complete documentation.
