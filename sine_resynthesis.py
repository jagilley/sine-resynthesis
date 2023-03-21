import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt

def sine(freq, amp, phase=0, length=1, rate=48000):
    length = int(length * rate)
    factor = float(freq) * (np.pi * 2) / rate
    return np.sin(np.arange(length) * factor + phase) * amp

def peak_picking(signal, threshold):
    peaks = []
    for i in range(1, len(signal)-1):
        if signal[i] > signal[i-1] and signal[i] > signal[i+1] and signal[i] > threshold:
            peaks.append(i)
    return peaks

def audio_to_sine_waves(audio_file, threshold=0.1):
    y, sr = librosa.load(audio_file, mono=False)
    y = y[0] # take only left channel
    S = librosa.stft(y)
    freqs = librosa.fft_frequencies(sr=sr)
    times = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr)
    
    magnitude_spectrum = np.abs(S)
    
    sine_waves = []
    
    peak_indices = peak_picking(magnitude_spectrum[:, 4], threshold)

    for i in peak_indices:
        sine_wave = {'frequency': freqs[i], 'amplitudes': np.abs(S[i]), 'phases': np.angle(S[i]), 'times': times}
        sine_waves.append(sine_wave)

    return sine_waves

def synthesize_sines(sine_waves):
    sines = [sine(sine_wave['frequency'], sine_wave['amplitudes'][4]/750, length=3, rate=48000, phase=sine_wave['phases'][0]) for sine_wave in sine_waves]
    sines = np.array(sines)
    sines = np.sum(sines, axis=0)
    return sines

if __name__=="__main__":
    target_file = 'audio/triangle.wav'
    sine_waves = audio_to_sine_waves(target_file, threshold=0.1)
    
    for sine_wave in sine_waves:
        print(sine_wave['frequency'], max(sine_wave['amplitudes']))
    
    sines = synthesize_sines(sine_waves)
    sf.write(target_file.replace('.wav', '_resynth.wav'), sines, 48000)