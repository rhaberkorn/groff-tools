#!/usr/local/bin/python3.9
from pygments.lexers import get_lexer_by_name, RawTokenLexer
from pygments.formatters import GroffFormatter
from pygments import highlight
import re
from sys import stdin, stdout, stderr

formatter = GroffFormatter(style="sas")

start_pattern = re.compile(r"\. *HIGHLIGHT +([^ ]+)( +(.*))?\n")
end_pattern = re.compile(r"\. *HIGHLIGHT *\n")

while True:
    for line in stdin:
        stdout.write(line)
        params = start_pattern.match(line)
        if params:
            break
    if not params: # EOF
        break

    lang, filename = params.group(1, 3)

    lexer = RawTokenLexer() if lang == "default" else get_lexer_by_name(lang)
    # NOTE: This option is broken and will result in a bogus empty line with the GroffFormatter
    lexer.ensurenl = False

    contents = []
    if filename:
        contents.append(open(filename).read())
        stdout.write(".ds HIGHLIGHT-LF \\n[.c] \\n[.F]\n")
        stdout.write(".lf 1 "+filename+"\n")
    else:
        for line in stdin:
            if end_pattern.match(line):
                stdout.write(line)
                break
            contents.append(line)

    formatted = highlight("".join(contents), lexer, formatter)
    stdout.write(formatted.replace("\n\n", "\n\\&\n")+"\n")
    if filename:
        stdout.write(".lf \\*[HIGHLIGHT-LF]\n")
