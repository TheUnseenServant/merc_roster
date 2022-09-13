#!/usr/bin/env python3

import io
import os
import sys
import tempfile
import unittest

import merc_roster

class TestMercRoster(unittest.TestCase):
 
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

        self.team_file = os.path.join(self.test_dir.name, 'team.txt')
        with open(self.team_file, 'w') as f:
            f.write("CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR\n")
            f.write("LT:Liv:Ellis:F:898AA8-B:34:4:Imperial Navy:GunCbt(Pistol)-2:13:Mrs Domici:4mmGaussP\n")

        self.weapons_file = os.path.join(self.test_dir.name, 'weapons.txt')
        with open(self.weapons_file, 'w') as f:
            f.write("9mmACR:GunCbt(CbtR):45 (6) +2:60 (3) +1: -\n")
            f.write("4mmGaussP:GunCbt(Pistol):20 (4): 40 (3): 60 (1)\n")

        self.weapons = merc_roster.build_weapons(self.weapons_file)
        self.team = merc_roster.build_team(self.team_file, self.weapons)

    def tearDown(self):
        self.test_dir.cleanup()


    def test_base_data(self):
        jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR"
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
        jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR"
        jakob = merc_roster.Char(jakob_data)
        self.assertTrue(jakob.skill_level("GunCbt(CbtR)") == 1)
        self.assertTrue(jakob.skill_level("Telling Jokes") == -3)

    def test_stat_modifier(self):
        jakob_data = "CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR"
        jakob = merc_roster.Char(jakob_data)
        self.assertTrue(jakob.stat_modifier(3) == 2)

    def test_combatant(self):
        person = merc_roster.Char("CPT:Jakob:Domici:m:7ABC56-7:32:4:Imperial Marines:GunCbt(CbtR)-1:15:Jakob:9mmACR")
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
        data = merc_roster.list_from_file(self.team_file)
        self.assertTrue(len(data) == 2)
        self.assertTrue(data[1].startswith('LT'))

    def test_roll_attacks(self):
        attacks = merc_roster.roll_attacks(self.team)
        self.assertTrue(len(attacks) == 2)
        self.assertTrue("Extreme" in attacks[0])

    def test_build_weapons(self):
        weapons = merc_roster.build_weapons(self.weapons_file)
        self.assertTrue("9mmACR" in weapons.keys())

    def test_build_team(self):
        self.assertTrue(len(self.team) == 2)
        self.assertIsInstance(self.team[0], merc_roster.Combatant)

    def test_print_attack_rounds(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        merc_roster.print_attack_rounds(self.team, "Domici", 1)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertTrue("Domici" in output)

if __name__ == "__main__":
    unittest.main()
