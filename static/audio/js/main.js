// DOM Elements
const ttsForm = document.getElementById('tts-form');
const textArea = document.getElementById('text');
const engineSelect = document.getElementById('engine');
const voiceSelect = document.getElementById('voice');
const speedInput = document.getElementById('speed');
const speedValue = speedInput.nextElementSibling;
const convertBtn = document.getElementById('convert-btn');
const resultCard = document.getElementById('result-card');
const textPreview = document.getElementById('text-preview');
const audioPlayer = document.getElementById('audio-player');
const downloadBtn = document.getElementById('download-btn');
const loadingElement = document.getElementById('loading');
const navLinks = document.querySelectorAll('nav a');
const sections = document.querySelectorAll('.section');

// API Endpoints
const API_BASE = '/api/tts';
const API_VOICES = `${API_BASE}/voices`;
const API_TTS = `${API_BASE}`;

// State
let currentAudioUrl = null;
let voicesData = [];

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    loadVoices();
    setupEventListeners();
});

// Load available voices from API
async function loadVoices() {
    try {
        const response = await fetch(API_VOICES);
        if (!response.ok) {
            throw new Error('Failed to load voices');
        }
        
        voicesData = await response.json();
        updateVoiceOptions();
        
        // Set default engine to edge-tts
        engineSelect.value = 'edge-tts';
        updateVoiceOptions();
    } catch (error) {
        console.error('Error loading voices:', error);
        showError('Failed to load voices. Please reload the page.');
    }
}

// Update voice options based on selected engine
function updateVoiceOptions() {
    const selectedEngine = engineSelect.value;
    const engineVoices = voicesData.find(item => item.engine === selectedEngine);
    
    // Clear existing options
    voiceSelect.innerHTML = '';
    
    if (engineVoices && engineVoices.voices.length > 0) {
        // Sort voices by locale and name
        const sortedVoices = [...engineVoices.voices].sort((a, b) => {
            // First sort by locale (if available)
            if (a.locale && b.locale) {
                if (a.locale !== b.locale) {
                    return a.locale.localeCompare(b.locale);
                }
            }
            // Then by name
            return a.name.localeCompare(b.name);
        });
        
        // Add options
        sortedVoices.forEach(voice => {
            const option = document.createElement('option');
            option.value = voice.id;
            
            // Format display name
            let displayName = voice.name;
            if (voice.locale) {
                displayName += ` (${voice.locale})`;
            }
            
            option.textContent = displayName;
            voiceSelect.appendChild(option);
        });
        
        // Select a default English voice if available
        if (selectedEngine === 'edge-tts') {
            const enUsVoice = sortedVoices.find(v => v.id.startsWith('en-US'));
            if (enUsVoice) {
                voiceSelect.value = enUsVoice.id;
            }
        }
    } else {
        // Add a placeholder if no voices are available
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No voices available';
        voiceSelect.appendChild(option);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    ttsForm.addEventListener('submit', handleFormSubmit);
    
    // Engine change
    engineSelect.addEventListener('change', updateVoiceOptions);
    
    // Speed slider
    speedInput.addEventListener('input', () => {
        speedValue.textContent = speedInput.value;
    });
    
    // Download button
    downloadBtn.addEventListener('click', handleDownload);
    
    // Navigation
    // Update active class on nav links
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            link.classList.add('active');
            
            // Show the targeted section
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
        });
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form values
    const text = textArea.value.trim();
    const engine = engineSelect.value;
    const voice = voiceSelect.value;
    const speed = parseFloat(speedInput.value);
    
    // Validate form
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    // Show loading state
    setLoading(true);
    
    // Create request body
    const requestBody = {
        text,
        engine,
        voice,
        speed,
        language: voice && voice.includes('-') ? voice.split('-')[0] : 'en'
    };
    
    try {
        // Send API request
        const response = await fetch(API_TTS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate speech');
        }
        
        const data = await response.json();
        
        // Display results
        displayResult(data);
    } catch (error) {
        console.error('Error generating speech:', error);
        showError(error.message || 'Failed to generate speech');
    } finally {
        setLoading(false);
    }
}

// Display result
function displayResult(data) {
    // Show result card
    resultCard.style.display = 'block';
    
    // Update text preview
    textPreview.textContent = data.text_preview;
    
    // Update audio player
    currentAudioUrl = data.audio_url;
    audioPlayer.src = currentAudioUrl;
    audioPlayer.load();
    
    // Scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth' });
}

// Handle download
function handleDownload() {
    if (!currentAudioUrl) return;
    
    // Create a temporary link
    const link = document.createElement('a');
    link.href = currentAudioUrl;
    link.download = `speech-${Date.now()}.mp3`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Show loading state
function setLoading(isLoading) {
    if (isLoading) {
        loadingElement.style.display = 'flex';
        convertBtn.disabled = true;
    } else {
        loadingElement.style.display = 'none';
        convertBtn.disabled = false;
    }
}

// Show error message
function showError(message) {
    alert(message);
}