import json
from google import genai
from google.genai import types

# Initialize the Gemini Client
# Ensure your GEMINI_API_KEY environment variable is configured in your system
client = genai.Client()

def get_cinematic_matrix(project_bpm: float) -> dict:
    """
    Calculates exact alignment variables to sync audio transitions 
    perfectly with 23.976 FPS industry-standard film cut markers.
    """
    fps = 23.976
    seconds_per_beat = 60.0 / project_bpm
    seconds_per_bar = seconds_per_beat * 4  # Assuming standard 4/4 time signature
    frames_per_bar = seconds_per_bar * fps
    
    return {
        "seconds_per_bar": round(seconds_per_bar, 4),
        "frames_per_bar": round(frames_per_bar, 3),
        "sample_rate_target": "96,000 Hz",
        "audio_bit_depth": "32-Bit Float"
    }

def compile_epic_studio_macro(user_intent: str, project_bpm: float = 80.0):
    """
    Blends absolute engineering specifications with Gemini Pro 2.5 
    to generate native FL Studio engine scripts.
    """
    matrix = get_cinematic_matrix(project_bpm)
    
    system_instruction = f"""
    You are the primary computing mind of EPIC-STUDIO'S. Your objective is to engineer 
    operational Python modules tailored exclusively for FL Studio.
    
    Current Master Project Constraints:
    - Target Audio Standards: {matrix['sample_rate_target']} at {matrix['audio_bit_depth']} (Studio Master)
    - Film Grid Synchronization: {matrix['frames_per_bar']} frames per musical bar at 23.976 FPS
    
    Provide ONLY valid Python code blocks wrapped in standard markdown code formatting. No conversational filler.
    """
    
    prompt = f"""
    User Creative Request: {user_intent}
    Mathematical Sync Link: Each bar must align exactly with {matrix['frames_per_bar']} film frames.
    
    Task: Write an optimized FL Studio script utilizing the 'flpianoroll' or native hardware APIs 
    to perfectly satisfy this directive.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.15
        )
    )
    
    return response.text

if __name__ == "__main__":
    # Test compiling a top-tier orchestral crescendo request
    test_request = "Generate a piano roll script that applies an exponential velocity crescendo and adds micro-timing humanization."
    print(compile_epic_studio_macro(test_request, project_bpm=80.0))
