import cv2
import mido
import threading
import time

class ThreadedVideoStream:
    """
    Dedicated background thread for ingesting video frames.
    Prevents OpenCV's blocking I/O from stuttering the MIDI output rate.
    """
    def __init__(self, src=0, name="Camera"):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.name = name

    def start(self):
        # Daemon thread ensures it dies when the main program closes
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

def start_multi_camera_tracker(camera_sources):
    """
    Instantiates multiple threaded streams and routes their detection 
    coordinates to separate MIDI CC channels.
    """
    print("[EPIC-STUDIO'S] Booting Multi-Threaded Vision Matrix...")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    try:
        midi_out = mido.open_output('EPIC-VISION-PORT 1')
    except Exception as e:
        print(f"Failed to open virtual MIDI port: {e}")
        return

    # Start independent video threads
    streams = []
    for idx, src in enumerate(camera_sources):
        stream = ThreadedVideoStream(src, name=f"Cam_{idx}").start()
        streams.append(stream)

    try:
        while True:
            for idx, stream in enumerate(streams):
                frame = stream.read()
                if frame is None:
                    continue
                
                # Fast grayscale conversion for the cascade model
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
                
                frame_height, frame_width = gray.shape

                # Process the most prominent face per camera
                if len(faces) > 0:
                    (x, y, w, h) = faces[0] 
                    center_x = x + (w // 2)
                    center_y = y + (h // 2)
                    
                    # Normalize to 0-127 MIDI constraints
                    cc_x = int((center_x / frame_width) * 127)
                    cc_y = int((center_y / frame_height) * 127)
                    
                    # Route Cam 0 to CC 16/17, Cam 1 to CC 18/19, etc.
                    base_cc = 16 + (idx * 2)
                    midi_out.send(mido.Message('control_change', control=base_cc, value=cc_x))
                    midi_out.send(mido.Message('control_change', control=base_cc+1, value=cc_y))
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Show local monitoring windows for each stream
                cv2.imshow(f"EPIC-STUDIO'S - {stream.name}", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        for stream in streams:
            stream.stop()
        cv2.destroyAllWindows()
        midi_out.close()

if __name__ == "__main__":
    # Pass 0 for local webcam, or standard 'rtsp://...' strings for IP streams
    camera_inputs = [0, "rtsp://username:password@192.168.1.50/stream1"] 
    start_multi_camera_tracker(camera_inputs)
