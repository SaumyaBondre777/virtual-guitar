# Virtual Guitar Project - Plan (ponytail: MVP-focused)

## Architecture (ponytail: minimal, 3 components only)

### 1. Hand Tracking (ponytail: finger states, not full landmark pipeline)
- OpenCV webcam capture (ponytail: 640x480, default backend)
- MediaPipe Hands: one hand, confidence 0.5 (ponytail: global settings, not per-hand tuning)
- Finger-up detection using 4 landmarks (tip + pip/mcp) (ponytail: ceiling - thumb geometry differs, upgrade per-hand later)

### 2. Fretboard Mapping (ponytail: 2 zones, not per-fret positions)
- Hand x-position maps to 6 strings (ponytail: divide width by 6, no calibration)
- Finger up/down maps to chord zone (ponytail: 3 zones = G/C/D, upgrade to full fretboard later)
- Binary pressed/unpressed state (ponytail: ceiling - no velocity/pressure tracking)

### 3. Chord Display (ponytail: text only, no audio)
- 3 chord patterns matched to finger counts (ponytail: G=3 fingers, C=3 fingers diff config, D=2 fingers)
- cv2.putText overlay (ponytail: ceiling - no anti-aliased fonts, no scrolling history)
- Webcam feed with overlay (ponytail: single composite operation per frame)

## Workflow (ponytail: 4 steps, not 8)
1. Read webcam frame (ponytail: ignore failures, just skip)
2. Process with MediaPipe Hands (ponytail: results.multi_hand_landsmarks)
3. Determine finger states + chord name (ponytail: pattern matching table)
4. Render overlay + show window (ponytail: cv2.imshow, waitKey(1))

## Success Criteria (ponytail: 3 bars, not 5)
- Real-time hand tracking (ponytail: <200ms latency acceptable for MVP)
- Recognize 3 basic chords (ponytail: ceiling - upgrade to 5+ later)
- Visual fretboard responds to hand (ponytail: upgrade to position mapping)
- Program runs stable 5min+ (ponytail: memory leak check later)

## Technology Stack (ponytail: 3 libs, not 5)
- Python (ponytail: 3.10+, no version pinning overhead)
- opencv-python + mediapipe (ponytail: pip install, no source build)
- No audio library (ponytail: skip until Phase 2, upgrade when needed)