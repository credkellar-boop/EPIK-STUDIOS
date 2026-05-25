import json
from google import genai
from google.genai import types
from scraper import get_latest_midi_methods

def run_epic_engine(user_prompt: str):
    """
    Main orchestration block. Combines local configuration state, 
    live GitHub scraper trends, and Gemini to generate dynamic code assets.
    """
    # Load settings from configuration file
    with open('config.json', 'r') as f:
        config = json.load(f)
        
    system_settings = config.get("system_settings", {})
    
    # Gather live developer context from GitHub
    github_context = get_latest_midi_methods()
    
    # Initialize the client API
    client = genai.Client()
    
    system_instruction = f"""
    You are the primary computing mind of EPIC-STUDIO'S. 
    Your mission is to construct operational Python code modules tailored to FL Studio.
    Current System Global State:
    - Reference Frequency: {system_settings.get('target_tuning_reference_hz')}Hz
    - Active Scale Blueprint: {system_settings.get('default_scale_signature')}
    Return only pristine code output wrapped inside standard markdown code formatting blocks.
    """
    
    prompt = f"""
    Recent engineering patterns scraped from GitHub:
    {github_context}
    
    User Directive: {user_prompt}
    
    Instruction: Generate an optimized FL Studio extension module matching the user directive.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2
        )
    )
    
    return response.text

if __name__ == "__main__":
    # Test executing an auto-tone initialization call
    test_intent = "Create an active MIDI processing script that maps incoming CC modulations to parametric band-pass filters."
    output_script = run_epic_engine(test_intent)
    print(output_script)
