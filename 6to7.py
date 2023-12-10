#!/usr/bin/env python

import sys
import os.path
import json

import numpy
import argparse
import twmap

example_text = '''example:

  6to7.py ~/.teeworlds/maps/dm1.map dm1_07.map'''
all_args = argparse.ArgumentParser(
                                 epilog=example_text,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
all_args.add_argument('-v', '--verbose',  help='verbose output')
all_args.add_argument('INPUT_MAP')
all_args.add_argument('OUTPUT_MAP')

args = vars(all_args.parse_args())

m = twmap.Map(args['INPUT_MAP'])

def replace_doodads(layer, mapping):
    progress = 0
    edited_tiles = layer.tiles
    for (y, x, flags), tile in numpy.ndenumerate(layer.tiles):
        progress += 1
        if progress % 100 == 0:
            print(x, y)
        if flags == 0:
            if str(tile) in mapping:
                edited_tiles[y][x][flags] = mapping[str(tile)]
    layer.tiles = edited_tiles

def get_mapping(image_name):
    mapping_path = f"./mappings/{image_name}.json"
    if os.path.isfile(mapping_path):
        with open(mapping_path) as f:
            return json.load(f)
    return None

for group in m.groups:
    for layer in group.layers:
        if layer.kind() != 'Tiles':
            continue
        img_name = m.images[layer.image].name
        print(img_name)
        mapping = get_mapping(img_name)
        if mapping:
            print(f"found {img_name} layer '{layer.name}'")
            replace_doodads(layer, mapping['mappings'])

m.save(args['OUTPUT_MAP'])

