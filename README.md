# SciPySynth
A simple music synthesizer created from scratch using SciPy and Numpy.

## Design
### Basic Math of Musical Notes
#### Fundamentals of Musical Sound
- A4 (right above middle C) is defined as 440Hz
- Going up 1 octave is a doubling in frequency: the whole scale is logarithmic
- There are 12 notes per octave (including semitones)
- Therefore any other note's frequency in Hz can be calculated: `440*2**((X-A)/12)`
- This equal spacing is known as "Twelve-tone equal temperament". Other ways to divide the scale exist.

#### Scales
- A scale is a set of notes ordered by pitch
- The scale with all 12 notes in an octave is the chromatic scale.
- Generally of subset of 7 notes (heptatonic scale) are chosen for a composition
   - Generally these 7 notes are as a diatonic sclae: they are separated by 5 whole-steps (2 notes) and two half-steps (1 note) 
   - Notice `5+2 == 7` and `5*2 + 2*1 == 12`
- Diatonic scales are classified by their starting note (tonic) and the pattern of steps.
   - For the following "W" and "H" will represent "whole-step" and "half-step" respectively.
   - Major scale: [W, W, H, W, W, W, H]
   - Minor scale: [W, H, W, W, H, W, W]
   - Notice these are the same pattern, just cyclically shifted: in total 7 types of scale can be made
   - Notice this means same scales can be equivalent: e.g. C Major and A Minor. These are known as "relative keys".
   - Being equivalent in music but written in a different way is also called "enharmonically equivalent"

#### Chords and Progressions

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
Evelopes shape the amplitude of a wave over time. They make the difference between quick "plucks", and longer "sustained" notes.  
Envelopes are defined by as an amplitude multiplier over time. Taking on values between 0 and 1.

They are 4 main parameters:
- Attack (time): the amount of time for the signal to reach it's peak loudest.
   - Short attacks make more "plucky" and "punchy" sounds.
   - Long attacks make gradually building up sounds, like pads
- Decay (time): the amound of time for the signal to go from its peak to sustained level.
- Sustain (percentage): The fraction of the initial peak volume that the note has when held for longer.
   - Think of how when you strike a piano key it's immediately loud, but as you hold it it dies down.
- Release (time): The amount of time it takes the note to die out after it is released.


#### Filters
Filters have the effect of reducing certain frequencies in the sound.  

The main classes of filter are:
- low-pass filter: allows lower frequencies to pass through
- high-pass filter: allows higher frequencies to pass through
- band-pass filter: allows an interval of frequencies to pass through

Filters are generally specified to have *pass-band* which are the frequencies unaffected, a *stop-band* in which the frequencies are filterd out. 
The **cut-off frequency** is the point of transition between the pass-band and stop-band.

#### Delay (and convolution)
Echo and reverb are examples of the audio signal being replayed on top of the original several times, with each replay being later and quieter.
- Echo: Delay >100ms
	- Produces an audible delay in the signal.
- Reverb: Delay <100ms
	- Fast enought to blend the signals.
	- Used for recreating sound of playing in different rooms.

These effects can be recreated by performing a convolution with the signal: Imagine a decaying comb of impluses.

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
- https://en.wikipedia.org/wiki/12_equal_temperament
- https://en.wikipedia.org/wiki/Equal_temperament
#### Oscillators
- https://en.wikipedia.org/wiki/Sine_wave
- https://en.wikipedia.org/wiki/Sawtooth_wave
- https://en.wikipedia.org/wiki/Square_wave
- https://en.wikipedia.org/wiki/Triangle_wave
#### Envelopes
- https://en.wikipedia.org/wiki/Envelope_(waves)
#### Reverb
- https://en.wikipedia.org/wiki/Reverberation
- https://en.wikipedia.org/wiki/Convolution_reverb
- https://en.wikipedia.org/wiki/Delay_(audio_effect)
- https://en.wikipedia.org/wiki/Echo
#### Filters
- https://en.wikipedia.org/wiki/Filter_(signal_processing)
- https://en.wikipedia.org/wiki/Low-pass_filter
- https://en.wikipedia.org/wiki/Butterworth_filter
#### Other Effects
- https://en.wikipedia.org/wiki/Chorus_effect
- https://en.wikipedia.org/wiki/Beat_(acoustics)
- https://en.wikipedia.org/wiki/Flanging

### Music Theory
#### Scales
- https://en.wikipedia.org/wiki/Scale_(music)
- https://en.wikipedia.org/wiki/Chromatic_scale
- https://en.wikipedia.org/wiki/Heptatonic_scale
- https://en.wikipedia.org/wiki/Diatonic_scale
- https://en.wikipedia.org/wiki/Tonic_(music)
- https://en.wikipedia.org/wiki/Key_signature
- https://en.wikipedia.org/wiki/Degree_(music)
- https://en.wikipedia.org/wiki/Vi%E2%80%93ii%E2%80%93V%E2%80%93I

### Algorithmic Composition
- https://en.wikipedia.org/wiki/Algorithmic_composition
