---
title: "Seedance 2.0 Prompt Guide — OpenArt Video Generation Framework"
url: "https://openart-seedance-guide.vercel.app/"
author: "OpenArt (community guide)"
date: "2026-04-30"
source: "OpenArt Seedance 2.0官方提示词指南"
model: "Seedance 2.0"
---

# Seedance 2.0 Prompt Guide — OpenArt Video Generation Framework

A comprehensive framework for crafting high-performance prompts across text-to-video, image-to-video, and multimodal generation workflows on OpenArt.

## 01 — The Prompt Architecture

### Core Prompt Formula

**Subject + Action + Environment + Camera Language + Visual Style + Sound Design**

The model processes natural language with deep semantic comprehension. Think of your prompt as a shot list collapsed into a single paragraph.

### Dimension Breakdown

| Dimension | What to Specify | Impact Level |
|---|---|---|
| Subject | Identity, appearance, clothing, expression, posture | Critical |
| Motion | Action type, speed, intensity, direction, physics | Critical |
| Environment | Location, weather, time of day, depth, background elements | High |
| Lighting | Direction, color temperature, contrast, volumetric effects | High |
| Camera | Shot size, movement (pan, dolly, crane), focal length, depth of field | High |
| Style | Photorealistic, cel-shaded, film grain, color grade, era | Medium |
| Audio | Ambient sound, dialogue, voiceover, music cues | Medium |

**Writing philosophy:** Write your prompt the way a director gives instructions to a crew: start with the subject, describe the motion, set the scene, then layer in technical direction. Use temporal markers ("first," "then," "as the camera pulls back") to guide the model through multi-beat shots.

## 02 — Multimodal Anchoring

By uploading reference images, audio clips, or video segments alongside your prompt, you give the model concrete anchors.

**Two principles:**
- **Explicit Mapping:** Always name your reference assets in the prompt. "Use the composition from Image 1" or "Match the pace of Video 2."
- **Upload order matters.** Reference them as "Image 1," "Image 2," "Audio 1," etc.

## 03 — On-Screen Typography

**Typography Prompt Structure:** [Text Content] + [Timing] + [Position] + [Entrance Animation] + [Color, Font Style]

Best practices: slogans of 3-5 words perform best. Stick to common vocabulary.

**Subtitles syntax:** Display subtitles at the bottom-center with the text "[your dialogue]."

**Speech bubbles syntax:** [Character] says, "[Dialogue]." Speech bubbles appear around the character.

### Example — Text-to-Video (Subtitles)
A cinematic aerial shot slowly descending over a fog-covered valley at golden hour. Voiceover: A calm female voice narrates, "There are places the map forgot, and those are the ones worth finding." Render the narration as subtitles at the bottom-center, perfectly synchronized with the voiceover timing.

### Example — Text-to-Video (Speech Bubbles)
Anime style: Two teenagers stand at the edge of a rooftop overlooking a sprawling city at sunset. The girl turns to the boy with a grin and says, "Race you to the bottom." The boy laughs and replies, "You always say that." Speech bubbles containing their lines appear beside each character as they speak.

## 04 — Visual Asset Referencing

### Multi-Angle Subject Locking

**Syntax:** Refer to / Extract / Combine the [Subject] from [Image 1], [Image 2], and [Image 3] to generate [Scene], maintaining consistent [Subject] features throughout.

### Example — Product Showcase (Reference + I2V)
Use the wireless headphones from Image 1 (front view), Image 2 (side profile), and Image 3 (case open). Place them on a matte black pedestal in a studio with soft overhead lighting. The camera opens on a tight close-up of the ear cup texture, then orbits 360 degrees around the headphones, revealing every angle. Slow, deliberate movement. Minimal ambient soundtrack with a low hum.

### Example — Character Consistency (Reference + T2V)
Refer to the young woman from Image 1 (front), Image 2 (three-quarter), and Image 3 (profile). Generate a scene of her walking through an autumn park, leaves falling around her. She pauses at a bench, sits down, and opens a leather-bound notebook. Warm afternoon light, shallow depth of field on the background trees.

### Example — Storyboard Sequencing
Follow the storyboard layout in Image 1. Panel 1: Wide shot of a rain-soaked city street at night. Panel 2: Medium shot of a woman under an umbrella, looking at her phone. Panel 3: Close-up of the phone screen showing a message. Panel 4: She smiles and steps into the rain. Execute each panel composition in strict order, with smooth dissolve transitions between shots. Neo-noir lighting, high contrast, teal and orange color grade.

## 05 — Audio Layer Control

### Voice Cloning for Characters

**Syntax:** [Character] says: "[Dialogue]," using the voice from [Audio N].

### Example — Image + Audio Reference
The woman from Image 1 stands at a podium in a modern conference hall. Warm stage lighting. She speaks with the voice from Audio 1, delivering the line: "The future is not something we wait for. It is something we design." Confident posture, natural hand gestures, and precise lip-sync. The camera slowly tightens from a medium shot to a close-up on her face as she finishes the sentence.

### Example — Multi-Character Dialogue
The man from Image 1 and the woman from Image 2 are walking through a botanical garden in soft afternoon light. The man speaks with the voice of Audio 1, saying with a smirk: "I told you this was the shortcut." The woman responds with the voice of Audio 2, rolling her eyes playfully: "This is the third time you've said that." Shallow depth of field, natural ambient bird sounds underneath the dialogue, expressive facial movements, and perfectly synchronized lip motion.

## 06 — Motion Transfer and Video Referencing

### Example — Motion Transfer
Reference the fluid dance choreography from Video 1. Apply it to the character from Image 1, now performing in a rain-slicked alleyway at night. Neon reflections on the wet ground. The camera matches a handheld documentary feel with tight framing. High-energy electronic soundtrack implied by the movement pacing.

### Example — Camera Movement Transfer
Using the first-person diving camera motion from Video 1, create a concept reel for a futuristic vertical city. The camera plunges from cloud level down through layers of glass bridges and hovering gardens, with the tower from Image 1 as the central visual anchor. High-contrast sci-fi color grade, lens flare on descent.

## 07 — Post-Generation Editing

### Adding Elements
In Video 1, add a steaming cup of coffee and an open book to the table in front of the seated character. Both items should appear naturally from the start of the clip.

### Removing Elements
Remove the pedestrians and street traffic from Video 1, leaving only the main character walking down the empty avenue. Preserve all original camera movement and lighting.

### Replacing Elements
Replace the glass bottle featured in Video 1 with the skincare serum from Image 1. Maintain all original hand movements, camera angles, and lighting. The serum bottle should catch the same reflections and highlights as the original object.

### Video Extension
- **Forward:** Extend Video 1 forward: After the group high-fives, they turn and walk toward the sunset along the beach.
- **Backward:** Extend Video 1 backward: Before the door opens, show a close-up of a hand hesitating on the doorknob.

### Multi-Clip Stitching
Video 1. As the skateboarder lands the trick, a burst of chalk dust fills the frame, dissolving into Video 2. The dust settles to reveal a dancer mid-spin on a rooftop at golden hour.

**Limits:** Maximum 3 input clips. Combined duration ≤ 15 seconds.

## 08 — Prompt Library (Ready-to-Use Templates)

### Cinematic Narrative — Astronaut
A lone astronaut stands at the edge of a massive crater on a barren moon. The visor reflects a distant blue planet. She takes one step forward and plants a small flag with an unknown insignia. The camera starts tight on her boot hitting the dust, then cranes upward to reveal the vast emptiness of the landscape. Desaturated palette with a single teal accent from the planet's reflection. Low rumble of wind across the surface.

### Cinematic Narrative — Detective
A 1970s-styled detective sits in a dimly lit office, rain streaking the window behind him. He lights a cigarette. The smoke curls upward in slow motion, and the camera follows the smoke trail until it fills the frame. Through the haze, the scene dissolves into a rain-soaked street corner where a woman in a red coat waits under a flickering streetlight. Film grain, 35mm anamorphic distortion, muted greens and deep shadows.

### Product — Sneaker Waterproof
The sneaker from Image 1 sits on a concrete surface. Water droplets begin falling onto it in slow motion, each drop exploding into a micro-splash that reveals the waterproof coating. The camera orbits 180 degrees during the sequence. Then a hand reaches in, picks up the sneaker, and flexes it to show the sole. Studio lighting with a single hard key light from the upper left, dark background, shallow depth of field.

### Product — Luxury Perfume
A perfume bottle made of dark amber glass rests on a bed of wet black stones. Steam rises from the stones as if from a hot spring. The camera slowly pushes in from a wide shot to an extreme close-up of the bottle's faceted cap, where light refracts into prismatic rainbows. The word "NOIR" fades in below the bottle in thin gold serif type. Luxury aesthetic, warm low-key lighting, rich blacks.

### Animation — Watercolor
Watercolor animation style: A paper boat floats down a stream through a forest. Cherry blossom petals land on the water surface. The boat drifts under a small stone bridge where a frog watches from the railing. As the boat exits the bridge's shadow, the camera tilts up to reveal a vast mountain range painted in soft washes of indigo and rose. Gentle piano melody implied by the pacing.

### Animation — Pixel Art
3D isometric pixel art: A tiny character in a red cap runs across a floating island, jumping between platforms made of stacked cubes. They collect glowing orbs that leave particle trails. The camera follows from a fixed isometric angle as the character reaches the final platform and a treasure chest opens, releasing a column of golden light. Chiptunecore energy, bright saturated palette, crisp shadows.

## Prompt Engineering Quick Reference

| Goal | Technique |
|---|---|
| More cinematic output | Specify lens type (anamorphic, 35mm), film stock (Kodak Portra, Fuji Velvia), and color grade |
| Better motion coherence | Use temporal sequencing words: "first," "then," "as X happens, Y begins" |
| Precise text rendering | Keep text short (3 to 5 words), specify position and entrance style, use common vocabulary |
| Character consistency | Upload 2 to 3 angles of the same character and reference all images explicitly |
| Brand integration | Upload logo as a separate image, reference it by number, specify persistent placement |
| Smooth transitions | Describe the transitional moment explicitly: "dissolve," "blur transition," "particle burst leading into" |
| Realistic lip-sync | Upload character image + audio reference, write out exact dialogue in the prompt |
