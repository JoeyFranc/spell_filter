import read
import json
import bisect
from enums import *


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
    'cost'
    'level'
]


class Inquiry(dict):

    # For each key specified, init the value
    def __init__(self, json_obj):
        for key in ENUM_KEYS+BOOL_KEYS+INT_KEYS:
            self[key] = json_obj[key]


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
            self.enums[enum_name] = [[]] * size  # Init to N empty arrays


    # Add an index to correct enum array if spell[i].enum is defined
    def _add_enums(self, spell, i)

        # Add this spell to appropriate array if attr is defined
        value = getattr(spell, enum_name)
        if value is not None:
            self.enums[enum_name][value] += [i]


    # Return all spells that meet each enum inquiry
    def _get_enums(self, inquiry):

        # Everything matches null inquiry
        matches = [i for i in range(len(self.spellbook))]

        for (enum_name, size) in ENUM_KEYS:
            # This field has a valid inquiry
            value = inquiry[enum_name]
            if value is not None and value < size:
                # Get intersection of matches and new enum matches
                matches = [ match for match in matches
                            if match in self.enums[enum_name][value] ]

        return matches


    # Init an empty array for each bool
    def _init_bools(self):

        self.bools = {}
        for bool_name in BOOL_KEYS:
            self.bools[bool_name] = []


    # Add this index iff spell.bool is True for EVERY bool
    def _add_bool(self, spell, i):
        
        # Add all non-None types
        for bool_name in BOOL_KEYS:
            value = getattr(spell, bool_name)
            if value is not None:
                self.bools[bool_name] += [(value,i)]  # (Truth value, index)


    # Return all bools that match the inquiry
    def _get_bools(self, inquiry):

        matches = None

        for bool_name in BOOL_KEYS:
            # Init to everything
            if matches is None:
                matches = self.bools[bool_name] 

            # This field has a valid inquiry
            value = inquiry[bool_name]
            if value is not None:
                # Get intersection of matches and new bool matches
                matches = [ match for match in matches
                            if match in self.bools[bool_name][0] == value ]

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

        for key in INT_KEYS:
            self.ranges[key].sort()


    def _get_ranges(self, inquiry):

        # Special init
        matches = None

        # For every key
        for key in inquiry:
            if key in INT_KEYS:

                # Init the matches here due to tuple values in range arrays
                if matches is not None:
                    matches = self.ranges[key]

                # Get specified range and lb and rb
                min_val, max_val = inquiry[key]
                lb = bisect.bisect_left(self.ranges[key], min_val)
                rb = bisect.bisect(self.ranges[key], max_val)
                matches = [ match for match in matches
                            if match in self.ranges[key][lb:rb]


    # Init a spell filter from a json file
    def __init__(self, data_file='spells.json'):

        # Init values
        self.spellbook = read.get_spellbook(data_file)
        self.display = []

        # Indexes
        self._init_spell_idx()
        self._init_enums()
        self._init_bools()

        # Fill indexes
        i = 0
        for spell in self.spellbook:
            self._add_spell_idx(spell, i)
            self._add_enums(spell, i)
            self._add_bools(spell, i)
            self._add_ranges(spell, i)
            i += 1
        self._sort_ranges()

    def query_by_name(self, names)

        # Clear display if instructed
        if inquiry[IS_RESET]: self.display = []

        # Do some minor input cleaning, first
        for name in names.split(',')
            name = name.strip().lower()
            if name in self.spell_idx:
                self.display += [ self.spellbook[self.spell_idx[name]] ]

    # Update display based on inquiry
    def filter(self, inquiry):

        # Clear display if instructed
        if inquiry[IS_RESET]: self.display = []

        # Get all matches
        enums = self._get_enums()
        bools = self._get_bools()
        ranges = self._get_ranges()
        matches = [match for match in enums if match in bools and match in ranges]

        # Update display
        for match in matches:
            if match not in self.display:
                self.display += [match]
