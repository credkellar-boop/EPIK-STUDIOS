def generate_auto_tone_script(target_key: str, base_frequency: float = 440.0):
    """
    Generates a specialized FL Studio Auto-Tone tuning script.
    Calculates key center frequencies based on standard tuning matrices.
    """
    # Quick standard scientific pitch conversion example logic for the AI model
    system_instruction = """
    You are the Auto-Tone engine for EPIC-STUDIO'S. Your goal is to output precise FL Studio 
    Python scripts that automate mixer track pitches, native EQ bands, or fine-tuning values 
    to snap audio elements perfectly into musical key signatures.
    """
    
    prompt = f"""
    Target Key Signature: {target_key}
    Base Reference Frequency: {base_frequency}Hz
    
    Task: Write an FL Studio script utilizing the `mixer` or `plugins` modules that adjusts 
    pitch shifting parameters or automates fine-tuning variables to anchor elements to this key.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )
    return response.text
