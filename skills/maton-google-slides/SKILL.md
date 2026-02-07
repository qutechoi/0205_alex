---
name: maton-google-slides
description: Create and style Google Slides decks via Maton Google Slides API. Use when generating executive-style decks, programmatically building slides with text boxes, applying corporate themes (colors/typography), or automating slide creation with a Maton connection id.
---

# Maton Google Slides

## Overview
Create Google Slides decks through Maton’s Google Slides API, including layout, text boxes, and executive styling (colors, fonts, cards).

## Workflow
1) Ensure you have a Maton API key and Google Slides connection id.
2) Use the script to create a 5‑slide OpenClaw intro deck with executive styling.
3) Share the resulting Google Slides link with the user.

## Quick start (OpenClaw exec deck)
Run the script:

```bash
python3 skills/maton-google-slides/scripts/create_openclaw_exec_deck.py \
  --api-key-path /Users/qute/clawd/.secrets/maton.key \
  --connection-id <GOOGLE_SLIDES_CONNECTION_ID> \
  --title "OpenClaw 소개 (5장)"
```

It prints the `presentationId`. Share:

```
https://docs.google.com/presentation/d/<presentationId>/edit
```

## Notes
- Uses `BLANK` layouts for full control.
- Styles: navy/white base, gold/sky accents, bold minimal typography.
- If you need to adjust API details, read `references/maton-google-slides.md`.

## Resources
- `scripts/create_openclaw_exec_deck.py`: creates + styles a 5‑slide OpenClaw deck.
- `references/maton-google-slides.md`: Maton Google Slides API quick reference.
