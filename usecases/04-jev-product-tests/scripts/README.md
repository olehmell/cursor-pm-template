# Scripts

Call Jev with `TYPESAFE_API_KEY`:

```bash
curl -s https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @request.json
```

Endpoint: `POST https://api.typesafe.ai/v1/systemone`
