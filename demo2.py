from playsound import playsound
from scipy.io import wavfile
import sys

from instruments import *
from music import *


key = 'C'
samplerate=44100
fs = 261.63
bpm = 120
s = synth_pad(bpm=bpm, fs=fs, samplerate=samplerate)


music = []
for (bar,(degree,inversion)) in enumerate([('vi',2), ('ii',0), ('V',1), ('I',0)]*2):
	t = 2*4*bar
	music += gen_progression(key=key, degree=degree, inversion=inversion, time=t, hold=4)

data = s.play_song(music)


t_tot = 8
s = pluck_lead(bpm=bpm, fs=fs, samplerate=samplerate)

music = []
for (bar,(degree,inversion)) in enumerate([('vi',2), ('ii',0), ('V',1), ('I',0)]):
	t = 2*4*bar
	music += gen_progression(key=key, degree=degree, octave=5, time=t, hold=1, arpeggio=0.25)

music += [{**note, 'time':note['time']+2} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+2*16} for i,note in enumerate(music)]
lead_data = s.play_song(music)
data[:lead_data.size] += 0.8*lead_data


data *= 0.8*np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
