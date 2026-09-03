#!/usr/bin/env bash

set -euo pipefail

workwork_test_dir="$(mktemp -d)"
trap 'rm -rf "${workwork_test_dir}"' EXIT

workwork_fake_codex="${workwork_test_dir}/codex"
workwork_log="${workwork_test_dir}/calls.log"
workwork_marketplace_state="${workwork_test_dir}/marketplace-added"

cat >"${workwork_fake_codex}" <<'EOF'
#!/usr/bin/env bash

set -euo pipefail

printf '%s\n' "$*" >>"${WORKWORK_TEST_LOG}"

case "$*" in
  "plugin --help")
    exit 0
    ;;
  "--version")
    printf 'codex-test 1.0.0\n'
    ;;
  "plugin marketplace list")
    if [[ -f "${WORKWORK_TEST_MARKETPLACE_STATE}" ]]; then
      printf 'workwork https://example.test/workwork-plugin.git\n'
    fi
    ;;
  "plugin marketplace add "*)
    touch "${WORKWORK_TEST_MARKETPLACE_STATE}"
    ;;
  "plugin marketplace upgrade workwork")
    ;;
  "plugin add workwork@workwork")
    ;;
  *)
    printf 'Unexpected fake Codex invocation: %s\n' "$*" >&2
    exit 1
    ;;
esac
EOF

chmod +x "${workwork_fake_codex}"

run_installer() {
  WORKWORK_CODEX_BIN="${workwork_fake_codex}" \
  WORKWORK_MARKETPLACE_SOURCE="https://example.test/workwork-plugin.git" \
  WORKWORK_TEST_LOG="${workwork_log}" \
  WORKWORK_TEST_MARKETPLACE_STATE="${workwork_marketplace_state}" \
    bash scripts/install-workwork-plugin.sh >/dev/null
}

run_installer
run_installer

grep -Fqx \
  "plugin marketplace add https://example.test/workwork-plugin.git --ref main --sparse .agents/plugins --sparse plugins/workwork" \
  "${workwork_log}"
grep -Fqx "plugin marketplace upgrade workwork" "${workwork_log}"

workwork_install_count="$(grep -Fxc "plugin add workwork@workwork" "${workwork_log}")"
if [[ "${workwork_install_count}" != "2" ]]; then
  printf 'Expected two plugin installs, got %s.\n' "${workwork_install_count}" >&2
  exit 1
fi

printf 'Installer behavior is valid.\n'
