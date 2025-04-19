document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const convertBtn = document.getElementById('convert-btn');
    const clearBtn = document.getElementById('clear-btn');
    const downloadBtn = document.getElementById('download-btn');
    const audioContainer = document.getElementById('audio-container');
    const audioPlayer = document.getElementById('audio-player');
    const statusDiv = document.getElementById('status');
    const engineSelect = document.getElementById('engine-select');
    const voiceSelect = document.getElementById('voice-select');
    const speedSlider = document.getElementById('speed-slider');
    const pitchSlider = document.getElementById('pitch-slider');
    const volumeSlider = document.getElementById('volume-slider');
    const speedValue = document.getElementById('speed-value');
    const pitchValue = document.getElementById('pitch-value');
    const volumeValue = document.getElementById('volume-value');

    // Load voices when engine changes
    engineSelect.addEventListener('change', loadVoices);
    
    // Update slider value displays
    speedSlider.addEventListener('input', () => speedValue.textContent = speedSlider.value);
    pitchSlider.addEventListener('input', () => pitchValue.textContent = pitchSlider.value);
    volumeSlider.addEventListener('input', () => volumeValue.textContent = volumeSlider.value);

    // Clear button functionality
    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        audioContainer.classList.add('hidden');
        showStatus('Text cleared', 'success');
    });

    // Download button functionality
    downloadBtn.addEventListener('click', () => {
        const audioUrl = audioPlayer.src;
        if (audioUrl) {
            const link = document.createElement('a');
            link.href = audioUrl;
            link.download = 'text-to-speech.mp3';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showStatus('Download started', 'success');
        }
    });

    // Load available voices
    async function loadVoices() {
        const engine = engineSelect.value;
        voiceSelect.innerHTML = '<option value="">Loading voices...</option>';
        
        try {
            const response = await fetch(`/api/tts/voices?engine=${engine}`);
            if (!response.ok) throw new Error('Failed to load voices');
            
            const data = await response.json();
            const voices = data.find(v => v.engine === engine)?.voices || [];
            
            voiceSelect.innerHTML = voices.map(voice => 
                `<option value="${voice.id}">${voice.name}${voice.locale ? ` (${voice.locale})` : ''}</option>`
            ).join('');
            
            if (voices.length === 0) {
                voiceSelect.innerHTML = '<option value="">No voices available</option>';
            }
        } catch (error) {
            console.error('Error loading voices:', error);
            voiceSelect.innerHTML = '<option value="">Error loading voices</option>';
        }
    }

    // Convert button functionality
    convertBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showStatus('Please enter some text', 'error');
            return;
        }

        try {
            // Disable button and show loading state
            convertBtn.disabled = true;
            convertBtn.innerHTML = '<span class="loading"></span> Converting...';
            showStatus('Converting text to speech...');

            // Prepare request data
            const requestData = {
                text: text,
                engine: engineSelect.value,
                language: voiceSelect.value.split('-')[0] || 'en',
                voice: voiceSelect.value,
                speed: parseFloat(speedSlider.value),
                pitch: parseFloat(pitchSlider.value),
                volume: parseFloat(volumeSlider.value)
            };

            // Call the API
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to convert text to speech');
            }

            const data = await response.json();
            
            // Update audio player
            audioPlayer.src = data.audio_url;
            audioContainer.classList.remove('hidden');
            
            showStatus('Conversion successful!', 'success');
        } catch (error) {
            console.error('Error:', error);
            showStatus('Error: ' + error.message, 'error');
        } finally {
            // Reset button state
            convertBtn.disabled = false;
            convertBtn.innerHTML = '<i class="fas fa-microphone-alt mr-2"></i>Convert to Speech';
        }
    });

    // Text input validation
    textInput.addEventListener('input', () => {
        const text = textInput.value.trim();
        if (text.length > 5000) {
            showStatus('Text is too long. Maximum 5000 characters allowed.', 'error');
            convertBtn.disabled = true;
        } else if (text.length === 0) {
            convertBtn.disabled = true;
        } else {
            convertBtn.disabled = false;
            statusDiv.textContent = '';
        }
    });

    function showStatus(message, type = '') {
        statusDiv.textContent = message;
        statusDiv.className = 'mt-4 text-center text-gray-600';
        if (type) {
            statusDiv.classList.add(type);
        }
    }

    // Initialize
    loadVoices();
    convertBtn.disabled = true;
}); 