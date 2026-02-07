# Maton Google Slides API quick reference

- Base URL: `https://gateway.maton.ai/google-slides/v1`
- Auth: `Authorization: Bearer <MATON_API_KEY>`
- Connection header: `X-Maton-Connection-Id: <connection-id>`

## Create presentation
`POST /presentations` with `{ "title": "..." }`

## Batch update
`POST /presentations/{presentationId}:batchUpdate` with `{ "requests": [...] }`

## Common errors
- 400: Missing/invalid connection, malformed request
- 401: Invalid API key
- 404: Presentation not found
- 429: Rate limit

## Notes
- Use `BLANK` layout for full control with custom text boxes.
- IDs must be unique within a presentation.
- Sizes/positions use EMU (914400 per inch).
