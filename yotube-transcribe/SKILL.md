---
name: yotube-transcribe
description: Use for YouTube spoken-content tasks (transcripts, subtitles/captions, spoken summaries, quotes with timestamps, translation/localization, video speech comparison). Outputs clean markdown via scripts/subs with frontmatter (title, description, url).
metadata:
  tags: "youtube, transcript, subtitles, captions, localization"
  category: "media-processing"
license: MIT
allowed-tools: Bash
---

# yotube-transcribe

Skill for extracting transcript text from YouTube subtitles via `scripts/subs`.

## When to use

- The user asks for a YouTube transcript.
- The user asks to watch a video and summarize what is said in it.
- The user asks to describe a video based on its spoken content.
- The user provides links to YouTube domains (`youtube.com`, `youtu.be`, etc.) and needs transcript-based analysis.
- The user asks for subtitles in a specific language (`ru`, `en`, etc.).
- You need original auto subtitles when the language is unknown or not important.
- You need markdown output with frontmatter (`title`, `description`, `url`) and transcript text.
- The user asks to extract exact quotes/timestamps from spoken content.
- The user wants to translate, adapt, or localize subtitles based on original speech.
- The user needs to compare what is said across multiple YouTube videos.

## Instructions

1. Run the script from the skill directory:
   - `scripts/subs -l <lang> <youtube_url>` for an explicit language.
   - `scripts/subs -a <youtube_url>` for auto mode (uses `.*-orig`).
2. If the user does not provide a language, default to `-l en`.
3. If `-l <lang>` fails, retry with `-a` (or `-l '.*-orig'`) as fallback.
4. Return the script's markdown output as-is (including frontmatter).
5. Intermediate `.vtt/.srt` files are written to a temp directory and removed automatically.

## `subs` command: usage modes

### 1) Explicit language

Use this when the user specifies a language.

```bash
scripts/subs -l ru https://youtu.be/F1Ulyh55w7E
scripts/subs -l en https://youtu.be/F1Ulyh55w7E
```

- Only one language is supported per run.
- If multiple comma-separated languages are provided, the script returns an error.

### 2) Auto mode

Use this when language is not provided, unknown, or when original auto subtitles are preferred.

```bash
scripts/subs -a https://www.youtube.com/watch?v=xxxx
```

- Internally uses `--sub-langs '.*-orig'`.

### 3) Default behavior

If neither `-l` nor `-a` is provided, `en` is used:

```bash
scripts/subs https://youtu.be/F1Ulyh55w7E
```

### 4) Help

```bash
scripts/subs -h
```

Shows usage and examples.

## Output format

The script prints markdown:

```markdown
---
title: <video title>
description: |
  <video description multiline>
url: <canonical video url>
---

<clean subtitles text>
```

- Text is cleaned from timecodes, WEBVTT markers, HTML tags, technical lines, and duplicates.
- Sentences are merged into readable lines.

## Errors and constraints

- Requires exactly one URL as the last argument.
- Missing arguments or invalid flags return usage and a non-zero exit code.
- If a language is unavailable, the script tries fallback `.*-orig` (when not started with `-a`).
- If both language and fallback fail, the script returns an error.

## Agent rules

- Return useful content (frontmatter + transcript text), not raw `yt-dlp` logs.
- If the user requested a specific language, try it first.
- If language is not specified, use `en`, then fall back to `-a` on failure.
- Do not change output format unless explicitly asked.

## Requirements

- Install `yt-dlp` from: https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#recommended
