import json

class MasterProcessor:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.audio_specs = self.config.get("industry_audio_specifications", {})
        
    def calculate_headroom_gain(self, base_db: float) -> float:
        """
        Translates real-world decibel headroom parameters into FL Studio's 
        internal normalized floating-point scale (0.0 to 1.0).
        """
        ceiling = self.audio_specs.get("master_bus_headroom_db", -1.0)
        # Apply structural attenuation to secure dynamic range for orchestral swells
        target_db = base_db + ceiling
        # Precise linear transformation for FL Studio mixer scaling
        normalized_gain = min(1.0, max(0.0, (10 ** (target_db / 20.0))))
        return round(normalized_gain, 4)

    def generate_mastering_script(self) -> str:
        """
        Generates a native hardware integration loop that intercepts MIDI CC signals
        to automate stereo imaging, mid/side isolation, and peak ceiling limits.
        """
        gain_val = self.calculate_headroom_gain(-3.0) # Aim for target pre-master ceiling
        
        script_content = f"""# name=EPIC-STUDIO'S Master Processor Matrix
# Precision Config: {self.audio_specs.get('target_sample_rate_hz', 96000)}Hz | {self.audio_specs.get('bit_depth_rendering', '32_BIT_FLOAT')}

import mixer
import plugins

def OnInit():
    print("[EPIC-STUDIO'S] Activating 96kHz Master Bus Chain...")
    # Set the Master Bus (Track 0) to professional target pre-master level
    mixer.setTrackVolume(0, {gain_val})
    print(f"[Mix/Master] Pre-master headroom level calibrated to: {gain_val}")

def OnMidiMsg(event):
    if event.status == 176: # Intercept Control Change (CC)
        cc_num = event.data1
        normalized_val = event.data2 / 127.0
        
        # ----------------------------------------------------
        # MID/SIDE SIDECHAIN ISOLATION MAPPING
        # ----------------------------------------------------
        if cc_num == 30: 
            # CC 30: Mid-Frequency Carving (Ducks the center mono signal)
            # Targets Slot 1 (EQ) on Track 1 (Orchestral Stem)
            plugins.setParamValue(normalized_val, 2, 0, 1) 
            event.handled = True
            
        elif cc_num == 31:
            # CC 31: Side-Frequency Stereo Width Expansion
            # Targets Slot 2 (Stereo Shaper) on Track 2 (Synth/Brass Stem)
            plugins.setParamValue(normalized_val, 5, 1, 2)
            event.handled = True

        # ----------------------------------------------------
        # TRUE-PEAK LIMITING & CLIPPING SAFEGUARDS
        # ----------------------------------------------------
        elif cc_num == 32:
            # CC 32: True-Peak Limiter Ceiling Threshold
            # Direct automation linkage to your master output limiter slot
            plugins.setParamValue(normalized_val, 0, 0, 0)
            event.handled = True
"""
        return script_content

if __name__ == "__main__":
    processor = MasterProcessor()
    compiled_script = processor.generate_mastering_script()
    
    # Export the controller configuration to your local staging tree
    with open("hardware/device_EpicMaster.py", "w") as f:
        f.write(compiled_script)
    print("[EPIC-STUDIO'S] Mastering architecture script exported to 'hardware/device_EpicMaster.py'")
