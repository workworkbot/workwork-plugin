# Changelog

All notable changes to the WorkWork plugin are documented here.

## 0.5.2 - 2026-09-22

- Explain optional server fallback matching from approved public profiles when an agent has not answered; private rules remain in the client.
- Point members to the offline-matching switch on their agent page.
- Teach returning agents to respect a match already recorded by WorkWork and show the owner how to leave an unwanted chat or disable future fallback matches.
- Preserve broadcast delivery and the existing MCP tool inventory. Server activation follows a staged production rollout.

## 0.4.0 - 2026-09-15

- Review a campaign-prepared profile first: keep, refine, or dismiss it before ordinary onboarding.
- Acknowledge an existing saved or published profile without writing, discarding, or publishing.
- Add the generate-workwork-sources skill for suggested feeds and daily collection.

## 0.3.0 - 2026-09-15

- Add the Claude marketplace and plugin manifests alongside the existing OpenAI marketplace.
- Support installation from the same GitHub repository in Claude Desktop and Cowork.
- Use portable configure, operate, and chat skills across Claude, ChatGPT, and Codex.
- Add a deterministic, allowlisted Claude direct-upload ZIP builder.
- Keep the hosted OAuth-protected MCP server as the only runtime dependency.

## 0.2.0 - 2026-09-09

- Resume persistent profile drafts and publish the exact approved saved revision.
- Recover publication receipts and compare/restore retained profile history.
- Show optional profile, incoming-request, and recorded-activity widgets.
- Preserve automated processing, explicit agent selection, and text-only fallback.
- Respect decisions recorded manually while a background agent is processing.
- Record the application source revision and exported file hashes in SOURCE.json.

## 0.1.0 - 2026-09-03

- Package personal and organization agent configuration.
- Package safe manual and scheduled opportunity processing.
- Package matched-conversation management.
- Add the OAuth-protected WorkWork MCP connection.
- Add a standalone marketplace, installer, artwork, and validation workflow.
