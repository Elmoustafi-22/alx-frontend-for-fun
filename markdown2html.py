<<<<<<< HEAD
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
=======
#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re


def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file
    '''
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            # Get the content of the heading
            h_content = match.group(2)
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_content.append(line)

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)

>>>>>>> dbafe34a98d26c338132c7e9ea844f37d4e4b9b0

