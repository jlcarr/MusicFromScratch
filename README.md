# SciPySynth
A simple music synthesizer created from scratch using SciPy and Numpy.

## Design
### Basic Math of Musical Notes
- A4 (right above middle C) is defined as 440Hz
- Going up 1 octave is a doubling in frequency: the whole scale is logarithmic
- There are 12 notes per octave (including semitones)
- Therefore any other note's frequency in Hz can be calculated: `440*2**((X-A)/12)`

### Oscillators
Synthesizers combine fundamental waveforms with filters and other effects to construct their instruments.  
The fundamental waveforms are:
- Sine waves
- Square waves
- Sawtooth waves
- Triangle waves

### Filters


## Resources
### Python
- https://python.plainenglish.io/making-a-synth-with-python-oscillators-2cb8e68e9c3b
- https://docs.scipy.org/doc/scipy/reference/signal.html

### Sound Design / Synth
- https://en.wikipedia.org/wiki/A440_(pitch_standard)
