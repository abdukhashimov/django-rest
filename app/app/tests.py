from django.test import TestCase

from .calc import (
    add,
    subtract
)

class CalcTest(TestCase):
    def test_add_two_numbers(self):
        """Test that two numbers are correctly added"""
        self.assertEqual(add(1,1), 2)
    
    def test_subtract_two_numbers(self):
        """Test that two numbers are subtracted correctly"""
        self.assertEqual(subtract(3,1), 2)