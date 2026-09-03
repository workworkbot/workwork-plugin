# Releasing WorkWork

This repository is prepared for distribution but must remain private until a
WorkWork maintainer explicitly approves public visibility.

## Release checklist

1. Copy the reviewed plugin sources from the canonical WorkWork application
   repository. Do not copy application code, environment files, logs, exports,
   customer data, or credentials.
2. Set a SemVer version in
   `plugins/workwork/.codex-plugin/plugin.json` and add the corresponding entry
   to `CHANGELOG.md`.
3. Run:

   ```bash
   python3 scripts/validate.py
   bash -n scripts/install-workwork-plugin.sh
   bash tests/test-installer.sh
   ```

4. Test install, OAuth, all bundled skills, and an upgrade from the prior
   release using a clean ChatGPT desktop or Codex profile.
5. Confirm that `https://api.workwork.bot/mcp`, the website, support email, and
   privacy-policy URL are production-ready.
6. Decide and document the public-source license before making the repository
   public. Absence of a license does not grant reuse rights.
7. Tag the reviewed commit as `vX.Y.Z` and publish release notes.
8. Sync `scripts/install-workwork-plugin.sh` to
   `https://workwork.bot/install-workwork-plugin.sh` and verify that the served
   file matches the tagged release.
9. Change repository visibility only after explicit approval. Visibility is
   not changed by any release or CI workflow in this repository.

For workspace pilots, keep the repository private and grant the importing
GitHub account read access. Workspace admins can pin their import to a release
tag or commit.
