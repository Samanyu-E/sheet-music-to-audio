<p align="center">  
  <img src="docs/logo.png" alt="Sheet Music to Audio Logo" width="200"/>  
</p>  

<h1 align="center">Sheet Music to Audio</h1>  

<p align="center">  
  <a href="https://github.com/samanyu-e/sheet-music-to-audio/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/samanyu-e/sheet-music-to-audio/ci.yml?branch=main" alt="CI Status">
  </a> 
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  </a>
</p>  

---

<p align="center">  
  <img src="docs/demo.gif" alt="Demo" width="75%"/>  
</p>  

**Sheet Music to Audio** lets you upload an image or one page PDF of sheet music, choose a MIDI instrument, and download a high-quality WAV file—all via a web interface.

---

## 🔑 Features

* **Optical Music Recognition**
  Uses **Audiveris** to convert images/PDFs into MusicXML.

* **MIDI Generation**
  Parses MusicXML with **music21**, inserts your chosen General MIDI instrument.

* **Audio Synthesis**
  Renders `.wav` via **FluidSynth** and the **FluidR3\_GM** SoundFont.

* **Instrument Picker**
  Choose from **128** General MIDI instruments (piano, strings, brass, leads…).

* **Responsive UI**
  Mobile-friendly upload form and download page.

---

## 🚀 Quick Start

**Clone the repo**

```
git clone https://github.com/Samanyu-E/sheet-music-to-audio.git
cd sheet-music-to-audio
```

**Create & activate virtualenv**

```
python -m venv venv
```
* macOS/Linux
  ```
  source venv/bin/activate
  ```
* Windows
  ```
  venv\Scripts\activate
  ```

**Install Python dependencies**

```
pip install -r requirements.txt
```

Verify external tools:

* Audiveris CLI in `./audiveris/bin/audiveris.bat`
* FluidSynth installed on your system
* `FluidR3_GM.sf2` in `./soundfont/`

**Run the web server**

```
python main.py
```

Open your browser at
[http://localhost:8000](http://localhost:8000)

---

## 🗂 Project Structure

```
sheet-music-to-audio/
├── audiveris/bin/audiveris.bat    # OMR engine  
├── soundfont/FluidR3_GM.sf2       # General MIDI SoundFont  
├── templates/                     # HTML views  
│   ├── index.html                 # Upload & instrument form  
│   └── result.html                # Download page  
├── static/                        # CSS/JS assets  
├── uploads/                       # (gitignored) user uploads  
├── output/                        # (gitignored) generated WAVs  
├── main.py                        # Flask backend  
├── requirements.txt               # Python dependencies  
├── LICENSE                        # MIT license for this repo  
└── NOTICE                         # Third-party attribution  
```

---

## 📜 License & Attribution

* **This repository**: MIT License © 2025 Samanyu Earna
* **Audiveris**: Apache License 2.0
* **FluidR3 GM SoundFont**: CC BY-SA 3.0

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feat/your-feature`
5. Open a Pull Request

