import subprocess
from flask import Flask, request, send_file, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
from music21 import converter, midi
from music21.instrument import instrumentFromMidiProgram
import shutil

# Init Flask app
app = Flask(
    __name__,
    template_folder='templates',  # HTML templates
    static_folder='static'        # Static files like CSS
)

# Configuration
BASE_DIR       = Path(__file__).parent
OMR_BIN  = BASE_DIR / "omr" / "bin" / "audiveris.bat"  # OMR engine
SOUNDFONT_PATH = BASE_DIR / "soundfont" / "FluidR3_GM.sf2"         # Soundfont for rendering
UPLOAD_FOLDER  = BASE_DIR / "uploads"                              # Uploaded files
OUTPUT_FOLDER  = BASE_DIR / "output"                               # Output files
ALLOWED_EXTS   = {'png', 'jpg', 'jpeg', 'pdf'}                     # Allowed input types

# Clearing folder
def clear_folder(folder: Path):
    for item in folder.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except Exception as e:
            print(f"Error deleting {item}: {e}")

for d in (UPLOAD_FOLDER, OUTPUT_FOLDER):
    d.mkdir(exist_ok=True)
    clear_folder(d)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS

# Routes

# Home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Upload handler
@app.route('/upload', methods=['POST'])
def upload():
    # Validate file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid filename or extension'}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    upload_path = UPLOAD_FOLDER / filename
    file.save(upload_path)

    # Prepare output folder
    base = upload_path.stem
    session_out = OUTPUT_FOLDER / base
    session_out.mkdir(exist_ok=True)

    # Extracting MusicXML
    cmd = [
        str(OMR_BIN),
        '-batch', '-export',
        '-output', str(session_out),
        str(upload_path)
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Audiveris failed', 'details': e.stderr.strip()}), 500

    # Find MusicXML output
    mxl_path = None
    for ext in ('mxl', 'xml'):
        candidate = session_out / f"{base}.{ext}"
        if candidate.exists():
            mxl_path = candidate
            break
    if not mxl_path:
        return jsonify({'error': 'No MusicXML file produced'}), 500

    # Convert to MIDI with selected instrument
    score = converter.parse(str(mxl_path))
    try:
        prog = int(request.form.get('instrument', 0))  # Get selected instrument
    except ValueError:
        prog = 0
    instr = instrumentFromMidiProgram(prog)
    for part in score.parts:
        part.insert(0, instr)  # Insert instrument into score

    # Save as MIDI file
    midi_path = session_out / f"{base}.mid"
    mf = midi.translate.music21ObjectToMidiFile(score)
    mf.open(str(midi_path), 'wb')
    mf.write()
    mf.close()

    # Convert MIDI to WAV
    wav_path = session_out / f"{base}.wav"
    cmd_wav = [
        "fluidsynth",
        "-ni",
        "-F", str(wav_path),
        str(SOUNDFONT_PATH),
        str(midi_path)
    ]
    try:
        subprocess.run(cmd_wav, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'FluidSynth failed', 'details': e.stderr}), 500

    # Redirect to download page
    return redirect(url_for('upload_result', filename=wav_path.name, subdir=base))

# Result page
@app.route('/result')
def upload_result():
    filename = request.args.get('filename')
    subdir = request.args.get('subdir')
    if not filename or not subdir:
        return redirect(url_for('index'))
    return render_template('result.html', filename=filename, subdir=subdir)

# WAV file download
@app.route('/download/<subdir>/<filename>')
def download_file(subdir, filename):
    file_path = OUTPUT_FOLDER / subdir / filename
    if file_path.exists():
        return send_file(file_path, mimetype='audio/wav')
    return "File not found", 404

# Start Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
