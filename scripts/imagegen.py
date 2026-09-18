#!/usr/bin/env python3
"""Generate the visual behind a creative with whichever image model this
app has a key for. The model paints the scene; the template sets the
words, the logo, and the colours (DESIGN.md), so every prompt ends with the
no-text rule and names the copy-space.

    python3 scripts/imagegen.py --prompt "…" --ratio 4:5 --out creatives/generated/<id>/visual.png
                                [--ref photo.png …] [--provider openrouter|gemini|bfl|fal|openai]
                                [--model …] [--size 1K|2K] [--seed N] [--no-suffix]
    python3 scripts/imagegen.py --prompt-file prompt.txt --ratio 4:5 --out …   # from scripts/prompt.py
    python3 scripts/imagegen.py --check          # which providers are configured

Providers, in the order tried (the first with a key wins):

  OPENROUTER_API_KEY   POST $OPENROUTER_BASE_URL/images (default https://openrouter.ai/api/v1);
                       one key for Gemini, GPT Image and FLUX; default model
                       google/gemini-3.1-flash-image. OPENROUTER_BASE_URL may point at a
                       gateway that needs no key (the Sprites managed connector): then set
                       OPENROUTER_BASE_URL alone.
  GEMINI_API_KEY       generateContent on gemini-3.1-flash-image (also GOOGLE_API_KEY)
  BFL_API_KEY          api.bfl.ai flux-2-pro (hex colours in the prompt work best here)
  FAL_KEY              fal.run fal-ai/nano-banana-2 (also FAL_API_KEY)
  OPENAI_API_KEY       gpt-image-2 (org verification may be required; last for that reason)

A key arrives through Connections as <SLUG>_API_KEY in ~/.env; with none,
the static-ad skill asks the owner with request_connection. The bytes are
written to --out as PNG; the provider, model, cost (when reported) and the
prompt go to <out>.json beside it. Exit 3 when no provider is configured.
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

NO_TEXT = (" No text, no letters, no numbers, no logos, no watermarks, no user interface"
           " anywhere in the image.")


def style_anchor(app_root, anchor_path=None):
    """The brand's style anchor from brand/visual-identity.md (the Imagery
    block's 'Style anchor' line, else its filled bullets joined), or the
    campaign's own from --anchor. Empty when nothing is filled."""
    if anchor_path:
        with open(anchor_path, encoding="utf-8") as fh:
            text = fh.read()
        _, body = split_fm(text)
        return " ".join(line.strip() for line in body.splitlines() if line.strip() and not line.startswith("#"))
    note = os.path.join(app_root, "brand", "visual-identity.md")
    if not os.path.isfile(note):
        return ""
    with open(note, encoding="utf-8") as fh:
        text = fh.read()
    block = text.split("## Imagery")[1] if "## Imagery" in text else ""
    block = block.split("\n## ")[0]
    lines = [l.strip()[2:].strip() for l in block.splitlines() if l.strip().startswith("- ")]
    lines = [l for l in lines if "to fill" not in l]
    for l in lines:
        if l.lower().startswith("**style anchor:**"):
            return l.split(":**", 1)[1].strip()
    if not lines:
        return ""
    return " ".join(l.replace("**", "") for l in lines)


def split_fm(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end], text[end + 4:]
    return "", text

RATIO_SIZES = {  # for providers that take width/height or fixed sizes
    "1:1": (1024, 1024), "4:5": (1024, 1280), "9:16": (1024, 1820), "16:9": (1820, 1024),
    "1.91:1": (1536, 804), "2:3": (1024, 1536), "3:2": (1536, 1024), "4:3": (1365, 1024), "3:4": (1024, 1365),
}
OPENAI_SIZES = {"1:1": "1024x1024", "4:5": "1024x1536", "9:16": "1024x1536", "2:3": "1024x1536",
                "16:9": "1536x1024", "1.91:1": "1536x1024", "3:2": "1536x1024"}


def providers():
    env = os.environ
    out = []
    if env.get("OPENROUTER_API_KEY") or env.get("OPENROUTER_BASE_URL"):
        out.append("openrouter")
    if env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY"):
        out.append("gemini")
    if env.get("BFL_API_KEY"):
        out.append("bfl")
    if env.get("FAL_KEY") or env.get("FAL_API_KEY"):
        out.append("fal")
    if env.get("OPENAI_API_KEY"):
        out.append("openai")
    return out


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()


def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def _requests():
    try:
        import requests
        return requests
    except ImportError:
        die("requests is not installed (setup.sh installs it)")


def _fail(provider, resp):
    body = resp.text[:600] if hasattr(resp, "text") else str(resp)[:600]
    die(f"{provider} answered {getattr(resp, 'status_code', '?')}: {body}")


def gen_openrouter(prompt, ratio, refs, model, size, seed):
    requests = _requests()
    base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    headers = {"Content-Type": "application/json", "HTTP-Referer": "https://taskandtool.app", "X-Title": "Task & Tool creatives"}
    if os.environ.get("OPENROUTER_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["OPENROUTER_API_KEY"]
    body = {"model": model or "google/gemini-3.1-flash-image", "prompt": prompt, "aspect_ratio": ratio,
            "resolution": size or "1K", "output_format": "png", "n": 1}
    if seed is not None:
        body["seed"] = seed
    if refs:
        body["input_references"] = [{"type": "image_url", "image_url": {"url": data_url(r)}} for r in refs]
    r = requests.post(base + "/images", headers=headers, json=body, timeout=240)
    if r.status_code != 200:
        _fail("openrouter", r)
    data = r.json()
    item = data["data"][0]
    if item.get("b64_json"):
        img = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        img = requests.get(item["url"], timeout=120).content
    else:
        die(f"openrouter returned no image: {json.dumps(data)[:400]}")
    return img, {"provider": "openrouter", "model": body["model"], "cost": (data.get("usage") or {}).get("cost")}


def gen_gemini(prompt, ratio, refs, model, size, seed):
    requests = _requests()
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    model = model or "gemini-3.1-flash-image"
    parts = [{"text": prompt}] + [{"inline_data": {"mime_type": mimetypes.guess_type(r)[0] or "image/png", "data": b64(r)}} for r in refs]
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": ratio, "imageSize": size or "1K"}}}
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                      headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=body, timeout=240)
    if r.status_code != 200:
        _fail("gemini", r)
    data = r.json()
    for cand in data.get("candidates") or []:
        for part in (cand.get("content") or {}).get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"]), {"provider": "gemini", "model": model, "cost": None}
    die(f"gemini returned no image: {json.dumps(data)[:400]}")


def gen_bfl(prompt, ratio, refs, model, size, seed):
    requests = _requests()
    headers = {"x-key": os.environ["BFL_API_KEY"], "Content-Type": "application/json"}
    model = model or "flux-2-pro"
    w, h = RATIO_SIZES.get(ratio, (1024, 1024))
    w, h = (w // 16) * 16, (h // 16) * 16
    body = {"prompt": prompt, "width": w, "height": h, "output_format": "png", "safety_tolerance": 2}
    if seed is not None:
        body["seed"] = seed
    for i, ref in enumerate(refs[:8]):
        body["input_image" + ("" if i == 0 else f"_{i + 1}")] = b64(ref)
    r = requests.post(f"https://api.bfl.ai/v1/{model}", headers=headers, json=body, timeout=120)
    if r.status_code != 200:
        _fail("bfl", r)
    job = r.json()
    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(1.0)
        res = requests.get(job["polling_url"], headers={"x-key": headers["x-key"]}, timeout=60).json()
        status = res.get("status")
        if status == "Ready":
            img = requests.get(res["result"]["sample"], timeout=120).content  # the URL lives 10 minutes
            return img, {"provider": "bfl", "model": model, "cost": job.get("cost")}
        if status in ("Error", "Failed", "Content Moderated", "Request Moderated"):
            die(f"bfl: {status}: {json.dumps(res)[:400]}")
    die("bfl: timed out waiting for the image")


def gen_fal(prompt, ratio, refs, model, size, seed):
    requests = _requests()
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    model = model or "fal-ai/nano-banana-2"
    body = {"prompt": prompt, "aspect_ratio": ratio, "resolution": size or "1K", "output_format": "png"}
    if seed is not None:
        body["seed"] = seed
    if refs:
        if not model.endswith("/edit"):
            model += "/edit"
        body["image_urls"] = [data_url(r) for r in refs]
    r = requests.post(f"https://fal.run/{model}", headers={"Authorization": f"Key {key}", "Content-Type": "application/json"}, json=body, timeout=300)
    if r.status_code != 200:
        _fail("fal", r)
    data = r.json()
    images = data.get("images") or ([data["image"]] if data.get("image") else [])
    if not images:
        die(f"fal returned no image: {json.dumps(data)[:400]}")
    img = requests.get(images[0]["url"], timeout=120).content
    return img, {"provider": "fal", "model": model, "cost": None}


def gen_openai(prompt, ratio, refs, model, size, seed):
    requests = _requests()
    headers = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    model = model or "gpt-image-2"
    px = OPENAI_SIZES.get(ratio, "1024x1024")
    quality = {"1K": "medium", "2K": "high", "4K": "high"}.get(size or "1K", "medium")
    if refs:
        files = [("image[]", (os.path.basename(p), open(p, "rb"), mimetypes.guess_type(p)[0] or "image/png")) for p in refs]
        r = requests.post("https://api.openai.com/v1/images/edits", headers=headers, files=files,
                          data={"model": model, "prompt": prompt, "size": px, "quality": quality}, timeout=300)
    else:
        r = requests.post("https://api.openai.com/v1/images/generations", headers={**headers, "Content-Type": "application/json"},
                          json={"model": model, "prompt": prompt, "size": px, "quality": quality, "output_format": "png"}, timeout=300)
    if r.status_code != 200:
        _fail("openai", r)
    data = r.json()
    return base64.b64decode(data["data"][0]["b64_json"]), {"provider": "openai", "model": model, "cost": None}


GENERATORS = {"openrouter": gen_openrouter, "gemini": gen_gemini, "bfl": gen_bfl, "fal": gen_fal, "openai": gen_openai}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt")
    ap.add_argument("--prompt-file", help="read the prompt from a file (scripts/prompt.py --out)")
    ap.add_argument("--ratio", default="4:5", choices=sorted(RATIO_SIZES))
    ap.add_argument("--out")
    ap.add_argument("--ref", action="append", default=[], help="a reference image (the product, the place); repeatable")
    ap.add_argument("--provider", choices=sorted(GENERATORS))
    ap.add_argument("--model")
    ap.add_argument("--size", choices=["512", "1K", "2K", "4K"])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--no-suffix", action="store_true", help="do not append the no-text rule to the prompt")
    ap.add_argument("--brand", action="store_true", help="append the brand's style anchor (brand/visual-identity.md, Imagery)")
    ap.add_argument("--anchor", help="a file whose body is the campaign's style anchor (campaigns/<slug>/style.md)")
    ap.add_argument("--check", action="store_true", help="print the configured providers and exit")
    args = ap.parse_args()

    avail = providers()
    if args.check:
        from common import root as app_root
        anchor = style_anchor(app_root())
        print("style anchor: " + (anchor[:120] + ("…" if len(anchor) > 120 else "") if anchor else "not filled (brand/visual-identity.md, Imagery)"))
        if avail:
            print("image providers configured, in the order tried: " + ", ".join(avail))
        else:
            print("no image provider configured (OPENROUTER_API_KEY, GEMINI_API_KEY, BFL_API_KEY, FAL_KEY, OPENAI_API_KEY); ask with request_connection")
            sys.exit(3)
        return
    if args.prompt_file and not args.prompt:
        with open(args.prompt_file, encoding="utf-8") as fh:
            args.prompt = fh.read().strip()
    if not args.prompt or not args.out:
        die("--prompt (or --prompt-file) and --out are required (or --check)")
    provider = args.provider or (avail[0] if avail else None)
    if not provider:
        die("no image provider configured; ask the owner for one with request_connection (the static-ad skill says how)", 3)
    if provider not in avail:
        die(f"{provider} has no key in the environment; configured: {', '.join(avail) or 'none'}", 3)
    for ref in args.ref:
        if not os.path.isfile(ref):
            die(f"reference image not found: {ref}")

    prompt = args.prompt.strip()
    if args.brand or args.anchor:
        from common import root as app_root
        anchor = style_anchor(app_root(), args.anchor)
        if anchor:
            prompt += " " + anchor
        else:
            print("note: no style anchor filled in brand/visual-identity.md (Imagery); the prompt goes without one", file=sys.stderr)
    if not args.no_suffix:
        prompt += NO_TEXT
    img, meta = GENERATORS[provider](prompt, args.ratio, args.ref, args.model, args.size, args.seed)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(img)
    # a PNG whatever the provider sent, with the sRGB tag, when Pillow is there
    try:
        from PIL import Image, ImageCms
        im = Image.open(args.out).convert("RGB")
        icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
        im.save(args.out, "PNG", icc_profile=icc)
        meta["size"] = f"{im.size[0]}x{im.size[1]}"
    except Exception:  # noqa: BLE001
        pass
    meta.update({"prompt": prompt, "ratio": args.ratio, "refs": [os.path.basename(r) for r in args.ref], "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(args.out + ".json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    cost = f" (${meta['cost']:.3f})" if isinstance(meta.get("cost"), (int, float)) else ""
    print(f"{args.out} via {meta['provider']} {meta['model']}{cost} {meta.get('size', '')}")


if __name__ == "__main__":
    main()
