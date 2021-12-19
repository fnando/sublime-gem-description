# Gem Description for Sublime Text

Show Rubygems description and annotate your code.

Just mouse over your Gemfile's `gem` definitions to show the popup.

https://user-images.githubusercontent.com/3009/146667868-dfd13c6d-1a9e-4e3b-be94-8f138c5aed40.mp4

## Installation

### Setup Package Control Repository

1. Follow the instructions from https://sublime.fnando.com.
2. Open the command pallete, run “Package Control: Install Package“, then search
   for “Gem Description“.

### Git Clone

Clone this repository into the Sublime Text “Packages” directory, which is
located where ever the “Preferences” -> “Browse Packages” option in sublime
takes you.

## Usage

You can configure this plugin by editing the settings file. You can either open
the command palette and search for “Gem Description: Settings” or use “Sublime
Text -> Preferences -> Package Settings -> Gem Description -> Settings”. The
default settings are:

```jsonc
{
  // The ruby command that will be used.
  // If you use something like asdf, you may need to add the full path, as in
  // "/Users/fnando/.asdf/shims/ruby".
  "command": "ruby",

  // Enable debug mode.
  "debug": false
}
```

## License

Copyright (c) 2021 Nando Vieira

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
