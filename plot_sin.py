"""aim:
to generate a Python program which maps the individual fundamental waveforms (harmonics not yet considered) for the
intro riff on lead guitar to Queens of the Stone Age - Better Living Through Chemistry.

problems:
    -Plotting a wave visually
        -using matplotlib library
    |Working out time intervals between notes in the song and mapping them in terms of time
        |how many beats go into a second of music? Or should it be the inverse - how many seconds' duration is a 4-beat bar?
    |Discerning what the frequency of each individual note played is
        |online resources can be used to discern the fundamental wave frequency for a specific note played
    -Combining ranges of y values to make combined wave shapes
        -offsetting a specific range a certain number of zeros such that the wave starts at the correct point on the x-axis
        -Python has built-in functionality to add lists together
    -Designing dataset to input into program via argv
        |using .json format
        -what fields should be used? (current: "frequency", "note", "start", "end", where "start" and "end are numbers as multiple of time-per-beat")
        -ensure that program treats an "end" field as terminating just before the start of the actual beat which is shown
        -ensure notes do not end until that note is unfretted, muted or fret is changed in the song, and not before
"""
import numpy
from collections import Mapping
import matplotlib.pyplot as plt
from sys import argv
import json
import pprint
import collections
import math
from random import choice

#setup vars etc.
#taking input file from user
script, json_in = argv

pp = pprint.PrettyPrinter(indent=4)

#end setup

class Sequence():
    resolution = 1000
    def __init__(self, notes):
        """initialise a wave sequence based upon a iterable sequence of Note instances"""
        self.start, self.end, self.min_freq, self.max_freq = self._define_parameters(notes)
        assert float(self.start) != float('inf'), "Sequence.__init__() has failed"
        assert self.end != -1, "Sequence.__init__() has failed"
        assert float(self.min_freq) != float('inf'), "Sequence.__init__() has failed, min_freq: {}".format(self.min_freq)
        assert self.max_freq != -1, "Sequence.__init__() has failed"
        #popualate the dict with time points as the keys
        self.fromkeys(numpy.arange(self.start, self.end, 0.5), [])
        for note in notes:
            assert isinstance(note, Note), "sequence contains members which are not an instance of 'Note'"
            #assumes that the bars are counted in 'eighth notes' and so for a 4-beat bar there are are 8 notes, hence the '0.5' interval
            for beat in numpy.arange(note.start, note.end, 0.5):
                self[beat].append(note.frequency)

    def _calibrate_fig(self):
        """function to set appropriate settings for matplotlib figure"""
        self.fig = plt.figure()
        self.fig.set_dpi(100)
        plt.style.use('dark_background')
        plt.grid(True, which="both", axis="both", color="w", linewidth="1")
        #divide the x axis plot labels up by a user-defined system (numpy.arange(<start>, <stop>, <step>) -> range of all plot labels)
        plt.xticks(numpy.linspace(riff.start, t_per_beat * riff.end, riff.end))

    def _define_parameters(self, notes):
        start = float('inf')
        end = -1
        min_freq = float('inf')
        max_freq = -1
        #look through the data given for the earliest start time of a wave and the latest temination of a wave, thus defining the total time range
        #max_frequecncy and min_frequency are arbitrary and not required but are there to ensure that correct data is being disseminated correctly
        for note in notes:
            if note.frequency > max_freq:
                max_freq = note.frequency
            if note.frequency < min_freq:
                min_freq = note.frequency
            if note.start < start:
                start = note.start
            elif note.end > end:
                end = note.end
        return (start, end, min_freq, max_freq)

    def plot_graph(self):
        #call method to calculate axes
        self._plot_axes()
        #perform necessary setup functions for graph
        self._calibrate_fig()
        plt.plot(self.x, self.y, color=gen_colour())

    def _plot_axes(self):
        self.x = numpy.arange(self.start, self.end, 0.001)
        self.y = numpy.zeros(self.x.shape)
        for note in self:
            if (len(self[note]) < 1):
                print("beat {} of the sequence has no notes attached to it")
            x0 = numpy.arange(note.start, note.start + 0.5, 0.001)
            w = sineWaveZero( note.frequency, x0 )
            y_add = numpy.zeros(self.y.shape)
            y_add[int(note.start * 500), int(note.end * 500)] = w
            #add the calculated values on to self.y
            self.y += y_add


class Note(object):
    def __init__(self, frequency, note, start, end):
        self.frequency, self.note, self.start, self.end = frequency, note, start, end
        self.colour = gen_colour()

    def waveGen(self, xRange):
        """function to calculate all y values for a given input range of x-coordinates: (   y = f(x) = sin( xRange[i]*t )    )
        frequency -> cycles per second of a wave
        duration -> is the time duration of the entire input wave (end point relative to t = 0). Value will be a number as a multiple of t_per_beat, but must be a multiple of 0.25
        xRange is an input of values to be plotted on the x-axis """
        #instantiate list for return
        a = []
        assert self.frequency % 1 == 0, "Frequency argument for waveGen is not an integer value"
        #need to determine closest s where s >= starting time and e where e <= ending time where s & e are points in xRange
        for i in xRange:
            value = sineWaveZero( self.frequency, i )
            a.append(value)
        return a

def unwrap_json(json_obj):
    notes = []
    #perform sanity checks on the input argument to the system
    assert isinstance(json_obj, list), "the data into the sequence is not of the correct type, it is of type '{}' needs to be of type 'list'".format(json_data.__class__.__name__)
    intended_keys = [u"frequency", u"note", u"sections"]
    for record in json_obj:
        for key in intended_keys:
            assert key in record, "list argument to NoteFactory does not have the correct keys.\nIt has: {}, but it should have: {}".format(record.keys(), intended_keys)
    #unwrap raw data parsed from JSON
    for payload in json_obj:
        print(payload.keys())
        for interval in payload["sections"]:
            notes.append(Note(payload["frequency"], payload["note"], interval["start"], interval["end"]))
    return notes

def sineWaveZero(w,t):
    return numpy.sin(w * t)

def gen_colour():
    val_list = []
    # range of all values for all hexadecimal digits
    vals = range( 15 )
    #cycle through random
    for index in range(6):
        new_value = choice(vals)
        val_list.append( hex(new_value)[2:] )
    return ("#" + "".join(val_list))

assert json_in.endswith(".json"), "The input file to the program does not end with a '.json' file extension"

#load JSON data into a Python dictionary
data_in = {}
with open(json_in, "r") as f:
    data_in = json.loads(f.read())

pp.pprint(data_in)

notes = unwrap_json(data_in)
#set up an instance with which to draw the graph
riff = Sequence(notes)
riff.plot_graph()

#display deduced total sequence information
print("Information about the total {}".format(riff.__dict__))


# actual_start = sequence["start"]
# if sequence['start'] > 0:
#     while actual_start == None:
#         u_input = raw_input("Your audio sequence does not have musical information all the way to t=0, would you like to backfill to t = 0 with zeros?\t").lower()
#         if u_input == "y":
#             actual_start = 0
#         elif u_input == "n":
#             #exit out because the appropriate start point is already set
#             break
#
#print("Actual start position is now:\t" + str(actual_start) + "(in beats per minute)")

print("t_per_beat: %f, t_per_bar: %f" %(t_per_beat, t_per_bar))

plt.show()
