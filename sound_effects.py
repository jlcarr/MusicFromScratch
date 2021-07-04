from playsound import playsound
from scipy.io import wavfile
import sys

from MusicFromScratch import *
from instruments import *

samplerate=44100
fs = 261.63


# crash
s = synth(bpm=60)

note_envelope = envelope(attack=0.1, decay=2, sustain=0, release=0, decay_func=lambda x: np.exp(-12*x))
osc = oscillator(shape='whitenoise', note_envelope=note_envelope)
sos = signal.butter(2, 2*2*fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
s.add_oscillator(osc)

data = s.play_notes(fs, hold=2)


data *= np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("crash.wav", samplerate, data.astype(np.int16))
playsound('crash.wav')


# goal
key = 'D'
degree = 'vi'
s = pluck_lead(bpm=120, fs=fs, samplerate=samplerate)


music = gen_progression(key=key, degree=degree, octave=5, time=0, hold=4, arpeggio=1/64)
#music += [{**note, 'time':note['time']+0.5} for i,note in enumerate(music)]
data = s.play_song(music)


data *= 0.8*np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("goal.wav", samplerate, data.astype(np.int16))
playsound('goal.wav')
