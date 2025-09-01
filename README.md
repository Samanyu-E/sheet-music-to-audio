

<h1 align="center">Sheet Music to Audio</h1>  

<p align="center">  
  <img src="docs/demo.gif" alt="Demo" width="75%"/>  
</p>  

**Sheet Music to Audio** lets you upload an image or one page PDF of sheet music, choose a MIDI instrument, and download a high-quality WAV file via a web interface.

---

## 🔑 Features

* **Flask Web Frontend**  
  Simple and intuitive web interface for uploading sheet music and downloading audio.

* **Optical Music Recognition**  
  Uses **Audiveris** to convert images/PDFs into MusicXML.

* **Instrument Picker**  
  Choose from **128** General MIDI instruments (piano, strings, brass, leads…) to play music in

* **MIDI Generation**  
  Parses MusicXML with **music21**, inserts your chosen General MIDI instrument.

* **Audio Synthesis**  
  Renders `.wav` via **FluidSynth** and the **FluidR3_GM** SoundFont

---

## 🚀 Starting with git clone

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

**Verify external tools:**

* Audiveris CLI in `./omr/bin/audiveris.bat`
* pyfluidSynth installed on your system
* `FluidR3_GM.sf2` in `./soundfont/`
  * Note: Due to file size limitations, the FluidR3_GM.sf2 file is not included in this repository.
  * Download [FluidR3_GM.sf2](https://member.keymusician.com/Member/FluidR3_GM/index.html) and place it in `./soundfont/` 

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
├── omr/bin/audiveris.bat          # OMR engine  
├── soundfont/FluidR3_GM.sf2       # General MIDI SoundFont  
├── templates/                     # HTML pages  
│   ├── index.html                 # Upload & instrument form  
│   └── result.html                # Download page  
├── work-in-prog/                  # Work in progress
│   ├── img-enhance.py             # Working on image enhancement  
│   └── PROGESS                    # Description
├── uploads/                       # (gitignored) user uploads  
├── output/                        # (gitignored) generated WAVs  
├── main.py                        # Flask backend  
├── requirements.txt               # Python dependencies
├── README                         # Prgect Description
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

