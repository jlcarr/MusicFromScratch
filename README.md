# SciPySynth
A simple music synthesizer created from scratch using SciPy and Numpy.

## Design
### Basic Math of Musical Notes
- A4 (right above middle C) is defined as 440Hz
- Going up 1 octave is a doubling in frequency: the whole scale is logarithmic
- There are 12 notes per octave (including semitones)
- Therefore any other note's frequency in Hz can be calculated: `440*2**((X-A)/12)`

### Synth Building Blocks
#### Oscillators
Synthesizers combine fundamental waveforms with filters and other effects to construct their instruments.  
The fundamental waveforms are:
- Sine waves
	- Composed of one harmonic (itself).
	- This is the "purest" and more simple wave.
- Square waves
	- Composed of only odd harmonics, falling off linearly.
	- Often described as "wooden". Reminiscent of "Chiptunes"
- Sawtooth waves
	- Contains all harmonics, falling off linearly.
	- Often described as "buzzy". Useful for strings.
- Triangle waves
	- Composed of only odd harmonics, falling off quadratically.
	- Not as commonly used.
- White noise
	- Atonal: An even distribution over all frequencies.
	- Generated from a Gaussian distribution.
	- Sounds like TV static.

#### Envelopes

#### Filters

#### Reverb
Related concepts are echo and delay.

## Resources
### Python
- https://python.plainenglish.io/making-a-synth-with-python-oscillators-2cb8e68e9c3b
- https://docs.scipy.org/doc/scipy/reference/signal.html

### Similar Projects
- https://www.youtube.com/watch?v=ogFAHvYatWs (Ignio Quilez makes synths with basic maths)
- https://www.youtube.com/watch?v=vY5iyMa2_VI (song made with Audacity only)
- https://www.youtube.com/watch?v=iW0lvWs2aFo (song made with Audacity only)

### Sound Design / Synth
- https://en.wikipedia.org/wiki/A440_(pitch_standard)
- https://en.wikipedia.org/wiki/Scientific_pitch_notation
#### Oscillators
- https://en.wikipedia.org/wiki/Sawtooth_wave
#### Envelopes
- https://en.wikipedia.org/wiki/Envelope_(waves)
#### Reverb
- https://en.wikipedia.org/wiki/Reverberation
- https://en.wikipedia.org/wiki/Convolution_reverb
#### Filters
- https://en.wikipedia.org/wiki/Filter_(signal_processing)
- https://en.wikipedia.org/wiki/Low-pass_filter
- https://en.wikipedia.org/wiki/Butterworth_filter
