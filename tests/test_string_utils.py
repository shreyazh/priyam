import unittest
from priyam.string_utils import title_case_with_exceptions, reverse_words, slugify

class TestStringUtils(unittest.TestCase):
    
    def test_title_case_with_exceptions(self):
        self.assertEqual(title_case_with_exceptions("the lord of the rings", ["the", "of"]), 
                         "The Lord of the Rings")
        self.assertEqual(title_case_with_exceptions("a tale of two cities"), 
                         "A Tale of Two Cities")
        self.assertEqual(title_case_with_exceptions("hello world", []), 
                         "Hello World")
    
    def test_reverse_words(self):
        self.assertEqual(reverse_words("Hello World"), "World Hello")
        self.assertEqual(reverse_words("Python is awesome"), "awesome is Python")
        self.assertEqual(reverse_words("Single"), "Single")
    
    def test_slugify(self):
        self.assertEqual(slugify("Hello World!"), "hello-world")
        self.assertEqual(slugify("Python & Django"), "python-django")
        self.assertEqual(slugify("Test with spaces"), "test-with-spaces")
        self.assertEqual(slugify("Test with -- multiple --- separators"), "test-with-multiple-separators")

if __name__ == "__main__":
    unittest.main()