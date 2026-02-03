"""
HTML conversion module for articles
"""
import re
import os
from typing import Dict, Any, Optional, List
from datetime import datetime


class HTMLConverter:
    """Convert articles to HTML format with templates"""

    def __init__(self, template_path: Optional[str] = None):
        """Initialize with optional HTML template"""
        self.template = None
        if template_path and os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template = f.read()

    def convert_article(self, article: Dict[str, Any], template: Optional[str] = None) -> str:
        """Convert article to HTML"""
        # Use provided template or default
        html_template = template or self.template or self._get_default_template()

        # Convert content to HTML
        content_html = self._article_to_html(article)

        # Replace placeholders in template
        html = html_template
        html = html.replace('{{title}}', article.get('title', 'Untitled'))
        html = html.replace('{{content}}', content_html)
        html = html.replace('{{meta_description}}', article.get('meta', {}).get('description', ''))
        html = html.replace('{{meta_keywords}}', ', '.join(article.get('meta', {}).get('keywords', [])))
        html = html.replace('{{published_date}}', article.get('generated_at', datetime.now().isoformat()))

        return html

    def markdown_to_html(self, markdown: str) -> str:
        """Convert markdown to HTML"""
        html = markdown

        # Convert headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # Convert bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # Convert links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)

        # Convert bullet lists
        html = self._convert_lists(html)

        # Convert paragraphs
        html = self._convert_paragraphs(html)

        # Convert tables
        html = self._convert_tables(html)

        return html

    def _article_to_html(self, article: Dict[str, Any]) -> str:
        """Convert article dict to HTML content"""
        html = f'<article class="seo-article">\n'

        # Title
        html += f'  <h1 class="article-title">{article["title"]}</h1>\n'

        # Intro
        html += f'  <div class="article-intro">\n'
        html += f'    <p>{article["intro"]}</p>\n'
        html += f'  </div>\n'

        # Key takeaways
        if 'key_takeaways' in article:
            html += '  <div class="key-takeaways">\n'
            html += '    <h2>Key Takeaways</h2>\n'
            html += '    <ul>\n'
            for takeaway in article['key_takeaways']:
                html += f'      <li>{self._escape_html(takeaway)}</li>\n'
            html += '    </ul>\n'
            html += '  </div>\n'

        # Content sections
        for section in article.get('content_sections', []):
            html += self._section_to_html(section)

        # Conclusion
        if 'conclusion' in article:
            html += '  <div class="article-conclusion">\n'
            html += '    <h2>Conclusion</h2>\n'
            html += f'    <p>{self._escape_html(article["conclusion"])}</p>\n'
            html += '  </div>\n'

        html += '</article>\n'
        return html

    def _section_to_html(self, section: Dict[str, Any]) -> str:
        """Convert section to HTML"""
        html = '  <section class="article-section">\n'

        if section['type'] == 'list_item':
            html += f'    <h2>{section["number"]}. {self._escape_html(section["title"])}</h2>\n'
            html += f'    <p>{self._escape_html(section["content"])}</p>\n'
            if 'benefits' in section and section['benefits']:
                html += '    <div class="benefits">\n'
                html += '      <h3>Key Benefits:</h3>\n'
                html += '      <ul>\n'
                for benefit in section['benefits']:
                    html += f'        <li>{self._escape_html(benefit)}</li>\n'
                html += '      </ul>\n'
                html += '    </div>\n'

        elif section['type'] == 'steps':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += '    <ol class="steps">\n'
            for step in section['steps']:
                html += '      <li>\n'
                html += f'        <h3>{self._escape_html(step["title"])}</h3>\n'
                html += f'        <p>{self._escape_html(step["description"])}</p>\n'
                html += '      </li>\n'
            html += '    </ol>\n'

        elif section['type'] == 'comparison_table':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += '    <div class="table-responsive">\n'
            html += '      <table class="comparison-table">\n'
            html += '        <thead>\n'
            html += '          <tr>\n'
            for header in section['table']['headers']:
                html += f'            <th>{self._escape_html(header)}</th>\n'
            html += '          </tr>\n'
            html += '        </thead>\n'
            html += '        <tbody>\n'
            for row in section['table']['rows']:
                html += '          <tr>\n'
                for cell in row:
                    html += f'            <td>{self._escape_html(cell)}</td>\n'
                html += '          </tr>\n'
            html += '        </tbody>\n'
            html += '      </table>\n'
            html += '    </div>\n'

        elif section['type'] == 'tips':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += '    <ul class="tips">\n'
            for tip in section['tips']:
                html += f'      <li>{self._escape_html(tip)}</li>\n'
            html += '    </ul>\n'

        elif section['type'] == 'prerequisites':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += '    <ul class="prerequisites">\n'
            for item in section['items']:
                html += f'      <li>{self._escape_html(item)}</li>\n'
            html += '    </ul>\n'

        elif section['type'] == 'chapter':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += f'    <p>{self._escape_html(section["content"])}</p>\n'
            if 'subsections' in section:
                html += '    <div class="subsections">\n'
                for subsection in section['subsections']:
                    html += f'      <h3>{self._escape_html(subsection)}</h3>\n'
                    html += '      <p>Content for this subsection...</p>\n'
                html += '    </div>\n'

        elif section['type'] == 'resources':
            html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            html += '    <ul class="resources">\n'
            for resource in section['resources']:
                html += f'      <li><strong>{self._escape_html(resource["type"])}:</strong> '
                html += f'{self._escape_html(resource["description"])}</li>\n'
            html += '    </ul>\n'

        else:
            # Generic section
            if 'title' in section:
                html += f'    <h2>{self._escape_html(section["title"])}</h2>\n'
            if 'content' in section:
                html += f'    <p>{self._escape_html(section["content"])}</p>\n'

        html += '  </section>\n'
        return html

    def _convert_lists(self, text: str) -> str:
        """Convert markdown lists to HTML"""
        lines = text.split('\n')
        result = []
        in_list = False

        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item = line.strip()[2:]
                result.append(f'  <li>{item}</li>')
            elif line.strip().startswith('* '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item = line.strip()[2:]
                result.append(f'  <li>{item}</li>')
            elif re.match(r'^\d+\. ', line.strip()):
                if in_list and result[-1] == '</ul>':
                    result.pop()
                    result.append('</ol>')
                if not in_list:
                    result.append('<ol>')
                    in_list = True
                item = re.sub(r'^\d+\. ', '', line.strip())
                result.append(f'  <li>{item}</li>')
            else:
                if in_list:
                    if '<ol>' in result[-len(result):]:
                        result.append('</ol>')
                    else:
                        result.append('</ul>')
                    in_list = False
                result.append(line)

        if in_list:
            if '<ol>' in result[-len(result):]:
                result.append('</ol>')
            else:
                result.append('</ul>')

        return '\n'.join(result)

    def _convert_paragraphs(self, text: str) -> str:
        """Convert text blocks to paragraphs"""
        # Split by double newlines
        blocks = text.split('\n\n')
        result = []

        for block in blocks:
            block = block.strip()
            if block and not block.startswith('<'):
                result.append(f'<p>{block}</p>')
            else:
                result.append(block)

        return '\n'.join(result)

    def _convert_tables(self, text: str) -> str:
        """Convert markdown tables to HTML"""
        # Simple table detection and conversion
        lines = text.split('\n')
        result = []
        in_table = False
        table_lines = []

        for line in lines:
            if '|' in line and not in_table:
                in_table = True
                table_lines = [line]
            elif '|' in line and in_table:
                table_lines.append(line)
            elif in_table and '|' not in line:
                # End of table
                if len(table_lines) >= 3:  # Header, separator, at least one row
                    result.append(self._parse_table(table_lines))
                else:
                    result.extend(table_lines)
                table_lines = []
                in_table = False
                result.append(line)
            else:
                result.append(line)

        # Handle table at end of text
        if table_lines and len(table_lines) >= 3:
            result.append(self._parse_table(table_lines))

        return '\n'.join(result)

    def _parse_table(self, lines: List[str]) -> str:
        """Parse markdown table lines into HTML"""
        html = '<table>\n'

        # Parse header
        header = lines[0].strip('|').split('|')
        header = [cell.strip() for cell in header]

        html += '  <thead>\n    <tr>\n'
        for cell in header:
            html += f'      <th>{cell}</th>\n'
        html += '    </tr>\n  </thead>\n'

        # Parse body (skip separator line)
        html += '  <tbody>\n'
        for line in lines[2:]:
            if line.strip():
                row = line.strip('|').split('|')
                row = [cell.strip() for cell in row]
                html += '    <tr>\n'
                for cell in row:
                    html += f'      <td>{cell}</td>\n'
                html += '    </tr>\n'
        html += '  </tbody>\n'

        html += '</table>'
        return html

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        if not isinstance(text, str):
            text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text

    def _get_default_template(self) -> str:
        """Get default HTML template"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{meta_description}}">
    <meta name="keywords" content="{{meta_keywords}}">
    <title>{{title}}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 2em; }
        h3 { color: #7f8c8d; }
        .key-takeaways {
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #3498db;
            margin: 2em 0;
        }
        .key-takeaways h2 {
            margin-top: 0;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #f4f4f4;
            font-weight: bold;
        }
        .article-intro {
            font-size: 1.1em;
            color: #555;
            margin: 1.5em 0;
        }
        .article-conclusion {
            background: #f0f8ff;
            padding: 20px;
            border-radius: 5px;
            margin-top: 2em;
        }
        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }
        li {
            margin: 0.5em 0;
        }
        .table-responsive {
            overflow-x: auto;
        }
        .steps {
            counter-reset: step-counter;
        }
        .steps li {
            counter-increment: step-counter;
            position: relative;
            padding-left: 3em;
        }
        .steps li::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            background: #3498db;
            color: white;
            width: 2em;
            height: 2em;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    {{content}}
</body>
</html>'''