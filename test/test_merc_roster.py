#!/usr/bin/env python3

import unittest

import merc_roster
# python -m unittest discover test

class TestUSS268Chars(unittest.TestCase):
 
  def test_base_data(self):
    jakob_data = "CPT:Jakob::Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15"
    jakob = merc_roster.Char(jakob_data)
    jakob.add_weapon('ACR', 'GunCbt(CbtR)-1')
    self.assertTrue(jakob.first_name == 'Jakob')

  def test_base_weapon(self):
    weapon = merc_roster.Weapon("ACR:GunCbt(CbtR):yes:10/6:15/2:20/2")
    self.assertTrue(weapon.name     == 'ACR')     
    self.assertTrue(weapon.skill    == 'GunCbt(CbtR)')     
    self.assertTrue(weapon.has_auto == 'yes')     
    self.assertTrue(weapon.short    == '10/6')     
    self.assertTrue(weapon.medium   == '15/2')     
    self.assertTrue(weapon.long     == '20/2')     

if __name__ == "__main__":
  unittest.main()
