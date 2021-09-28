import Freelancer
import Validation as Valid
import FreelancerCollection
import sys

a = FreelancerCollection.FreelancerCollection()
a.link_to_file("text.txt")
a.read_from_file("test.txt")
a.sort()
print(a)
i = a.get_index(lambda f: f.id == "1551")
a.edit(i, "name", "DSds")
print(a)