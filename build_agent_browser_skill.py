from pathlib import Path
import shutil
import subprocess
import tempfile


REPO_URL = "https://github.com/vercel-labs/agent-browser.git"
ROOT = Path("agent-browser")
UPSTREAM_SKILLS_DIR = "skill-data"

FRONTMATTER = """---
name: agent-browser
description: Use when the user needs agent-browser browser automation, including opening websites, clicking and filling pages, screenshots, data extraction, web app testing, authentication flows, Electron desktop app automation, Slack automation, exploratory QA, Vercel Sandbox browsers, or AWS Bedrock AgentCore cloud browsers. This bundled skill mirrors vercel-labs/agent-browser skill-data; core is the primary skill and the others are helpers.
metadata:
  tags: "agent-browser, browser-automation, web-automation, cdp, chrome, screenshots, scraping, testing, qa, electron, slack, vercel-sandbox, agentcore"
  category: "browser-automation"
license: Apache-2.0
---
"""


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}

    end = text.find("\n---", 4)
    if end == -1:
        return {}

    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    return data


def clone_repo(destination: Path) -> None:
    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            REPO_URL,
            str(destination),
        ],
        check=True,
    )


def copy_skill_data(source: Path, target: Path) -> list[dict[str, str]]:
    target.mkdir(parents=True, exist_ok=True)

    skills = []
    for entry in sorted(source.iterdir(), key=lambda path: path.name):
        if not entry.is_dir():
            continue

        skill_file = entry / "SKILL.md"
        if not skill_file.exists():
            continue

        destination = target / entry.name
        shutil.copytree(entry, destination)

        metadata = parse_frontmatter(skill_file.read_text())
        skills.append(
            {
                "name": metadata.get("name", entry.name),
                "description": metadata.get("description", ""),
                "path": f"./{entry.name}/SKILL.md",
            }
        )

    return sorted(skills, key=lambda skill: (skill["name"] != "core", skill["name"]))


def write_main_skill(skills: list[dict[str, str]]) -> None:
    rows = []
    for skill in skills:
        role = "primary" if skill["name"] == "core" else "helper"
        rows.append(
            f"| `{skill['name']}` | {role} | [{skill['path']}]({skill['path']}) | {skill['description']} |"
        )

    helpers = [skill for skill in skills if skill["name"] != "core"]
    helper_links = [
        f"- [`{skill['name']}`]({skill['path']}) - {skill['description']}"
        for skill in helpers
    ]

    body = f"""# agent-browser

This skill bundles every runtime skill from [`vercel-labs/agent-browser/{UPSTREAM_SKILLS_DIR}`]({REPO_URL.rstrip(".git")}/tree/main/{UPSTREAM_SKILLS_DIR}).

## How To Use

- Start with [`core`](./core/SKILL.md). It is the primary agent-browser workflow guide and should be read before running `agent-browser` commands.
- Use the other bundled skills only as helpers when the task leaves normal web-page automation: Electron apps, Slack, exploratory QA, Vercel Sandbox, or AWS Bedrock AgentCore.
- The skill directories (`./core/`, `./electron/`, and the other helpers) are copied from upstream `skill-data`, including their `references/` and `templates/` directories.
- Regenerate this skill with `python3 ./build_agent_browser_skill.py`; do not edit generated files by hand unless you intend to fork the upstream content.

## Included Skills

| Skill | Role | Link | Description |
| --- | --- | --- | --- |
{chr(10).join(rows)}

## Primary Skill

Read [`./core/SKILL.md`](./core/SKILL.md) first. It covers the standard snapshot-and-ref loop, navigation, clicking, filling, extracting text/data, screenshots, tabs, sessions, waiting, auth, and troubleshooting.

## Helper Skills

{chr(10).join(helper_links)}
"""

    (ROOT / "SKILL.md").write_text(FRONTMATTER + "\n" + body)


def main() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir()

    with tempfile.TemporaryDirectory(prefix="agent-browser-skill-") as tmp:
        repo = Path(tmp) / "repo"
        clone_repo(repo)

        source = repo / UPSTREAM_SKILLS_DIR
        if not source.is_dir():
            raise RuntimeError(f"Upstream directory not found: {source}")

        skills = copy_skill_data(source, ROOT)

    if not any(skill["name"] == "core" for skill in skills):
        raise RuntimeError("Upstream skill-data does not contain the core skill")

    write_main_skill(skills)


if __name__ == "__main__":
    main()
