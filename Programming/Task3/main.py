import Validation as Valid
import FreelancerCollection
from fuzzywuzzy import fuzz

Str1 = "1234"
Str2 = ""
Ratio = fuzz.partial_ratio(Str1.lower(),Str2.lower())
print(Ratio)