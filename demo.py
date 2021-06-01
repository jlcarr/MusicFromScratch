from playsound import playsound
from scipy.io import wavfile
import sys

import matplotlib.pyplot as plt

from synth import *

samplerate=44100
fs = 261.63
t_tot = 4.
s = synth()

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


data = s.play_song([
	{'pitch':60-12, 'time':0.0, 'hold':t_tot},
	{'pitch':64-12, 'time':0.0, 'hold':t_tot},
	{'pitch':67-12, 'time':0.0, 'hold':t_tot},

	{'pitch':72-12, 'time':t_tot, 'hold':t_tot},
	{'pitch':64-12, 'time':t_tot, 'hold':t_tot},
	{'pitch':67-12, 'time':t_tot, 'hold':t_tot},
])

data *= np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
#playsound('example.wav')

#sys.exit()


samplerate=44100
fs = 261.63
t_tot = 2.0
s = synth()

note_envelope = envelope(attack=0.05, decay=0.1, sustain=0.0)
osc = oscillator(shape='sawtooth', note_envelope=note_envelope, voices=3, detune=0.01)
sos = signal.butter(2, fs, 'lowpass', fs=samplerate, output='sos')
osc.add_filter(sos)
impulse_response = np.zeros(samplerate)
impulse_response[::int(1*samplerate/8)] = 1
impulse_response *= np.exp(-np.linspace(0.,10.,impulse_response.size))
osc.add_reverb(impulse_response)
s.add_oscillator(osc)

#data = s.play_notes(fs, t_tot)
#data *= np.iinfo(np.int16).max / np.max(np.abs(data))
#wavfile.write("example.wav", samplerate, data.astype(np.int16))
#playsound('example.wav')

#sys.exit()


samplerate=44100
fs = 261.63
t_tot = 2.0
s = synth()

note_envelope = envelope(attack=0.01, decay=1.5, sustain=0.0, decay_func=lambda x: np.exp(-8*x))
#note_envelope = envelope(attack=0, decay=0, sustain=1.0, release=0)
osc = oscillator(shape='sine', note_envelope=note_envelope)
impulse_response = np.zeros(2*samplerate)
impulse_response[::int(1*samplerate/4)] = 1
impulse_response *= np.exp(-np.linspace(0.,10.,impulse_response.size))
#osc.add_reverb(impulse_response)
s.add_oscillator(osc)

music = []
for bar in range(8):
	music += [
		{'pitch':72-12, 'time':t_tot*(bar/2+1/8), 'hold':t_tot},
		{'pitch':76-12, 'time':t_tot*(bar/2+2/8), 'hold':t_tot},
		{'pitch':79-12, 'time':t_tot*(bar/2+3/8), 'hold':t_tot},
	]
lead_data = s.play_song(music)
data[:lead_data.size] += lead_data

data *= np.iinfo(np.int16).max / np.max(np.abs(data))
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
