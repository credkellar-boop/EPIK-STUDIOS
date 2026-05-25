import cv2
import mido
import time

def start_av_vision_tracker(camera_index_or_stream=0):
    """
    Captures live video/RTSP streams, tracks facial movement, 
    and outputs the normalized data as MIDI CC messages to control DAW A/V.
    """
    print("[EPIC-STUDIO'S] Booting Computer Vision MIDI Bridge...")
    
    # Initialize the Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(camera_index_or_stream)
    
    # Open a virtual MIDI output port (requires loopMIDI on Windows or IAC Driver on Mac)
    try:
        midi_out = mido.open_output('EPIC-VISION-PORT 1')
    except Exception as e:
        print(f"Failed to open MIDI port. Ensure a virtual MIDI port is created: {e}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        frame_height, frame_width = gray.shape

        for (x, y, w, h) in faces:
            # Calculate the center of the detected face
            center_x = x + (w // 2)
            center_y = y + (h // 2)
            
            # Normalize X and Y coordinates to MIDI CC range (0 to 127)
            midi_cc_x = int((center_x / frame_width) * 127)
            midi_cc_y = int((center_y / frame_height) * 127)
            
            # CC 16 controls Audio (e.g., Filter Cutoff)
            midi_out.send(mido.Message('control_change', control=16, value=midi_cc_x))
            
            # CC 17 controls Visuals (e.g., ZGameEditor Camera X-Axis)
            midi_out.send(mido.Message('control_change', control=17, value=midi_cc_y))
            
            # Draw a visual box for local monitoring
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            break # Track primary subject only to avoid MIDI crossing
            
        cv2.imshow('EPIC-STUDIO\'S Vision Tracker', frame)
        
        # Press 'q' to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    midi_out.close()

if __name__ == "__main__":
    # Can pass an RTSP stream URL here instead of 0 for live network monitoring
    start_av_vision_tracker(0) 
