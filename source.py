# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:19:49 2018

@author: jfranc
"""
SOURCES_FILE_NAME = 'sources.config'
SOURCES_DELIMITER = '\category'
SOURCE_CLASSNAME_MAP = {
    ' ' : '_'
}


class Source(object):
    """
    Defines a source of a D&D spell.  This includes the page number and any
    relevant characteristics defined by SOURCES_FILE_NAME.
    
    This is the abstract class that all actual source classes inherit from.
    """
    def __init__(self, page_number):
        """
        Remember the page number this spell is cited from.  (Only the page
        number is specific to spell instances).
        
        PARAMETERS
        (int) page_number - The page number of this citation.
        """
        self.page_number = page_number


def _get_class_name(source_name):
    """
    Converts a normal name into a valid python class name.
    (e.g. 'ee uu' -> 'EE_UU')
    
    PARAMETERS
    (str) source_name - The name to convert.
    
    RETURNS (str)
    A valid python name string.
    """
    return source_name.lower().strip().translate(SOURCE_CLASSNAME_MAP)


def _get_class(class_name, **kwargs):
    """
    Creates a source class with class (aka python-static) variables defined by
    the kwargs dictionary.
    
    PARAMETERS
    (str) class_name - The name of the class.
    (dict) **kwargs - (variable_name, value) pairs.
    
    RETURNS (type)
    A customized Python class object.
    """
    return type(class_name, (Source,), kwargs)


def _get_mapping(attributes, column_names):
    """
    Helper function for returning (name: class) pairs.
    Given a list of attributes and column_names, create a name class mapping.
    
    PARAMETERS
    (list<str>) attributes - The value for each attribute.  The first MUST be
        the name.
    (list<str>) column_names - The corresponding attribute name for each
        attribute in attributes.  This MUST be the same length as attributes.
    
    RETURNS (tuple(str, type))
    A single entry in the name to class mapping.
    """
    source_name = attributes[0]
    return (source_name, _get_class(
        _get_class_name(source_name),
        zip(attributes[1:], column_names[1:])))


def _read_table(source_table, column_names):
    return map(
        # Make (name, class) doubles from attribute touples
        lambda attributes: tuple(
            attributes[0],
            _get_mapping(attributes, column_names)),
        # Get a tuple of all attributes for each line in the document
        map(lambda line: tuple(map(
                # Remove whitespace around the delimiter
                lambda datum: datum.strip(),
                line.split(SOURCES_DELIMITER))),
            source_table))


def load_sources(file_name):
    """
    Creates a mapping from the source table defined in config file, file_name,
    of source names to classes representing that source.
    
    PARAMETERS
    (str) file_name - The location of the config file.
    
    RETURNS (dict(str: subtype_of:Source))
    A dictionary of all defined sources in the config file.
    """
    with open(file_name, 'rb') as source_file:
        column_names = source_file.readline()  # First line is the column names
        return _read_table(source_file, column_names)


SOURCE_CLASSES = load_sources(SOURCES_FILE_NAME)
