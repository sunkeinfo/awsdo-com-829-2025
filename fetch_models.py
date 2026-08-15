import urllib.request
import json

url = "https://api.edenai.run/v3/models"
try:
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read())
    models = data.get('data', [])
    for m in models:
        pricing = m.get('pricing') or {}
        inp = pricing.get('input_cost_per_token')
        out = pricing.get('output_cost_per_token')
        inp_per_m = round(inp * 1000000, 4) if inp is not None else None
        out_per_m = round(out * 1000000, 4) if out is not None else None
        print(f"{m['id']}|{m['owned_by']}|{inp_per_m}|{out_per_m}|{m.get('context_length','N/A')}")
except Exception as e:
    print(f"ERROR: {e}")
