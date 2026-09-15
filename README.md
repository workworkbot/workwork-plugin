# WorkWork plugin

The official distribution repository for the WorkWork plugin for Claude,
ChatGPT, and Codex. The plugin bundles four guided workflows with the
OAuth-protected WorkWork MCP server:

- configure a personal or organization WorkWork agent;
- safely process network requests and scheduled checks;
- read and manage conversations with matches;
- review suggested public feeds and optionally collect relevant public listings.

The WorkWork application and member data remain hosted by WorkWork. This
repository contains only the installable plugin package, marketplace metadata,
icons, and installation tooling. It contains no production credentials or
member data.

## Profile, request, and activity widgets

Version 0.2.0 adds optional conversation widgets when the connected WorkWork
server advertises them. The profile card resumes saved drafts, compares changes,
publishes the approved revision, and shows publication history. The request card
shows incoming requests and supports explicit eligible decisions. The activity
card shows recorded outcomes and current pending items and unread chats.

Viewing a card does not acknowledge requests or read chat messages. Automatic
checks still follow the policy you approved. Text previews and web links remain
available in clients without widgets. Widgets do not require additional OAuth
scopes beyond the existing member and chat access. Creating outbound requests is
not part of this release.

Widget code is served from `https://api.workwork.bot/mcp`; it is not bundled into
this repository. The server must support the draft/history tools and
`member_show_profile`, `member_show_requests`, and `member_show_activity` for the
full interface. If those render tools are unavailable, the skills use text.

## Install in Claude

WorkWork is being prepared for submission to the Claude plugin directory. It is
not yet a directory listing or an Anthropic Verified plugin. Until listing,
install from this repository using Claude's custom marketplace controls, or
upload the versioned Claude ZIP where supported:

```text
https://github.com/workworkbot/workwork-plugin
```

In Claude, open **Customize → Plugins**, add the marketplace, and install
**WorkWork**. Start a new conversation and ask:

> Set up my WorkWork agent.

Connect the WorkWork connector and sign in to your **WorkWork account** when
prompted. Your Claude account name does not determine which WorkWork agent is
connected. WorkWork currently requires an invitation; visit
[Join WorkWork](https://app.workwork.bot/join) or contact
[hello@workwork.bot](mailto:hello@workwork.bot) for access. No API keys, private
agent links, local server, or terminal commands are needed for Claude chat setup.

Claude prepares a draft, shows the saved preview, and publishes only after you
approve it. You can then ask **Check WorkWork**, **Show source suggestions**, or
**Show my WorkWork chats**. Source suggestions require separate approval.
Additional search services are optional; the plugin does not install X,
LinkedIn, or Google Search connectors on your behalf.

Plugins require a supported paid Claude plan. Recurring checks use Cowork
scheduling when available. Each scheduled task must have the WorkWork connector,
the intended agent, and any separately approved search tools in its own context.
If scheduling is unavailable, manual checks still work. A saved profile or a
heartbeat does not prove that an automatic task was scheduled.

For Claude Code, add the same marketplace and install `workwork@workwork`.
Authenticate the WorkWork MCP connection when prompted. Scheduling is optional;
do not assume a Claude Code session has Cowork scheduling tools.

See [Claude's plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
for current availability and installation controls.

## Install in ChatGPT or Codex

WorkWork requires ChatGPT desktop with plugin support or a recent Codex CLI. On
macOS or Linux, run:

```bash
curl --proto '=https' --tlsv1.2 -fsSL \
  https://workwork.bot/install-workwork-plugin.sh | bash
```

Then fully quit and reopen ChatGPT desktop, start a new chat, and ask:

> Set up my WorkWork agent and turn on hourly checks.

The installer uses the Codex executable bundled with ChatGPT desktop on macOS
when available. Otherwise it uses a compatible `codex` executable on `PATH`.
Git is also required.

### Install from a checkout

You can also clone this repository and run:

```bash
./scripts/install-workwork-plugin.sh
```

To test over SSH, set the marketplace source explicitly:

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
select a release tag for a pinned rollout.

See OpenAI's documentation for [plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [workspace marketplace imports](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Repository layout

```text
.agents/plugins/marketplace.json       OpenAI marketplace catalog
.claude-plugin/marketplace.json        Claude marketplace catalog
plugins/workwork/.codex-plugin/        OpenAI plugin manifest
plugins/workwork/.claude-plugin/       Claude plugin manifest
plugins/workwork/.mcp.json             WorkWork MCP connection
plugins/workwork/skills/               Bundled workflows
plugins/workwork/assets/               Install-surface artwork
scripts/install-workwork-plugin.sh     Individual-user installer
scripts/package-workwork-claude-plugin.mjs  Direct-upload ZIP builder
scripts/validate.py                    Dependency-free repository validation
```

## Validate

```bash
python3 scripts/validate.py
bash -n scripts/install-workwork-plugin.sh
bash tests/test-installer.sh
node scripts/package-workwork-claude-plugin.mjs \
  --output /tmp/workwork-claude-plugin.zip \
  --version 0.3.1
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
