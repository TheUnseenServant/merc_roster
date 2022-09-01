# test_create_npcs.py

import os.path
import tempfile
import unittest

import create_npcs

class TestCreateNPCs(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "weapons.txt")
        with open(self.test_file, 'w') as fh:
            fh.write("# comment line\n")
            fh.write("\n")  # empty line that should be stripped out.
            fh.write("9mmACR:GunCbt(CbtR):450 (6) +2:600 (3) +1: -\n") 

    def tearDown(self):
        self.test_dir.cleanup()

    def test_string(self):
        expected = "PVT:::M:777777:22:1::GunCbt(CbtR)-1:7:npc_1:7mmAK"
        result = create_npcs.base_string.format("GunCbt(CbtR)", "npc_1", "7mmAK")
        self.assertTrue(result == expected)

    def test_list_from_string(self):
        list_ = create_npcs.list_from_file(self.test_file)
        self.assertTrue(len(list_) == 1)
        self.assertTrue(list_[0].startswith('9mmACR'))

    def test_create_weapons_skills(self):
        list_ = create_npcs.list_from_file(self.test_file)
        weapons = create_npcs.create_weapons_skills(list_)
        self.assertTrue(weapons['9mmACR']) 
        self.assertTrue(weapons['9mmACR'] == "GunCbt(CbtR)")
        self.assertFalse('6mmACR' in weapons.keys()) 

