import re


def format_text(text, indent="", column_size=80):
    words = re.sub(r"\s+", " ", text).strip().split(" ")
    prefix = "#"

    lines = []
    current_line = indent + prefix

    for index, word in enumerate(words):
        next_input = " " + word

        if len(current_line + next_input) <= column_size:
            current_line += next_input
        else:
            lines.append(current_line.rstrip())
            current_line = indent + prefix + next_input

    lines.append(current_line)

    return "\n".join(lines)


import unittest


class TestFormatText(unittest.TestCase):
    def test_breaks_text_into_lines(self):
        text = "Modern concurrency tools for Ruby. Inspired by Erlang, Clojure, Scala, Haskell, F#, C#, Java, and classic concurrency patterns."
        expected_text = "\n".join([
            "# Modern concurrency tools for Ruby. Inspired by Erlang, Clojure, Scala,",
            "# Haskell, F#, C#, Java, and classic concurrency patterns."
        ])
        self.assertEqual(format_text(text), expected_text)

    def test_considers_indent(self):
        text = "Loofah is a general library for manipulating and transforming HTML/XML documents and fragments, built on top of Nokogiri"
        expected_text = "\n".join([
            "  # Loofah is a general library for manipulating and transforming HTML/XML",
            "  # documents and fragments, built on top of Nokogiri"
        ])
        self.assertEqual(format_text(text, indent="  "), expected_text)

    def test_considers_column_size(self):
        text = "A simple and reliable solution for controlling external programs running in the background on any Ruby / OS combination."
        expected_text = "\n".join([
            "# A simple and reliable solution for controlling external programs",
            "# running in the background on any Ruby / OS combination."
        ])
        self.assertEqual(format_text(text, column_size=72), expected_text)


if __name__ == "__main__":
    unittest.main()
