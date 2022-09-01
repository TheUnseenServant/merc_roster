#!/usr/bin/env python3

# name:     merc_roster.py
# version:  0.0.1
# date:     20220717
# author:   Leam Hall
# desc:     In game roster for SEMC troops and combat.

# Notes:
#  Datafiles are colon delmited

# TODO
#   Error checking for input.
#   Add verbose roster data.
#   Consider TOE layout.
#   Add loadouts.
#   [done] Add text file input processing.
#   [done] - Don't include headers or blank lines.
#   [done] Think through end user experience.  
#   [done] Add tests.
#   [done] Process and sort the skills
#   [done] Add a Builder

import argparse
import collections
import random

class Combatant():
  def __init__(self, person, weapon):
    self.person = person
    self.weapon = weapon

  def key(self):
    return self.person.key.strip()

  def weapon_mod(self):
    weapon_used   = self.person.weapon
    skill_needed  = self.weapon.skill
    modifier      = self.person.skill_level(skill_needed) + self.person.dex_mod
    return modifier

  def weapon_name(self):
    return self.weapon.name

  def format_string(self):
    return self.person.format_string()


class Char():
  def __init__(self, data = ''):
    self.set_data(data)
 
  def set_data(self, data): 
    if len(data) > 2:
      data_a          = data.split(":")
      self.rank       = data_a[0]
      self.first_name = data_a[1]
      self.last_name  = data_a[2]
      self.gender     = data_a[3]
      self.upp        = data_a[4]
      self.age        = data_a[5]
      self.terms      = data_a[6]
      self.service    = data_a[7]
      self.set_skills(data_a[8])
      self.morale     = data_a[9] if len(data_a) > 10 else 4
      self.key        = data_a[10]
      self.weapon     = data_a[11].strip() if len(data_a) > 10 else ""
      self.weapons    = {}
      self.dex_mod    = self.stat_modifier(1)

  def format_string(self):
    if self.gender:
      self.gender = self.gender.upper()
    f_string = "{} {} ".format(self.rank, self.first_name)
    f_string += "{} [{}] {} Age: {}  ".format( self.last_name, self.gender, self.upp, self.age)
    f_string += "Morale: {}  ".format(self.morale)
    f_string += "{} terms {}\n".format(self.terms, self.service)
    skill_string = ''
    for key in sorted(self.skills.keys()):
      if len(skill_string) > 1:
        skill_string += ", "
      skill_string  += "{}-{}".format(key, self.skills[key])
    f_string += "{}\n".format(skill_string)
    if len(self.weapons) > 0:
      counter = 0
      for weapon, skill in self.weapons.items():
        if counter > 0:
          f_string += ", " 
        if skill > 0:
          signed = "+"
        else:
          signed = ""
        f_string += "{} at {}{}".format(weapon, signed, skill )
        counter += 1
      f_string += "\n"
    return f_string

  def stat_modifier(self, index):
    stat = self.upp[index:index + 1].upper()
    if stat == 'F':
      mod = 3
    elif stat in ['C', 'D', 'E']:
      mod = 2
    elif stat in ['9', 'A', 'B']:
      mod = 1
    elif stat in ['3', '4', '5']:
      mod = -1
    elif stat in ['1', '2']:
      mod = -2
    else:
      mod = 0
    return mod

  def skill_level(self, skill):
    skill_mod = -3
    if skill in self.skills:
      skill_mod = self.skills[skill] 
    return skill_mod

  def set_skills(self, skill_string):
    self.skills   = {}
    skill_string  = skill_string.strip()
    skill_string  = skill_string.replace(',', ' ')
    for s in skill_string.split():
      key, value = s.split('-')
      self.skills[key.strip()] = int(value.strip())


def roll_2d6():
  return random.randint(1,6) + random.randint(1,6)

def show_roster(team):
  for person in team:
    print(person.format_string())

def build_team(file, weapons, sep = ':'):
  data = list_from_file(file)
  team = []
  for line in data:
    if line.count(sep) > 5:
      person = Char(line)
    weapon = weapons[person.weapon]    
    combatant = Combatant(person, weapon)
    team.append(combatant)
  return team
 
Weapon  = collections.namedtuple(
            'Weapon', ['name', 'skill', 'effective', 'long', 'extreme']
          )

def make_weapon(line, sep = ':'):
  return Weapon(*list_from_line(line, sep))

def build_weapons(file, sep = ':'):
  weapons = {}
  weapon_data = list_from_file(file)
  for line in weapon_data:
    new_weapon = make_weapon(line, sep)
    weapons[new_weapon.name] = new_weapon
  return weapons

def list_from_line(line, sep):
  data = line.split(sep)
  for index, item in enumerate(data):
    data[index] = item.strip()
  return data

def list_from_file(file):
  with open(file, 'r') as f:
    data  = []
    l     = f.readlines()
    for line in l:
      if line_clean(line):
        data.append(line)
  return data

def line_clean(line):
  line = line.strip()
  if len(line) < 5:
    return False
  if line[0] == '#':
    return False
  if line[0] == '/':
    return False
  return True


def roll_attacks(header, team):
  attack_strings = []
  for member in team:
    roll          = roll_2d6()
    modified_roll = roll + member.weapon_mod()
    long_roll     = modified_roll - 2
    extreme_roll  = long_roll - 2
    attack_strings.append("{:<14} {:3}    {:10} Effective:  {:2} [{:10}]  Long: {:2} [{:12}]  Extreme: {:2} [{:10}] ".format(
      member.key(), roll, member.weapon_name(), modified_roll, member.weapon.effective,
      long_roll, member.weapon.long, extreme_roll, member.weapon.extreme
      ))
  print(header)
  for s in attack_strings:
    print(" ", s)

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--attack', action = "store_true")
  args  = parser.parse_args()

  weapons   = build_weapons('data/weapons.txt')
  #semc_data = list_from_file('data/semc.txt')
  #npc_data  = list_from_file('data/npcs.txt')

  semc = build_team('data/semc.txt', weapons, sep = ':')
  npcs = build_team('data/npcs.txt', weapons, sep = ':')

  if args.attack:
    roll_attacks("== SEMC rolls", semc)
    print()
    roll_attacks("== API rolls", npcs)
  else:
    show_roster(semc)


  
