#!/usr/bin/env python3
"""Tests for the creatives scripts against a copy of the app, with a fake
obscura on the PATH (the real one is Linux-only; the live check runs it).
Standard library + Pillow.

    python3 .claude/skills/creatives/test_scripts.py
"""

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
# The repository root is the app: the scripts under test are ~/app/scripts.
TEMPLATE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(TEMPLATE, "scripts"))
import common  # noqa: E402

FAKE_OBSCURA = r'''#!/usr/bin/env python3
# a stand-in for obscura: writes a PNG of the viewport size and prints the
# text boxes the --eval would report, so render.py's pipeline runs end to end
import os, sys, json
from PIL import Image, ImageDraw
args = sys.argv[1:]
w, h = int(float(os.environ.get("OBSCURA_SHOT_W", 1280))), int(float(os.environ.get("OBSCURA_SHOT_H", 720)))
if "-s" in args:
    out = args[args.index("-s") + 1]
    img = Image.new("RGB", (w, h), (246, 243, 236))
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(h * 0.6), w, h], fill=(20, 17, 13))
    img.save(out)
elif "-e" in args:
    # obscura prints the eval result as JSON: a JSON string holding the array
    print("some log line")
    print(json.dumps(json.dumps([[144, 200, 800, 190, "rgb(25, 22, 18)"], [144, int(h * 0.7), 600, 80, "rgb(246, 243, 236)"]])))
'''


def run(app, script, *args, env=None, ok=True):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run([sys.executable, os.path.join(app, "scripts", script), *args], cwd=app, capture_output=True, text=True, env=e)
    if ok:
        assert p.returncode == 0, f"{script} {' '.join(args)} failed ({p.returncode}):\n{p.stdout}\n{p.stderr}"
    return p


class Frontmatter(unittest.TestCase):
    def test_roundtrip(self):
        data = {"type": "creative", "id": "x", "files": ["a.png", "b.png"], "copy": {"headline": "Hi \"there\"", "hashtags": []},
                "claims": [{"text": "built by two", "source": "public/team.md"}], "history": [{"status": "generated", "at": "2026-09-07T10:00:00Z", "by": "ai"}],
                "scheduled_for": None, "n": 3}
        text = common.dump_frontmatter(data)
        back = common.parse_frontmatter(text)
        self.assertEqual(back["copy"]["headline"], 'Hi "there"')
        self.assertEqual(back["files"], ["a.png", "b.png"])
        self.assertEqual(back["claims"][0]["source"], "public/team.md")
        self.assertEqual(back["history"][0]["by"], "ai")
        self.assertIsNone(back["scheduled_for"])
        self.assertEqual(back["n"], 3)

    def test_hand_written_note_with_comments(self):
        fm = common.parse_frontmatter('title: The business\ntype: business   # a comment\nname: "Harlow Joinery"\nopening_hours: []\naddress: { street: "12 Dock Rd", locality: Bristol }\nitems:\n  - { quote: "great", who: "Jo" }\n')
        self.assertEqual(fm["type"], "business")
        self.assertEqual(fm["address"]["locality"], "Bristol")
        self.assertEqual(fm["items"][0]["who"], "Jo")
        self.assertEqual(fm["opening_hours"], [])

    def test_template_language(self):
        tpl = "{{a}}|{{{raw}}}|{{#items}}[{{n}}:{{text}}]{{/items}}|{{^missing}}none{{/missing}}|{{#flag}}yes{{/flag}}|{{#list}}<{{.}}>{{/list}}"
        out = common.render_template(tpl, {"a": "<b>", "raw": "<i>", "items": [{"n": 1, "text": "x"}], "flag": True, "list": ["p", "q"]})
        self.assertEqual(out, "&lt;b&gt;|<i>|[1:x]|none|yes|<p><q>")

    def test_copy_gate(self):
        f = common.copy_findings("It's not a kitchen, it's a lifestyle. Say goodbye to clutter. Struggling with your weight?", ad=True)
        rules = [r for r, _ in f]
        self.assertIn("refused phrase", rules)
        self.assertIn("personal attribute (Meta policy)", rules)
        self.assertEqual(common.copy_findings("We measure the room and talk through how you cook.", ad=True), [])


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="creatives-")
        self.app = os.path.join(self.tmp, "app")
        shutil.copytree(TEMPLATE, self.app, ignore=shutil.ignore_patterns("__pycache__"))
        bin_dir = os.path.join(self.tmp, "bin")
        os.makedirs(bin_dir)
        fake = os.path.join(bin_dir, "obscura")
        with open(fake, "w") as fh:
            fh.write(FAKE_OBSCURA)
        os.chmod(fake, os.stat(fake).st_mode | stat.S_IEXEC)
        self.env = {"PATH": bin_dir + os.pathsep + os.environ.get("PATH", "")}
        # a named business so the label fills
        biz = os.path.join(self.app, "public", "business.md")
        text = open(biz).read().replace("name: to fill", 'name: "Harlow Joinery"')
        open(biz, "w").write(text)
        os.makedirs(os.path.join(self.app, "campaigns", "autumn"), exist_ok=True)
        open(os.path.join(self.app, "campaigns", "autumn", "brief.md"), "w").write("---\ntype: brief\n---\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def new(self, **kw):
        args = ["--platform", kw.get("platform", "meta"), "--format", kw.get("format", "us-vs-them"), "--campaign", "autumn",
                "--ratio", kw.get("ratio", "4:5"), "--title", kw.get("title", "Showroom vs workshop")]
        p = run(self.app, "new.py", *args)
        rel = p.stdout.strip().splitlines()[-1]
        return os.path.join(self.app, rel), os.path.basename(rel)

    def fill(self, d, copy=None, claims=None, fields=None):
        path = os.path.join(d, "creative.md")
        fm, body = common.read_record(path)
        fm["copy"] = copy or {"headline": "Showroom kitchen. Workshop kitchen.", "primary_text": "Measured, drawn, built and fitted by the same two people.", "cta": "Book a workshop visit", "caption": "", "hashtags": []}
        fm["claims"] = claims if claims is not None else [{"text": "built and fitted by the same two people", "source": "public/team.md"}]
        body = "Why this creative: a comparison for cold readers.\n\nVisual prompt: none.\n\nNotes: none.\n"
        common.write_record(path, fm, body)
        fp = os.path.join(d, "fields.json")
        with open(fp) as fh:
            f = json.load(fh)
        f.update(fields or {"headline": "Showroom kitchen. Workshop kitchen.", "rows": [{"left": "Drawn by a salesperson", "right": "Measured by the maker"}], "cta": "Book a workshop visit"})
        with open(fp, "w") as fh:
            json.dump(f, fh)

    def test_new_render_qa_check_resize(self):
        d, cid = self.new()
        self.assertTrue(cid.endswith("-us-vs-them-meta-01"))
        fm, _ = common.read_record(os.path.join(d, "creative.md"))
        self.assertEqual(fm["status"], "generated")
        fields = json.load(open(os.path.join(d, "fields.json")))
        self.assertEqual(fields["template"], "us-vs-them")
        self.assertEqual(fields["business"], "Harlow Joinery")
        self.fill(d)

        p = run(self.app, "render.py", cid, env=self.env)
        self.assertIn("1080x1350", p.stdout)
        from PIL import Image
        img = Image.open(os.path.join(d, "master.png"))
        self.assertEqual(img.size, (1080, 1350))
        html = open(os.path.join(d, "render.html")).read()
        self.assertIn("Showroom kitchen", html)
        self.assertIn("Measured by the maker", html)
        self.assertIn("--scale: 2.0000", html)
        self.assertIn('class="card r-45', html)
        fields = json.load(open(os.path.join(d, "fields.json")))
        self.assertEqual(len(fields["_boxes"]), 2)
        self.assertEqual(fields["_boxes"][0][4], "#191612")
        fm, _ = common.read_record(os.path.join(d, "creative.md"))
        self.assertEqual(fm["files"], ["master.png"])

        run(self.app, "qa.py", cid)
        run(self.app, "check.py")
        p = run(self.app, "resize.py", cid)
        self.assertIn("1440x1800.png", p.stdout)
        self.assertTrue(os.path.isfile(os.path.join(d, "1440x1800.png")))
        fm, _ = common.read_record(os.path.join(d, "creative.md"))
        self.assertIn("1440x1800.png", fm["files"])

    def test_render_other_sizes_and_html_only(self):
        d, cid = self.new(platform="linkedin", format="statement", ratio="1.91:1")
        self.fill(d, fields={"headline": "Kitchens built by the people who fit them.", "cta": "Book a visit"})
        p = run(self.app, "render.py", cid, "--html-only")
        self.assertIn("render.html", p.stdout)
        html = open(os.path.join(d, "render.html")).read()
        self.assertIn('class="card r-1911', html)
        self.assertIn("width:2400px;height:1256px", html)
        run(self.app, "render.py", cid, "--dpr", "1", env=self.env)
        from PIL import Image
        self.assertEqual(Image.open(os.path.join(d, "master.png")).size, (1200, 628))

    def test_check_catches_bad_copy_claims_and_files(self):
        d, cid = self.new()
        self.fill(d, copy={"headline": "It's not a kitchen, it's a lifestyle you deserve", "primary_text": "x", "cta": "Learn more", "caption": "", "hashtags": ["#kitchens"]},
                  claims=[{"text": "award winning", "source": "public/awards.md"}])
        fm, body = common.read_record(os.path.join(d, "creative.md"))
        fm["files"] = ["master.png"]
        common.write_record(os.path.join(d, "creative.md"), fm, body)
        p = run(self.app, "check.py", ok=False)
        self.assertEqual(p.returncode, 1)
        for needle in ["refused phrase", "hashtags", "Learn more", "public/awards.md does not exist", "master.png is missing"]:
            self.assertIn(needle, p.stderr, needle)

    def test_status_board_and_decisions(self):
        d, cid = self.new()
        self.fill(d)
        p = run(self.app, "status.py", "move", cid, "approved", ok=False)
        self.assertEqual(p.returncode, 1)  # nothing rendered yet
        self.assertIn("rendered file", p.stderr)
        run(self.app, "render.py", cid, env=self.env)
        p = run(self.app, "status.py", "move", cid, "scheduled", ok=False)
        self.assertEqual(p.returncode, 1)  # scheduled needs a date
        run(self.app, "status.py", "move", cid, "approved", "--note", "Looks right", "--by", "owner")
        self.assertTrue(os.path.isdir(os.path.join(self.app, "creatives", "approved", cid)))
        self.assertFalse(os.path.exists(d))
        fm, _ = common.read_record(os.path.join(self.app, "creatives", "approved", cid, "creative.md"))
        self.assertEqual(fm["status"], "approved")
        self.assertEqual(fm["history"][-1]["note"], "Looks right")
        run(self.app, "check.py")

        # a portal's decisions arrive by mirror
        inbox = os.path.join(self.app, "inbox", "decisions")
        open(os.path.join(inbox, "001.md"), "w").write(f"---\ntype: decision\ncreative: {cid}\ndecision: schedule\nby: \"Jo (client)\"\nat: \"2026-09-08T09:00:00Z\"\nscheduled_for: \"2026-09-12T09:00:00+01:00\"\n---\nGo on Friday.\n")
        open(os.path.join(inbox, "002.md"), "w").write(f"---\ntype: decision\ncreative: {cid}\ndecision: comment\nby: \"Jo (client)\"\n---\nCan the second line be shorter?\n")
        open(os.path.join(inbox, "003.md"), "w").write("---\ntype: decision\ncreative: nope\ndecision: approve\n---\n")
        p = run(self.app, "status.py", "apply")
        self.assertIn("schedule", p.stdout)
        self.assertIn("comment", p.stdout)
        self.assertIn("could not apply 003.md", p.stdout)
        fm, _ = common.read_record(os.path.join(self.app, "creatives", "scheduled", cid, "creative.md"))
        self.assertEqual(fm["scheduled_for"], "2026-09-12T09:00:00+01:00")
        self.assertEqual(fm["history"][-1]["note"], "Can the second line be shorter?")
        p = run(self.app, "status.py", "apply")
        self.assertIn("nothing new", p.stdout)
        p = run(self.app, "status.py", "list")
        self.assertIn("scheduled", p.stdout)
        p = run(self.app, "status.py", "move", cid, "posted", "--post-url", "https://www.instagram.com/p/abc/")
        fm, _ = common.read_record(os.path.join(self.app, "creatives", "posted", cid, "creative.md"))
        self.assertTrue(fm["posted_at"])

    def test_carousel_and_video(self):
        d, cid = self.new(format="listicle", ratio="1:1")
        self.fill(d)
        for n, fields in enumerate([
            {"template": "statement", "headline": "Four steps, one team.", "cta": ""},
            {"template": "listicle", "headline": "Visit", "items": ["We measure the room and talk through how you cook."]},
            {"template": "statement", "headline": "Save this for your kitchen.", "cta": "Book a workshop visit", "tone": "dark"},
        ], start=1):
            base = json.load(open(os.path.join(d, "fields.json")))
            base.update(fields)
            with open(os.path.join(d, f"fields-{n:02d}.json"), "w") as fh:
                json.dump(base, fh)
        p = run(self.app, "carousel.py", cid, "--pdf", env=self.env)
        self.assertIn("3 card(s)", p.stdout)
        fm, _ = common.read_record(os.path.join(d, "creative.md"))
        self.assertEqual(fm["kind"], "carousel")
        self.assertIn("slides/03.png", fm["files"])
        self.assertIn("document.pdf", fm["files"])
        from PIL import Image
        self.assertEqual(Image.open(os.path.join(d, "slides", "02.png")).size, (1080, 1080))
        self.assertTrue(os.path.isfile(os.path.join(d, "document.pdf")))
        # the deck's own fields.json is untouched by the per-card renders
        self.assertEqual(json.load(open(os.path.join(d, "fields.json")))["template"], "listicle")
        run(self.app, "check.py", cid)
        if shutil.which("ffmpeg"):
            p = run(self.app, "video.py", cid, "--length", "3", "--fps", "12")
            self.assertIn("cut.mp4", p.stdout)
            fm, _ = common.read_record(os.path.join(d, "creative.md"))
            self.assertIn("cut.mp4", fm["files"])
            secs = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(d, "cut.mp4")], capture_output=True, text=True).stdout.strip()
            self.assertAlmostEqual(float(secs), 3.0, delta=0.5)

    def test_limits_soft_and_hard(self):
        d, cid = self.new(platform="linkedin", format="statement", ratio="1:1")
        self.fill(d, copy={"headline": "x" * 80, "primary_text": "y" * 200, "cta": "Book a visit", "caption": "", "hashtags": []})
        p = run(self.app, "check.py", cid)
        self.assertIn("note:", p.stdout)
        self.assertIn("past the visible cutoff", p.stdout)
        self.fill(d, copy={"headline": "x" * 80, "primary_text": "y" * 700, "cta": "Book a visit", "caption": "", "hashtags": []})
        p = run(self.app, "check.py", cid, ok=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("over the limit", p.stderr)

    def test_style_anchor_from_brand_note(self):
        import imagegen
        self.assertEqual(imagegen.style_anchor(self.app), "")  # the template is to fill
        note = os.path.join(self.app, "brand", "visual-identity.md")
        text = open(note).read().replace(
            "- **Style anchor:** to fill (one paragraph in the vocabulary above, reused at the end of every image prompt; `scripts/imagegen.py --brand` appends it)",
            "- **Style anchor:** Photographed, not illustrated. Oak, ash and birch ply, north light, sawdust, the brand's blue on one thing.")
        open(note, "w").write(text)
        self.assertTrue(imagegen.style_anchor(self.app).startswith("Photographed, not illustrated."))
        anchor = os.path.join(self.app, "campaigns", "autumn", "style.md")
        open(anchor, "w").write("---\ntype: style\n---\n# Autumn\n\nCold light, steam, a red van.\n")
        self.assertEqual(imagegen.style_anchor(self.app, anchor), "Cold light, steam, a red van.")

    def test_prompt_assembly_from_brand_slots(self):
        # unfilled notes: the template's slots are questions, not guesses
        p = run(self.app, "prompt.py", "--format", "photo")
        self.assertIn("{subject}", p.stdout)
        self.assertIn("slots the notes do not fill", p.stderr)
        self.assertIn("subject", p.stderr)
        # fill the Imagery block as the sources skill would
        note = os.path.join(self.app, "brand", "visual-identity.md")
        text = open(note).read()
        for label, value in [
            ("What the owner's photography shows", "the finished kitchen, the bench, hands on a plane"),
            ("Settings", "the workshop on Cumberland Road and the customer's kitchen"),
            ("Light", "north light from tall windows, overcast"),
            ("Materials and objects that carry the brand", "oak, ash, birch ply, and the blue enamel mug"),
            ("People", "hands and backs only"),
            ("Never shows", "stock smiles, a spotless room, purple"),
            ("Style anchor", "Photographed, not illustrated. Sawdust in the light. Nothing staged."),
        ]:
            text = re.sub(r"(- \*\*" + re.escape(label) + r":\*\*) to fill[^\n]*", r"\1 " + value, text)
        open(note, "w").write(text)
        brief = os.path.join(self.app, "campaigns", "autumn", "brief.md")
        open(brief, "w").write("---\ntype: brief\nproduct: fitted kitchens measured, built and fitted by us\n---\n")
        open(os.path.join(self.app, "campaigns", "CURRENT"), "w").write("autumn\n")
        p = run(self.app, "prompt.py", "--slots")
        self.assertIn("oak, ash, birch ply", p.stdout)
        self.assertIn("(missing", p.stdout)  # audience_place still to fill
        p = run(self.app, "prompt.py", "--format", "before-after", "--side", "after", "--json")
        data = json.loads(p.stdout)
        self.assertEqual(data["missing"], [])
        self.assertIn("the same doorway", data["prompt"])
        self.assertIn("north light from tall windows", data["prompt"])
        self.assertTrue(data["prompt"].endswith("Nothing staged."))
        self.assertNotIn("{", data["prompt"])
        p = run(self.app, "prompt.py", "--format", "environment", "--audience_place", "a kitchen at 7am with a cold kettle", "--out", os.path.join(self.app, "uploads", "env.txt"))
        self.assertIn("a kitchen at 7am", p.stdout)
        self.assertIn("fitted kitchens measured", p.stdout)
        self.assertTrue(os.path.isfile(os.path.join(self.app, "uploads", "env.txt")))
        p = run(self.app, "prompt.py", "--format", "us-vs-them", ok=False)
        self.assertIn("template-only", p.stderr)

    def test_every_template_renders(self):
        import glob
        fields_by_template = {
            "statement": {"headline": "One line.", "cta": "Book"},
            "photo": {"image": "visual.png", "headline": "One line.", "cta": "Book"},
            "quote": {"quote": "They measured twice.", "who": "Ruth"},
            "us-vs-them": {"headline": "A or B", "left_label": "A", "right_label": "B", "rows": [{"left": "x", "right": "y"}]},
            "before-after": {"before_image": "visual.png", "after_image": "visual.png", "before_label": "Before", "after_label": "After", "headline": "Then and now"},
            "offer": {"headline": "Offer", "includes": ["a", "b"], "price": "Free", "cta": "Book"},
            "listicle": {"headline": "Three", "items": ["a", "b", "c"]},
            "product": {"image": "visual.png", "headline": "The thing"},
            "checklist": {"headline": "Check", "items": [{"text": "a", "done": True}, {"text": "b", "done": False}]},
            "note": {"text": "A note.", "signoff": "Sam"},
            "screenshot": {"thread": None, "notification": None, "review": None, "comment": {"who": "Jo", "text": "Do you?", "reply": "Yes."}, "app": None},
            "banner": {"offer": "300 off", "headline": "Any kitchen drawn in October", "terms": "Ends 31 October", "cta": "Book"},
            "snapshot": {"image": "visual.png", "caption": "Day three."},
            "steps": {"headline": "How", "steps": [{"n": "1", "title": "Measure", "text": "We measure."}, {"n": "2", "title": "Build"}]},
            "proof-stack": {"rating": "4.9", "count": "118 reviews", "source": "Google", "quotes": [{"text": "Great", "who": "Ruth"}]},
            "grid": {"headline": "The range", "columns": 2, "cells": [{"image": "visual.png", "text": "A"}, {"image": "visual.png", "text": "B"}, {"text": "C"}, {"image": "visual.png"}]},
            "stats": {"headline": "Clifton", "stats": [{"value": "3", "label": "days"}, {"value": "0", "label": "return visits"}], "source": "the job sheet"},
        }
        templates = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(self.app, "templates", "*.html")))
        self.assertEqual(set(templates), set(fields_by_template), "every template needs a fields example, and every example a template")
        from PIL import Image
        for tpl in templates:
            p = run(self.app, "new.py", "--platform", "meta", "--format", tpl, "--campaign", "autumn", "--ratio", "1:1", "--title", tpl, "--template", tpl)
            d = os.path.join(self.app, p.stdout.strip().splitlines()[-1])
            Image.new("RGB", (400, 400), (120, 100, 80)).save(os.path.join(d, "visual.png"))
            with open(os.path.join(d, "fields.json")) as fh:
                f = json.load(fh)
            f.update(fields_by_template[tpl])
            with open(os.path.join(d, "fields.json"), "w") as fh:
                json.dump(f, fh)
            run(self.app, "render.py", d, "--html-only")
            html = open(os.path.join(d, "render.html")).read()
            self.assertNotIn("{{", html, f"{tpl}: an unfilled tag survived")
            self.assertIn('class="card', html)
            run(self.app, "render.py", d, "--dpr", "1", env=self.env)
            self.assertEqual(Image.open(os.path.join(d, "master.png")).size, (1080, 1080), tpl)

    def _frame_colour(self, video, t):
        out = os.path.join(self.tmp, f"probe-{t}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-ss", str(t), "-frames:v", "1", out], check=True)
        from PIL import Image
        with Image.open(out) as im:
            return im.convert("RGB").getpixel((10, 10))

    def test_video_shows_every_shot(self):
        """The slideshow must advance: zoompan emits `d` frames per input
        frame, so a looped input holds the first card for the whole cut."""
        if not shutil.which("ffmpeg"):
            self.skipTest("ffmpeg not installed")
        from PIL import Image
        d, cid = self.new(ratio="9:16")
        self.fill(d)
        slides = os.path.join(d, "slides")
        os.makedirs(slides, exist_ok=True)
        cream, night = (246, 243, 236), (20, 17, 13)
        for i, colour in enumerate([cream, night], start=1):
            Image.new("RGB", (1080, 1920), colour).save(os.path.join(slides, f"{i:02d}.png"))
        run(self.app, "video.py", cid, "--ratio", "9:16", "--length", "4", "--fps", "24")
        cut = os.path.join(d, "cut.mp4")
        first, second = self._frame_colour(cut, 0.8), self._frame_colour(cut, 3.4)
        for got, want, when in [(first, cream, "0.8s"), (second, night, "3.4s")]:
            self.assertLess(sum(abs(a - b) for a, b in zip(got, want)), 40,
                            f"at {when} the cut shows {got}, not the card {want}: the slideshow is not advancing")

    def test_video_cuts_real_footage_with_cards(self):
        if not shutil.which("ffmpeg"):
            self.skipTest("ffmpeg not installed")
        from PIL import Image
        d, cid = self.new(ratio="9:16")
        self.fill(d)
        os.makedirs(os.path.join(self.app, "media", "clips"), exist_ok=True)
        clip = os.path.join(self.app, "media", "clips", "bench.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=green:size=1280x720:rate=25:duration=4",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", clip], check=True)
        os.makedirs(os.path.join(d, "slides"), exist_ok=True)
        Image.new("RGB", (1080, 1920), (246, 243, 236)).save(os.path.join(d, "slides", "01.png"))
        with open(os.path.join(d, "shots.json"), "w") as fh:
            json.dump([{"slide": "slides/01.png", "seconds": 2},
                       {"clip": "media/clips/bench.mp4", "in": 0.5, "out": 3.0}], fh)
        p = run(self.app, "video.py", cid, "--ratio", "9:16", "--fps", "24")
        self.assertIn("1 clip", p.stdout)
        self.assertIn("1 slide", p.stdout)
        cut = os.path.join(d, "cut.mp4")
        card, footage = self._frame_colour(cut, 1.0), self._frame_colour(cut, 3.2)
        self.assertLess(sum(abs(a - b) for a, b in zip(card, (246, 243, 236))), 40, "the card should open the cut")
        self.assertGreater(footage[1], footage[0] + 40, f"the footage should follow the card, got {footage}")
        # a missing clip is named, not silently dropped
        with open(os.path.join(d, "shots.json"), "w") as fh:
            json.dump([{"clip": "media/clips/nope.mp4", "in": 0, "out": 2}], fh)
        p = run(self.app, "video.py", cid, ok=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("media/clips/nope.mp4", p.stderr)

    def test_media_index(self):
        from PIL import Image
        photos = os.path.join(self.app, "media", "photos")
        os.makedirs(photos, exist_ok=True)
        Image.new("RGB", (1600, 2000), (200, 180, 160)).save(os.path.join(photos, "kitchen.jpg"))
        Image.new("RGB", (300, 300), (100, 100, 100)).save(os.path.join(photos, "tiny.jpg"))
        p = run(self.app, "media.py", "--for", "4:5")
        self.assertIn("no note yet", p.stdout)
        self.assertIn("kitchen.jpg", p.stdout)
        with open(os.path.join(self.app, "media", "_notes.md"), "a") as fh:
            fh.write("| photos/kitchen.jpg | the Clifton kitchen | none | yes | 2026-09-07 |\n")
            fh.write("| photos/tiny.jpg | a detail | none | yes | 2026-09-07 |\n")
        p = run(self.app, "media.py", "--for", "4:5")
        self.assertIn("usable: 1", p.stdout)
        self.assertIn("too small for this placement", p.stdout)
        index = json.load(open(os.path.join(self.app, "media", "_index.json")))
        by_name = {r["name"]: r for r in index["files"]}
        self.assertEqual(by_name["kitchen.jpg"]["orientation"], "portrait")
        self.assertTrue(by_name["kitchen.jpg"]["noted"])
        self.assertTrue(by_name["kitchen.jpg"]["mirrorable"])

    def test_captions_ass(self):
        out = os.path.join(self.app, "uploads", "caps.ass")
        p = run(self.app, "captions.py", "--text", "Half price today. Ends Friday.", "--seconds", "6", "--ratio", "9:16", "--out", out)
        self.assertIn("5 words", p.stdout)
        ass = open(out).read()
        self.assertIn("PlayResX: 1080", ass)
        self.assertIn("PlayResY: 1920", ass)
        # a sentence end breaks the group, so two groups
        self.assertEqual(ass.count("Dialogue:"), 2)
        self.assertIn("{\\k", ass)                          # word timing
        self.assertRegex(ass, r"\\pos\(540,\d+\)")           # centred, inside the safe band
        y = int(re.search(r"\\pos\(540,(\d+)\)", ass).group(1))
        self.assertGreater(y, 1920 * 0.2)
        self.assertLess(y, 1920 * 0.8)
        self.assertIn("Style: Cap,", ass)
        self.assertIn("no TTF or OTF", p.stderr)             # honest about the fallback face
        # from a script's beat table
        script = os.path.join(self.app, "uploads", "script.md")
        open(script, "w").write("---\ntype: script\nlength: 15\n---\n\n| t (s) | on screen | spoken | picture |\n|---:|---|---|---|\n| 0-3 | Six weeks of waiting | the hook | the room |\n| 3-6 | We measure and draw | the mechanism | the bench |\n")
        p = run(self.app, "captions.py", "--script", script, "--out", out)
        ass = open(out).read()
        self.assertIn("Six", ass)
        self.assertIn("measure", ass)
        self.assertEqual(ass.count("Dialogue:"), 2)

    def test_videogen_check(self):
        env = {k: v for k, v in os.environ.items() if not k.endswith("_API_KEY") and k not in ("FAL_KEY", "OPENROUTER_BASE_URL")}
        p = subprocess.run([sys.executable, os.path.join(self.app, "scripts", "videogen.py"), "--check"], cwd=self.app, capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 3)
        env["FAL_KEY"] = "x"
        p = subprocess.run([sys.executable, os.path.join(self.app, "scripts", "videogen.py"), "--check"], cwd=self.app, capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 0)
        self.assertIn("fal", p.stdout)

    def test_imagegen_check_and_no_provider(self):
        env = {k: v for k, v in os.environ.items() if not k.endswith("_API_KEY") and k not in ("FAL_KEY", "OPENROUTER_BASE_URL")}
        p = subprocess.run([sys.executable, os.path.join(self.app, "scripts", "imagegen.py"), "--check"], cwd=self.app, capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 3)
        env["OPENROUTER_API_KEY"] = "x"
        env["GEMINI_API_KEY"] = "y"
        p = subprocess.run([sys.executable, os.path.join(self.app, "scripts", "imagegen.py"), "--check"], cwd=self.app, capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 0)
        self.assertIn("openrouter, gemini", p.stdout)

    def test_qa_background_contrast_ignores_the_glyphs(self):
        import qa
        ink = (25, 22, 18)
        light = [(246, 243, 236)] * 300 + [ink] * 120 + [(120, 110, 100)] * 20  # the antialiased fringe is a thin minority
        self.assertGreater(qa.background_contrast(ink, light), 4.5)
        grey = [(90, 88, 84)] * 300 + [ink] * 120
        self.assertLess(qa.background_contrast(ink, grey), 3.0)
        self.assertIsNone(qa.background_contrast(ink, [ink] * 50))

    def test_qa_tokens(self):
        run(self.app, "qa.py", "--tokens")
        css = os.path.join(self.app, "templates", "brand.css")
        text = open(css).read().replace("--ink-2: var(--brand-neutral);", "--ink-2: #cccccc;")
        open(css, "w").write(text)
        p = run(self.app, "qa.py", "--tokens", ok=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("ink-2", p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
