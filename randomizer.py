#!/usr/bin/env python3

# Copyright (c) 2019 David Callanan
# See `LICENSE` file for license details

#######################################
# IMPORTS
#######################################

import sys
import random
import argparse
import json

#######################################
# COMMAND-LINE INTERFACE
#######################################

# Default values

default_seed = None
default_config_fn = 'config.json'
default_output_fn = 'randomized-loot.zip'

# Parse arguments

parser = argparse.ArgumentParser(description='Random loot datapack generator for Minecraft')
parser.add_argument('-d', '--default', action='store_true', help='use default values instead of user input')
parser.add_argument('-s', '--seed', help='seed for randomizer')
parser.add_argument('-c', '--config', help='location of config file')
parser.add_argument('-o', '--output', help='output location of datapack')
args = parser.parse_args()

# Get values

use_defaults = args.default
if use_defaults:
	seed = args.seed or default_seed
	config_fn = args.config or default_config_fn
	output_fn = args.output or default_output_fn
else:
	if args.seed:
		seed = args.seed
	else:
		seed = input('Seed (random): ')
		seed = default_seed if seed == "" else seed
	
	if args.config:
		config_fn = args.config
	else:
		config_fn = input(f'Config file ({default_config_fn}): ')
		config_fn = default_config_fn if config_fn == "" else config_fn
	
	if args.output:
		output_fn = args.output
	else:
		output_fn = input(f'Output file ({default_output_fn}): ')
		output_fn = default_output_fn if output_fn == "" else output_fn

# Open files and parse config

try:
	config_file = open(config_fn)
except Exception as e:
	print(e)
	print("Error opening config file")
	sys.exit(1)

try:
	output_file = open(output_fn, 'w')
except Exception as e:
	print(e)
	print("Error opening output file")

try:
	with config_file:
		config = json.load(config_file)
except Exception as e:
	print(e)
	print("Error parsing config file")

# Generate datapack

with output_file:
	pass
	#generate_datapack(seed, config, output_file)
