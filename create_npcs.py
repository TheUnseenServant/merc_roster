#!/usr/bin/env python3

# name:     create_npcs.py
# version:  0.0.1
# date:     20220901
# author:   Leam Hall
# desc:     Produce a list of generic NPCs.

# Notes:
#  Datafiles are colon delmited

# TODO
#   Verify the weapons against the data.

import argparse
import os.path

def list_from_file(file):
    """ Takes a file and returns a list of non-empty, uncommented lines """
    new_list = list()
    with open(file, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line:
                new_list.append(line)
    return new_list  

def create_weapons_skills(list_):
    """ Takes a colon separated list, and returns a dict with list[0] as key and list[1] as value """
    weapons = dict()
    for item in list_:
        weapon, skill, *rest = item.split(':')
        weapons[weapon.strip()] = skill.strip()
    return weapons

base_string = "PVT:::M:777777:22:1::{}-1:7:{}:{}"

if __name__ == "__main__":

    datadir = "data"
    weapons_file = os.path.join(datadir, "weapons.txt")
    weapons_list = list_from_file(weapons_file)
    weapon_skills = create_weapons_skills(weapons_list)
    help_epilog = "Useable weapons: " +  ', '.join(sorted(weapon_skills.keys()))

    parser = argparse.ArgumentParser(epilog = help_epilog)
    parser.add_argument("-c", "--count", help = "Count of npcs (default 10)", type = int, default = 10)
    parser.add_argument("-w", "--weapon", help = "Weapon (default 7mmAK)", type = str, default = "7mmAK")
    args = parser.parse_args()

    if args.weapon in weapon_skills.keys():
        # This assumes the relevant skill is also present.
        weapon = args.weapon
        skill = weapon_skills[weapon]
    else:
        weapon = "7mmAK"
        skill = "GunCbt(CbtR)"

    for x in range(args.count):
        ident = "npc_" + str(x)
        print(base_string.format(skill, ident, weapon))

