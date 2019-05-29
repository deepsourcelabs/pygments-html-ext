#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import run
from lxml import html, etree


SAMPLE_FILE = 'tests/data/sample.py'


def test_html_slice_without_range(tmp_path):
    """
    Verify that using the HtmlSliceFormatter without passing
    begin_line and end_line works identical to HtmlFormatter.
    """

    # run with HtmlFormatter
    output_html = tmp_path / 'html'
    run([
        'pygmentize', '-f', 'html',
        '-O', 'linenos=table,hl_lines="28 29 30"',
        '-o', output_html, SAMPLE_FILE
    ])
    with open(output_html, 'r') as file_desc:
        output_html_content = file_desc.read()

    # run with HtmlSliceFormatter
    output_html_slice = tmp_path / 'html_slice'
    run([
        'pygmentize', '-f', 'formatters/html_slice.py:HtmlSliceFormatter', '-x',
        '-O', 'linenos=table,hl_lines="28 29 30"',
        '-o', output_html_slice, SAMPLE_FILE
    ])
    with open(output_html_slice, 'r') as file_desc:
        output_html_slice_content = file_desc.read()

    assert output_html_content == output_html_slice_content


def test_html_slice_with_range(tmp_path):
    """
    Verify that using the HtmlSliceFormatter when passing
    begin_line and end_line works as expected.
    """
    # run with HtmlFormatter
    output_html = tmp_path / 'html'
    run([
        'pygmentize', '-f', 'html',
        '-O', 'linenos=table,hl_lines="28 29 30"',
        '-o', output_html, SAMPLE_FILE
    ])
    with open(output_html, 'r') as file_desc:
        output_html_content = file_desc.read()
    tree = html.fromstring(output_html_content)

    # run with HtmlSliceFormatter
    output_html_slice = tmp_path / 'html_slice'
    run([
        'pygmentize', '-f', 'formatters/html_slice.py:HtmlSliceFormatter', '-x',
        '-O', 'linenos=table,hl_lines="28 29 30",begin_line=24,end_line=32',
        '-o', output_html_slice, SAMPLE_FILE
    ])
    with open(output_html_slice, 'r') as file_desc:
        output_html_slice_content = file_desc.read()
    slice_tree = html.fromstring(output_html_slice_content)

    # in the output for slice, check that line numbers are sane
    line_nos = slice_tree.xpath(
        "//div[contains(@class, 'linenodiv')]"
    )[0][0].text.split('\n')
    assert int(line_nos[0]) == 24
    assert int(line_nos[-1]) == 32

    # the markup for the highlighted code must be a subset of the original
    # highlighted code
    original_code = ''.join(
        [etree.tostring(child).decode() for
         child in tree.xpath(
             "//div[contains(@class, 'highlight')]")[0][0].iterdescendants()
         ])

    sliced_code = ''.join(
        [etree.tostring(child).decode() for
         child in tree.xpath(
             "//div[contains(@class, 'highlight')]")[0][0].iterdescendants()
         ])

    assert sliced_code in original_code
