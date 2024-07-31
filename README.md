# Groff Preprocessors and Tools

This repository is home to an assortment of preprocessors and
macros for the [GNU Troff](http://www.gnu.org/software/groff/) typesetting
package.

I have written all of them except `sequence.pic` which is part of the
[UML Graph](http://www.umlgraph.org/) package and included here for convenience
only.
These scripts do not strive to be complete, well tested and fit for general usage - they
are merely quick and dirty hacks that accumulated on my hard drive :-).

## EBNF

`ebnf.sno` is a [CSNOBOL4](http://www.snobol4.org/csnobol4/) program that compiles
extended BNF descriptions into GNU pic code using macros from `syntax.pic`.
This effectively allows you to embed EBNF grammars in Groff source code and
have it rendered as (box and arrow) syntax diagrams.
Most EBNF constructs and some extensions are supported, but I'm too lazy to document
all of them now.

To build the sample `select-from.ebnf`, type something like:

    cat samples/select-from.ebnf | ./ebnf.sno | pic | groff -Tps >select-from.ps

## HIGHLIGHT (Python)

`pygments-groff.py` is a syntax highlighting preprocessor based on [Pygments](https://pygments.org/) and
consequently written in Python 3.
It is the most powerful (and probably fastest) of the syntax highlighting preprocessors presented here.
It should also be more portable as it does not rely on stdout redirection magic.
It should work with all Groff macro suites and even preserves the line numbering
in Groff error messages.

You can process embedded blocks of code as in the following ms-based example:

```groff
.LD
.CW
.lg 0
.HIGHLIGHT c
#include <stdio.h>

int main(int argc, char **argv)
{
	printf("Hello world!\n");
	return 0;
}
.HIGHLIGHT
.DE
```

Note that you may have to do more before `.HIGHLIGHT` - for instance redefine chars -
depending on your use case.

The `default` language identifier is useful to include code without highlighting,
but still benefit from Pygment's preprocessing in order to achieve verbatim text.
A list of language identifiers (short names) can be found on the [Pygments website](https://pygments.org/languages/).

Just like `highlight.lua`, you can specify a file name directly after the language identifier:

```groff
.HIGHLIGHT c hello.c
```

## HIGHLIGHT (SNOBOL4)

`highlight.sno` is a small preprocessor written in [CSNOBOL4](http://www.snobol4.org/csnobol4/)
that processes blocks of source code embedded in your Groff document with
[GNU Source-highlight](http://www.gnu.org/software/src-highlite/) to produce
syntax highlighted text.

The output is formatted according to `groff.outlang`.
Versions for the [mom macros](http://www.schaffter.ca/mom/) (`groff-mom.outlang`) and
for the classic ms macros (`groff-ms.outlang`) are provided.

Example (mom):

```groff
.QUOTE
.CODE
.HIGHLIGHT c
#include <stdio.h>

int main(int argc, char **argv)
{
	printf("Hello world!\n");
	return 0;
}
.HIGHLIGHT
.CODE OFF
.QUOTE OFF
```

## HIGHLIGHT (Lua)

`highlight.lua` is a reimplementation of `highlight.sno` in Lua 5.2 and may work
better on some operating systems.

In addition to the aforementioned syntax, the Lua version allows you to specify a filename after
the language identifier to process an external file:

```groff
.HIGHLIGHT c hello.c
```

## UML

`uml.sno` is a small preprocessor (again requires CSNOBOL4) that
renders an embedded diagram with [PlantUML](http://plantuml.sourceforge.net/)
and automatically emits the appropriate Mom `PDF_IMAGE` macro calls.

Naturally, this leaves around PDF images (`uml_tempX.pdf`) that you should remove
after generating your document.

## HTML Tables

`htbl.tes` is a quick and dirty [SciTECO](http://rhaberkorn.github.com/sciteco/) script
that can act as a drop-in replacement for the tbl preprocessor that generates
proper HTML tables when the Groff html output device is used.
With the original tbl preprocessor, tables are (and must be) rendered by the postscript
device and will be embedded as images into the HTML page.
