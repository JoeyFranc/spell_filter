import json
from enums import *
from source import get_source



""" Public Methods """

class Spell(object):

    def __init__(self, json_obj):
        
        # Default information
        self.name               = json_obj['name']
        self.source             = get_source(json_obj['page'])
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
        self.is_touch           = 'Touch' in self.range
        self.is_self            = 'Self' in self.range
        self.is_ritual          = json_obj['ritual'] == 'yes'
        self.is_instant         = "nstantaneous" in self.duration
        self.is_concentration   = json_obj['concentration'] == 'yes'
        self.higher_level       = json_obj.get('higher_level', None)
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
            if self.material:
                output += self.material
            output+='('+str(self.cost)+' gp)'
        return output

    def __str__(self):
        # The title
        output = _h1(self.name) + '\n\n'

        # Make the heading
        output += _h2('Level '+ str(self.level) + ' ' + self.school) + '\n\n'
        output += _h3(', '.join(self.classes) + ' spell.') + '\n\n'
        output += _p('Source:  ' + str(self.source)) + '\n\n'

        # Points of interest
        output += str(
            _p( _b('Casting Time: ')+str(self.casting_time) ) +'\n' +
            _p( _b('Range: ')+str(self.range) ) + '\n' +
            _p( _b('Components: ')+self._print_components() ) + '\n' +
            _p( _b('Duration: ')+str(self.duration) ) + '\n\n')

        # Add the description
        output += self.description

        # Add higher level
        if self.higher_level:
            output += self.higher_level

        return output

def get_spellbook(fn):
# Get a spellbook (dictionary) from file 'fn'

    with open(fn,'r') as json_file: 
        jsons = json.load(json_file)
        spellbook = []
        for json_obj in jsons:
            spellbook += [Spell(json_obj)]
        return spellbook   



""" Private Methods """

def _h1(string): return '<h1>'+string+'</h1>'
def _h2(string): return '<h2>'+string+'</h2>'
def _h3(string): return '<h3>'+string+'</h3>'
def _b(string): return '<b>'+string+'</b>'
def _p(string): return '<p>'+string+'</p>'


def _get_level(line):
# Convert a json level string to an integer
    level = ''.join(filter(lambda c: c.isdigit(), line))
    return int(level) if level else 0


SCHOOLS = set()
def _get_school(line):
# Convert a json value to a school of magic enum
    SCHOOLS.add(line)
    return line


CLASSES = set()
def _get_class(line):
    classes = set(line.split(','))
    CLASSES.add(classes)
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



if __name__ == '__main__':
    
    spellbook = get_spellbook('spells.json')
    for spell in spellbook: print(spell)
    print(spellbook[-1].classes)
