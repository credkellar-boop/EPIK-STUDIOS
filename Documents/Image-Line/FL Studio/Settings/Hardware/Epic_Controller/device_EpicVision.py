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

