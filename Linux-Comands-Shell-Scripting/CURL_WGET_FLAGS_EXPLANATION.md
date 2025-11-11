# curl vs wget Flags Explanation

## Flag Comparison

| Task | curl | wget |
|------|------|------|
| Save to specific file | `-o filename` | `-O filename` |
| Save using URL filename | `-O` (capital O) | (default behavior) |
| Follow redirects | `-L` (required) | (default, up to 20) |
| Silent/quiet mode | `-s` | `-q` |
| Show progress | (default) | (default) or `--progress=bar` |
| Resume download | `-C -` | `-c` |

## Detailed Examples

### curl Examples

```bash
# Download and save to specific file
curl -o data.csv "https://api.example.com/data.csv"

# Download and save with URL filename
curl -O "https://api.example.com/data.csv"

# Follow redirects and save to file
curl -L -o data.csv "https://api.example.com/data.csv"

# Silent mode (no progress bar)
curl -s -o data.csv "https://api.example.com/data.csv"

# With headers (REST API)
curl -H "Authorization: Bearer token" \
     -H "Accept: application/json" \
     -o response.json \
     "https://api.example.com/endpoint"
```

### wget Examples

```bash
# Download and save to specific file
wget -O data.csv "https://api.example.com/data.csv"

# Download using URL filename (default)
wget "https://api.example.com/data.csv"

# Quiet mode
wget -q -O data.csv "https://api.example.com/data.csv"

# With headers (REST API)
wget --header="Authorization: Bearer token" \
     --header="Accept: application/json" \
     -O response.json \
     "https://api.example.com/endpoint"
```

## REST API Context

### HTTP Status Codes and Redirects

REST APIs use HTTP status codes:
- **200 OK**: Success
- **301/302**: Redirect (temporary or permanent)
- **400**: Bad Request
- **401**: Unauthorized (need authentication)
- **404**: Not Found
- **500**: Server Error

### Why -L Matters for REST APIs

Many REST APIs use redirects:
1. **Short URLs**: `https://api.example.com/v1/data` → redirects to → `https://api.example.com/v1/data.csv`
2. **CDN redirects**: API endpoint redirects to CDN server
3. **Version changes**: Old endpoint redirects to new endpoint

**Without `-L` in curl**: You get the redirect response (301/302) instead of the actual data
**With `-L` in curl**: Follows the redirect and gets the actual data
**wget**: Follows redirects automatically (no flag needed)

### Real-World REST API Example

```bash
# Your call_API.py script uses curl-like behavior:
# GET request to API endpoint
# Headers: X-API-KEY, Accept: application/json
# Params: limit=5, currency=USD

# Equivalent curl command:
curl -L \
  -H "X-API-KEY: your_api_key" \
  -H "Accept: application/json" \
  -G \
  -d "limit=5" \
  -d "currency=USD" \
  -o coins.json \
  "https://openapiv1.coinstats.app/coins"

# Equivalent wget command:
wget \
  --header="X-API-KEY: your_api_key" \
  --header="Accept: application/json" \
  -O coins.json \
  "https://openapiv1.coinstats.app/coins?limit=5&currency=USD"
```

## Key Differences Summary

1. **Output file flag**: 
   - curl: `-o` (lowercase)
   - wget: `-O` (uppercase)

2. **Redirects**:
   - curl: Needs `-L` flag
   - wget: Automatic (default)

3. **URL filename**:
   - curl: Needs `-O` (capital O) to use URL filename
   - wget: Uses URL filename by default

4. **REST API support**:
   - curl: Better for REST (easier headers, POST/PUT/DELETE)
   - wget: Better for simple downloads, can do REST but more verbose

5. **Default behavior**:
   - curl: Prints to stdout by default
   - wget: Saves to file by default

## Best Practices

1. **Always use `-L` with curl** when calling REST APIs (unless you specifically want to handle redirects manually)

2. **Always specify output file** for scripts:
   - curl: `-o filename`
   - wget: `-O filename`

3. **For REST APIs**, curl is often preferred because:
   - Easier header syntax: `-H "Header: Value"`
   - Better support for POST/PUT/DELETE
   - More control over request methods

4. **For simple file downloads**, either works fine, but wget is more straightforward

