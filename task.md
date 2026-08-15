# Virtual Guitar Project - Task List (ponytail: minimized for MVP)

## Core Tasks - Minimum Viable Product

### 1. Environment Setup
- Create venv: `python -m venv .venv` (ponytail: global lock, specific Python 3.11+)
- Install deps: `pip install opencv-python mediapipe` (ponytail: pip install only)
- Configure webcam access (ponytail: default 0 index, skip camera selection UI)

### 2. Hand Tracking Module (ponytail: finger states only, not full 21-landmark analysis)
- MediaPipe Hands initialization (ponytail: max_num_hands=1, min_detection_confidence=0.5)
- Finger-up/down detection using tip/MCP landmarks (ponytail: thumb uses IP joint, others use pip)
- Single-hand tracking (ponytail: right-hand only, skip left-hand mirroring)

### 3. Virtual Fretboard (ponytail: 2 zones only - "fret zone" vs "open string zone")
- 6 strings mapped to hand width (ponytale: index finger position = string selection)
- 3 chord zones (ponytail: G, C, D major positions based on finger count)
- No fret number tracking (ponytail: binary fretboard: pressed/unpressed)

### 4. Chord Recognition (ponytail: 3 chords only, finger-pattern matching)
- G major: 3 fingers up (ponytail: pattern match on index/middle/ring)
- C major: 3 fingers up different position (ponytail: same count, different landmark config)
- D major: 2 fingers up (ponytail: simplest check)
- Chord display: text overlay (ponytail: no fancy UI, just cv2.putText)

### 5. Visual Feedback (ponytail: minimal overlay)
- Webcam feed background (ponytale: 640x480, no resize logic)
- Fretboard lines drawn once (ponytail: not re-drawn every frame if unchanged)
- Finger indicators (ponytail: circles at tip landmarks only)
- Current chord name (ponytail: single line text, no background box)

### 6. Exit Handling
- Press 'q' to quit (ponytail: simplest key check, no menu system)

## Milestones (ponytail: 2 phases instead of 5)
- Phase 1: Hand tracking + chord display (ponytail: no audio, no strumming)
- Phase 2: Add visual fretboard mapping (ponytail: upgrade from binary zones)