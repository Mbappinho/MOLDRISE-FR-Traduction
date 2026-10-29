"""Minimal Gemini (Google AI Studio) client: reads GEMINI_API_KEY from the project .env (never printed)."""
import json, os, pathlib, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = "https://generativelanguage.googleapis.com/v1beta"


def key() -> str:
    k = os.environ.get("GEMINI_API_KEY", "")
    if not k:
        for line in (ROOT / ".env").read_text("utf-8").splitlines():
            if line.startswith("GEMINI_API_KEY="):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        raise SystemExit("GEMINI_API_KEY missing in .env")
    return k


def _req(path, body=None, retries=1, wait=30):
    url = f"{API}{path}"
    for attempt in range(retries):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                     headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")[:400]
            if e.code in (429, 500, 503) and attempt < retries - 1:
                time.sleep(wait * (attempt + 1))
                continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
    raise SystemExit("unreachable")


def models():
    return _req("/models?pageSize=200")


def generate(model, system, user, json_mode=True, temperature=0.2, retries=4):
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": temperature},
    }
    if json_mode:
        body["generationConfig"]["responseMimeType"] = "application/json"
    r = _req(f"/models/{model}:generateContent", body, retries=retries)
    parts = r["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts), r.get("usageMetadata", {})
