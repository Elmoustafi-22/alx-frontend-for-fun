#!/usr/bin/python3
"""
markdown2html.py: Convert a Markdown file to HTML.
"""

import sys
import os

def parse_line(line):
    """
    Parse a single line of Markdown and convert to HTML.
    Handles headings, unordered lists, ordered lists, and paragraphs.
    """
    stripped = line.strip()

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

    # Treat non-empty lines as paragraph content
    elif stripped:
        return stripped

    return None

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
    inside_p = False
    with open(input_file, 'r') as md_file:
        for line in md_file:
            parsed_line = parse_line(line)

            # Detect if we are entering an unordered list
            if parsed_line and parsed_line.startswith("<li>") and line.lstrip().startswith('-') and not inside_ul:
                if inside_ol:
                    html_lines.append("</ol>")
                    inside_ol = False
                html_lines.append("<ul>")
                inside_ul = True

            # Detect if we are entering an ordered list
            elif parsed_line and parsed_line.startswith("<li>") and line.lstrip().startswith('*') and not inside_ol:
                if inside_ul:
                    html_lines.append("</ul>")
                    inside_ul = False
                html_lines.append("<ol>")
                inside_ol = True

            # Detect if we are exiting a list
            if not parsed_line and (inside_ul or inside_ol):
                if inside_ul:
                    html_lines.append("</ul>")
                    inside_ul = False
                if inside_ol:
                    html_lines.append("</ol>")
                    inside_ol = False

            # Handle paragraphs
            if parsed_line and not parsed_line.startswith("<li>") and not parsed_line.startswith("<h"):
                if not inside_p:
                    html_lines.append("<p>")
                    inside_p = True
                html_lines.append(parsed_line + "<br/>")
            elif inside_p:
                html_lines[-1] = html_lines[-1][:-5]  # Remove last <br/>
                html_lines.append("</p>")
                inside_p = False

        # Close any open tags at the end of the file
        if inside_ul:
            html_lines.append("</ul>")
        if inside_ol:
            html_lines.append("</ol>")
        if inside_p:
            html_lines[-1] = html_lines[-1][:-5]  # Remove last <br/>
            html_lines.append("</p>")

    with open(output_file, 'w') as html_file:
        html_file.write("\n".join(html_lines))

    sys.exit(0)

if __name__ == "__main__":
    main()
