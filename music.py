from playsound import playsound
from scipy.io import wavfile
import sys

from synth import *


scale_types = {
	'major': [0,2,4,5,7,9,11], # accumulate major scale [2,2,1,2,2,2,1]
	'minor': [0,2,3,5,7,8,10]
}
degree_types = {'I':0, 'ii':1, 'iii': 2, 'IV': 3, 'V': 4, 'vi':5, 'vii':6}

def gen_chord(name, octave=4, inversion=0, hold=1, time=0, arpeggio=0):
	root = name[0]
	root = scale_types['major'][ord(root) - ord('C')] 
	root += 1 if '#' in name else 0
	mod = name[2:] if '#' in name else name[1:]
	print(root, mod)

	root = 12*(octave+1) + root

	chord = []
	if mod == '':
		chord = [0,4,7]
	elif mod == 'm':
		chord = [0,3,7]
	elif mod == 'dim':
		chord = [0,3,6]
	elif mod == 'aug':
		chord = [0,4,8]

	if inversion == 1:
		chord[1],chord[2] = chord[1]-12,chord[2]-12
	if inversion == 2:
		chord[2] = chord[2]-12

	time += 0 if arpeggio >=0 else 3*hold
	return [{'pitch':root+note, 'time':time + arpeggio*hold*i, 'hold':hold} for i,note in enumerate(chord)]


def gen_progression(key='C', degree='I', octave=4, inversion=0, time=0, hold=1, arpeggio=0):
	minor = not 'A' <= degree[0] <= 'Z'
	scale = scale_types['minor'] if minor else scale_types['major']
	degree = scale[degree_types[degree]]
	key = scale[ord(key) - ord('C')]
	root = (key + degree) % 12
	if root in scale:
		name = chr((scale.index(root) + ord('C') - ord('A')) % 7 + ord('A'))
	else: # enharmonic equivalent, choosing sharps
		root -= 1
		name = chr((scale.index(root) + ord('C') - ord('A')) % 7 + ord('A'))
		name += '#'
	if minor:
		name += 'm'
	print(name)
	return gen_chord(name, octave=octave, inversion=inversion, time=time, hold=hold, arpeggio=arpeggio)


key = 'C'
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

note_envelope = envelope(attack=1., decay=0.0, sustain=1.0, release=3)
osc = oscillator(shape='whitenoise', amp=0.03, note_envelope=note_envelope)
sos = signal.butter(2, 2*2*fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
s.add_oscillator(osc)

music = []
music += gen_progression(key=key, degree='vi', inversion=2, time=0, hold=4)
music += gen_progression(key=key, degree='ii', time=4, hold=4)
music += gen_progression(key=key, degree='V', inversion=1, time=8, hold=4)
music += gen_progression(key=key, degree='I', time=12, hold=4)

music += [{**note, 'time':note['time']+16} for i,note in enumerate(music)]
print(music)

data = s.play_song(music)


t_tot = 8
s = synth(bpm=100)

note_envelope = envelope(attack=0.01, decay=1.5, sustain=0.0, decay_func=lambda x: np.exp(-4*x), release=0)
#note_envelope = envelope(attack=0, decay=0, sustain=1.0, release=0)
osc = oscillator(shape='sine', note_envelope=note_envelope)
impulse_response = np.zeros(samplerate)
impulse_response[::int(1*samplerate/64)] = 1
impulse_response *= np.exp(-np.linspace(0,4,impulse_response.size))
impulse_response *= np.linspace(1,0,impulse_response.size)
#osc.add_reverb(impulse_response)
sos = signal.butter(4, fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
s.add_oscillator(osc)

music = []
music += gen_progression(key=key, degree='vi', octave=5, time=0, hold=1, arpeggio=0.25)
music += gen_progression(key=key, degree='ii', octave=5, time=4, hold=1, arpeggio=0.25)
music += gen_progression(key=key, degree='V', octave=5, time=8, hold=1, arpeggio=0.25)
music += gen_progression(key=key, degree='I', octave=5, time=12, hold=1, arpeggio=0.25)

	#music += [{**note, 'time':note['time']+1} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+2} for i,note in enumerate(music)]
music += [{**note, 'time':note['time']+16} for i,note in enumerate(music)]
lead_data = s.play_song(music)
data[:lead_data.size] += 0.8*lead_data


data *= 0.8*np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
