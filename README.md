# WorkWork plugin

The official distribution repository for the WorkWork plugin for ChatGPT and
Codex. The plugin bundles three guided workflows with the OAuth-protected
WorkWork MCP server:

- configure a personal or organization WorkWork agent;
- safely process network requests and scheduled checks;
- read and manage conversations with matches.

The WorkWork application and member data remain hosted by WorkWork. This
repository contains only the installable plugin package, marketplace metadata,
icons, and installation tooling. It contains no production credentials or
member data.

## Install

WorkWork requires ChatGPT desktop with plugin support or a recent Codex CLI.
On macOS or Linux, run:

```bash
curl --proto '=https' --tlsv1.2 -fsSL \
  https://workwork.bot/install-workwork-plugin.sh | bash
```

Then fully quit and reopen ChatGPT desktop, start a new chat, and ask:

> Set up my WorkWork agent and turn on hourly checks.

The installer uses the Codex executable bundled with ChatGPT desktop on macOS
when available. Otherwise it uses a compatible `codex` executable on `PATH`.
Git is also required.

### Install from this private repository

Until this repository is public, testers need GitHub read access. Clone it and
run:

```bash
./scripts/install-workwork-plugin.sh
```

If HTTPS Git authentication is not configured, use the SSH source explicitly:

```bash
WORKWORK_MARKETPLACE_SOURCE=git@github.com:workworkbot/workwork-plugin.git \
  ./scripts/install-workwork-plugin.sh
```

Run the same installer again to refresh the marketplace and reinstall the
latest plugin version.

## Workspace installation

ChatGPT workspace administrators can import this repository from
**Admin → Plugins → Add → Import marketplace** using:

```text
https://github.com/workworkbot/workwork-plugin
```

Leave **Path** empty because `.agents/plugins/marketplace.json` is at the
repository root. Leave **Branch, tag, or commit** empty to follow `main`, or
select a release tag for a pinned rollout. Private imports require a GitHub
account that can read this repository.

See OpenAI's documentation for [plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [workspace marketplace imports](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Repository layout

```text
.agents/plugins/marketplace.json       Marketplace catalog
plugins/workwork/.codex-plugin/        Plugin manifest
plugins/workwork/.mcp.json             WorkWork MCP connection
plugins/workwork/skills/               Bundled workflows
plugins/workwork/assets/               Install-surface artwork
scripts/install-workwork-plugin.sh     Individual-user installer
scripts/validate.py                    Dependency-free repository validation
```

## Validate

```bash
python3 scripts/validate.py
bash -n scripts/install-workwork-plugin.sh
bash tests/test-installer.sh
```

CI runs the same checks for every push and pull request. See
[`RELEASING.md`](RELEASING.md) before changing repository visibility or cutting
a release.

## Security and privacy

The plugin connects only to `https://api.workwork.bot/mcp` and authenticates
users through OAuth. Never add access tokens, client secrets, cookies, member
data, or private matching policies to this repository. See
[`SECURITY.md`](SECURITY.md) for reporting instructions and the
[WorkWork privacy policy](https://workwork.bot/privacy) for service details.
