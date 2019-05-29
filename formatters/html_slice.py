#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygments.formatters import HtmlFormatter
from itertools import islice


class HtmlSliceFormatter(HtmlFormatter):
    """
    HtmlSliceFormatter inherits from the in-built HtmlFormatter and adds
    additional functionalities: like extracting a portion of the highlighted
    file without messing up the syntax highlighting.

    New options added:
        begin_line (int) starting line of the range
        end_line (int) ending line of the range
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        begin_line = kwargs.get('begin_line')

        if begin_line:
            self.begin_line = int(begin_line)
            # if begin_line is set, set `linenostart` to match it
            self.linenostart = self.begin_line

            # since we've changed the beginning of this file, we'll need to
            # offset the hl_lines, if available, appropriately.
            hl_line_offset = self.begin_line - 1
            self.hl_lines = [i - hl_line_offset for i in self.hl_lines or []]
        else:
            self.begin_line = None

        end_line = kwargs.get('end_line')
        self.end_line = int(end_line) if end_line else None

        # validate sanity of begin_line and end_line
        if ((self.begin_line and self.end_line) and
                (self.end_line < self.begin_line)):
            raise ValueError(
                "Value for `end_line` must be less than or equal to `begin_line`"
            )

    def _format_lines(self, tokensource, *_, **__):
        """
        Override the default method to support extraction of the expected
        range.

        The `tokensource` object is a generator that contains all lines in the
        file. We simply slice the generator to get the range we expect.
        """

        source = super()._format_lines(tokensource)

        if self.begin_line and self.end_line:
            return islice(source, self.begin_line - 1, self.end_line)
        return source
