---
title: "How I Made a 90-Second AI Animated Reel Using 9 Tools (and What I Learned)"
url: "https://www.sophiesbureau.com/digital-ops/how-i-made-90-second-reel-ai-tools"
author: "Sophie Kazandjian"
date: "2026-01-04"
source: "Sophie's Bureau blog"
---

# How I Made a 90-Second AI Animated Reel Using 9 Tools (and What I Learned)

I recently finished a short animated reel called "Timing, Not Time." It's 90 seconds long. It took me an afternoon over the holiday period to make. And it involved nine different AI tools, plus a few non-AI resources along the way.

## The Tool Stack

| Tool | Role |
|---|---|
| Claude (Anthropic) | Script development, creative direction, initial image prompts |
| ChatGPT | Refining image prompts, Kling animation prompts |
| Leonardo AI (Lucid Origin model) | Generating the illustrated stills |
| Nano Banana Pro (Google Gemini) | Upscaling and refining images |
| Kling AI | Animating the stills |
| Suno | Ambient soundtrack |
| ElevenLabs | Voice cloning for narration |
| Freesound | Sound effects (not AI) |
| Filmora | Video editing and audio assembly |
| Canva | Text overlays and final export |

## The Process

### 1. Starting with the Script (Claude)

I began with Claude. Not with visuals, not with mood boards — with words.

We worked through the concept together. "Timing, Not Time" emerged as a framework: the idea that productivity isn't about managing hours, but about recognising rhythms.

**Learning: Start with words, not pictures.** The script shaped everything that followed. If I'd jumped straight to visuals, I'd have been decorating without direction.

### 2. Finding the Visual Style with Lucid Origin

This was the hardest part. I worked with Claude to write a detailed prompt for Leonardo AI, specifying my brand palette: sage greens, dusty golds, ambers, soft teals. I wanted dense crosshatch texture like a European graphic novel.

But then I made a mistake. I tried to "improve" the prompt for subsequent frames, adding more specific instructions about style. The results drifted — some too flat, others too soft. I'd lost the magic of the original.

This is where ChatGPT helped. I shared the original image and prompt, explained what was working and what wasn't, and asked for refinements. ChatGPT's approach was more technical and structured.

**Learning: Protect what works.** When I found a prompt that captured the style, I should have built a template around it rather than reinventing each time.

**Learning: Simple prompts often outperform complex ones.** My original, slightly looser prompt gave Leonardo room to interpret. The over-specified versions constrained it too much.

### 3. Creating the 8 Frames

The reel needed 8 distinct frames, each matching a section of the script:
1. Rolling fields at dawn — the opening question
2. Terraced hillside at midday — the productivity trap
3. Coastal cliffs at dusk — exhaustion
4. Mountains under stars — the reframe
5. Mountain lake at blue hour — reflection
6. Olive grove in morning light — natural rhythm
7. Lavender field at golden hour — release
8. Rolling hills at twilight — invitation to continue

I built a universal prompt template that kept the core style instructions consistent while varying the landscape, time of day, and figure position.

### 4. Animating with Kling AI

Writing the animation prompts was the trickiest part. Kling needs very specific, structured instructions. Vague prompts produce vague results.

ChatGPT was essential here. When I wanted the figure to stand still and gaze at the moon, for example, Kling kept making her walk. ChatGPT helped me understand that I needed to explicitly forbid leg movement, specify that her feet remain planted, and give Kling an alternative micro-movement (a subtle head tilt, a weight shift) so the animation engine had something to do.

**Learning: AI tools have personalities.** Claude excels at strategy, structure, and creative direction. ChatGPT was more effective at the specific, literal, technical instructions Kling needed.

### 5. Soundtrack and Voiceover

Suno generated a custom ambient drone. ElevenLabs cloned my voice for narration.

**Learning: Sound matters more than you think.** The ambient track transformed static images into something emotional.

### 6. Assembly

Filmora for video editing and audio. Canva for typography and final polish.

## What I Learned

1. **Start with words, not pictures.** The script shapes everything.
2. **Protect what works.** When you find a prompt or style that captures what you want, template it.
3. **AI tools have personalities.** Claude for strategy, ChatGPT for technical prompts, Leonardo for illustration, Kling for animation.
4. **Iteration isn't failure.** Some frames took 10+ generations to get right.
5. **Human judgement is the throughline.** The AI proposed. I disposed.
6. **Simple prompts often outperform complex ones** — except for animation prompts, which need precision.
7. **Sound matters more than you think.**
8. **The creative process is still creative.**
