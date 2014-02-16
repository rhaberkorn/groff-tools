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

## HIGHLIGHT

`highlight.sno` is a small preprocessor written in [CSNOBOL4](http://www.snobol4.org/csnobol4/)
that processes blocks of source code embedded in your Groff document with
[GNU Source-highlight](http://www.gnu.org/software/src-highlite/) to produce
syntax highlighted text.

The output is formatted according to `groff.outlang` which currently only works with
the [mom macros](http://www.schaffter.ca/mom/).

Example:

```
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
