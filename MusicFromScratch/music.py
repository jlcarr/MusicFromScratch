"""A library for handling basic music theory concepts for composing, which can be fed into the synth module.
"""

import numpy as np

scale_types = {
	'major': [0,2,4,5,7,9,11], # accumulate major scale [2,2,1,2,2,2,1]
	'minor': [0,2,3,5,7,8,10] # accumulate minor scale [2,1,2,2,1,2,2]
}

degree_types = {'I':0, 'ii':1, 'iii': 2, 'IV': 3, 'V': 4, 'vi':5, 'vii':6}

chord_types = {'':[0,4,7], 'm':[0,3,7], 'dim':[0,3,6], 'aug':[0,4,8]}

def to_midi_number(name, octave=4):
	value = scale_types['major'][ord(name[0]) - ord('C')]
	value += 1 if '#' in name else 0
	value += 12*(octave+1)
	return value

def gen_chord(name, octave=4, inversion=0, invert_to=None, hold=1, time=0, arpeggio=0):
	"""Translates musical notation of chords into the mathematical definition.
	Can be fed into the synth module.
	"""
	# compute root
	root = to_midi_number(name, octave=octave)

	# compute other notes in chord
	mod = name[2:] if '#' in name else name[1:]
	chord = chord_types[mod]
	chord_notes = [root+note for note in chord]

	# handle inversions
	if invert_to:
		print("Invert to: ", invert_to)
		print("Uninverted notes: ", chord_notes)
		invert_target = to_midi_number(invert_to, octave=octave)
		for i,note in enumerate(chord_notes):
			mod_dist = (note - invert_target)%12
			chord_notes[i] = invert_target + mod_dist
			chord_notes[i] += 0 if mod_dist < 12-mod_dist else -12
		print("Inderted notes: ", chord_notes)
	if inversion == 1:
		chord_notes[1],chord_notes[2] = chord_notes[1]-12,chord_notes[2]-12
	if inversion == 2:
		chord_notes[2] = chord_notes[2]-12
	chord_notes.sort()
	print("Inverted notes sorted: ", chord_notes)
	print()

	# put it together with timing
	time += 0 if arpeggio >=0 else 3*hold
	return [{'pitch':note, 'time':time + arpeggio*hold*i, 'hold':hold} for i,note in enumerate(chord_notes)]


def gen_progression(key='C', degree='I', octave=4, inversion=0, invert_to=None, time=0, hold=1, arpeggio=0):
	"""Given the music notation for a chord in a progression will output the mathematical definition.
	Can be fed into the synth module.
	"""
	minor_degree = not 'A' <= degree[0] <= 'Z'
	minor_key = 'm' in key
	scale = scale_types['minor'] if minor_key else scale_types['major']
	degree = scale[degree_types[degree]]
	key = scale_types['major'][ord(key[0]) - ord('C')] + (1 if '#' in key else 0)
	root = (key + degree) % 12
	if root in scale:
		name = chr((scale.index(root) + ord('C') - ord('A')) % 7 + ord('A'))
	else: # enharmonic equivalent, choosing sharps
		root -= 1
		name = chr((scale.index(root) + ord('C') - ord('A')) % 7 + ord('A'))
		name += '#'
	if minor_degree:
		name += 'm'
	print("Chord in progression: ", name)
	return gen_chord(name, octave=octave, inversion=inversion, invert_to=invert_to, time=time, hold=hold, arpeggio=arpeggio)

