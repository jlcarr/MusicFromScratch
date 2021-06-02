import numpy as np
from scipy import signal


class envelope:
	def __init__(self, attack=0.5, decay=0.25, sustain=0.5, release=1., 
		attack_func=lambda x: x, decay_func=lambda x: 1.-x, release_func=lambda x: 1.-x):
		self.attack = attack
		self.decay = decay
		self.sustain = sustain
		self.release = release

		self.attack_func = attack_func
		self.decay_func = decay_func
		self.release_func = release_func

	def gen_envelope(self, hold, samplerate=44100):
		t_tot = hold + self.release
		size = int(t_tot*samplerate)
		envelope = np.zeros(size)

		t_start, t_end = 0, min(self.attack, hold)
		start, end = int(t_start*samplerate), int(t_end*samplerate)
		envelope[start:end] = self.attack_func(np.linspace(0., 1., end-start))

		if hold > self.attack:
			t_start, t_end = t_end, min(self.attack+self.decay,hold)
			start, end = int(t_start*samplerate), int(t_end*samplerate)
			envelope[start:end] = self.sustain + (1-self.sustain)*self.decay_func(np.linspace(0., 1., end-start))

		if hold > self.attack+self.decay:
			t_start, t_end = t_end, hold
			start, end = int(t_start*samplerate), int(t_end*samplerate)
			envelope[start:end] = self.sustain*np.ones(end-start)

		t_start, t_end = t_end, t_end+self.release
		start, end = int(t_start*samplerate), int(t_end*samplerate)
		envelope[start:end] = self.sustain*self.release_func(np.linspace(0., 1., end-start))

		return envelope
		
		

class oscillator:
	def __init__(self, amp=1.0, shape='sine', note_envelope=envelope(), voices=1, detune=0.):
		self.amp = amp
		self.shape = shape

		self.note_envelope = note_envelope

		self.voices = voices
		self.detune = detune

		self.filters = []
		self.reverb = []

	def add_filter(self, sos):
		self.filters.append(sos)

	def add_reverb(self, impulse_response):
		self.reverb.append(impulse_response)

	def play_note(self, fs, hold, samplerate=44100):
		t_tot = hold + self.note_envelope.release
		size = int(t_tot*samplerate)
		t = np.linspace(0., t_tot, size)
		data = np.zeros(size)

		wave_func = np.sin
		if self.shape == 'sawtooth':
			wave_func = signal.sawtooth
		if self.shape == 'square':
			wave_func = signal.square
		if self.shape == 'whitenoise':
			wave_func = lambda t: np.random.normal(0.0, 1.0, size=t.size)
		if self.shape == 'brownnoise':
			wave_func = lambda t: np.cumsum(np.random.normal(0.0, 1.0, size=t.size))

		data += wave_func(2. * np.pi * fs * t)
		for voice in range(1,self.voices//2 + 1):
			data += wave_func(2. * np.pi * fs * 2**(voice*self.detune) * t)
			data += wave_func(2. * np.pi * fs * 2**(-voice*self.detune) * t)
		
		envelope = self.note_envelope.gen_envelope(hold, samplerate=samplerate)
		data *= envelope

		for sos in self.filters:
			data = signal.sosfilt(sos, data)

		for impulse_response in self.reverb:
			data = signal.convolve(data, impulse_response, mode='same')#[:data.shape[0]]

		data *= self.amp * np.iinfo(np.int16).max / np.max(np.abs(data))
		return data


class synth:
	def __init__(self, bpm=60, samplerate=44100):
		self.samplerate = samplerate
		self.bpm = bpm
		self.oscillators = []

	def add_oscillator(self, osc):
		self.oscillators.append(osc)


	def play_notes(self, fs, hold = 1.):
		t_tot = hold + max([osc.note_envelope.release for osc in self.oscillators])
		size = int(t_tot*self.samplerate)
		data = np.zeros(size)
		
		for osc in self.oscillators:
			data += osc.play_note(fs, hold, self.samplerate)

		return data

	def play_song(self, music):
		release = max([osc.note_envelope.release for osc in self.oscillators])
		final_release = max([note['time']+note['hold'] for note in music])
		final_release *= 60 / self.bpm
		t_tot = final_release + release
		size = int(t_tot*self.samplerate)
		data = np.zeros(size)

		for note in music:
			note_time = note['time'] * 60 / self.bpm
			start = int(self.samplerate * note_time)
			note_hold = note['hold'] * 60 / self.bpm
			pitch = 440*2**((note['pitch'] - 69)/12)
			note_data = self.play_notes(pitch, hold=note_hold)
			note_size = note_data.size
			data[start:start+note_size] += note_data

		return data

