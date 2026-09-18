# media/

The business's own pictures and video: what the creatives are made from.
Real material beats anything a model can generate, and it is the one thing
only the owner has.

```
media/photos/     stills: the work, the place, the product, the team, before and after pairs
media/clips/      video the owner filmed: a phone clip of the work, a walk round, a testimonial
media/logo/       the mark, when it is not already in brand/logo/
media/_index.json what is here, written by scripts/media.py: size, shape, duration, orientation
media/_notes.md   what each file shows, who is in it, whether it may be used (the owner's answers)
```

## Three ways files get here

1. **The owner uploads them** in the app's Files tab, or drops them into a
   chat message, or copies them onto the machine.
2. **A mirror from a Company Brain or a website in the same project.** The
   owner sets it up once in this app's Settings (Mirrored folders): the
   brain's `raw/web/images` (the pictures the crawl already pulled off the
   owner's site) onto `media/photos`, or a folder the owner keeps in the
   brain onto `media/`. The copy is read only here and refreshes when the
   source changes, the same way `brand/` and `public/` arrive. This is the
   pattern the website uses for the brain's notes; media works the same.
3. **The site crawl**, when this app collected its own sources: `tt-crawl`
   writes the owner's pictures into `raw/web/images/` with `_media.json`
   saying which are photographs. The `sources` skill copies the real
   photographs across into `media/photos`.

## What a mirror will and will not carry

The platform's mirrors copy real files, with limits: **20 MB a file, 200 MB
a folder, 2000 files**. A file over the cap is skipped, and the sync says
so. In practice:

- Photographs: fine, hundreds of them.
- Short social clips (a 30-second phone video at 1080p is usually 5 to 15
  MB): fine, a few dozen.
- Raw camera footage, 4K, or anything long: **too big**. Those stay
  wherever the owner keeps them, and what comes here is the trimmed
  export. Say this plainly to an owner who asks why a file did not
  arrive.

## Before a file is used

`media/_notes.md` records, per file or per folder, what it shows, whether
a recognisable person consented, and whether a customer's property may
appear. A picture with a person in it needs the owner's word that it may
be used; a customer's home needs theirs. No file is used in a creative
until that line exists.

`python3 scripts/media.py` writes `_index.json` and tells you what is
usable, what is too small for the placement you want, and what has no note
yet.
