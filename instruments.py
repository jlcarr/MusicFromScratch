from synth import *


def synth_pad(samplerate=44100, bpm=60, fs=261.63):
	s = synth(bpm=bpm)
	
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
	
	return s


def pluck_lead(samplerate=44100, bpm=60, fs=261.63):
	s = synth(bpm=bpm)
	
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

	return s


