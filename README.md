# sheet-music-to-audio
- First uploaded: 06/22/2025
- Last updated:   06/25/2025
<p align="center">
  <img src="docs/logo.png" alt="Sheet Music to Audio Logo" width="120" />
  <h1 align="center">Sheet Music to Audio</h1>
  <p align="center"><strong>Convert sheet-music images into playable audio</strong></p>
  <p align="center">
    <a href="https://github.com/your-username/sheet-music-to-audio/actions"><img src="https://img.shields.io/github/actions/workflow/status/your-username/sheet-music-to-audio/ci.yml?branch=main" alt="CI Status"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  </p>
</p>

---

![Demo](docs/demo.gif)  
*Upload a photo or PDF of your score, pick an instrument, and download the rendered audio.*

---

## 🚀 Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/your-username/sheet-music-to-audio.git
cd sheet-music-to-audio

# 2. Create & activate venv
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. Install Python deps
pip install -r requirements.txt

# 4. Ensure external tools:
#    • Audiveris CLI in ./audiveris/bin/audiveris.bat
#    • FluidSynth on your system & place FluidR3_GM.sf2 in ./soundfont/

# 5. Run the app
python main.py

# 6. Open browser at:
http://localhost:8000
💡 Features
Optical Music Recognition
Uses Audiveris to convert images/PDFs into MusicXML.

MIDI Generation
Parses MusicXML with music21 and applies your chosen MIDI instrument.

Audio Synthesis
Renders .wav audio via FluidSynth and a General MIDI SoundFont.

Instrument Picker
Choose from 128 General MIDI instruments (piano, strings, brass, etc.).

Clean UI
Responsive upload form and download page.

🗂 Project Structure
bash
Copy
Edit
sheet-music-to-audio/
├── audiveris/bin/audiveris.bat    # OMR engine
├── soundfont/FluidR3_GM.sf2       # GM SoundFont
├── main.py                        # Flask backend
├── templates/
│   ├── index.html                 # Upload form
│   └── result.html                # Download page
├── static/                        # (optional) CSS/JS
├── uploads/                       # (gitignored) user uploads
├── output/                        # (gitignored) generated audio
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT license
└── NOTICE                         # Third-party attribution
📜 License & Attribution
This repo: MIT License © 2025 Samanyu Earna

Audiveris: Apache License 2.0

FluidR3 GM SoundFont: CC BY-SA 3.0

See LICENSE and NOTICE for details.

🤝 Contributing
Fork & clone

Create a branch: git checkout -b feat/your-feature

Commit changes & push

Open a Pull Request
