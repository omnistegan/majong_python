#!/bin/env python

from random import shuffle, choice

import hand

class Wall():

    def __init__(self):
        self.tiles = create_numbered_suits() + create_special_suits()
        shuffle(self.tiles)
        self.discard = []
        self.hands = []

    def deal(self):
        roll1 = die_roll() + die_roll()
        roll2 = die_roll() + die_roll()
        index = ((((roll1)*36)%144)-((roll1+roll2)*2))
        if index < 0:
            index += 144
        tile_sections = []
        dealt_tiles = [[],[],[],[]]
        for i in range(0, 48, 4):
            if index-(i+4) < 0 and index-i >= 0:
                tile_sections.append(self.tiles[index-(i+4):] + self.tiles[:index-i])
            else:
                tile_sections.append(self.tiles[index-(i+4):index-i])
        for i in range(49, 54):
            # Giving the wrong tiles here, pulling off the back wall, indexes are messes
            # If the index of the last non-empty space is odd,we can flip the last two
            # non-empty elements before taking?
            if (index-i) % 2 != 0:
                tile_sections.append([self.tiles[(index-i)-1]])
            else:
                tile_sections.append([self.tiles[(index-i)+1]])
        self.tiles[index-54] = {'name': '        '}
        for i in range(index-52, index):
            self.tiles[i] = {'name': '        '}
        for i in range(4):
            for each in tile_sections[i::4]:
                dealt_tiles[i].extend(each)
        for tiles in dealt_tiles:
            # Make a Hand object with each deal, the first one is always East (14 tiles)
            self.hands.append(hand.Hand(tiles))

    def print_tiles(self):
        for i in range(0, len(self.tiles), 2):
            print(self.tiles[i]['name'] + '\t\t--\t\t' + self.tiles[i+1]['name'])
            if (i+2) % 36 == 0:
                print()
        print()

    def print_hands(self):
        for each in self.hands:
            each.print_tiles()

def die_roll():
    return choice(range(6))+1

def create_tile(suit, id, name):
    """
    Suit: ['Characters', 'Dots', 'Bams', 'Winds', 'Dragons', 'Flowers']
    name: ['East wind', 'West wind', 'South wind', 'North wind']
          ['White dragon', 'Green dragon', 'Red dragon']
          ['Spring flower', 'Summer flower', 'Autumn flower',
           'Winter flower', 'Plum flower', 'Orchid flower',
           'Bamboo flower', 'Chrysanthemum flower']
          [1 of [suit], 2 of [suit], ...]
    id:   [1, 2, 3, 4, 5, 6, 7, 8, 9]       For numbered suits
          [0, 1, 2, 3, 4, 5, 6, 7]          For special suits

    A tile object is a dict with the key, value pairs:
        'suit' : string
        'id'   : int for numbered suits, string for special suits

    """
    return {'suit': suit, 'id': id, 'name': name}

def create_numbered_suit(suit_name):
    # Return a list of tile objects with ids 1 through 9 and suit : suit_name
    suit = []
    for i in range(1,10):
        for _ in range(4):
            suit.append(create_tile(suit_name, i, (str(i) + ' of ' + suit_name)))
    return suit

def create_special_suit(suit_name):
    # Return a list of tile objects with named ids and suit : suit_name
    suit = []
    if suit_name.startswith('W'):
        winds = ['East wind', 'South wind', 'West wind', 'North wind']
        for i, wind in enumerate(winds):
            for _ in range(4):
                suit.append(create_tile(suit_name, i, wind))
    elif suit_name.startswith('D'):
        dragons = ['White dragon', 'Green dragon', 'Red dragon']
        for i, dragon in enumerate(dragons):
            for _ in range(4):
                suit.append(create_tile(suit_name, i, dragon))
    elif suit_name.startswith('F'):
        flowers = ['Spring flower', 'Summer flower', 'Autumn flower',
                   'Winter flower', 'Plum flower', 'Orchid flower',
                   'Bamboo flower', 'Chrysanthemum flower']
        for i, flower in enumerate(flowers):
            suit.append(create_tile(suit_name, i, flower))
    return suit

def create_numbered_suits(numbered_suits=['Characters', 'Dots', 'Bams']):
    # Returns a list containing all tiles from all numbered suits
    return [item for sublist in list(map(create_numbered_suit, numbered_suits)) for item in sublist]

def create_special_suits(special_suits=['Winds', 'Dragons', 'Flowers']):
    # Returns a list containing all tiles from all special suits
    return [item for sublist in list(map(create_special_suit, special_suits)) for item in sublist]

wall = Wall()
wall.deal()
wall.print_tiles()
wall.print_hands()
