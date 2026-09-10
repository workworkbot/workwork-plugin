# Changelog

All notable changes to the WorkWork plugin are documented here.

## 0.3.0 - Unreleased

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
