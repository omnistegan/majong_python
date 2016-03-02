#!/bin/env python

class Hand():

    def __init__(self, tiles):
        self.tiles = tiles
        self.exposed_tiles = []

    def print_tiles(self):
        for each in self.tiles:
            print(each['name'])
        print()
