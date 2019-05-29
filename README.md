# pygments-html-ext

Example usage:

```bash
pygmentize -f pygments-html-ext/formatters/html_slice.py:HtmlSliceFormatter -x -O linenos=table,hl_lines="28 29 30",begin_line=8,end_line=32 -o output.html sample_python_script.py
```

Where:
 -  `begin_line` and `end_line` define the line range to extract from the entire file.
 - `hl_lines` is a space-separated string of line numbers that need to be highlighted.
