#!/usr/bin/env python3
"""Build llms-full.txt by concatenating the pages listed in llms.txt."""
import re
from pathlib import Path

BASE = "https://arviz-devs.github.io/EABM/"
SRC_ROOT = Path(".")  # repo root; Chapters/Foo.qmd <-> Chapters/Foo.html

LINK = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

def source_for(url: str) -> Path | None:
    if not url.startswith(BASE) or not url.endswith(".html"):
        return None
    return SRC_ROOT / (url[len(BASE):-5] + ".qmd")

def main() -> None:
    llms = Path("llms.txt").read_text(encoding="utf-8")
    header = llms.split("\n## ", 1)[0].rstrip()
    parts = [header, ""]
    for line in llms.splitlines():
        m = LINK.match(line)
        if not m:
            continue
        src = source_for(m["url"])
        if src is None:
            continue
        if not src.exists():
            raise SystemExit(f"Missing source for {m['url']}: {src}")
        body = FRONTMATTER.sub("", src.read_text(encoding="utf-8")).strip()
        parts += ["\n---\n", f"<!-- Source: {m['url']} -->", body, ""]
    Path("llms-full.txt").write_text("\n".join(parts), encoding="utf-8")

if __name__ == "__main__":
    main()