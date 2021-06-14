from synth import *


def synth_pad(samplerate=44100, bpm=60, fs=261.63):
	s = synth(bpm=bpm)
	
	note_envelope = envelope(attack=2., decay=0.0, sustain=1.0, release=3.)
	osc = oscillator(shape='sawtooth', note_envelope=note_envelope, voices=3, detune = 0.01)
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
	
	note_envelope = envelope(attack=0.01, decay=2.5, sustain=0.0, decay_func=lambda x: np.exp(-4*x), release=0)
	#note_envelope = envelope(attack=0, decay=0, sustain=1.0, release=0)
	osc = oscillator(shape='sine', note_envelope=note_envelope)
	impulse_response = np.zeros(samplerate)
	impulse_response[::int(1*samplerate/2)] = 1
	impulse_response *= np.exp(-np.linspace(0,8,impulse_response.size))
	#impulse_response *= np.linspace(1,0,impulse_response.size)
	#osc.add_reverb(impulse_response)
	sos = signal.butter(4, fs, 'lowpass', fs=samplerate, output='sos')
	osc.add_filter(sos)
	s.add_oscillator(osc)

	return s


def cymbals(samplerate=44100, bpm=60, fs=261.63):
	s = synth(bpm=bpm)

	note_envelope = envelope(attack=0.05, decay=1.5, sustain=0.0, release=0., decay_func=lambda x: np.exp(-24*x))
	osc = oscillator(shape='whitenoise', note_envelope=note_envelope)
	sos = signal.butter(6, 8*fs, 'highpass', fs=samplerate, output='sos')
	osc.add_filter(sos)
	s.add_oscillator(osc)

	return s

def bass_drum(samplerate=44100, bpm=60, fs=261.63):
	s = synth(bpm=bpm)

	note_envelope = envelope(attack=0.05, decay=1.0, sustain=0.0, release=0., decay_func=lambda x: np.exp(-8*x))
	osc = oscillator(shape='whitenoise', note_envelope=note_envelope)
	sos = signal.butter(4, fs, 'lowpass', fs=samplerate, output='sos')
	osc.add_filter(sos)
	s.add_oscillator(osc)

	return s

if __name__=="__main__":
	from playsound import playsound
	from scipy.io import wavfile
	samplerate=44100
	s = cymbals(bpm=100)
	data = s.play_song([
	        {'pitch':0, 'time':0.0, 'hold':1},
	        {'pitch':0, 'time':1.0, 'hold':1},
	        {'pitch':0, 'time':2.0, 'hold':1},
	        {'pitch':0, 'time':3.0, 'hold':1},
	])

	data *= np.iinfo(np.int16).max / np.max(np.abs(data))
	wavfile.write("example.wav", samplerate, data.astype(np.int16))
	playsound('example.wav')

