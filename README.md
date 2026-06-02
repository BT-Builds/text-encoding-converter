# Text Encoding Converter API

Convert text between common encodings: base64, hex, URL encoding, HTML entities, and JSON.

## Endpoints

### Base64

**Encode**: `POST /base64/encode`
```bash
curl -X POST https://text-encoding-converter.vercel.app/base64/encode \
  -H "Content-Type: application/json" \
  -H "X-API-Key: free-demo-key" \
  -d '{"text": "Hello World"}'
```

**Decode**: `POST /base64/decode`
```bash
curl -X POST https://text-encoding-converter.vercel.app/base64/decode \
  -H "Content-Type: application/json" \
  -H "X-API-Key: free-demo-key" \
  -d '{"text": "SGVsbG8gV29ybGQ="}'
```

### Hex

**Encode**: `POST /hex/encode`
```bash
curl -X POST https://text-encoding-converter.vercel.app/hex/encode \
  -H "Content-Type: application/json" \
  -H "X-API-Key: free-demo-key" \
  -d '{"text": "Hello"}'
```

**Decode**: `POST /hex/decode`
```bash
curl -X POST https://text-encoding-converter.vercel.app/hex/decode \
  -H "Content-Type: application/json" \
  -H "X-API-Key: free-demo-key" \
  -d '{"text": "48656c6c6f"}'
```

### URL Encoding

**Encode**: `POST /url/encode` - URL encode (percent-encode) a string
**Decode**: `POST /url/decode` - URL decode a percent-encoded string

### HTML Entities

**Encode**: `POST /html/encode` - Convert special characters to HTML entities
**Decode**: `POST /html/decode` - Convert HTML entities back to characters

### JSON

**Validate & Format**: `POST /json/validate` - Validate JSON and return formatted version (2-space indent)
**Minify**: `POST /json/minify` - Minify JSON string

### Health Check

**GET /health** - No auth required, returns `{"status": "ok"}`

## Pricing

- Free tier: 100 requests/day with `free-demo-key`
- Pro tier: $19/month for 10,000 requests/day

List on RapidAPI for $15/month subscription.