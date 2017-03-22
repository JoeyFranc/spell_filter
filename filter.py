import read
import json
import bisect
from enums import *
from collections import namedtuple


# Keys that should be filterable
ENUM_KEYS = [
    ('source', SOURCE_SIZE),
    ('classes', CLASSES_SIZE),
    ('school', SCHOOL_SIZE)
]
BOOL_KEYS = [
    'v',
    's',
    'm',
    'is_touch',
    'is_self',
    'is_ritual',
    'is_instant',
    'is_concentration',
    'higher_level',
    'material'
]
INT_KEYS = [
    'cost',
    'level'
]
IS_RESET = 'reset'

IntRange = namedtuple('IntRange', 'min max')

class Inquiry(dict):

    def _copy(self, inquiry):

        # Create a value for every entry in json
        for key in inquiry:
            self[key] = inquiry[key]

    def _init(self):
        # Default start

        self[IS_RESET] = True  # Default behavior is to reset every time

        # Set all enum keys
        for enum in ENUM_KEYS:
            self[enum[0]] = [True]*enum[1]

        # Set all bools
        for bool_key in BOOL_KEYS:
            self[bool_key] = None

        # Set all int ranges
        for int_key in INT_KEYS:
            self[int_key] = IntRange(0,0)

    # For each key specified, init the value
    def __init__(self, *args):
        
        # Copy or default accordingly
        if len(args):
            self._copy(args[0])
        else:
            self._init()


class Filter(object):

    # Init spell_idx [spell name] -> idx in spellbook
    def _init_spell_idx(self):
        self.spell_idx = {}


    def _add_spell_idx(self, spell, i):
        # Add EVERY spell
        name = spell.name.strip().lower()
        self.spell_idx[name] = i


    # For every enum variable in Spell(), create an array of appropriate size
    def _init_enums(self):

        # Init enum keys
        self.enums = {}
        for (enum_name, size) in ENUM_KEYS:
            self.enums[enum_name] = [[]]
            for i in range(size-1):
                self.enums[enum_name] += [[]]  # Init to N empty arrays


    # Add an index to correct enum array if spell[i].enum is defined
    def _add_enums(self, spell, i):

        # Add this spell to appropriate array if attr is defined
        for (enum_name, size) in ENUM_KEYS:
            # Get value for this spell
            value = getattr(spell, enum_name)

            # Check if this is multiple values or not
            if type(value) == type([]):
                for v in value:
                    self.enums[enum_name][v] += [i]
            else:
                self.enums[enum_name][value] += [i]


    # Return all spells that meet each enum inquiry
    def _get_enums(self, inquiry):

        matches = [ i for i in range(len(self.spellbook)) ]

        # Define every value
        for (enum_name, size) in ENUM_KEYS:

            # Add all spell indexes that match filter request
            if enum_name in inquiry and 'None' not in inquiry[enum_name]:
                print(enum_name)
                # Find all spells that match this enum filter
                query = []
                for checked_value in inquiry[enum_name]:
                    query += self.enums[enum_name][int(checked_value)]
                    print(int(checked_value))

                # Get intersection of matches and query
                matches = [ match for match in matches if match in query ]

        return matches


    # Init an empty array for each bool
    def _init_bools(self):

        self.bools = {}
        for bool_name in BOOL_KEYS:
            self.bools[bool_name] = []


    # For each field, add this index iff spell.bool is True
    def _add_bools(self, spell, i):
        
        for bool_name in BOOL_KEYS:
            if getattr(spell, bool_name):
                self.bools[bool_name] += [i]


    # Return all bools that match the inquiry
    def _get_bools(self, inquiry):

        # Everything matches null inquiry
        matches = [i for i in range(len(self.spellbook))]

        for bool_name in BOOL_KEYS:
            # Get intersection of matches and new bool matches
            value = None  # Default to doing nothing for undefined bools
            if bool_name in inquiry: value = inquiry[bool_name][0]
            if value == 'True':
                matches = [ match for match in matches
                            if match in self.bools[bool_name] ]
            if value == 'False':  # Bool was purposefully set to False
                matches = [ match for match in matches
                            if match not in self.bools[bool_name] ]

        return matches


    # Init ranges to empty arrays
    def _init_ranges(self):
        
        self.ranges = {}
        for key in INT_KEYS:
            self.ranges[key] = []


    # Add a new spell to ranges
    def _add_ranges(self, spell, i):

        for range_name in INT_KEYS:
            value = getattr(spell, range_name)
            # Add this to the array
            if value is not None:
                self.ranges[range_name] += [(value,i)]


    def _sort_ranges(self):
        ''' Sorts all ranged entries from low to high
        '''
        for key in INT_KEYS:
            self.ranges[key].sort()


    def _get_ranges(self, inquiry):
        ''' returns all spell indexes that match the specified range conditions
            in the inquiry
        '''
        matches = [ i for i in range(len(self.spellbook)) ]

        # For every set key
        for key in INT_KEYS:

            # Read min and max values
            min_val = None
            if key+'_min' in inquiry and inquiry[key+'_min'][0].isdigit():
                min_val = inquiry[key+'_min'][0]
            max_val = None
            if key+'_max' in inquiry and inquiry[key+'_max'][0].isdigit():
                max_val = inquiry[key+'_max'][0]
                
            # Get specified range and lb and rb
            if not (min_val is None and max_val is None):

                # Set left bound and right bound
                if min_val is None: lb = 0
                else: lb = bisect.bisect_left(self.ranges[key], (int(min_val),0))
                if max_val is None: rb = len(self.ranges[key])
                else: rb = bisect.bisect(self.ranges[key], (int(max_val),0))
                matches = [ i for (value,i) in self.ranges[key][lb:rb]
                            if i in matches ]

        return matches


    # Init a spell filter from a json file
    def __init__(self, data_file='spells.json'):

        # Init values
        self.spellbook = read.get_spellbook(data_file)
        for i in range(len(self.spellbook)):
            self.spellbook[i].id = i
        self.display = []

        # Init values
        self._init_spell_idx()  # name -> spellbook_idx
        self._init_enums()  # enumeration values
        self._init_bools()  # boolean values
        self._init_ranges()  # integer ranges

        # Fill indexes
        i = 0
        for spell in self.spellbook:
            self._add_spell_idx(spell, i)
            self._add_enums(spell, i)
            self._add_bools(spell, i)
            self._add_ranges(spell, i)
            i += 1
        self._sort_ranges()

    # Add queries to display
    def query_by_name(self, names):

        # Do some minor input cleaning, first
        for name in names.split(','):
            name = name.strip().lower()
            if name in self.spell_idx:
                self.display += [ self.spellbook[self.spell_idx[name]] ]

    # Add queries to display
    def query_by_value(self, inquiry):

        # Get intersection of sub-category matches
        enums = self._get_enums(inquiry)
        bools = self._get_bools(inquiry)
        ranges = self._get_ranges(inquiry)
        print(len(enums), 'enums')
        print(len(bools), 'bools')
        print(len(ranges), 'ranges')
        self.display += [ self.spellbook[match] for match in enums
                         if match in bools and match in ranges ]

    def filter(self, inquiry):
        if inquiry['search_method'][0] == 'name':
            self.query_by_name(inquiry['name'][0])
        else:
            self.query_by_value(inquiry)
