from playsound import playsound
import sys

import numpy as np
from scipy.io import wavfile
from scipy import signal

import matplotlib.pyplot as plt


class oscillator:
	def __init__(self, amp=1.0, shape='sine', voices=1, detune=0.):
		self.amp = amp
		self.shape = shape
		self.voices = voices
		self.detune = detune

	def play_note(self, fs, t_tot, samplerate):
		size = int(t_tot*samplerate)
		t = np.linspace(0., t_tot, size)
		data = np.zeros(size)

		wave_func = np.sin
		if self.shape == 'sawtooth':
			wave_func = signal.sawtooth
		if self.shape == 'square':
			wave_func = signal.square

		data += self.amp * wave_func(2. * np.pi * fs * t)
		for voice in range(self.voices//2 + 1):
			data += self.amp * wave_func(2. * np.pi * fs * 2**(voice*self.detune) * t)
			data += self.amp * wave_func(2. * np.pi * fs * 2**(-voice*self.detune) * t)
		
		return data


class synth:
	def __init__(self, samplerate=44100):
		self.samplerate = samplerate
		self.oscillators = []

	def add_oscillator(self, osc):
		self.oscillators.append(osc)

	def play_notes(self, fs, t_tot = 1.):
		size = int(t_tot*self.samplerate)
		t = np.linspace(0.0, t_tot, size)
		data = np.zeros(size)
		
		for osc in self.oscillators:
			data += osc.play_note(fs, t_tot, self.samplerate)

		return data




samplerate = 44100
fs = 261.63
t_tot = 8.
s = synth()
s.add_oscillator(oscillator(shape='sawtooth', voices=3, detune = 0.0001))
data = s.play_notes(fs, t_tot)
data += s.play_notes(fs*2**(4/12), t_tot)
data += s.play_notes(fs*2**(7/12), t_tot)

sos = signal.butter(2, 2*fs, 'lowpass', fs=samplerate, output='sos')
data = signal.sosfilt(sos, data)

data *= np.iinfo(np.int16).max / np.max(data)
wavfile.write("example.wav", samplerate, data.astype(np.int16))
playsound('example.wav')
