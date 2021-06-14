from playsound import playsound
from scipy.io import wavfile
import sys

from instruments import *
from music import *


key = 'D'
samplerate=44100
fs = 261.63
bpm = 120


# Backing chords pad
s = synth_pad(bpm=bpm, fs=fs, samplerate=samplerate)

music = []
for bar,degree in enumerate(['vi', 'ii', 'V', 'I']*2):
	t = 2*4*bar
	music += gen_progression(key=key, degree=degree, octave=3, time=t, hold=4)
data = s.play_song(music)


# Lead arpeggio pluck
s = pluck_lead(bpm=bpm, fs=fs, samplerate=samplerate)

music = []
for bar,degree in enumerate(['vi', 'ii', 'V', 'I']):
	t = 2*4*bar
	music += gen_progression(key=key, degree=degree, octave=5, time=t, hold=2, arpeggio=1/4)
music += [{**note, 'time':note['time']+2} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+2*16} for i,note in enumerate(music)]
lead_data = s.play_song(music)
data[:lead_data.size] += 0.8*lead_data


data *= 0.8*np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
