import sys
sys.path.append('./src')
from lvs import LV
from rules import Rule
import numpy as np
from fuzzy import FuzzyMagic

"""Testing full library with Tip Problem"""

# Read the linguistic variables from file
lv = LV()
lv.read_lvs_from_file('./data/LV_Mamdani_example.json')

# Add them to the Fuzzy System (that is not created)
FS = lv.add_lvs_to_fs()

# Read the rules from file
rule = Rule()
# and add them to the Fuzzy System
rule.add_rules_from_file('./data/rule_example.txt')

FS = rule.add_rules_to_fs(FS)

# Set antecedents values
FS.set_variable("Service", 8)
FS.set_variable("Food", 8)

print(FS.produce_figure("./image.png"))

# Perform Mamdani inference and print output
print(FS.Mamdani_inference(["Tip"]))

# Or do a magic trick: 

FM = FuzzyMagic('./data/LV_Mamdani_example.json', './data/rule_example.txt')
FS = FM.do_magic()

# Set antecedents values
FS.set_variable("Service", 8)
FS.set_variable("Food", 8)

# Perform Mamdani inference and print output
print(FS.Mamdani_inference(["Tip"]))


# Creation of the rule file!
# FuzzyMagic.create_fuzzy_rules("./data/rule_creation_example.txt")

FM2 = FuzzyMagic('./data/LV_Mamdani_example.json', './data/rule_creation_example.txt')
FS2 = FM2.do_magic()

# Set antecedents values
FS.set_variable("Service", 8)
FS.set_variable("Food", 8)

# Perform Mamdani inference and print output
print(FS.Mamdani_inference(["Tip"]))