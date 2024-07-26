#!/usr/bin/env python3

import sys
import os

if len(sys.argv) != 3:
    print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.exists(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    sys.exit(1)

def parse_line(line):
    """
    Parse a single line of Markdown and convert to HTML.
    Handles headings and list items.
    """
    stripped = line.lstrip()

    # Check for headings
    if stripped.startswith('#'):
        heading_level = len(stripped.split()[0])
        if heading_level > 6:
            heading_level = 6
        content = stripped[heading_level:].strip()
        return f"<h{heading_level}>{content}</h{heading_level}>"

    # Check for list items
    elif stripped.startswith('-'):
        content = stripped[1:].strip()
        return f"<li>{content}</li>"

    return line

html_lines = []
with open(input_file, 'r') as md_file:
    inside_list = False
    for line in md_file:
        parsed_line = parse_line(line)

        # Detect if we are entering a list
        if parsed_line.startswith("<li>") and not inside_list:
            html_lines.append("<ul>")
            inside_list = True

        # Detect if we are exiting a list
        if not parsed_line.startswith("<li>") and inside_list:
            html_lines.append("</ul>")
            inside_list = False

        html_lines.append(parsed_line)

    # Close the list if the file ends with list items
    if inside_list:
        html_lines.append("</ul>")

with open(output_file, 'w') as html_file:
    html_file.write("\n".join(html_lines))

sys.exit(0)

