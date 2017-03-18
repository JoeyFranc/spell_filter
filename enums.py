""" This file contains useful enums """

# Constants
NUM_SPELLS = 415

# source
PHB = 0
EE = 1
SCAG = 2
TROT = 3
UA = 4
SOURCE_SIZE = 5

# race
HUMAN = 0
DWARF = 1
ELF = 2
HAFLING = 3
DRAGONBORN = 4
GNOME = 5
HALF_ELF = 6
HALF_ORC = 7
TIEFLING = 8

# stat
STR = 0
DEX = 1
CON = 2
INT = 3
WIS = 4
CHA = 5

# classes
BARBARIAN = 0
BARD = 1
CLERIC = 2
DRUID = 3
FIGHTER = 4
MONK = 5
PALADIN = 6
RANGER = 7
ROGUE = 8
SORCERER = 9
WARLOCK = 10
WIZARD = 11
RITUAL_CASTER = 12
CLASSES_SIZE = 13

# school
ABJURATION = 0
CONJURATION = 1
DIVINATION = 2
ENCHANTMENT = 3
EVOCATION = 4
ILLUSION = 5
NECROMANCY = 6
TRANSMUTATION = 7
SCHOOL_SIZE = 8


class Invalid_Enum(Exception):

    def __init__(self, family, value):
        self.family = family
        self.value = value

    def __str__(self): return 'Attempted to find a class for ' + self.role


def v_source2str(source):
# Verbosely return a string describing a source

    if   source == PHB:     return 'Players Handbook'
    elif source == EE:      return 'Elemental Evil Player\'s Companion'
    elif source == SCAG:    return 'Sword Coast Adventurer\'s Guide'
    elif source == TROT:    return 'The Rise of Tiamat'
    elif source == UA:      return 'Unearthed Arcana'

    raise Invalid_Enum('Source Material', source)

def school2str( school ):
# Return the string representation of a school

    if   school == ABJURATION:      return 'Abjuration'
    elif school == CONJURATION:     return 'Conjuration'
    elif school == DIVINATION:      return 'Divination'
    elif school == ENCHANTMENT:     return 'Enchantment'
    elif school == EVOCATION:       return 'Evocation'
    elif school == ILLUSION:        return 'Illusion'
    elif school == NECROMANCY:      return 'Necromancy'
    elif school == TRANSMUTATION:   return 'Transmuation'

    raise Invalid_Enum('Magic School', school)

def str2class( string ):

    if   string == 'BARBARIAN' or string == 'barbarian' or string == 'Barbarian':   return BARBARIAN
    elif string == 'bard' or string == 'Bard' or string == 'BARD':                  return BARD
    elif string == 'cleric' or string == 'Cleric' or string == 'CLERIC':            return CLERIC
    elif string == 'druid' or string == 'Druid' or string == 'DRUID':               return DRUID
    elif string == 'figher' or string == 'Figher' or string == 'FIGHTER':           return FIGHTER
    elif string == 'monk' or string == 'Monk' or string == 'MONK':                  return MONK
    elif string == 'paladin' or string == 'Paladin' or string == 'PALADIN':         return PALADIN
    elif string == 'ranger' or string == 'Ranger' or string == 'RANGER':            return RANGER
    elif string == 'rogue' or string == 'Rogue' or string == 'ROGUE':               return RANGER
    elif string == 'sorcerer' or string == 'Sorcerer' or string == 'SORCERER':      return SORCERER
    elif string == 'warlock' or string == 'Warlock' or string == 'WARLOCK':         return WARLOCK
    elif string == 'wizard' or string == 'Wizard' or string == 'WIZARD':            return WIZARD
    elif string == 'ritual caster' or string == 'Ritual Caster' \
    or   string == 'RITUAL CASTER' or string == 'Ritual caster':                    return RITUAL_CASTER

    raise Invalid_Enum('Class',string)

def class2str( class_enum ):

    if   class_enum == BARBARIAN:     return 'Barbarian'
    elif class_enum == BARD:          return 'Bard'
    elif class_enum == CLERIC:        return 'Cleric'
    elif class_enum == DRUID:         return 'Druid'
    elif class_enum == FIGHTER:       return 'Figher'
    elif class_enum == MONK:          return 'Monk'
    elif class_enum == PALADIN:       return 'Paladin'
    elif class_enum == RANGER:        return 'Ranger'
    elif class_enum == ROGUE:         return 'Rogue'
    elif class_enum == SORCERER:      return 'Sorcerer'
    elif class_enum == WARLOCK:       return 'Warlock'
    elif class_enum == WIZARD:        return 'Wizard'
    elif class_enum == RITUAL_CASTER: return 'Ritual Caster'

    raise Invalid_Enum('Class',class_enum)
