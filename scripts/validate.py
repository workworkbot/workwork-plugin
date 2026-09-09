#!/usr/bin/env python3

"""Validate the standalone WorkWork plugin distribution without dependencies."""

from __future__ import annotations

import json
import hashlib
import re
import struct
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_ROOT = ROOT / "plugins" / "workwork"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MCP_PATH = PLUGIN_ROOT / ".mcp.json"


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"Missing required file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def resolve_plugin_path(value: str) -> Path:
    require(value.startswith("./"), f"Plugin path must start with './': {value}")
    resolved = (PLUGIN_ROOT / value).resolve()
    require(resolved.is_relative_to(PLUGIN_ROOT.resolve()), f"Plugin path escapes root: {value}")
    return resolved


def validate_marketplace() -> None:
    marketplace = load_json(MARKETPLACE_PATH)
    require(isinstance(marketplace, dict), "Marketplace root must be an object")
    require(marketplace.get("name") == "workwork", "Marketplace name must be 'workwork'")
    interface = marketplace.get("interface")
    require(isinstance(interface, dict), "Marketplace interface must be an object")
    require(interface.get("displayName") == "WorkWork", "Marketplace displayName must be 'WorkWork'")

    plugins = marketplace.get("plugins")
    require(isinstance(plugins, list) and len(plugins) == 1, "Marketplace must contain one plugin")
    entry = plugins[0]
    require(isinstance(entry, dict), "Marketplace plugin entry must be an object")
    require(entry.get("name") == "workwork", "Marketplace plugin name must be 'workwork'")
    require(entry.get("category") == "Productivity", "Plugin category must be 'Productivity'")
    require(
        entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "Marketplace policy must use AVAILABLE and ON_INSTALL",
    )
    source = entry.get("source")
    require(isinstance(source, dict), "Marketplace source must be an object")
    require(source.get("source") == "local", "Marketplace source type must be 'local'")
    require(source.get("path") == "./plugins/workwork", "Marketplace path must be './plugins/workwork'")


def validate_url(value: object, field: str, expected_host: str | None = None) -> None:
    require(isinstance(value, str), f"{field} must be a URL string")
    parsed = urlparse(value)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"{field} must use HTTPS")
    require(not parsed.username and not parsed.password, f"{field} must not contain credentials")
    require(not parsed.query and not parsed.fragment, f"{field} must not contain a query or fragment")
    if expected_host:
        require(parsed.hostname == expected_host, f"{field} must use host {expected_host}")


def validate_png(path: Path, minimum_size: int) -> None:
    try:
        data = path.read_bytes()[:24]
    except FileNotFoundError as exc:
        raise ValidationError(f"Missing image: {path.relative_to(ROOT)}") from exc
    require(data[:8] == b"\x89PNG\r\n\x1a\n", f"Not a PNG: {path.relative_to(ROOT)}")
    width, height = struct.unpack(">II", data[16:24])
    require(width >= minimum_size and height >= minimum_size, f"Image too small: {path.relative_to(ROOT)}")


def validate_manifest() -> None:
    manifest = load_json(MANIFEST_PATH)
    require(isinstance(manifest, dict), "Plugin manifest root must be an object")
    require(manifest.get("name") == "workwork", "Plugin manifest name must be 'workwork'")
    version = manifest.get("version")
    require(
        isinstance(version, str)
        and re.fullmatch(
            r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?",
            version,
        ),
        "Plugin version must be SemVer",
    )
    require(bool(manifest.get("description")), "Plugin description is required")
    require(manifest.get("repository") == "https://github.com/workworkbot/workwork-plugin", "Repository URL is incorrect")
    validate_url(manifest.get("homepage"), "homepage", "workwork.bot")

    for field in ("skills", "mcpServers"):
        value = manifest.get(field)
        require(isinstance(value, str), f"Manifest field {field} is required")
        require(resolve_plugin_path(value).exists(), f"Manifest path does not exist: {value}")

    interface = manifest.get("interface")
    require(isinstance(interface, dict), "Plugin interface must be an object")
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(bool(interface.get(field)), f"Plugin interface field {field} is required")
    validate_url(interface.get("websiteURL"), "interface.websiteURL", "workwork.bot")
    validate_url(interface.get("privacyPolicyURL"), "interface.privacyPolicyURL", "workwork.bot")

    composer_icon = resolve_plugin_path(interface.get("composerIcon", ""))
    logo = resolve_plugin_path(interface.get("logo", ""))
    validate_png(composer_icon, 128)
    validate_png(logo, 512)


def validate_mcp() -> None:
    config = load_json(MCP_PATH)
    require(isinstance(config, dict), "MCP config root must be an object")
    servers = config.get("mcpServers")
    require(isinstance(servers, dict), "MCP config must contain mcpServers")
    workwork = servers.get("workwork")
    require(isinstance(workwork, dict), "MCP config must contain the workwork server")
    require(workwork.get("type") == "http", "WorkWork MCP transport must be http")
    require(workwork.get("url") == "https://api.workwork.bot/mcp", "WorkWork MCP URL is incorrect")


def validate_skills() -> None:
    skills_root = PLUGIN_ROOT / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    expected = {"configure-workwork-agent", "manage-workwork-chats", "operate-workwork-agent"}
    require({path.name for path in skill_dirs} == expected, "Unexpected WorkWork skill set")

    for skill_dir in skill_dirs:
        skill_path = skill_dir / "SKILL.md"
        agent_path = skill_dir / "agents" / "openai.yaml"
        require(skill_path.is_file(), f"Missing {skill_path.relative_to(ROOT)}")
        require(agent_path.is_file(), f"Missing {agent_path.relative_to(ROOT)}")
        content = skill_path.read_text(encoding="utf-8")
        require(content.startswith("---\n"), f"Missing frontmatter in {skill_path.relative_to(ROOT)}")
        require(
            re.search(rf"^name:\s*[\"']?{re.escape(skill_dir.name)}[\"']?\s*$", content, re.MULTILINE) is not None,
            f"Skill name does not match folder: {skill_dir.name}",
        )
        require("description:" in content.split("---", 2)[1], f"Missing description in {skill_path.relative_to(ROOT)}")


def validate_source() -> None:
    source = load_json(ROOT / "SOURCE.json")
    require(isinstance(source, dict), "SOURCE.json must be an object")
    require(isinstance(source.get("sourceCommit"), str) and re.fullmatch(r"[a-f0-9]{40}", source["sourceCommit"]) is not None, "Missing application source commit")
    require(isinstance(source.get("sourceDirty"), bool), "Missing source cleanliness marker")
    require(source.get("version") == load_json(MANIFEST_PATH).get("version"), "Source version differs from manifest")
    files = source.get("files")
    expected = {
        "plugins/workwork/.mcp.json", "plugins/workwork/.codex-plugin/plugin.json",
        "scripts/install-workwork-plugin.sh",
        *[f"plugins/workwork/skills/{name}/SKILL.md" for name in ("configure-workwork-agent", "operate-workwork-agent", "manage-workwork-chats")],
    }
    require(isinstance(files, dict) and set(files) == expected, "Unexpected exported file set")
    for name, digest in files.items():
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT.resolve()), "Exported file escapes repository")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"Exported file has drifted: {name}")
    if source["sourceDirty"]:
        print("Source checkout had local changes; regenerate from the reviewed clean commit before tagging.")


def main() -> int:
    try:
        validate_marketplace()
        validate_manifest()
        validate_mcp()
        validate_skills()
        validate_source()
    except (ValidationError, OSError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    print("WorkWork plugin distribution is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
