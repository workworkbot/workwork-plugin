# Claude directory candidate

Status: 0.3.1 candidate; live acceptance and submission pending.

## Listing copy

**Name:** WorkWork

**Short description:** Set up your WorkWork agent, review opportunities, and manage conversations with your matches in Claude.

**Description:** WorkWork helps you find relevant collaborators and opportunities through an agent that represents you. Describe what you offer and what you are looking for; Claude prepares your profile, saves a draft, and publishes only after you approve the exact preview. Review incoming requests, manage conversations with matches, and choose public feeds relevant to your interests. Optional Cowork tasks can check requests or collect public listings on a schedule you approve.

**Requirements:** An invited WorkWork account and a Claude plan that supports plugins. Scheduling requires available Cowork scheduling and the tools needed by the task. Additional search services are optional and are not supplied by WorkWork.

**Publisher:** WorkWork. Use the WorkWork-controlled Anthropic Console organization, with the actual authorized submitter identity.

**Repository:** https://github.com/workworkbot/workwork-plugin

**Plugin path:** plugins/workwork

**Homepage:** https://workwork.bot

**Privacy:** https://workwork.bot/privacy

**Support / reviewer access:** hello@workwork.bot

**Category suggestion:** Productivity

## Data and access disclosure

The plugin connects to `https://api.workwork.bot/mcp` through WorkWork OAuth. It can read the connected user's permitted agents, drafts, profiles, requests, source suggestions, and conversations, and make the user-authorized changes exposed by member/chat tools. Draft profile content is saved on WorkWork before publication; public profile publication requires approval. Reading a chat marks it read. Messages require explicit authorization. Scheduled request processing can record decisions and acknowledge completed items under the user's delegated policy.

Private matching preferences stay in the AI client. Do not put credentials or raw imported profile material into the profile. WorkWork receives submitted listing content and relevant source metadata, not third-party search credentials. The package contains no local executable service; the WorkWork server is hosted remotely. Do not claim Anthropic Verified status or list unsupported surfaces.

## Reviewer walkthrough

1. Obtain a WorkWork invitation through hello@workwork.bot and create a dedicated test account. Reviewer access is not bundled in this repository.
2. Install the WorkWork candidate and connect its hosted WorkWork connector through OAuth. Ask “Set up my WorkWork agent.”
3. Describe a truthful offering, inspect the saved draft, and approve the exact preview to publish it. Verify the returned publication result.
4. Ask to resume setup; confirm the published profile is shown before changes. Ask to review requests or show source suggestions. These are separate workflows from profile setup.
5. Run a request-processing cycle only when authorized. If testing scheduling, authorize a Cowork task, observe its result, and pause it afterward. Publishing a profile alone does not schedule checks.
6. Chat actions and additional source creation require their own user instructions. Do not send messages to real members as part of an unannounced test.

## Release evidence

- Candidate exported from the source commit and hashes recorded in SOURCE.json.
- Claude Code 2.1.272 accepted the plugin and marketplace manifests during preparation.
- Public package validation, installer behavior tests, and ZIP integrity checks pass locally.
- The application source passed 36 focused OAuth/onboarding tests and 6 package/export/profile-prompt tests.
- A live Claude OAuth round trip, publication, reconnect, and scheduled run have not yet been recorded for this candidate. No directory approval or verification badge is claimed.

After live acceptance, submit the tested public GitHub plugin path using the WorkWork-controlled Console organization. Review the current form and terms with the authorized publisher. Record the actual submission receipt before changing this status.

[Official submission process](https://claude.com/docs/plugins/submit)
