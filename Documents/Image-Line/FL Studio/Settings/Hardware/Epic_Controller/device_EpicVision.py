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
