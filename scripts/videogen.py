#!/usr/bin/env python3
"""Generate a short clip (b-roll behind a script, four to eight seconds)
with whichever video model this app has a key for. Video is expensive and
slow next to a picture; the video-script skill says when a clip earns it.

    python3 scripts/videogen.py --prompt "…" --ratio 9:16 --seconds 6 --out creatives/generated/<id>/clip.mp4
                                [--ref frame.png] [--provider openrouter|fal] [--model …]
    python3 scripts/videogen.py --check

Providers, in the order tried:

  OPENROUTER_API_KEY   POST $OPENROUTER_BASE_URL/videos (async: 202 with a polling URL, then
                       GET until done); default model google/veo-3.1; a reference image goes
                       in as input_references.
  FAL_KEY              queue.fal.run (async: status_url, then response_url); default model
                       fal-ai/veo3.1 (also FAL_API_KEY).

Direct Gemini Veo and Runway are not wired (their request shapes were not
verified when this was written); OpenRouter reaches Veo, Hailuo and Wan
with the one key. The bytes go to --out (mp4) and the provider, model,
cost and prompt to <out>.json. Exit 3 when no provider is configured.
The same no-text rule as pictures applies: the template and the captions
carry the words; the clip carries the scene.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import die  # noqa: E402

NO_TEXT = " No text, no letters, no logos, no watermarks, no captions burnt into the picture."


def providers():
    env = os.environ
    out = []
    if env.get("OPENROUTER_API_KEY") or env.get("OPENROUTER_BASE_URL"):
        out.append("openrouter")
    if env.get("FAL_KEY") or env.get("FAL_API_KEY"):
        out.append("fal")
    return out


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()


def _requests():
    try:
        import requests
        return requests
    except ImportError:
        die("requests is not installed (setup.sh installs it)")


def gen_openrouter(prompt, ratio, seconds, refs, model):
    requests = _requests()
    base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    headers = {"Content-Type": "application/json", "HTTP-Referer": "https://taskandtool.app", "X-Title": "Task & Tool creatives"}
    if os.environ.get("OPENROUTER_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["OPENROUTER_API_KEY"]
    body = {"model": model or "google/veo-3.1", "prompt": prompt, "aspect_ratio": ratio, "duration": seconds}
    if refs:
        body["input_references"] = [{"type": "image_url", "image_url": {"url": data_url(r)}} for r in refs]
    r = requests.post(base + "/videos", headers=headers, json=body, timeout=120)
    if r.status_code not in (200, 201, 202):
        die(f"openrouter answered {r.status_code}: {r.text[:600]}")
    job = r.json()
    poll = job.get("polling_url") or (base + f"/videos/{job.get('id')}" if job.get("id") else None)
    if not poll:
        die(f"openrouter returned no job: {json.dumps(job)[:400]}")
    deadline = time.time() + 900
    while time.time() < deadline:
        time.sleep(5)
        res = requests.get(poll, headers=headers, timeout=60).json()
        status = str(res.get("status", "")).lower()
        if status in ("completed", "succeeded", "done", "ready"):
            item = (res.get("data") or [res])[0]
            url = item.get("url") or item.get("video_url")
            if item.get("b64_json"):
                return base64.b64decode(item["b64_json"]), {"provider": "openrouter", "model": body["model"], "cost": (res.get("usage") or {}).get("cost")}
            if url:
                return requests.get(url, timeout=300).content, {"provider": "openrouter", "model": body["model"], "cost": (res.get("usage") or {}).get("cost")}
            die(f"openrouter finished without a file: {json.dumps(res)[:400]}")
        if status in ("failed", "error", "cancelled"):
            die(f"openrouter: {status}: {json.dumps(res)[:400]}")
    die("openrouter: timed out waiting for the clip (15 minutes)")


def gen_fal(prompt, ratio, seconds, refs, model):
    requests = _requests()
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    headers = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
    model = model or "fal-ai/veo3.1"
    body = {"prompt": prompt, "aspect_ratio": ratio, "duration": f"{seconds}s"}
    if refs:
        if not model.endswith("/image-to-video"):
            model += "/image-to-video"
        body["image_url"] = data_url(refs[0])
    r = requests.post(f"https://queue.fal.run/{model}", headers=headers, json=body, timeout=120)
    if r.status_code not in (200, 201, 202):
        die(f"fal answered {r.status_code}: {r.text[:600]}")
    job = r.json()
    status_url, response_url = job.get("status_url"), job.get("response_url")
    if not status_url:
        die(f"fal returned no queue job: {json.dumps(job)[:400]}")
    deadline = time.time() + 900
    while time.time() < deadline:
        time.sleep(5)
        st = requests.get(status_url, headers=headers, timeout=60).json()
        if st.get("status") == "COMPLETED":
            res = requests.get(response_url, headers=headers, timeout=60).json()
            video = res.get("video") or {}
            url = video.get("url") if isinstance(video, dict) else None
            if not url:
                die(f"fal finished without a file: {json.dumps(res)[:400]}")
            return requests.get(url, timeout=300).content, {"provider": "fal", "model": model, "cost": None}
        if st.get("status") in ("FAILED", "CANCELLED"):
            die(f"fal: {st.get('status')}: {json.dumps(st)[:400]}")
    die("fal: timed out waiting for the clip (15 minutes)")


GENERATORS = {"openrouter": gen_openrouter, "fal": gen_fal}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt")
    ap.add_argument("--ratio", default="9:16", choices=["9:16", "16:9", "1:1"])
    ap.add_argument("--seconds", type=int, default=6, choices=[4, 5, 6, 8])
    ap.add_argument("--out")
    ap.add_argument("--ref", action="append", default=[], help="a first-frame or reference image")
    ap.add_argument("--provider", choices=sorted(GENERATORS))
    ap.add_argument("--model")
    ap.add_argument("--no-suffix", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    avail = providers()
    if args.check:
        if avail:
            print("video providers configured, in the order tried: " + ", ".join(avail))
        else:
            print("no video provider configured (OPENROUTER_API_KEY or FAL_KEY); ask with request_connection when a clip is worth its cost")
            sys.exit(3)
        return
    if not args.prompt or not args.out:
        die("--prompt and --out are required (or --check)")
    provider = args.provider or (avail[0] if avail else None)
    if not provider:
        die("no video provider configured; the video-script skill says when and how to ask for one", 3)
    if provider not in avail:
        die(f"{provider} has no key in the environment; configured: {', '.join(avail) or 'none'}", 3)
    for ref in args.ref:
        if not os.path.isfile(ref):
            die(f"reference image not found: {ref}")
    prompt = args.prompt.strip() + ("" if args.no_suffix else NO_TEXT)
    clip, meta = GENERATORS[provider](prompt, args.ratio, args.seconds, args.ref, args.model)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(clip)
    meta.update({"prompt": prompt, "ratio": args.ratio, "seconds": args.seconds, "refs": [os.path.basename(r) for r in args.ref],
                 "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(args.out + ".json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    cost = f" (${meta['cost']:.2f})" if isinstance(meta.get("cost"), (int, float)) else ""
    print(f"{args.out} via {meta['provider']} {meta['model']}{cost} {len(clip) // 1000} KB")


if __name__ == "__main__":
    main()
