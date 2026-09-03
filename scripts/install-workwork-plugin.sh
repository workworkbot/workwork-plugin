#!/usr/bin/env bash

set -euo pipefail

workwork_marketplace_name="workwork"
workwork_marketplace_source="${WORKWORK_MARKETPLACE_SOURCE:-https://github.com/workworkbot/workwork-plugin.git}"
workwork_marketplace_ref="${WORKWORK_MARKETPLACE_REF:-main}"
workwork_plugin_selector="workwork@${workwork_marketplace_name}"
workwork_codex_bin=""

workwork_info() {
  printf '[WorkWork] %s\n' "$1"
}

workwork_fail() {
  printf '[WorkWork] Error: %s\n' "$1" >&2
  exit 1
}

workwork_try_codex() {
  local workwork_candidate="$1"

  if [[ -n "${workwork_candidate}" ]] && [[ -x "${workwork_candidate}" ]] \
    && "${workwork_candidate}" plugin --help >/dev/null 2>&1; then
    workwork_codex_bin="${workwork_candidate}"
    return 0
  fi

  return 1
}

if [[ -n "${WORKWORK_CODEX_BIN:-}" ]]; then
  workwork_try_codex "${WORKWORK_CODEX_BIN}" \
    || workwork_fail "WORKWORK_CODEX_BIN does not point to a Codex executable with plugin support."
fi

if [[ -z "${workwork_codex_bin}" ]] && [[ "$(uname -s)" == "Darwin" ]]; then
  workwork_try_codex "/Applications/ChatGPT.app/Contents/Resources/codex" || true
fi

if [[ -z "${workwork_codex_bin}" ]] && command -v codex >/dev/null 2>&1; then
  workwork_try_codex "$(command -v codex)" || true
fi

if [[ -z "${workwork_codex_bin}" ]]; then
  for workwork_candidate in \
    "${HOME}/.local/bin/codex" \
    "/opt/homebrew/bin/codex" \
    "/usr/local/bin/codex"; do
    if workwork_try_codex "${workwork_candidate}"; then
      break
    fi
  done
fi

if [[ -z "${workwork_codex_bin}" ]]; then
  workwork_fail "No working Codex CLI with plugin support was found. Install ChatGPT desktop or follow https://learn.chatgpt.com/docs/codex/cli, then run this installer again."
fi

command -v git >/dev/null 2>&1 \
  || workwork_fail "Git is required to install the WorkWork plugin."

workwork_info "Using $("${workwork_codex_bin}" --version)."

if "${workwork_codex_bin}" plugin marketplace list \
  | awk -v marketplace="${workwork_marketplace_name}" '$1 == marketplace { found = 1 } END { exit !found }'; then
  workwork_info "Refreshing the existing ${workwork_marketplace_name} marketplace."
  "${workwork_codex_bin}" plugin marketplace upgrade "${workwork_marketplace_name}"
else
  workwork_info "Connecting the WorkWork marketplace."
  if ! "${workwork_codex_bin}" plugin marketplace add \
    "${workwork_marketplace_source}" \
    --ref "${workwork_marketplace_ref}" \
    --sparse .agents/plugins \
    --sparse plugins/workwork; then
    workwork_fail "Could not download the WorkWork marketplace. Check your network connection and repository access, then run this installer again."
  fi
fi

workwork_info "Installing ${workwork_plugin_selector}."
"${workwork_codex_bin}" plugin add "${workwork_plugin_selector}"

printf '\n'
workwork_info "WorkWork is installed."
workwork_info "Fully quit and reopen ChatGPT desktop, then start a new chat with:"
printf '\n  Set up my WorkWork agent and turn on hourly checks.\n\n'
workwork_info "Authenticate with your own WorkWork account when prompted."
