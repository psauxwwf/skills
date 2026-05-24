from pathlib import Path
import posixpath
import re
import shutil

root = Path("iwe")
docs = [root / "docs/cli.md", *sorted(root.glob("docs/cli-*.md"))]
spec = root / "docs/spec.md"
frontmatter = """---
name: iwe
description: Use when the user works with an IWE knowledge base and needs to search notes, retrieve hierarchical context, inspect document trees, create or update documents, refactor links, normalize Markdown structure, analyze frontmatter/schema statistics, or export the note graph for AI-agent and documentation workflows.
metadata:
  tags: "iwe, markdown-notes, knowledge-base, knowledge-graph, second-brain, note-management, cli, search, retrieval, tree, backlinks, inclusion-links, refactoring, rename, extract, inline, normalize, frontmatter, schema, stats, graph-export, ai-agent-tools"
  category: "knowledge-management"
license: Apache-2.0
---
"""

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def rewrite_link(url: str) -> str:
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url

    path = url
    suffix = ""
    if "#" in path:
        path, fragment = path.split("#", 1)
        suffix = f"#{fragment}"
    if "?" in path:
        path, query = path.split("?", 1)
        suffix = f"?{query}{suffix}"

    if not path:
        return url

    if path.startswith("./iwe/"):
        normalized = posixpath.normpath(path[len("./iwe/") :])
        return f"./{normalized}{suffix}"

    if path.startswith("iwe/"):
        normalized = posixpath.normpath(path[len("iwe/") :])
        return f"./{normalized}{suffix}"

    if path.startswith(("./", "../")) or "/" in path or "." in Path(path).name:
        normalized = posixpath.normpath(posixpath.join("docs", path))
        return f"./{normalized}{suffix}"

    return url


chunks = []
for rel_path in docs:
    text = rel_path.read_text()
    text = link_re.sub(lambda m: f"[{m.group(1)}]({rewrite_link(m.group(2))})", text)
    chunks.append(text.rstrip())


(root / "SKILL.md").write_text(
    "\n".join(
        [
            frontmatter,
            "[IWE Query Language Specification](./SPEC.md)",
            "\n\n".join(chunks),
        ],
    )
)

spec.rename(root / "SPEC.md")

for entry in root.iterdir():
    if entry.name == "SKILL.md":
        continue
    if entry.name == "SPEC.md":
        continue
    if entry.is_dir() and not entry.is_symlink():
        shutil.rmtree(entry)
    else:
        entry.unlink()
