# Minecraft Item Drops Randomizer

**Version**: 1.0.0-dev

Random item drops datapack generator for Minecraft, based on [SethBling's loot table randomizer](https://www.youtube.com/watch?v=3JEXAZOrykQ&t=22s) packed with more features.

Randomizable loot: block drops, mob drops, loot chests, fishing, treasure and more!

Suitable for UHC, speedruns, survival and more!

## Start Randomizing

The following dependencies must be installed on your system:
 - [Python3](https://www.python.org/downloads/)

Simply run `randomizer.py` via Python3 or in the terminal using `python3 randomizer.py`.

## Compatible Minecraft Versions

Following are the Minecraft versions which have been checked to be compatible with this script. Missing versions may still be compatible. Please submit a pull request if you have tested a missing version.

 - Minecraft Java Edition 1.14 - `"j1.14"`

See [Config/Target](#target) to find out how to change your target Minecraft version.

## Config

This script's configuration is found inside `config.json` or another file if specified via the [CLI](#command-line-interface).

### Target

The `"target"` property changes what version of Minecraft should be targeted. Feel free to submit a pull request to add support for more targets. Available options:

 - `"j1.14"`

See [Compatible Minecraft Versions](#compatible-minecraft-versions) to determine what versions are supported

### Shuffle

The `"shuffle"` property specifies a list of shuffle steps and which loot tables to be shuffled in each step.

This allows you to:

 - Shuffle a custom selection of loot tables instead of all the loot tables.
 - Shuffle different loot tables separately. For example, you can shuffle block drops separately from mob drops or chest loot.

The value should be a list of [Shuffle Steps](#shuffle-step).

#### Shuffle Step

Each shuffle step is a list of strings, where each string is a [glob](https://en.wikipedia.org/wiki/Glob_%28programming%29) of loot table files to be included in that shuffle step.

Globs may begin with `!` to exclude files.

The root glob folder is `targets/j1.14/loot_tables`.

## Command-line Interface

Syntax: `python3 randomizer.py [config_file] [output_file] [seed]`

 - `config_file`
   - Sets the location of the configuration file
   - Default value: `config.json`
 - `output_file`
   - Sets the output location of the datapack
   - A number will be added to the end of the filename if a file with that name already exists
   - Default value: `randomized-block-drops-datapack.zip`
 - `seed`
  - Sets the seed for the randomized datapack generation
  - Default value: random

## License

See `LICENSE` file.
