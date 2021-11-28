import unittest
from copy import deepcopy

from FreelancerCollection import FreelancerCollection


class FreelancerCollectionTest(unittest.TestCase):
    empty = FreelancerCollection()
    from_file = [
        "1231 Roman mirkr37@gmail.com +380682017118 24 300 devops",
        "1331 Marko mazepa@ukr.net +78475639567 30 500 Be developer",
        "1531 Oleg shaldenialapski@gmail.com +48685636563 12 200 Fe developer",
        "1551 Denial hmazepa@gmail.com +380546753456 6 440 devops",
        "1553 denial denialmazepa@gmail.com +380546753456 6 440 devops",
        "1552 Denial denialmazepa@gmail.com +380546753456 6 440 devops"]

    def setUp(self) -> None:
        pass

    def test_add(self):
        local = deepcopy(self.empty)
        self.assertRaises(ValueError, local.add, 0)
        self.assertRaises(ValueError, local.add, "id name number email avail payment devops")
        self.assertIsNone(local.add("1552 Denial denialmazepa@gmail.com +380546753456 6 440 devops"))
        self.assertEquals(str(local[0]), "1552 Denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps")
        self.assertEquals(local.get_index(lambda f: f.id == '1552'), 0)

    def test_read_file(self):
        local = FreelancerCollection()
        manual = FreelancerCollection()
        manual.add_from_array(self.from_file)
        self.assertRaises(FileNotFoundError, local.read_from_file, "unexistpath.unexist")
        self.assertIsNone(
            local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt"))
        self.assertEquals(local, manual)
        local = FreelancerCollection()
        self.assertIsNone(local.read_from_file("/home/roman/Desktop/ProgramingHomework"
                                                "/Programming/Task3/test_file_error.txt"))
        self.assertEquals(local[0].__str__(), "1331 Marko mazepa@ukr.net +78475639567 30 500.0 BE Developer")

    def test_search(self):
        suggested = ['1531 Oleg shaldenialapski@gmail.com +48685636563 12 200.0 FE Developer',
                     '1551 Denial hmazepa@gmail.com +380546753456 6 440.0 DevOps',
                     '1553 denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps',
                     '1552 Denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps']
        local = FreelancerCollection()
        local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt")
        search_res = local.find_all("denial")
        self.assertEquals(len(search_res), len(suggested))
        for i, j in zip(search_res, suggested):
            self.assertEquals(i, j)
        self.assertEquals(local.find_all("qweweteyr"), [])

    def test_sort(self):
        suggested_list = [
            '1551 Denial hmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1553 denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1552 Denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1331 Marko mazepa@ukr.net +78475639567 30 500.0 BE Developer',
            '1531 Oleg shaldenialapski@gmail.com +48685636563 12 200.0 FE Developer',
            '1231 Roman mirkr37@gmail.com +380682017118 24 300.0 DevOps']
        suggested = FreelancerCollection()
        suggested.add_from_array(suggested_list)
        local = FreelancerCollection()
        local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt")
        self.assertIsNone(local.sort(lambda a: a.name.lower()))
        self.assertEquals(local, suggested)

    def test_delete(self):
        suggested_list = [
            "1231 Roman mirkr37@gmail.com +380682017118 24 300 devops",
            "1331 Marko mazepa@ukr.net +78475639567 30 500 Be developer",
            "1531 Oleg shaldenialapski@gmail.com +48685636563 12 200 Fe developer"]
        suggested = FreelancerCollection()
        suggested.add_from_array(suggested_list)
        local = FreelancerCollection()
        local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt")
        self.assertIsNone(local.delete(lambda b: b.name.lower() != "denial"))
        self.assertEquals(local, suggested)

    def test_edit(self):
        suggested_list = [
            "1231 Roman mirkr37@gmail.com +380682017118 24 300 devops",
            "1111 Pablo mazepa@ukr.net +78475639567 30 500 Be developer",
            "1531 Oleg shaldenialapski@gmail.com +48685636563 12 200 Fe developer",
            "1551 Denial hmazepa@gmail.com +380546753456 6 440 devops",
            "1553 denial denialmazepa@gmail.com +380546753456 6 440 devops",
            "1552 Denial denialmazepa@gmail.com +380546753456 6 440 devops"]
        suggested = FreelancerCollection()
        suggested.add_from_array(suggested_list)
        local = FreelancerCollection()
        local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt")
        self.assertRaises(ValueError, local.edit, *(1, "_Freelancer__id", "1531"))
        self.assertIsNone(local.edit(1, "_Freelancer__id", "1111"))
        self.assertIsNone(local.edit(1, "_Freelancer__name", "Pablo"))
        self.assertEquals(local, suggested)

    def test_undo_redo(self):
        begin = FreelancerCollection()
        begin.add_from_array(self.from_file)
        modified_list = [
            '1551 Denial hmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1553 denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1552 Denial denialmazepa@gmail.com +380546753456 6 440.0 DevOps',
            '1331 Marko mazepa@ukr.net +78475639567 30 500.0 BE Developer',
            '1531 Oleg shaldenialapski@gmail.com +48685636563 12 200.0 FE Developer',
            '1231 Roman mirkr37@gmail.com +380682017118 24 300.0 DevOps']
        modified = FreelancerCollection()
        modified.add_from_array(modified_list)
        local = FreelancerCollection()
        local.read_from_file("/home/roman/Desktop/ProgramingHomework/Programming/Task3/test_file.txt")
        local.sort(lambda a: a.name.lower())
        self.assertEquals(local, modified)
        self.assertIsNone(local.undo())
        self.assertEquals(local, begin)
        self.assertIsNone(local.redo())
        self.assertEquals(local, modified)


if __name__ == "__main__":
    unittest.main()
