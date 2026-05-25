import json
from google import genai
from google.genai import types

# Initialize the Gemini Client using your global environment API key
client = genai.Client()

def get_industry_specifications():
    """
    Returns the absolute technical standards required by major streaming platforms
    (Apple Music, Spotify Lossless) and Hollywood theatrical projection systems.
    """
    return {
        "audio": {
            "sample_rate": "96,000 Hz (Ultra-HD Mastering Standard)",
            "bit_depth": "32-Bit Floating Point (Infinite Internal Headroom)",
            "resampling": "512-point sinc (Flawless transient preservation)"
        },
        "visuals": {
            "resolution": "7680 x 4320 (True 8K Cinematic Blueprint)",
            "frame_rate": "23.976 FPS (Standard Hollywood Film Grid)",
            "bitrate": "150 Mbps (Lossless Presentation Profile)"
        }
    }

def compose_cinematic_asset(user_creative_intent: str, project_bpm: float = 120.0):
    """
    Commands Gemini Pro 2.5 to engineer flawless FL Studio Python code, mid/side routing,
    or advanced score manipulation macros matching top-tier film standards.
    """
    specs = get_industry_specifications()
    
    system_instruction = f"""
    You are the Master Director behind EPIC-STUDIO'S. Your sole purpose is helping the user create 
    commercial, chart-topping music industry audio and 8K blockbuster cinematic films.
    
    You operate strictly under these industry specs:
    - Audio Architecture: {specs['audio']['sample_rate']} at {specs['audio']['bit_depth']}
    - Visual Architecture: {specs['visuals']['resolution']} at {specs['visuals']['frame_rate']}
    
    Output exclusively functional Python code blocks, advanced midi automation, or exact music theory matrices.
    """
    
    # Calculate exact mathematical alignment for camera cuts to prevent audio/visual drifting
    fps = 23.976
    seconds_per_beat = 60.0 / project_bpm
    frames_per_bar = (seconds_per_beat * 4) * fps
    
    prompt = f"""
    Target Project Tempo: {project_bpm} BPM
    Mathematical Film Grid Link: {round(frames_per_bar, 3)} frames per musical bar.
    
    Creative Directive: {user_creative_intent}
    
    Task: Write an elite FL Studio tool or configuration script maximizing these constraints.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.15 # Kept low for surgical precision in calculations
        )
    )
    
    return response.text

if __name__ == "__main__":
    print("[EPIC-STUDIO'S] High-Fidelity Engine Initialized.")
    
    # Example Industry Request: Generating a complex, evolving string ensemble velocity map
    hollywood_directive = (
        "Create an advanced piano roll expression automation script that mimics a live "
        "symphonic string section performing a heavy, emotional crescendo matching a major cinematic film climax."
    )
    
    compiled_masterpiece = compose_cinematic_asset(hollywood_directive, project_bpm=78.0)
    print("\n--- COMPILED BLOCKBUSTER DIRECTIVE ---")
    print(compiled_masterpiece)
