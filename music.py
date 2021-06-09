from playsound import playsound
from scipy.io import wavfile
import sys

from synth import *


def gen_chord(name, octave=4, inversion=0, hold=1, time=0):
	root = name[0]
	scale = [0,2,4,5,7,9,11] # accumulate major scale [2,2,1,2,2,2,1]
	root = scale[ord(root) - ord('C')] 
	mod = name[1:]

	root = 12*(octave+1) + root

	chord = []
	if mod == '':
		chord = [0,4,7]
	elif mod == 'm':
		chord = [0,3,7]

	if inversion == 1:
		chord[1],chord[2] = chord[1]-12,chord[2]-12
	if inversion == 2:
		chord[2] = chord[2]-12

	return [{'pitch':root+note, 'time':time, 'hold':hold} for note in chord]


def gen_progression(key='C', degree='I', octave=4, time=0, hold=1, arpeggio=False):
	scale = [0,2,4,5,7,9,11] # accumulate major scale [2,2,1,2,2,2,1]
	degrees = {'I':0, 'IV': 3, 'V': 4}
	degree = scale[degrees[degree]]
	name = chr((ord(key) + degree - ord('A')) % 7 + ord('A'))
	print(name)

#gen_progression()
#sys.exit()

samplerate=44100
fs = 261.63
s = synth(bpm=100)

note_envelope = envelope(attack=2., decay=0.0, sustain=1.0, release=3.)
osc = oscillator(shape='sawtooth', note_envelope=note_envelope, voices=5, detune = 0.01)
sos = signal.butter(2, fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
#impulse_response = np.exp(-np.linspace(0., 20., 1*samplerate))
#osc.add_reverb(impulse_response)
#impulse_response = np.zeros(4*samplerate)
#impulse_response[::int(samplerate/4)] = 1
#impulse_response *= np.exp(-np.linspace(0.,10.,impulse_response.size))
#osc.add_reverb(impulse_response)
s.add_oscillator(osc)

note_envelope = envelope(attack=1.5, decay=0.0, sustain=1.0, release=3)
osc = oscillator(shape='whitenoise', amp=0.03, note_envelope=note_envelope)
sos = signal.butter(2, 2*2*fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
s.add_oscillator(osc)

music = []
music += gen_chord('Am', inversion=2, time=0, hold=4)
music += gen_chord('Dm', time=4, hold=4)
music += gen_chord('G', inversion=1, time=8, hold=4)
music += gen_chord('C', time=12, hold=4)
music += [{**note, 'time':note['time']+16} for i,note in enumerate(music)]
print(music)

data = s.play_song(music)


t_tot = 8
s = synth(bpm=100)

note_envelope = envelope(attack=0.01, decay=1.5, sustain=0.0, decay_func=lambda x: np.exp(-8*x), release=0)
#note_envelope = envelope(attack=0, decay=0, sustain=1.0, release=0)
osc = oscillator(shape='sine', note_envelope=note_envelope)
impulse_response = np.zeros(samplerate)
impulse_response[::int(1*samplerate/64)] = 1
impulse_response *= np.exp(-np.linspace(0,4,impulse_response.size))
impulse_response *= np.linspace(1,0,impulse_response.size)
#osc.add_reverb(impulse_response)
s.add_oscillator(osc)

music = []
music += gen_chord('Am', octave=5, time=0, hold=1)
music += gen_chord('Dm', octave=5, time=4, hold=1)
music += gen_chord('G', octave=5, time=8, hold=1)
music += gen_chord('C', octave=5, time=12, hold=1)
music = [{**note, 'time':note['time']+2*(i%3)/4}  for i,note in enumerate(music)]
#music += [{**note, 'time':note['time']+1} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+2} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+16} for i,note in enumerate(music)]
lead_data = s.play_song(music)
data[:lead_data.size] += lead_data









data *= np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
