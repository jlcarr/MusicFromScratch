"""A library for handling basic music theory concepts for composing, which can be fed into the synth module.
"""

scale_types = {
	'major': [0,2,4,5,7,9,11], # accumulate major scale [2,2,1,2,2,2,1]
	'minor': [0,2,3,5,7,8,10] # accumulate minor scale [2,1,2,2,1,2,2]
}

degree_types = {'I':0, 'ii':1, 'iii': 2, 'IV': 3, 'V': 4, 'vi':5, 'vii':6}

chord_types = {'':[0,4,7], 'm':[0,3,7], 'dim':[0,3,6], 'aug':[0,4,8]}


def gen_chord(name, octave=4, inversion=0, hold=1, time=0, arpeggio=0):
	"""Translates musical notation of chords into the mathematical definition.
	Can be fed into the synth module.
	"""
	# compute root
	root = name[0]
	root = scale_types['major'][ord(root) - ord('C')] 
	root += 1 if '#' in name else 0
	root = 12*(octave+1) + root

	# compute other notes in chord
	mod = name[2:] if '#' in name else name[1:]
	chord = chord_types[mod]

	# handle inversions
	if inversion == 1:
		chord[1],chord[2] = chord[1]-12,chord[2]-12
	if inversion == 2:
		chord[2] = chord[2]-12

	# put it together with timing
	time += 0 if arpeggio >=0 else 3*hold
	return [{'pitch':root+note, 'time':time + arpeggio*hold*i, 'hold':hold} for i,note in enumerate(chord)]


def gen_progression(key='C', degree='I', octave=4, inversion=0, time=0, hold=1, arpeggio=0):
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
	print(name)
	return gen_chord(name, octave=octave, inversion=inversion, time=time, hold=hold, arpeggio=arpeggio)

