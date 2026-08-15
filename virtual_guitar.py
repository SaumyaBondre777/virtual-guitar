import cv2
import mediapipe as mp
import numpy as np

class VirtualGuitar:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        
        # Chord definitions: finger patterns for G, C, D major
        # Each chord: list of which fingers are up (thumb=0, index=1, middle=2, ring=3, pinky=4)
        self.chords = {
            'G': [0, 1, 1, 1, 0],   # index, middle, ring up
            'C': [0, 1, 0, 1, 0],   # index and ring up (simplified)
            'D': [0, 1, 0, 0, 0]    # index only
        }
        
        # String mapping: 6 strings from low to high
        self.strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
        
    def fingers_up(self, landmarks):
        fingers = []
        # Thumb - compare tip (4) with IP joint (3)
        if landmarks[self.tip_ids[0]].x < landmarks[self.tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers - compare tip with PIP joint
        for id in range(1, 5):
            if landmarks[self.tip_ids[id]].y < landmarks[self.tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    def detect_chord(self, fingers):
        for chord_name, pattern in self.chords.items():
            if fingers == pattern:
                return chord_name
        return None
    
    def run(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break
            
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            
            chord_text = "No chord"
            fingers = [0, 0, 0, 0, 0]
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    fingers = self.fingers_up(hand_landmarks.landmark)
                    chord = self.detect_chord(fingers)
                    if chord:
                        chord_text = f"Chord: {chord}"
            
            # Draw simple fretboard overlay
            h, w, _ = img.shape
            cv2.rectangle(img, (0, 0), (w, 100), (30, 30, 30), -1)
            cv2.putText(img, chord_text, (10, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, "Fingers: " + str(sum(fingers)), (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Draw strings
            for i, string in enumerate(self.strings):
                x = int((i + 1) * w / 7)
                cv2.putText(img, string, (x, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            cv2.imshow('Virtual Guitar', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    guitar = VirtualGuitar()
    guitar.run()