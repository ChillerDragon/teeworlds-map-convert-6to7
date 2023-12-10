#!/usr/bin/env python

import os.path
import sys
import json
import argparse

import numpy
import twmap # type: ignore

EXAMPLE_TEXT = '''example:

  6to7.py ~/.teeworlds/maps/dm1.map dm1_07.map'''
all_args = argparse.ArgumentParser(
                                 epilog=EXAMPLE_TEXT,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
all_args.add_argument('-v', '--verbose',  help='verbose output')
all_args.add_argument('-s', '--strict',  help='fail instead of best effort translation on edge case doodads')
all_args.add_argument('INPUT_MAP')
all_args.add_argument('OUTPUT_MAP')

args = vars(all_args.parse_args())

def dbg(msg):
    if not args['verbose']:
        return
    print(msg)

def replace_doodads(layer, mapping):
    progress = 0
    edited_tiles = layer.tiles
    for (y, x, flags), tile in numpy.ndenumerate(layer.tiles):
        progress += 1
        if progress % 100 == 0:
            print(x, y)
        if flags == 0:
            if str(tile) in mapping:
                warn = f"{tile}_warn"
                if warn in mapping:
                    print(f"Warning: {mapping[warn]}")
                    if args['strict']:
                        print('abort on warning because strict mode is active')
                        sys.exit(1)
                edited_tiles[y][x][flags] = mapping[str(tile)]
    layer.tiles = edited_tiles

def get_mapping(image_name, direction):
    mapping_path = f"./mappings/{direction}_{image_name}.json"
    if os.path.isfile(mapping_path):
        with open(mapping_path, encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    m = twmap.Map(args['INPUT_MAP'])
    for group in m.groups:
        for layer in group.layers:
            if layer.kind() != 'Tiles':
                continue
            img_name = m.images[layer.image].name
            dbg(img_name)
            mapping = get_mapping(img_name, '6to7')
            if mapping:
                print(f"translating {img_name} layer '{layer.name}'")
                replace_doodads(layer, mapping['mappings'])

    m.save(args['OUTPUT_MAP'])

main()
