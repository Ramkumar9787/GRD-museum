import React, { useState } from 'react';
import './App.css';

function App() {
  const [buttonPressed1, setButtonPressed1] = useState(false);
  const [buttonPressed2, setButtonPressed2] = useState(false);
  const [imageKey1, setImageKey1] = useState(0);
  const [imageKey2, setImageKey2] = useState(0);

  const startRecording = async (noteNumber) => {
    const response = await fetch('http://127.0.0.1:5000/api/record_note', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ note: noteNumber }),
    });

    if (response.ok) {
      if (noteNumber === 1) {
        setImageKey1(prevKey => prevKey + 1);
        setButtonPressed1(true);  // Toggle the state to trigger a refresh
      } else if (noteNumber === 2) {
        setImageKey2(prevKey => prevKey + 1);
        setButtonPressed2(true);
      }
    } else {
      console.error('Failed to record note.');
    }
  };

  return (
    <div>
      <h1>Click on record when ready</h1>
      <div style={{ display: 'flex', flexDirection: 'row' }}>
        <div>
          <button onClick={() => startRecording(1)} >
            Record note 1
          </button>
          <div>
            {buttonPressed1 && <img src={`static/recording_1_time_amplitude.png?key=${imageKey1}`} alt="Time-Amplitude Graph" />}
          </div>
          <div>
            {buttonPressed1 && <img src={`static/recording_1_frequency.png?key=${imageKey1}`} alt="Frequency Spectrum" />}
          </div>
        </div>
        <div>
          <button onClick={() => startRecording(2)} >
            Record note 2
          </button>
          <div >
            {buttonPressed2 && <img src={`static/recording_2_time_amplitude.png?key=${imageKey2}`} alt="Time-Amplitude Graph" />}
          </div>
          <div>
            {buttonPressed2 && <img src={`static/recording_2_frequency.png?key=${imageKey2}`} alt="Frequency Spectrum" />}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
