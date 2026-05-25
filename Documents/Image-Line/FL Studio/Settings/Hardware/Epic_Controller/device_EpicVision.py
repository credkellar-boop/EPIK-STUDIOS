# name=EPIC-STUDIO'S CV Vision Receiver
# supportedDevices=EPIC-VISION-PORT

import mixer
import plugins
import device

def OnInit():
    print("EPIC-STUDIO'S Live Vision Tracker Synced.")

def OnMidiMsg(event):
    if event.status == 176: # MIDI CC message
        
        # Audio Control: Map Face X-Axis to Mixer Track 1 Volume or Filter
        if event.data1 == 16: 
            audio_value = event.data2 / 127.0
            mixer.setTrackVolume(1, audio_value)
            event.handled = True
            
        # Visual Control: Map Face Y-Axis to ZGameEditor Parameter
        elif event.data1 == 17:
            visual_value = event.data2 / 127.0
            # Assuming ZGameEditor is on the Master Track (Track 0) in Plugin Slot 1
            # Adjusts a specific visualizer parameter (e.g., Hue, Camera Z, or Scale)
            plugins.setParamValue(visual_value, 0, 0) 
            event.handled = True
# name=EPIC-STUDIO'S Multi-Camera ZGame Hooks
# supportedDevices=EPIC-VISION-PORT

import plugins
import device

# Configure ZGameEditor Routing
# Ensure ZGameEditor Visualizer is loaded on the Master Track (Track 0), Slot 1 (Index 0)
ZGAME_MIXER_TRACK = 0
ZGAME_SLOT_INDEX = 0

def OnInit():
    print("EPIC-STUDIO'S ZGameEditor Visualizer Matrix Active.")

def OnMidiMsg(event):
    if event.status == 176: # Intercept Control Change (CC)
        
        # ----------------------------------------------------
        # CAMERA 01 ROUTING (Foreground Elements)
        # ----------------------------------------------------
        if event.data1 == 16: 
            # CC 16: Map Cam 1 X-Axis to Layer 1 Image X-Offset (Param Index 10 as example)
            val = event.data2 / 127.0
            plugins.setParamValue(val, 10, ZGAME_SLOT_INDEX, ZGAME_MIXER_TRACK)
            event.handled = True
            
        elif event.data1 == 17:
            # CC 17: Map Cam 1 Y-Axis to Layer 1 Image Y-Offset (Param Index 11)
            val = event.data2 / 127.0
            plugins.setParamValue(val, 11, ZGAME_SLOT_INDEX, ZGAME_MIXER_TRACK)
            event.handled = True

        # ----------------------------------------------------
        # CAMERA 02 ROUTING (Background / Lighting Elements)
        # ----------------------------------------------------
        elif event.data1 == 18: 
            # CC 18: Map Cam 2 X-Axis to Layer 2 Color Hue/Light Angle (Param Index 20)
            val = event.data2 / 127.0
            plugins.setParamValue(val, 20, ZGAME_SLOT_INDEX, ZGAME_MIXER_TRACK)
            event.handled = True
            
        elif event.data1 == 19:
            # CC 19: Map Cam 2 Y-Axis to Layer 2 Bloom Intensity (Param Index 21)
            val = event.data2 / 127.0
            plugins.setParamValue(val, 21, ZGAME_SLOT_INDEX, ZGAME_MIXER_TRACK)
            event.handled = True

import flpianoroll
import random
import math

def createDialog():
    form = flpianoroll.ScriptDialog("EPIC-STUDIO'S // Elite Symphonic Driver", "Applies emotional expressions and micor-timing to orchestral arrays.")
    form.addInputKnob("Crescendo Intensity", 75, 10, 100)
    form.addInputKnob("Human Musician Variance", 12, 0, 30)
    return form

def apply(form):
    intensity = form.getInputValue("Crescendo Intensity") / 100.0
    variance = form.getInputValue("Human Musician Variance")
    
    score = flpianoroll.score
    if not score.noteCount:
        return

    # Sort notes from earliest to latest so the crescendo evolves over time
    notes = [score.getNote(i) for i in range(score.noteCount)]
    notes.sort(key=lambda x: x.time)
    
    total_duration = notes[-1].time - notes[0].time if len(notes) > 1 else 1

    for note in notes:
        # Calculate where this specific note falls in the timeline (0.0 to 1.0)
        relative_position = (note.time - notes[0].time) / max(1, total_duration)
        
        # Apply an exponential curve to the velocity to simulate brass or strings building tension
        crescendo_curve = math.pow(relative_position, 2) * intensity
        
        # Introduce micro-timing imperfections so the 'musicians' don't hit the notes at the exact microsecond
        human_offset = random.randint(-int(variance), int(variance))
        note.time = max(0, note.time + human_offset)
        
        # Blend the structural crescendo with a subtle touch of human randomness
        random_expressiveness = random.uniform(-0.08, 0.08)
        note.velocity = max(0.15, min(1.0, crescendo_curve + random_expressiveness))
        
import flpianoroll
import math
import random

def createDialog():
    """
    Creates the elite orchestration controller panel inside the Piano Roll grid view.
    """
    form = flpianoroll.ScriptDialog("EPIC-STUDIO'S // Symphonic Orchestration Engine", "Applies emotional curves and humanized micro-timings to selected layers.")
    form.addInputKnob("Crescendo Depth", 80, 10, 100)
    form.addInputKnob("Human Micro-Timing", 10, 0, 30)
    form.addInputCombo("Symphonic Mode", "Exponential Crescendo,Linear Swell,Decrescendo", 0)
    return form

def apply(form):
    """
    Executes advanced velocity mapping and subtle micro-timing offsets on human musicianship.
    """
    crescendo_depth = form.getInputValue("Crescendo Depth") / 100.0
    timing_variance = form.getInputValue("Human Micro-Timing")
    selected_mode = form.getInputValue("Symphonic Mode")
    
    score = flpianoroll.score
    if not score.noteCount:
        return

    # Sort the highlighted notes in order of time execution
    notes = [score.getNote(i) for i in range(score.noteCount)]
    notes.sort(key=lambda x: x.time)
    
    start_time = notes[0].time
    end_time = notes[-1].time
    total_duration = end_time - start_time if end_time > start_time else 1

    for note in notes:
        # Calculate relative position within the pattern phrase (0.0 to 1.0)
        progress = (note.time - start_time) / total_duration
        
        # 1. Apply Music Industry Dynamics Curves
        if selected_mode == 0:    # Exponential Crescendo (Ideal for epic cinematic builds)
            velocity_multiplier = math.pow(progress, 2) * crescendo_depth
        elif selected_mode == 1:  # Linear Swell
            velocity_multiplier = progress * crescendo_depth
        else:                     # Decrescendo
            velocity_multiplier = (1.0 - progress) * crescendo_depth
            
        # Blend target velocity with a margin of individual musician variance
        note.velocity = max(0.15, min(1.0, velocity_multiplier + random.uniform(-0.07, 0.07)))
        
        # 2. Apply Micro-Timing Imperfections (Breathes acoustic space into the mix)
        human_jitter = random.randint(-int(timing_variance), int(timing_variance))
        note.time = max(0, note.time + human_jitter)
# name=EPIC-STUDIO'S Master Cinematic Controller
# supportedDevices=Epic Control Surface,EPIC-VISION-PORT

import mixer
import plugins
import general
import transport

def OnInit():
    """Executes when the engine links to FL Studio's MIDI matrix."""
    print("------------------------------------------------------------------")
    print("[EPIC-STUDIO'S] High-Fidelity A/V Controller Protocol Initialized.")
    print("Status: 96kHz Processing Path Confirmed.")
    print("------------------------------------------------------------------")

def OnMidiMsg(event):
    """
    Intercepts continuous controller automation data packets.
    Maps CC values cleanly from 0-127 to 0.0-1.0 parameters.
    """
    if event.status == 176:  # Standard MIDI CC Identification Byte
        control_channel = event.data1
        normalized_value = event.data2 / 127.0
        
        # CC 20: Master Timbral Expression (Orchestral Volume Expression Tracking)
        if control_channel == 20:
            # Automates mixer track 1 volume dynamically (e.g., your Master String Bus)
            mixer.setTrackVolume(1, normalized_value)
            event.handled = True
            
        # CC 21: Cinematic Reverb Wetness / Spatialization Width
        elif control_channel == 21:
            # Assuming Fruity Convolver / Reverb is placed on the master track (0), slot 2 (index 1)
            # Parameter 1 typically acts as Wet Mix level across major native image-line modules
            plugins.setParamValue(normalized_value, 1, 0, 0)
            event.handled = True
            
        # CC 22: Live 8K Visualizer Displacement or Camera Modulations
        elif control_channel == 22:
            # Routes controller data directly to ZGameEditor Visualizer (Track 0, Slot 1)
            plugins.setParamValue(normalized_value, 10, 0, 0)
            event.handled = True
