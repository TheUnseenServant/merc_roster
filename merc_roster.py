#!/usr/bin/env python3

# name:     merc_roster.py
# version:  0.0.1
# date:     20220717
# author:   Leam Hall
# desc:     In game roster for SEMC troops and combat.

# Notes:
#  Datafiles are colon delmited

# TODO
#   Add text file input processing.
#   Think through end user experience.  
#   Error checking for input.
#   Add tests.
#   Process the skills


## Sample data that needs to be put into a text file.
# CPT:Jakob::Domici:m:7ABC56-7:32:4:Imperial Marines:Battledress-1, Blade-2, Demo-1, GunCbt(CbtR)-1, GunCbt(HighEWpns)-1, GunCbt(Laser)-2, GunCbt(Pistol)-0, HeavyWpns(GrenadeLauncher)-1, Instruction-2, Leader-2, Mechanic-1, Medic-1, Recon-1, Tactics-2:15

#SGT:Beauregard:Beau:Dawson:M:A78487:26:2:Imperial Marines:Leader-2, GunCbt(CbtR)-1, Cutlass-1, GunCbt(Pistol)-1:10

#PVT:Lovena:Love:Arcman:F:578898:22:1:Marine Infantry:GunCbt(CbtR)-2, Forward Observer-1, ZeroG-1, HvyWpn(VRF Gauss)-1, GravV-0, GunCbt(Pistol)-0:10

#PVT:George:Ginger:M:696673:22:1:Army Infantry:GunCbt(CbtR)-2, HvyWpn(HighEnergy)-1, Computer-1, Brawling-1, GravV-0, GunCbt(Pistol)-0, Demo-0, Recon-0:10

#:Liv:Mrs Domici:Ellis:F:898AA8-B:34:4:Imperial Navy:Animals-0, Admin-0, Medic-0, Streetwise-2, Drive(Grav)-1, Deception-2, Comm-1, Computer-1, Electronics(Intrusion)-1, Investigate-2, Recon-2, GunCbt(Pistol)-2, VaccSuit-0:?

class Weapon():
  def __init__(self, line = ''):
    self.make_data(line)

  def make_data(self, line):
    data          = line.split(':')
    self.name     = data[0]
    self.skill    = data[1]
    self.has_auto = data[2]
    self.short    = data[3]
    self.medium   = data[4]
    self.long     = data[5]


class Char():
  def __init__(self, data = ''):
    self.set_data(data)
 
  def set_data(self, data): 
    if len(data) > 2:
      data_a          = data.split(":")
      self.rank       = data_a[0]
      self.first_name = data_a[1]
      self.last_name  = data_a[2]
      self.nick_name  = data_a[3]
      self.gender     = data_a[4]
      self.upp        = data_a[5]
      self.age        = data_a[6]
      self.terms      = data_a[7]
      self.service    = data_a[8]
      self.skills     = data_a[9]
      self.morale     = data_a[10] if len(data_a) > 10 else 4
      self.looks      = data_a[11] if len(data_a) > 11 else ""
      self.weapons    = {}
      self.dex_mod    = self.stat_modifier(self.upp, 1)

  def format_string(self):
    if self.gender:
      self.gender = self.gender.upper()
    f_string = "{} {} ".format(self.rank, self.first_name)
    if self.nick_name:
      f_string += " {} ".format(self.nick_name)
    f_string += "{} [{}] {} Age {}\n".format( self.last_name, self.gender, self.upp, self.age)
    f_string += "{} terms {}\n".format(self.terms, self.service)
    f_string += "Skills {}\n".format(self.skills)
    f_string += "Morale: {}\n".format(self.morale)
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

  def stat_modifier(self, upp, index):
    stat = upp[index:index + 1].upper()
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

  def weapon_mod(self, skill):
    modifier = self.dex_mod + self.skill_level(skill)
    return modifier

  def skill_level(self, skill):
    return int(skill.split('-')[1])

  def add_weapon(self, weapon, skill):
    modifier = self.weapon_mod(skill)  # Just list the skill, have a skill array.
    self.weapons[weapon] = modifier



if __name__ == "__main__":

  weapons = {}
  # The lines needs to come from a text file
  lines = [
    "ACR:GunCbt(CbtR):yes:10/6:15/2:20/2",
    "Lacar:GunCbt(Laser):no:10/8:15/4:20/2",
  ]
  for line in lines:
    new_weapon = Weapon(line)
    weapons[new_weapon.name] = new_weapon
  
  jakob_data = "CPT:Jakob::Domici:m:7ABC56-7:32:4:Imperial Marines:Battledress-1, Blade-2, Demo-1, GunCbt(CbtR)-1, GunCbt(HighEWpns)-1, GunCbt(Laser)-2, GunCbt(Pistol)-0, HeavyWpns(GrenadeLauncher)-1, Instruction-2, Leader-2, Mechanic-1, Medic-1, Recon-1, Tactics-2:15"
  jakob = Char(jakob_data)
  jakob.add_weapon('ACR', 'GunCbt(CbtR)-1')
  jakob.add_weapon('Lacar', 'GunCbt(Laser)-2')
  
  print(jakob.format_string())

  
