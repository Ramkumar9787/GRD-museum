from flask import Flask, jsonify, request
import sounddevice as sd
import numpy as np
import os
import matplotlib.pyplot as plt
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Constants
samplerate = 44100 * 4  # Adjust as needed
duration = 3  # Adjust as needed

# Endpoint for recording notes
@app.route('/api/record_note', methods=['POST'])
def record_note():
    note_number = request.json.get('note')

    if note_number == 1:
        filename = 'recording_1'
    elif note_number == 2:
        filename = 'recording_2'
    else:
        return jsonify({'error': 'Invalid note number'}), 400

# Record audio
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate, channels=1, dtype='int16')
    sd.wait()

    # Convert audio data to float
    audio_data_float = audio_data.flatten() / np.iinfo(np.int16).max

    # Plot time-amplitude graph
    plt.figure(figsize=(10,5))
    time = np.arange(len(audio_data_float)) / samplerate
    plt.plot(time, audio_data_float, color='b', label='Audio')
    plt.title(f'Time-Amplitude Graph - Note {note_number}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    img_path_time_amplitude = f'static/{filename}_time_amplitude.png'
    plt.savefig(img_path_time_amplitude)
    plt.clf()

    # Plot frequency spectrum
    n = len(audio_data_float)
    k = np.arange(n)
    T = n / samplerate
    frq = k / T
    frq = frq[:n // 2]
    Y = np.fft.fft(audio_data_float) / n
    Y = Y[:n // 2]

    plt.plot(frq, abs(Y), 'r')
    plt.title(f'Frequency Spectrum - Note {note_number}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 5000)

    img_path_frequency_spectrum = f'static/{filename}_frequency.png'
    plt.savefig(img_path_frequency_spectrum)
    plt.clf()

    # Return the file paths
    return jsonify({
        'time_amplitude': f'static/{filename}_time_amplitude.png',
        'frequency_spectrum': f'static/{filename}_frequency.png'
    })

if __name__ == '__main__':
    app.run(debug=True)
