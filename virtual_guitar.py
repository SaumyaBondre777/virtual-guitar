import cv2
import mediapipe as mp
import numpy as np
import winsound  #ponytail: Windows native audio, no cross-platform upgrade needed yet

class VirtualGuitar:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        #ponytail: single hand, confidence 0.5 - global settings, not per-hand tuning
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

        # 3 chord patterns: G, C, D major (finger indices up)
        #ponytail: 3 chords only, upgrade to full chord set later
        self.chords = {
            'G': [0, 1, 1, 1, 0],   # index, middle, ring up
            'C': [0, 1, 0, 1, 0],   # index and ring up
            'D': [0, 1, 0, 0, 0]    # index only
        }

        # String mapping: 6 strings mapped to hand width
        #ponytail: divide width by 7 zones, no calibration - upgrade to position mapping later
        self.strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']

    def fingers_up(self, landmarks):
        """Detect which fingers are up using tip/MCP comparison."""
        #ponytail: tip/MCP only, not full 21-landmark analysis
        fingers = []
        # Thumb - compare tip (4) with IP joint (3)
        if landmarks[self.tip_ids[0]].x < landmarks[self.tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers - compare tip with PIP joint (landmark -2)
        for id in range(1, 5):
            if landmarks[self.tip_ids[id]].y < landmarks[self.tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def detect_chord(self, fingers):
        """Match finger pattern to chord name."""
        #ponytail: 3 chords only, finger-pattern matching
        for chord_name, pattern in self.chords.items():
            if fingers == pattern:
                return chord_name
        return None

    def run(self):
        print("Virtual Guitar - press 'q' to quit")
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
                        #ponytail: simple beep feedback - frequency mapped to chord, upgrade to chord samples later
                        frequency = { 'G': 392, 'C': 294, 'D': 330 }[chord]  # musical notes
                        duration = 0.1  # seconds
                        winsound.Beep(frequency, int(duration * 1000))

            # Draw minimal overlay - just chord text and string labels
            #ponytail: single composite operation per frame, no double-buffering
            h, w, _ = img.shape
            cv2.rectangle(img, (0, 0), (w, 40), (30, 30, 30), -1)
            cv2.putText(img, chord_text, (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Draw string labels at top
            for i, string in enumerate(self.strings):
                x = int((i + 1) * w / 7)
                cv2.putText(img, string, (x, 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # Non-blocking check for 'q' - will work if GUI is available
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    guitar = VirtualGuitar()
    guitar.run()