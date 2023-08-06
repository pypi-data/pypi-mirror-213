import sys
sys.path.append('./src')
from lvs import LV
from rules import Rule
import numpy as np

import json

lv = LV()
lv.read_lvs_from_file('./data/LV_Mamdani_example.json')

# print(lv.linguistic_variables)

FS = lv.add_lv_to_fs()

rule = Rule()

FS = rule.add_rules_from_file(FS, './data/rule_example.txt')

# Set antecedents values
FS.set_variable("Service", 8)
FS.set_variable("Food", 8)

print(FS.produce_figure("./image.png"))


# Perform Mamdani inference and print output
print(FS.Mamdani_inference(["Tip"]))