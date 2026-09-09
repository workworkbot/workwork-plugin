# Releasing WorkWork

This public repository distributes the reviewed plugin package. Widget resources
and application state are served by WorkWork's authenticated MCP server.

## Prepare the package

From a clean checkout of the reviewed application commit, run:

```bash
node scripts/export-workwork-plugin.mjs --target /path/to/workwork-plugin --version X.Y.Z
node scripts/export-workwork-plugin.mjs --target /path/to/workwork-plugin --version X.Y.Z --write
node scripts/export-workwork-plugin.mjs --target /path/to/workwork-plugin --version X.Y.Z --check
```

The first command lists proposed changes without writing. The exporter copies
only the enumerated skills, MCP configuration, and public installer; it preserves
this repository's identity, artwork, and release-owned documentation. It also
records the application commit and file hashes in SOURCE.json. Do not copy the
application tree, environment files, logs, credentials, or member data.

## Validate and release

1. Review the companion public PR and update the changelog and documentation.
   Require SOURCE.json to identify the reviewed application commit with
   sourceDirty=false. Set an ordinary release SemVer without a local cache suffix.
2. Run `python3 scripts/validate.py`, `bash -n scripts/install-workwork-plugin.sh`,
   and `bash tests/test-installer.sh`. Verify the SOURCE.json hashes.
3. Deploy compatible server resources first. Enable MCP_WIDGETS_ENABLED for the
   staged compatibility check before releasing widget instructions publicly.
4. Test clean installation, OAuth, saved drafts across conversations, publication,
   request actions, activity refresh, and an upgrade from the prior package in
   ChatGPT. Test the text-only Codex workflow too. Do not change OAuth scopes for
   this release.
5. Confirm production MCP, website, support, and privacy links. Keep the previous
   UI resource version available for existing conversations. Disabling widget
   discovery must preserve the data tools and text/web workflow.
6. Tag the reviewed package commit as vX.Y.Z and publish its release notes.
7. Verify the installer hosted at https://workwork.bot/install-workwork-plugin.sh
   matches this repository's scripts/install-workwork-plugin.sh. Its canonical
   application source is scripts/install-workwork-plugin-public.sh; the separate
   development installer is not the public release artifact.

Repository visibility is not changed by release tooling. This procedure does not
install plugins into a maintainer's personal profile automatically.
