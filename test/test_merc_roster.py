#!/usr/bin/env python3

import unittest

import merc_roster
# python -m unittest discover test


class TestUSS268Chars(unittest.TestCase):
 
  def test_base_data(self):
    jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:ACR"
    jakob = merc_roster.Char(jakob_data)
    self.assertTrue(jakob.first_name == 'Jakob')

  def test_base_weapon(self):
    weapon = merc_roster.make_weapon("9mmACR:GunCbt(CbtR):45 (6) +2:60 (3) +1: -")
    self.assertTrue(weapon.name       == '9mmACR')     
    self.assertTrue(weapon.skill      == 'GunCbt(CbtR)')     
    self.assertTrue(weapon.effective  == '45 (6) +2')     
    self.assertTrue(weapon.long       == '60 (3) +1')     
    self.assertTrue(weapon.extreme    == '-')     

  def test_skill_mod(self):
    jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:ACR"
    jakob = merc_roster.Char(jakob_data)
    self.assertTrue(jakob.skill_level("GunCbt(CbtR)") == 1)
    self.assertTrue(jakob.skill_level("Telling Jokes") == -3)

  def test_stat_modifier(self):
    jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:ACR"
    jakob = merc_roster.Char(jakob_data)
    self.assertTrue(jakob.stat_modifier(3) == 2)

  def test_combatant(self):
    person = merc_roster.Char("CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:ACR")
    weapon = merc_roster.make_weapon("9mmACR:GunCbt(CbtR):45 (6) +2:60 (3) +1: -")
    combatant = merc_roster.Combatant(person, weapon)
    self.assertTrue(combatant.key() == "Jakob")
    self.assertTrue(combatant.weapon_mod() == 2)

  def test_npc(self):
    npc = merc_roster.NPC("api_1:4:9mmACR")
    self.assertTrue(npc.key == "api_1")
    self.assertTrue(npc.morale == 4)
    self.assertTrue(npc.weapon == "9mmACR")
    self.assertTrue(npc.dex_mod == 0)
    self.assertTrue(npc.skill_level("nothing") == 1)

  def test_list_from_line(self):
    line      = "   9mmACR:  GunCbt(CbtR)   :  45 (6) +2  :   60 (3) +1   : -  "    
    sep       = ':'
    expected  = ["9mmACR", "GunCbt(CbtR)", "45 (6) +2", "60 (3) +1", "-"]
    result    = merc_roster.list_from_line(line, sep)
    self.assertTrue(result == expected)

if __name__ == "__main__":
  unittest.main()
