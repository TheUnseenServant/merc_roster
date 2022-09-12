#!/usr/bin/env python3

import os
import tempfile
import unittest

import merc_roster

class TestUSS268Chars(unittest.TestCase):
 
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()


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

    def test_list_from_line(self):
        line      = "   9mmACR:  GunCbt(CbtR)   :  45 (6) +2  :   60 (3) +1   : -  "    
        sep       = ':'
        expected  = ["9mmACR", "GunCbt(CbtR)", "45 (6) +2", "60 (3) +1", "-"]
        result    = merc_roster.list_from_line(line, sep)
        self.assertTrue(result == expected)

    def test_list_from_file(self):
        test_file = os.path.join(self.test_dir.name, 'team.txt')
        with open(test_file, 'w') as f:
            f.write("CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:ACR\n")
            f.write("LT:Liv:Ellis:F:898AA8-B:34:4:Imperial Navy:GunCbt(Pistol)-2:13:Mrs Domici:4mmGaussP\n")
        data = merc_roster.list_from_file(test_file)
        self.assertTrue(len(data) == 2)
        self.assertTrue(data[1].startswith('LT'))

    def test_roll_attacks(self):
        pass

    def test_build_weapons(self):
        test_weapon_file = os.path.join(self.test_dir.name, 'weapons.txt')
        with open(test_weapon_file, 'w') as f:
            f.write("9mmACR:GunCbt(CbtR):45 (6) +2:60 (3) +1: -\n")
            f.write("4mmGaussP:GunCbt(Pistol):20 (4): 40 (3): 60 (1)\n")
        weapons = merc_roster.build_weapons(test_weapon_file)


    def test_build_team(self):
        pass
        test_weapon_file = os.path.join(self.test_dir.name, 'weapons.txt')
        with open(test_weapon_file, 'w') as f:
            f.write("9mmACR:GunCbt(CbtR):45 (6) +2:60 (3) +1: -\n")
            f.write("4mmGaussP:GunCbt(Pistol):20 (4): 40 (3): 60 (1)\n")
        weapons = merc_roster.build_weapons(test_weapon_file)
        test_file = os.path.join(self.test_dir.name, 'team.txt')
        with open(test_file, 'w') as f:
            f.write("CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR\n")
            f.write("LT:Liv:Ellis:F:898AA8-B:34:4:Imperial Navy:GunCbt(Pistol)-2:13:Mrs Domici:4mmGaussP\n")
        team = merc_roster.build_team(test_file, weapons)

if __name__ == "__main__":
    unittest.main()
