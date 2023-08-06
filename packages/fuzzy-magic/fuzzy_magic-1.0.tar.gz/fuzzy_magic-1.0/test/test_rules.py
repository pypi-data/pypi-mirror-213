from simpful import *
import sys
sys.path.append('./src')
from rules import Rule
import unittest
from exceptions import InvalidRuleException

class TestRule(unittest.TestCase):
    rule = Rule()
    def test_no_consequent(self, line):
        with self.assertRaises(InvalidRuleException):
            rule.check_rule(line)
    
    def test_no_antecedent(self, line):
        with self.assertRaises(InvalidRuleException):
            rule.check_rule(line)
    
    def test_no_value(self, FS, name, value):
        with self.assertRaises(InvalidRuleException):
            rule.is_defined(FS, name, value)
    
    def test_no_then(self, line):
        with self.assertRaises(InvalidRuleException):
            rule.check_rule(line)

    def test_no_if(self, line): 
        with self.assertRaises(InvalidRuleException):
            rule.check_rule(line)
    
    def test_no_capital(self, line):
         with self.assertRaises(InvalidRuleException):
            rule.check_rule(line)
    def test_true(self, line): 
        self.assertTrue(rule.check_rule(line), "Test Failed")
"""
    Tipping problem with automatic rule creation from file
"""
                        
FS = FuzzySystem()

# Define fuzzy sets and linguistic variables
S_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=5), term="poor")
S_2 = FuzzySet(function=Triangular_MF(a=0, b=5, c=10), term="good")
S_3 = FuzzySet(function=Triangular_MF(a=5, b=10, c=10), term="excellent")
FS.add_linguistic_variable("Service", LinguisticVariable([S_1, S_2, S_3], concept="Service quality", universe_of_discourse=[0,10]))

F_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=10), term="meh")
F_2 = FuzzySet(function=Triangular_MF(a=0, b=10, c=10), term="awesome")
FS.add_linguistic_variable("Food", LinguisticVariable([F_1, F_2], concept="Food quality", universe_of_discourse=[0,10]))

# Define output fuzzy sets and linguistic variable
T_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=10), term="small")
T_2 = FuzzySet(function=Triangular_MF(a=0, b=10, c=20), term="average")
T_3 = FuzzySet(function=Trapezoidal_MF(a=10, b=20, c=25, d=25), term="generous")
FS.add_linguistic_variable("Tip", LinguisticVariable([T_1, T_2, T_3], universe_of_discourse=[0,25]))

rule = Rule()
tr = TestRule()

tr.test_true("IF (Service IS poor) THEN (Tip IS small)") #Easiest type of rule 
tr.test_no_consequent("IF (Service IS poor) THEN ") # No consequent testing
tr.test_no_antecedent("IF THEN (Tip IS small)")# No antecedent testing
tr.test_true("IF (Service IS poor) OR (Food IS meh) THEN (Tip IS small)") # Two antecedents test
tr.test_true("IF (Service IS poor) THEN (Tip IS small) OR (Tip IS average)")# Two consequents test
tr.test_no_value(FS, 'Service', 'low') #No Service IS low in fuzzy set
tr.test_no_then("IF (Service IS low) OR (Tip IS small)") # There is no THEN
tr.test_no_if("(Service IS low) THEN (Tip IS small)")
tr.test_no_capital("IF (Service is low) THEN (Tip IS small)") # "IS" not in capital letter

rule.add_rules_from_file(FS, "./data/rule_example.txt")
print(FS._rules)