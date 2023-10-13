#   import unittest
import pytest
#import undulator_analysis_hzb.demo1 as demo1
from undulator_analysis_hzb import demo1


class TestDemo():
    def test_one(self):
        inp = 1
        assert demo1.add_one(inp) == 2
        
    def test_two(self):
        inp = 2
        
        assert demo1.add_one(inp) == 3
        
    def test_three(self):
        inp = 3
        
        assert demo1.add_one(inp) == 4
        