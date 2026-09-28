---
title: "How to Make an AI Short Film for Under $200: Full Production Workflow with Claude and Seedance"
url: "https://www.mindstudio.ai/blog/how-to-make-ai-short-film-under-200-claude-seedance"
author: "Luis Chavez-Mattos (Director of Product, MindStudio)"
date: "2026-03-29"
source: "MindStudio blog"
---

# How to Make an AI Short Film for Under $200: Full Production Workflow with Claude and Seedance

Traditional short film production — even a stripped-down indie project — can easily hit $5,000 to $50,000. AI video generation has fundamentally changed that cost structure. This guide covers a complete AI short film production workflow — from concept to final export — using Claude for creative development, Luma Canvas for scene visualization, Nano Banana Pro for consistent image generation, and Seedance 2.0 for video clips. Total budget: under $200.

## The Tools in This Stack

### Claude: Story Development and Production Planning

Claude handles the creative and organizational backbone of the entire production. Using Claude's Projects feature — which lets you maintain persistent context across conversations — you can keep your script, shot list, character notes, and visual direction all in one place.

This context-persistence is the key advantage. It means Claude understands what scene you're describing when you ask it to write a prompt for shot 14, without you re-explaining the whole film.

### Luma Canvas: Scene and Environment Visualization

Luma Canvas is Luma AI's creative workspace for image generation and style exploration. It's most useful early in production for establishing visual tone — think mood boards, wide establishing shots, and environment concepts.

### Nano Banana Pro: Character-Consistent Image Generation

Keeping characters recognizable across scenes is the hardest problem in AI filmmaking. Nano Banana Pro is in this stack specifically for its ability to lock character appearances across multiple generations. You define a character's visual parameters once, and the tool holds that reference as you generate shots from different angles, lighting conditions, and scenes.

### Seedance 2.0: Image-to-Video Generation

Seedance 2.0 — developed by ByteDance — is where still images become video clips. It handles camera physics and subject motion well, producing output that feels cinematic rather than jittery or artificial.

## Step 1: Develop Your Concept with Claude

The fastest way to waste your budget is generating video before your story is defined.

### Set Up a Project in Claude

Start a new Claude Project and write a system prompt that defines your film's creative parameters:
- Genre and emotional tone (e.g., "quiet psychological drama, tense, muted color palette")
- Target length (a 2–3 minute short is the right scope for this budget)
- Visual style references
- Hard constraints — locations, characters, any thematic requirements

### Write the Script

A 2-minute film at standard pacing needs roughly 6–10 distinct shots. Keep the scope tight and the story self-contained.

A useful starting prompt: "Write a 2-minute short film script in [genre]. Two characters maximum. One or two locations. The story should resolve visually — minimal dialogue."

The minimal dialogue recommendation is practical, not stylistic. AI-generated lip sync adds complexity and cost. Let visuals carry the story where possible.

### Build a Shot List

Once the script is locked, ask Claude to convert it into a structured shot list. Each entry should include:
- Scene and shot number
- Shot type (wide, medium, close-up, POV, over-the-shoulder)
- Action description
- Camera movement (static, slow push-in, pan left, tracking)
- Lighting and mood notes

This shot list is your production contract. Every image and video clip you generate from this point maps to a row in this list.

## Step 2: Build Your Visual Bible

This phase is about establishing how your film looks before you generate a single final shot. It's cheap to iterate here. It's expensive to iterate during video generation.

### Define the Visual Style in Luma Canvas

Generate 8–12 concept images in Luma Canvas that represent your film's aesthetic. These aren't finished shots — they're tone references. When you find a look you want to commit to, save the exact prompt language that produced it. Those specific phrases carry forward into every prompt you write from here. Minor variations in language produce major visual drift across a film.

### Generate Character Reference Sheets

For each character, generate a reference set using Nano Banana Pro. The goal is 4–6 images per character showing:
- Front-facing portrait
- Three-quarter view
- Full body in the costume they wear throughout the film
- At least one image in your established lighting style

These reference images are your consistency anchor for the entire production.

## Step 3: Generate Scene Images for Each Shot

Work through your shot list sequentially. For each planned shot, you need one strong source image before you can generate video.

### Write Image Prompts with Claude

A strong prompt for this workflow includes:
- **Subject**: character name, pose, action, expression
- **Environment**: location description matching your location references
- **Lighting**: source direction, quality, time of day
- **Composition**: shot type translated into visual language (e.g., "character fills left third of frame, looking off-screen right")
- **Style**: your locked style language from the visual bible

### Generate and Select in Nano Banana Pro

Run each prompt through Nano Banana Pro using your character reference images as anchors. Generate 3–5 variations per shot. Select based on:
- Character matches reference sheets
- Composition matches intended shot type
- Lighting is consistent with established visual style
- Image is clean and readable enough for Seedance 2.0 to animate effectively

## Step 4: Animate Your Shots with Seedance 2.0

### Write Motion Prompts

Each clip needs a motion prompt that describes what moves and how — separate from the image prompt. Effective motion prompts include:
- **Subject motion**: what is the character doing? (turning head slowly, walking toward camera)
- **Camera motion**: static, slow push-in, pan, tracking shot
- **Ambient motion**: environmental detail that should move (curtains shifting, smoke, foliage)
- **Pace**: is the motion deliberate and slow, or sharp and quick?

Example: "Camera slowly pushes in. Character turns head slightly left, expression shifting from neutral to concern. Subtle ambient light flicker. Background softly out of focus."

### Generate Clips in Seedance 2.0

Generate 2–3 variations per shot. Key settings:
- **Aspect ratio**: Lock this early and don't change it.
- **Motion intensity**: Lower settings for contemplative shots, higher for action or tension.
- **Seed locking**: When a generation produces great lighting physics or motion quality, lock the seed and vary the prompt to iterate.

## Step 5: Post-Production

### Edit in DaVinci Resolve

- **Cut shorter than you think**: AI clips often work better at 2–3 seconds than 5.
- **Prefer straight cuts**: Simple cuts read better than complex transitions with AI footage.
- **Watch rough cuts without audio first**: If the visual rhythm feels off, fix it before you build audio around it.

### Add Music and Sound Design

This is where a $200 film separates from an amateur experiment. Good audio does more to elevate perceived production quality than almost anything else.

### Color Grade

Apply a consistent color grade across all clips in DaVinci Resolve's Color page. A single LUT applied uniformly will unify footage that has slight visual inconsistencies between generation sessions.

## The $200 Budget, Broken Down

| Tool / Service | Estimated Cost |
|---|---|
| Claude (monthly subscription) | $20 |
| Luma Canvas (image generation credits) | $20–30 |
| Nano Banana Pro (character-consistent generation) | $30–50 |
| Seedance 2.0 (video generation credits) | $60–80 |
| Music (Suno or licensed library) | $10–20 |
| DaVinci Resolve | Free |
| Sound effects (Freesound.org) | Free |
| **Total** | **$140–200** |

## Common Mistakes That Blow the Budget

- **Starting video generation before visuals are defined.** Build the visual bible first.
- **Underinvesting in audio.** A film with imperfect visuals and strong audio reads as more professional.
- **Accepting inconsistent character generations.** If a character looks different in shot 7 than in shot 3, regenerate.
- **Over-generating options.** Three variations per shot, maximum. Be decisive.
- **Skipping the shot list.** The shot list is the production structure that makes editing possible.
