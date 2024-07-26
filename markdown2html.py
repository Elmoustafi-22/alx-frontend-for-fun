#!/usr/bin/python3
"""
markdown2html.py: Convert a Markdown file to HTML.
"""

import sys
import os

def parse_line(line):
    """
    Parse a single line of Markdown and convert to HTML.
    Handles headings, unordered, and ordered list items.
    """
    stripped = line.lstrip()

    # Check for headings
    if stripped.startswith('#'):
        heading_level = len(stripped.split()[0])
        if heading_level > 6:
            heading_level = 6
        content = stripped[heading_level:].strip()
        return f"<h{heading_level}>{content}</h{heading_level}>"

    # Check for unordered list items
    elif stripped.startswith('-'):
        content = stripped[1:].strip()
        return f"<li>{content}</li>"

    # Check for ordered list items
    elif stripped.startswith('*'):
        content = stripped[1:].strip()
        return f"<li>{content}</li>"

    return line

def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    html_lines = []
    inside_ul = False
    inside_ol = False
    with open(input_file, 'r') as md_file:
        for line in md_file:
            parsed_line = parse_line(line)

            # Detect if we are entering an unordered list
            if parsed_line.startswith("<li>") and line.lstrip().startswith('-') and not inside_ul:
                if inside_ol:
                    html_lines.append("</ol>")
                    inside_ol = False
                html_lines.append("<ul>")
                inside_ul = True

            # Detect if we are entering an ordered list
            elif parsed_line.startswith("<li>") and line.lstrip().startswith('*') and not inside_ol:
                if inside_ul:
                    html_lines.append("</ul>")
                    inside_ul = False
                html_lines.append("<ol>")
                inside_ol = True

            # Detect if we are exiting a list
            if not parsed_line.startswith("<li>") and (inside_ul or inside_ol):
                if inside_ul:
                    html_lines.append("</ul>")
                    inside_ul = False
                if inside_ol:
                    html_lines.append("</ol>")
                    inside_ol = False

            html_lines.append(parsed_line)

        # Close the list if the file ends with list items
        if inside_ul:
            html_lines.append("</ul>")
        if inside_ol:
            html_lines.append("</ol>")

    with open(output_file, 'w') as html_file:
        html_file.write("\n".join(html_lines))

    sys.exit(0)

if __name__ == "__main__":
    main()

