import json
from enums import *



class Unknown_Value(Exception):
    def __init__(self, kind, value):
        self.kind   = kind
        self.source = value
    def __str__(self): return 'Unknown '+self.kind+':\n'+self.source



def _get_source(line):
# line is a json string containing the source name. returns source enum

    if   'phb'  in line: return PHB
    elif 'ee'   in line: return EE
    elif 'scag' in line: return SCAG
    elif 'trot' in line: return TROT
    elif 'ua'   in line: return UA

    raise Unknown_Value('spell source', line)

def _get_level(line):
# Convert a json value to an integer

    if 'antrip' in line: return 0
    for char in line:
        if char.isdigit(): return int(char)

    raise Unknown_Value('level', line)

def _get_school(line):
# Convert a json value to a school of magic enum

    if   'bjuration' in line:       return ABJURATION
    elif 'onjuration' in line:      return CONJURATION
    elif 'ivination' in line:       return DIVINATION
    elif 'nchantment' in line:      return ENCHANTMENT
    elif 'vocation' in line:        return EVOCATION
    elif 'llusion' in line:         return ILLUSION
    elif 'ecromancy' in line:       return NECROMANCY
    elif 'ransmutation' in line:    return TRANSMUTATION

    raise Unknown_Source('magic school', line)

def _get_class(line):
# Convert a json value into a list of class enums

    # 1. line.split converts to list of string representations of classes
    # 2. str2class turns a string representation into an enum
    # 3. Use str2class on every string in line.split(',')
    classes = []
    for string_repr in line.split(','):
        string_repr = string_repr.lstrip()
        string_repr = string_repr.rstrip()
        classes += [str2class(string_repr)]
    return classes

def _is_cost_valid(char):

    return char.isdigit() or char != ' ' or char != ','

def _get_cost(material):
# Converts a material description to a cost (int representing gp)

    end = material.find('gp')
    # Dummy check.  There is no cost
    if end == -1: return 0

    # Extract the (reversed) string representing the int of the cost
    i = end-1
    number = ''
    while True:
        # Add digits
        if material[i].isdigit(): number += material[i]
        # Ignore spaces and commas.  A different value is the term. condition
        elif (material[i] != ' ' and material[i] != ',') or i == 0: break
        i -= 1

    return int(number[::-1])

class Spell(object):

    def __init__(self, json_obj):
        
        # Default information
        self.name               = json_obj['name']
        self.source             = _get_source(json_obj['page'])
        self.description        = json_obj['desc']
        self.level              = _get_level(json_obj['level'])
        self.school             = _get_school(json_obj['school'])
        self.classes            = _get_class(json_obj['class'])
        self.casting_time       = json_obj['casting_time']
        self.range              = json_obj['range']
        self.v                  = 'V' in json_obj['components']
        self.s                  = 'S' in json_obj['components']
        self.m                  = 'M' in json_obj['components']
        self.duration           = json_obj['duration']

        # Other helpful tags
        self.is_touch           = 'Touch' in self.range
        self.is_self            = 'Self' in self.range
        self.ritual             = json_obj['ritual'] == 'yes'
        self.is_instant         = "nstantaneous" in self.duration
        self.is_concentration   = json_obj['concentration'] == 'yes'
        if 'higher_level' in json_obj:
            self.higher_level   = json_obj['higher_level']
        else:
            self.higher_level   = None
        if self.m and 'material' in json_obj:
            self.material       = json_obj['material']
            self.cost           = _get_cost(self.material)
        else:
            self.material       = None
            self.cost           = 0

    def _print_components(self):
        output = ''
        if self.v: output += 'V'
        if self.s: output += 'S'
        if self.m:
            output += 'M '
            if self.material: output += self.material
            output+='('+str(self.cost)+' gp)'
        if output: return output
        return 'None'

    def __str__(self):

        output = self.name + '\n\n' + 'Level '+str(self.level)
        for c in self.classes: output += ' '+class2str(c)
        output += ' '+school2str(self.school)+' spell from '+\
        v_source2string(self.source) + '\n\n'
        output += \
        'Casting Time: '+self.casting_time +'\n' + \
        'Range: '+self.range + '\n' + \
        'Components: '+self._print_components() + '\n'\
        'Duration: '+self.duration+'\n\n'+\
        self.description
        if self.higher_level: output += self.higher_level
        return output

def get_spellbook(fn):
# Get a spellbook (dictionary) from file 'fn'

    with open(fn,'r') as json_file: 
        jsons = json.load(json_file)
        spellbook = []
        for json_obj in jsons:
            spellbook += [Spell(json_obj)]
        return spellbook   

if __name__ == '__main__':
    
    spellbook = get_spellbook('spells.json')
    for spell in spellbook: print(spell)
    print(spellbook[-1].classes)
