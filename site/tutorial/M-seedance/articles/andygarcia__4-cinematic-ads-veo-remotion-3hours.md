---
title: "How I Made 4 Cinematic Ads for My Muslim App in 3 Hours (AI Video + React)"
url: "https://andygarcia.pro/en/blog/quranway-ugc-in-3-hours"
author: "Andy Garcia"
date: "2026-04-13"
source: "andygarcia.pro personal blog"
---

# How I Made 4 Cinematic Ads for My Muslim App in 3 Hours (AI Video + React)

I shipped QuranWay — a Muslim prayer app — without ever promoting it publicly. With v1.3 in review at Apple and zero budget, I gave myself one afternoon to launch its first UGC campaign. Four cinematic ads, ready for TikTok, Reels and YouTube Shorts, generated with AI and edited with code.

## The Constraints

- **5 credits on Google Flow / Veo Lite** — roughly 5 generations of 8-second clips
- **No actor, no studio, no shoot day** — pure AI generation
- **No video editing app** — reused a Remotion (React → MP4) setup
- **One afternoon** before another project pulled attention

## Two Creative Pivots Before the One That Worked

### Pivot 1 — the "Apple ad with a phone" trap (rejected)

My first instinct was to copy Apple ads. Phones floating in space, glowing screens. The render was gorgeous. But: what does a TikTok scroller actually learn from this in the half-second their thumb hesitates? Nothing. A phone. It could be Apple. It could be Samsung.

**Lesson 1: a beautiful product shot of a generic phone isn't marketing — it's stock footage.**

### Pivot 2 — phone + Muslim objects (still wrong)

Round two: keep the phone but add Muslim cultural markers around it. But the phone was still the visual hero. The viewer's eye would lock onto the screen, expect a UI, and find a vague glow instead.

**Lesson 2: don't put your product where your story should be.**

### Pivot 3 — no phone, life first (the one that worked)

The click came from flipping the question: instead of "how do I make a beautiful ad for an app", I asked "what does using QuranWay actually look like in someone's life?"

The answer wasn't a phone. It was the **moments** where the app shows up:
- Turning the pages of a Quran in the morning
- Doing ablutions before prayer
- Unrolling a prayer rug at dusk
- Counting a tasbih in the quiet of late afternoon

None of these moments need a phone in frame. The scroller's brain processes them in well under a second — the cultural markers do the targeting.

## The Four Winning Prompts

### Prompt 1 — Mushaf

```
Cinematic macro close-up of two hands gently turning the pages of an
open leather-bound book with delicate gold Arabic calligraphy on
cream-colored pages, resting on a warm wooden table. Soft morning
sunlight streams through a nearby window, creating warm highlights and
shallow shadows across the pages. A thumb slowly traces down a line of
script. 85mm macro lens, very shallow depth of field, cinematic ARRI
Alexa look. Slow meditative pace. Natural warm color palette. No text
overlays, no graphics, no modern devices in frame. 8 seconds.
```

### Prompt 2 — Wudu

```
Cinematic slow-motion macro close-up of two hands under gentle running
water in a modern white ceramic sink. Clear water droplets rise and
fall in extreme slow motion as the hands slowly wash one another,
fingertips to wrist. Natural soft daylight from a side window creates
clean highlights on the water and skin. Warm neutral tones. No faces
visible, only hands and water. 100mm macro lens, shallow depth of
field, cinematic ARRI Alexa look. Calm ritual atmosphere. No text,
no graphics. 8 seconds.
```

### Prompt 3 — Prayer Rug

```
Cinematic close-up of two hands slowly unrolling a richly woven prayer
rug with an intricate geometric Islamic pattern featuring eight-pointed
stars and arches in deep burgundy, teal and gold thread, across a warm
wooden parquet floor. Golden-hour sunlight streams through a tall
window, casting long warm shadows and illuminating the fabric's
texture. 35mm lens, low angle, shallow depth of field, ARRI Alexa
cinematic look. Slow deliberate movement, peaceful atmosphere. No text,
no graphics. 8 seconds.
```

### Prompt 4 — Tasbih

```
Cinematic extreme macro close-up of a single hand slowly counting a
string of 99 dark polished wooden prayer beads with a small tassel at
the end, sliding one bead at a time between the thumb and fingers.
Warm late-afternoon sunlight filters through a window, creating a soft
golden bokeh in the background. Shallow depth of field, 100mm macro
lens, ARRI Alexa cinematic look. Slow contemplative pace, peaceful
atmosphere. No text, no graphics. 8 seconds.
```

## Prompt Writing Tips

- **Describe ritual objects by their physical traits, not their religious name.** "Quran" can trip safety filters; "leather-bound book with gold Arabic calligraphy on cream-colored pages" never does.
- **Lock the lens.** "85mm macro", "ARRI Alexa look", "shallow depth of field" — that's language Veo's training data understands.
- **Forbid what you don't want.** Negative prompts in plain English ("no text overlays, no graphics, no modern devices in frame") work surprisingly well.

## The Remotion Edit

Total spent: 4 credits. Total time: about 45 minutes for generation, plus 15 minutes per clip for code-based editing.

The Remotion composition does three things per clip:
1. **Crops the Veo watermark** via CSS transform with biased origin
2. **Overlays a 3-line hook** in Plus Jakarta Sans with staggered word-by-word entrance
3. **Ends on a 1.5s logo outro**

The transform-origin trick: `transformOrigin: "30% 30%"` pushes the bottom-right corner (where the watermark lives) out of frame at 1.28× scale, without losing the subject.

## Key Takeaways

- Never let auto-generated metadata ship for a brand-sensitive product
- Pre-write titles and descriptions
- The whole pipeline — generation, editing, rendering, upload — runs from a terminal
- Four Veo prompts, one transform-origin, and `npm run render:all`
