'''
These unit tests are designed to verify the correctness of three utility functions from your utils.py file. Here's what each test checks:
1. test_is_youtube_url()

Tests the is_youtube_url() function to ensure it:

    Correctly identifies YouTube URLs (both youtube.com and youtu.be)

    Correctly rejects non-YouTube URLs

    Handles invalid URL formats 

Specific cases checked:

    Standard YouTube URL (https://youtube.com/watch?v=123)

    www-prefixed YouTube URL (https://www.youtube.com/watch?v=123)

    Shortened YouTube URL (https://youtu.be/123)

    Non-YouTube video URL (https://example.com/video.mp4)

    Plain text that's not a URL (not a url)

2. test_format_size()

Tests the format_size() function to ensure it:

    Correctly formats bytes in appropriate units (B, KB, MB, GB)

    Handles boundary values between units

    Formats numbers with proper decimal places

Specific cases checked:

    Small size in bytes (500 B)

    Exactly 1 KB (1024 bytes → "1.00 KB")

    3 MB (3145728 bytes → "3.00 MB")

    1 GB (1073741824 bytes → "1.00 GB")

3. test_validate_url()

Tests the validate_url() function to ensure it:

    Accepts valid HTTP/HTTPS URLs

    Rejects invalid URLs (missing protocol)

    Rejects empty strings

    Rejects non-HTTP protocols (like FTP)

    Raises ValueError for invalid cases

Specific cases checked:

    Valid HTTPS URL (https://example.com)

    Valid HTTP URL (http://example.com)

    URL missing protocol (example.com)

    Empty string ("")

    Non-HTTP URL (ftp://example.com)
'''

import unittest
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.utils import is_youtube_url, format_size, validate_url

class TestUtils(unittest.TestCase):
    def test_is_youtube_url(self):
        self.assertTrue(is_youtube_url("https://youtube.com/watch?v=123"))
        self.assertTrue(is_youtube_url("https://www.youtube.com/watch?v=123"))
        self.assertTrue(is_youtube_url("https://youtu.be/123"))
        self.assertFalse(is_youtube_url("https://example.com/video.mp4"))
        self.assertFalse(is_youtube_url("not a url"))
    
    def test_format_size(self):
        self.assertEqual(format_size(500), "500 B")
        self.assertEqual(format_size(2048), "2.00 KB")
        self.assertEqual(format_size(3145728), "3.00 MB")
        self.assertEqual(format_size(1073741824), "1.00 GB")
    
    def test_validate_url(self):
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://example.com"))
        with self.assertRaises(ValueError):
            validate_url("example.com")
        with self.assertRaises(ValueError):
            validate_url("")
        with self.assertRaises(ValueError):
            validate_url("ftp://example.com")
    
    def test_format_size_edge_cases(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(-100), "-100 B")
        self.assertEqual(format_size(1024), "1.00 KB")  # exact boundary

if __name__ == '__main__':
    unittest.main()