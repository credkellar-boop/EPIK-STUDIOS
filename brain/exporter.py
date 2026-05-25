import os
import re
import json

def export_to_fl_studio(raw_gemini_markdown: str, filename: str) -> str:
    """
    Parses code from markdown, identifies its target script structure,
    and exports it directly to the designated FL Studio user folder paths.
    """
    # 1. Extract pure code block out of Gemini's markdown wrapper
    code_match = re.search(r"```python\n(.*?)```", raw_gemini_markdown, re.DOTALL)
    if code_match:
        clean_code = code_match.group(1)
    else:
        clean_code = raw_gemini_markdown  # Fallback if text formatting was skipped

    # 2. Extract configuration system paths
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        base_user_path = config["system_settings"]["fl_user_data_path"]
    except Exception as e:
        return f"[EXPORTER ERROR] Could not read path from config.json: {e}"

    # 3. Detect system layer target via code fingerprinting
    if "flpianoroll" in clean_code or "ScriptDialog" in clean_code:
        # Destination: Piano roll scripting architecture
        sub_folder = "Piano roll scripts"
        if not filename.endswith(".py"):
            filename = f"Epic_{filename}.py"
    else:
        # Destination: Native hardware controller environment
        sub_folder = "Hardware/Epic_Controller"
        if not filename.startswith("device_"):
            filename = f"device_Epic_{filename}.py"

    # 4. Assemble the write path matrix safely
    target_directory = os.path.normpath(os.path.join(base_user_path, sub_folder))
    full_destination_path = os.path.join(target_directory, filename)

    try:
        # Verify nested folders are instantiated
        os.makedirs(target_directory, exist_ok=True)
        
        # Write asset out down to disk
        with open(full_destination_path, "w", encoding="utf-8") as script_out:
            script_out.write(clean_code.strip())
            
        return f"[SUCCESS] Extension written directly to FL Studio:\n-> {full_destination_path}"
    except Exception as e:
        return f"[EXPORTER ERROR] Failed to push code block to system disk: {e}"
