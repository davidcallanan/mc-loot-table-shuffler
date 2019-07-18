#!/usr/bin/env python3

# Copyright (c) 2019 David Callanan
# See `LICENSE` file for license details

#######################################
# IMPORTS
#######################################

import sys
import os
import glob
import random
import argparse
import json
import zipfile
import hashlib
import io

#######################################
# DATAPACK GENERATOR
#######################################

def generate_datapack(seed, config, output_file, log):
	if config["target"] != "j1.14":
		log("config.target must be one of [\"j1.14\"]")
		return False

	seed = seed or random.randint(0, 2 ** 64 - 1)
	log("Using seed " + str(seed))
	shuffle_random = random.Random(seed)
	dup_file_random = random.Random(seed)
	
	loot_tables_path = os.path.join("targets", "j1.14", "loot_tables")
	shuffle_steps = []

	log("Globbing loot tables...")

	for shuffle_step_globs in config["shuffle_steps"]:
		shuffle_step = set()

		for glob_pattern in shuffle_step_globs:
			for filename in glob.iglob(os.path.join(loot_tables_path, glob_pattern)):
				shuffle_step.add(filename)

		shuffle_steps.append(shuffle_step)

	log("Randomizing duplicate files...")

	fixed_filenames = set()
	filenames_to_remove = []

	for shuffle_step_a in shuffle_steps:
		for filename in sorted(shuffle_step):
			if filename in fixed_filenames:
				continue
			fixed_filenames.add(filename)
			shuffle_steps_with_filename = []
			for shuffle_step_b in shuffle_steps:
				if filename in shuffle_step_b:
					shuffle_steps_with_filename.append(shuffle_step_b)
			if len(shuffle_steps_with_filename) > 1:
				weights = [1 / len(shuffle_step) for shuffle_step in shuffle_steps_with_filename]
				amount = len(shuffle_steps_with_filename) - 1
				steps = dup_file_random.choices(shuffle_steps_with_filename, weights, k=amount)
				filenames_to_remove.append((steps, filename))
	
	for steps, filename in filenames_to_remove:
		for step in steps:
			step.remove(filename)

	log("Shuffling loot tables...")

	filename_mappings = []

	for filenames in shuffle_steps:
		filenames = sorted(filenames)
		remaining_filenames = list(filenames)
		
		for filename in filenames:
			index = shuffle_random.randint(0, len(remaining_filenames) - 1)
			filename_mappings.append((filename, remaining_filenames[index]))
			del remaining_filenames[index]

	log("Generating datapack...")

	datapack_name = "randomized_loot_" + hashlib.sha256(json.dumps(config).encode("utf-8")).hexdigest()[0:4] + "_" + str(seed)

	zip_file_buffer = io.BytesIO()
	zip_file = zipfile.ZipFile(zip_file_buffer, 'w', zipfile.ZIP_DEFLATED, False)

	for orig_filename, new_filename in filename_mappings:
		with open(orig_filename, 'r') as orig_file:
			orig_file_data = orig_file.read()

		zip_file.writestr(os.path.join('data', 'minecraft', os.path.relpath(new_filename, 'targets/j1.14')), orig_file_data)

	zip_file.writestr('pack.mcmeta', json.dumps({
		"pack": {
			"pack_format": 1,
			"description": f"Randomized loot (seed: {seed})"
		}
	}, indent="\t"))
	
	zip_file.writestr('data/minecraft/tags/functions/load.json', json.dumps({
		"values": [
			f"{datapack_name}:init"
		]
	}, indent="\t"))

	zip_file.writestr(f'data/{datapack_name}/functions/init.mcfunction',
'''
tellraw @a ["",{"text":"Randomized loot loaded\\nDatapack id: ''' + datapack_name + '''","color":"gold"}]
tellraw @a ["",{"text":"github.com/davidcallanan/mc-loot-randomizer","color":"yellow","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.github.com/davidcallanan/mc-loot-randomizer"},"hoverEvent":{"action":"show_text","value":{"text":"","extra":[{"text":"Generator source code","color":"green"}]}}}]
'''
	)

	with open('LICENSE', 'r') as license_file:
		zip_file.writestr('LICENSE', license_file.read())

	zip_file.close()

	log("Saving datapack to file...")

	with output_file:
		output_file.write(zip_file_buffer.getvalue())

	log("Complete.")

#######################################
# COMMAND-LINE INTERFACE
#######################################

# Default values

default_seed = None
default_config_fn = 'config.json'
default_output_fn = 'randomized_loot.zip'

# Parse arguments

parser = argparse.ArgumentParser(description='Random loot datapack generator for Minecraft')
parser.add_argument('-d', '--default', action='store_true', help='use default values instead of user input')
parser.add_argument('-s', '--seed', type=int, help='seed for randomizer')
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
		seed = input('Seed (random): ').strip()
		try:
			seed = default_seed if seed == "" else int(seed)
		except:
			print("Seed must be of type int (non-decimal number)")
			sys.exit(1)
	
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
	print("Failed to open config file")
	sys.exit(1)

try:
	output_file = open(output_fn, 'wb')
except Exception as e:
	print(e)
	print("Failed to open output file")
	sys.exit(1)

try:
	with config_file:
		config = json.load(config_file)
except Exception as e:
	print(e)
	print("Failed to parse config file")
	sys.exit(1)

# Generate datapack

with output_file:
	is_success = generate_datapack(seed, config, output_file, print)
	if not is_success: sys.exit(1)
