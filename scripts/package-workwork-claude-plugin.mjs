#!/usr/bin/env node
import { createHash } from "node:crypto";
import { copyFile, mkdir, mkdtemp, readFile, rm, utimes, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pluginRoot = resolve(root, "plugins/workwork");
const fixedTime = new Date("2000-01-01T00:00:00.000Z");

export const claudePluginFiles = [
  ".claude-plugin/plugin.json",
  ".mcp.json",
  "skills/configure-workwork-agent/SKILL.md",
  "skills/operate-workwork-agent/SKILL.md",
  "skills/manage-workwork-chats/SKILL.md",
];

function assertSafeRelativePath(path) {
  if (isAbsolute(path) || path === "" || path.split("/").includes("..")) {
    throw new Error(`Unsafe plugin path: ${path}`);
  }
}

function normalizeMcpUrl(value) {
  if (!value) return undefined;
  let url;
  try {
    url = new URL(value);
  } catch {
    throw new Error("The MCP URL must be a valid public HTTPS URL.");
  }
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash || url.pathname !== "/mcp") {
    throw new Error("The MCP URL must be a public HTTPS URL ending in /mcp, without credentials, query parameters, or a fragment.");
  }
  return url.toString();
}

export async function packageClaudePlugin({ output, version, mcpUrl } = {}) {
  if (!output) throw new Error("An output .zip path is required.");
  if (!/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(version ?? "")) {
    throw new Error("Use a release SemVer without a development cache suffix.");
  }
  const resolvedMcpUrl = normalizeMcpUrl(mcpUrl);
  const outputPath = resolve(output);
  if (!outputPath.endsWith(".zip")) throw new Error("Claude plugin output must be a .zip file.");
  const stage = await mkdtemp(join(tmpdir(), "workwork-claude-plugin-"));
  try {
    for (const path of claudePluginFiles) {
      assertSafeRelativePath(path);
      const source = resolve(pluginRoot, path);
      const within = relative(pluginRoot, source);
      if (within.startsWith("..") || isAbsolute(within)) throw new Error(`Plugin source escapes root: ${path}`);
      const target = resolve(stage, path);
      await mkdir(dirname(target), { recursive: true });
      await copyFile(source, target);
      if (path === ".claude-plugin/plugin.json") {
        const manifest = JSON.parse(await readFile(target, "utf8"));
        manifest.version = version;
        await writeFile(target, `${JSON.stringify(manifest, null, 2)}\n`);
      }
      if (path === ".mcp.json" && resolvedMcpUrl) {
        const mcpConfig = JSON.parse(await readFile(target, "utf8"));
        mcpConfig.mcpServers.workwork.url = resolvedMcpUrl;
        await writeFile(target, `${JSON.stringify(mcpConfig, null, 2)}\n`);
      }
      await utimes(target, fixedTime, fixedTime);
    }
    await mkdir(dirname(outputPath), { recursive: true });
    await rm(outputPath, { force: true });
    execFileSync("zip", ["-X", "-q", outputPath, ...claudePluginFiles], { cwd: stage, stdio: "inherit" });
    const sha256 = createHash("sha256").update(await readFile(outputPath)).digest("hex");
    const sourceCommit = execFileSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" }).trim();
    return { output: outputPath, version, mcpUrl: resolvedMcpUrl ?? "https://api.workwork.bot/mcp", sha256, sourceCommit, files: claudePluginFiles };
  } finally {
    await rm(stage, { recursive: true, force: true });
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const output = args[args.indexOf("--output") + 1];
  const version = args[args.indexOf("--version") + 1];
  const mcpUrl = args.includes("--mcp-url") ? args[args.indexOf("--mcp-url") + 1] : undefined;
  if (!args.includes("--output") || !args.includes("--version")) {
    throw new Error("Usage: node scripts/package-workwork-claude-plugin.mjs --output /path/workwork-claude-plugin.zip --version X.Y.Z [--mcp-url https://public-host/mcp]");
  }
  console.log(JSON.stringify(await packageClaudePlugin({ output, version, mcpUrl }), null, 2));
}
