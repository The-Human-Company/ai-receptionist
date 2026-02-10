Review and manage the project blockers list.

Steps:
1. Read the blockers section from `n8n-workflow-analysis.md` (Section 9) and `CLAUDE.md`
2. Display current blockers with their status
3. Ask the user if they want to:
   a. **Resolve a blocker** - Mark it resolved and update affected files with the new information
   b. **Add a blocker** - Add a new dependency/question to the list
   c. **Reprioritize** - Reorder based on what's most critical for next steps
4. Update both `n8n-workflow-analysis.md` and `CLAUDE.md` with changes
5. If a blocker is resolved with new info (e.g., Talkroute credentials provided), identify which workflow nodes need updating and offer to apply the changes
