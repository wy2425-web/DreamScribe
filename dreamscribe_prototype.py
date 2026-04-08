"""
DreamScribe Prototype — William Yang
-------------------------------------
A command-line prototype that demonstrates the full DreamScribe pipeline:
  1. Dream input (text or voice transcript)
  2. Dream parsing (extract characters, settings, mood)
  3. Story engine (build 6-beat narrative arc)
  4. Panel description generation (image prompts for each panel)
  5. Mock comic output (with placeholders for real image generation)
  6. Save to Dream Book (local JSON log)

Tools used: Python, OpenAI GPT-4 API (mocked), OpenAI DALL-E 3 (mocked),
            OpenAI Whisper ASR (mocked), Claude AI for ideation.

To use with real APIs, set your OPENAI_API_KEY environment variable and
switch the mock functions for real API calls (see comments below).
"""

import json
import os
import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class DreamInput:
    raw_text: str
    weirdest_part: str
    emotional_tone: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

@dataclass
class ParsedDream:
    characters: list[str]
    setting: str
    key_events: list[str]
    mood: str          # playful | surreal | dark | heartwarming
    art_style: str     # e.g. "soft watercolor", "gritty noir", "bright cartoon"

@dataclass
class ComicPanel:
    panel_number: int
    scene_description: str
    dialogue: str
    image_prompt: str
    image_path: Optional[str] = None   # path to generated image

@dataclass
class DreamComic:
    title: str
    panels: list[ComicPanel]
    mood: str
    art_style: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


# ─── Step 1: Voice/Text Input ─────────────────────────────────────────────────

def transcribe_voice(audio_path: str) -> str:
    """
    Transcribes an audio recording of a dream description using Whisper ASR.

    REAL IMPLEMENTATION:
        import openai
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
        return transcript.text
    """
    # MOCK: simulates Whisper output
    print(f"[Whisper ASR] Transcribing audio from: {audio_path}")
    return "I was flying over a city made of clouds, and my old teacher was there but she had no face. There were stairs everywhere but they all led to the same door."


# ─── Step 2: Dream Parser ─────────────────────────────────────────────────────

def parse_dream(dream_input: DreamInput) -> ParsedDream:
    """
    Uses an LLM to extract structured elements from raw dream text.

    REAL IMPLEMENTATION (GPT-4):
        import openai
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        prompt = f\"\"\"
        Parse the following dream into structured components. Return JSON only.
        Dream: {dream_input.raw_text}
        Weirdest part: {dream_input.weirdest_part}
        Emotional tone: {dream_input.emotional_tone}

        Return:
        {{
          "characters": [...],
          "setting": "...",
          "key_events": [...],
          "mood": "playful|surreal|dark|heartwarming",
          "art_style": "..."
        }}
        \"\"\"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return ParsedDream(**data)
    """
    print("[Dream Parser] Extracting characters, setting, events, and mood...")

    # MOCK: simulates GPT-4 output based on dream text
    mood_map = {
        "anxious": "surreal", "scared": "dark", "happy": "heartwarming",
        "confused": "surreal", "weird": "surreal", "peaceful": "heartwarming"
    }
    mood = "surreal"
    for keyword, m in mood_map.items():
        if keyword in dream_input.emotional_tone.lower() or keyword in dream_input.raw_text.lower():
            mood = m
            break

    art_style_map = {
        "surreal": "soft watercolor with dreamlike blending",
        "dark": "gritty noir with heavy shadows and muted tones",
        "heartwarming": "bright pastel illustration",
        "playful": "bold cartoon with vibrant colors"
    }

    return ParsedDream(
        characters=["The Dreamer (you)", "Faceless Teacher", "Shadow Figure"],
        setting="A city built on clouds, with infinite staircases",
        key_events=[
            "You discover you can fly",
            "You spot your old teacher — but she has no face",
            "You find a labyrinth of staircases",
            "Every staircase leads to the same mysterious door",
            "You try to open the door but wake up"
        ],
        mood=mood,
        art_style=art_style_map.get(mood, "soft watercolor with dreamlike blending")
    )


# ─── Step 3: Story Engine ─────────────────────────────────────────────────────

def build_story_arc(parsed: ParsedDream, dream_input: DreamInput) -> list[dict]:
    """
    Converts parsed dream elements into a 6-beat narrative arc with scene
    descriptions and dialogue, using an LLM.

    REAL IMPLEMENTATION:
        prompt = f\"\"\"
        You are a creative comic scriptwriter. Turn this dream into a 6-panel
        comic story arc. Each panel needs: scene_description and dialogue.
        Use the user's voice: casual, first-person.

        Characters: {parsed.characters}
        Setting: {parsed.setting}
        Events: {parsed.key_events}
        Mood: {parsed.mood}
        Art style: {parsed.art_style}
        Weirdest part the user flagged: {dream_input.weirdest_part}

        Return a JSON array of 6 panels.
        \"\"\"
        # ... call GPT-4 ...
    """
    print("[Story Engine] Structuring 6-beat narrative arc...")

    # MOCK: pre-built story beats based on parsed dream
    beats = [
        {
            "scene_description": "The dreamer floats up from their bed, slowly rising through the ceiling into an endless sky city made entirely of clouds.",
            "dialogue": "Wait... I'm flying? This is actually happening."
        },
        {
            "scene_description": "The dreamer soars above cloud-skyscrapers and glowing streets, amazed but slightly uneasy. Other people walk below, oblivious.",
            "dialogue": "Everyone's going about their day like this is normal. Am I the only one up here?"
        },
        {
            "scene_description": "The dreamer lands and comes face-to-face with their old teacher — but where her face should be, there is only a soft blur.",
            "dialogue": "Ms. Johnson? Is that... you? Why can't I see your face?"
        },
        {
            "scene_description": "The teacher gestures silently toward an impossible staircase that spirals in every direction. A hundred doors wait at the top.",
            "dialogue": "She's pointing at something. All these staircases... they're everywhere."
        },
        {
            "scene_description": "The dreamer climbs staircase after staircase, each one leading to the same single door no matter which path they take.",
            "dialogue": "Every door is the same door. That can't be right. I've climbed seventeen of these."
        },
        {
            "scene_description": "The dreamer reaches the door, hand on the handle — and everything dissolves into morning light as they wake up, heart pounding.",
            "dialogue": "No, no, no — I was so close. What was behind there?!"
        }
    ]
    return beats


# ─── Step 4: Image Generator ──────────────────────────────────────────────────

def generate_panel_image(panel: ComicPanel, art_style: str, output_dir: str) -> str:
    """
    Generates a comic panel image using DALL-E 3 (or Stable Diffusion).

    REAL IMPLEMENTATION:
        import openai
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.images.generate(
            model="dall-e-3",
            prompt=panel.image_prompt,
            size="1024x768",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        # Download and save locally
        import requests
        img_data = requests.get(image_url).content
        path = os.path.join(output_dir, f"panel_{panel.panel_number}.png")
        with open(path, "wb") as f:
            f.write(img_data)
        return path
    """
    # MOCK: just log the prompt and return a placeholder path
    path = os.path.join(output_dir, f"panel_{panel.panel_number}_placeholder.png")
    print(f"  [DALL-E 3] Panel {panel.panel_number}: Would generate image for → {panel.image_prompt[:80]}...")
    print(f"  [DALL-E 3] Saved placeholder to: {path}")
    return path


# ─── Step 5: Full Pipeline ────────────────────────────────────────────────────

def build_image_prompt(scene: str, art_style: str) -> str:
    """Constructs a DALL-E-ready image prompt from a scene description."""
    return (
        f"Comic panel illustration in {art_style} style. "
        f"No text or speech bubbles. "
        f"Scene: {scene}"
    )

def dream_to_comic(dream_input: DreamInput, output_dir: str = "dreamscribe_output") -> DreamComic:
    """
    Full DreamScribe pipeline:
      DreamInput → ParsedDream → Story Beats → ComicPanels → DreamComic
    """
    os.makedirs(output_dir, exist_ok=True)
    print("\n🌙 DreamScribe is processing your dream...\n")

    # Step 2: Parse
    parsed = parse_dream(dream_input)
    print(f"  ✓ Mood detected: {parsed.mood} ({parsed.art_style})")
    print(f"  ✓ Characters: {', '.join(parsed.characters)}")
    print(f"  ✓ Setting: {parsed.setting}\n")

    # Step 3: Story arc
    beats = build_story_arc(parsed, dream_input)
    print(f"  ✓ 6-panel story arc built\n")

    # Step 4: Generate panels
    panels = []
    print("🎨 Generating comic panels...\n")
    for i, beat in enumerate(beats, 1):
        image_prompt = build_image_prompt(beat["scene_description"], parsed.art_style)
        panel = ComicPanel(
            panel_number=i,
            scene_description=beat["scene_description"],
            dialogue=beat["dialogue"],
            image_prompt=image_prompt
        )
        panel.image_path = generate_panel_image(panel, parsed.art_style, output_dir)
        panels.append(panel)

    # Step 5: Assemble comic
    comic = DreamComic(
        title="Dream of the Cloud City",
        panels=panels,
        mood=parsed.mood,
        art_style=parsed.art_style
    )

    # Save JSON output
    output_path = os.path.join(output_dir, "comic_output.json")
    with open(output_path, "w") as f:
        json.dump(asdict(comic), f, indent=2)
    print(f"\n✅ Comic saved to: {output_path}")

    return comic


# ─── Step 6: Dream Book ───────────────────────────────────────────────────────

def save_to_dream_book(comic: DreamComic, dream_book_path: str = "dream_book.json"):
    """Appends the generated comic to the user's Dream Book log."""
    dream_book = []
    if os.path.exists(dream_book_path):
        with open(dream_book_path, "r") as f:
            dream_book = json.load(f)

    dream_book.append({
        "title": comic.title,
        "mood": comic.mood,
        "art_style": comic.art_style,
        "created_at": comic.created_at,
        "panel_count": len(comic.panels),
        "first_line": comic.panels[0].dialogue if comic.panels else ""
    })

    with open(dream_book_path, "w") as f:
        json.dump(dream_book, f, indent=2)
    print(f"📖 Saved to Dream Book ({len(dream_book)} dream(s) total)")


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def print_comic(comic: DreamComic):
    """Pretty-prints the comic to the terminal."""
    print("\n" + "═" * 60)
    print(f"  🌙 {comic.title.upper()}")
    print(f"  Mood: {comic.mood}  |  Style: {comic.art_style}")
    print("═" * 60)
    for panel in comic.panels:
        print(f"\n  PANEL {panel.panel_number}")
        print(f"  Scene: {panel.scene_description[:100]}...")
        print(f"  Dialogue: \"{panel.dialogue}\"")
        print(f"  [Image placeholder: panel_{panel.panel_number}_placeholder.png]")
    print("\n" + "═" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("         DREAMSCRIBE — Your Dreams, Illustrated")
    print("=" * 60)

    # Example dream input (simulating user speaking into the app)
    dream = DreamInput(
        raw_text=(
            "I was flying over a city made of clouds, and my old teacher "
            "was there but she had no face. There were stairs everywhere "
            "but they all led to the same door."
        ),
        weirdest_part="My teacher had no face — just a blur where her features should be.",
        emotional_tone="confused and slightly anxious, but also amazed by the flying"
    )

    print(f"\nDream text: \"{dream.raw_text}\"")
    print(f"Weirdest part: \"{dream.weirdest_part}\"")
    print(f"Emotional tone: \"{dream.emotional_tone}\"")

    # Run the pipeline
    comic = dream_to_comic(dream)
    print_comic(comic)
    save_to_dream_book(comic)

    print("\n🌟 Done! Open comic_output.json to see the full panel data.")
    print("   To use real AI: set OPENAI_API_KEY and swap mock functions for real API calls.")
    print("   See comments in each function for the real implementation.\n")
