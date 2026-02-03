"""
Batch processing for generating multiple articles
"""
import os
import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .generator import ArticleGenerator


class BatchProcessor:
    """Process multiple article generation requests efficiently"""

    def __init__(self, generator: ArticleGenerator, output_dir: str = "generated_articles"):
        """Initialize batch processor"""
        self.generator = generator
        self.output_dir = output_dir
        self.ensure_output_dir()

    def ensure_output_dir(self):
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'markdown'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'json'), exist_ok=True)

    def generate_batch(self, count: int, template_distribution: Optional[Dict[str, float]] = None,
                      parallel: bool = True, max_workers: int = 4) -> List[Dict[str, Any]]:
        """
        Generate a batch of articles

        Args:
            count: Number of articles to generate
            template_distribution: Dict of template_type -> probability (0-1)
            parallel: Whether to use parallel processing
            max_workers: Number of parallel workers

        Returns:
            List of generated articles
        """
        if template_distribution is None:
            # Default distribution
            template_distribution = {
                'listicle': 0.3,
                'how_to': 0.25,
                'comparison': 0.2,
                'ultimate_guide': 0.15,
                'location_based': 0.1
            }

        # Generate article specs
        article_specs = self._generate_article_specs(count, template_distribution)

        # Generate articles
        if parallel and count > 10:
            articles = self._generate_parallel(article_specs, max_workers)
        else:
            articles = self._generate_sequential(article_specs)

        # Save articles
        self._save_articles(articles)

        return articles

    def _generate_article_specs(self, count: int, distribution: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate specifications for articles to be created"""
        specs = []

        # Normalize distribution
        total = sum(distribution.values())
        normalized = {k: v/total for k, v in distribution.items()}

        for i in range(count):
            # Select template based on distribution
            template_type = self._weighted_choice(normalized)

            # Generate variables for this article
            variables = self._generate_variables(template_type)

            specs.append({
                'id': f"article_{i+1:04d}",
                'template_type': template_type,
                'variables': variables
            })

        return specs

    def _weighted_choice(self, weights: Dict[str, float]) -> str:
        """Make weighted random choice"""
        choices = list(weights.keys())
        probabilities = list(weights.values())
        return random.choices(choices, weights=probabilities)[0]

    def _generate_variables(self, template_type: str) -> Dict[str, Any]:
        """Generate variables for article based on template type"""
        # Get variable pools from config
        config = self.generator.config

        variables = {
            'year': datetime.now().year,
            'number': random.choice([5, 7, 10, 12, 15]),
        }

        # Add template-specific variables
        if 'variable_pools' in config:
            pools = config['variable_pools']

            # Common variables
            if 'products' in pools:
                variables['product'] = random.choice(pools['products'])
                variables['product1'] = pools['products'][0]  # Primary product

            if 'competitors' in pools:
                variables['product2'] = random.choice(pools['competitors'])
                variables['product3'] = random.choice(pools['competitors'])

            if 'use_cases' in pools:
                variables['use_case'] = random.choice(pools['use_cases'])

            if 'audiences' in pools:
                variables['audience'] = random.choice(pools['audiences'])

            if 'problems' in pools:
                variables['problem'] = random.choice(pools['problems'])

            if 'goals' in pools:
                variables['achieve_goal'] = random.choice(pools['goals'])

            if 'benefits' in pools:
                variables['benefit'] = random.choice(pools['benefits'])

            # Location-based variables
            if template_type == 'location_based' and 'locations' in pools:
                variables['location'] = random.choice(pools['locations'])
                variables['service'] = random.choice(pools.get('services', ['Service']))

            # Topic for guides
            if template_type == 'ultimate_guide' and 'topics' in pools:
                variables['topic'] = random.choice(pools['topics'])

            # Actions for how-to
            if template_type == 'how_to' and 'actions' in pools:
                variables['action'] = random.choice(pools['actions'])

        return variables

    def _generate_sequential(self, specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate articles sequentially"""
        articles = []

        for spec in specs:
            print(f"Generating {spec['id']}...")
            article = self._generate_single_article(spec)
            articles.append(article)

        return articles

    def _generate_parallel(self, specs: List[Dict[str, Any]], max_workers: int) -> List[Dict[str, Any]]:
        """Generate articles in parallel"""
        articles = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_spec = {
                executor.submit(self._generate_single_article, spec): spec
                for spec in specs
            }

            for future in as_completed(future_to_spec):
                spec = future_to_spec[future]
                try:
                    article = future.result()
                    articles.append(article)
                    print(f"Generated {spec['id']}")
                except Exception as e:
                    print(f"Error generating {spec['id']}: {e}")

        return articles

    def _generate_single_article(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a single article based on spec"""
        template_type = spec['template_type']
        variables = spec['variables']

        # Generate title
        title = self.generator.generate_title(template_type, variables)

        # Generate intro
        intro = self.generator.generate_intro(template_type, variables)

        # Generate full content
        article = self.generator.generate_content(template_type, title, intro, variables)

        # Add metadata
        article['id'] = spec['id']
        article['slug'] = self._generate_slug(title)
        article['template_type'] = template_type
        article['variables'] = variables

        return article

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().strip()
        slug = slug.replace(' ', '-')

        # Remove special characters
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789-'
        slug = ''.join(c for c in slug if c in allowed_chars)

        # Remove multiple hyphens
        while '--' in slug:
            slug = slug.replace('--', '-')

        # Remove leading/trailing hyphens
        slug = slug.strip('-')

        return slug

    def _save_articles(self, articles: List[Dict[str, Any]]):
        """Save articles to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for article in articles:
            # Save as JSON
            json_path = os.path.join(self.output_dir, 'json', f"{article['slug']}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(article, f, indent=2, ensure_ascii=False)

            # Save as Markdown
            markdown_path = os.path.join(self.output_dir, 'markdown', f"{article['slug']}.md")
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(self._article_to_markdown(article))

        # Create manifest
        manifest_path = os.path.join(self.output_dir, f"manifest_{timestamp}.json")
        manifest = {
            'generated_at': timestamp,
            'total_articles': len(articles),
            'articles': [
                {
                    'id': a['id'],
                    'title': a['title'],
                    'slug': a['slug'],
                    'template_type': a['template_type']
                }
                for a in articles
            ]
        }

        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        print(f"Saved {len(articles)} articles to {self.output_dir}/")
        print(f"Manifest: {manifest_path}")

    def _article_to_markdown(self, article: Dict[str, Any]) -> str:
        """Convert article dict to markdown format"""
        md = f"# {article['title']}\n\n"
        md += f"{article['intro']}\n\n"

        # Add key takeaways
        if 'key_takeaways' in article:
            md += "## Key Takeaways\n"
            for takeaway in article['key_takeaways']:
                md += f"- {takeaway}\n"
            md += "\n"

        # Add content sections
        for section in article.get('content_sections', []):
            md += self._section_to_markdown(section)

        # Add conclusion
        if 'conclusion' in article:
            md += "## Conclusion\n\n"
            md += f"{article['conclusion']}\n\n"

        # Add metadata as HTML comment
        md += f"\n<!-- Generated: {article.get('generated_at', 'Unknown')} -->\n"
        md += f"<!-- Template: {article.get('template_type', 'Unknown')} -->\n"

        return md

    def _section_to_markdown(self, section: Dict[str, Any]) -> str:
        """Convert section to markdown"""
        md = ""

        if section['type'] == 'list_item':
            md += f"## {section['number']}. {section['title']}\n\n"
            md += f"{section['content']}\n\n"
            if 'benefits' in section and section['benefits']:
                md += "**Key Benefits:**\n"
                for benefit in section['benefits']:
                    md += f"- {benefit}\n"
                md += "\n"

        elif section['type'] == 'steps':
            md += f"## {section['title']}\n\n"
            for i, step in enumerate(section['steps'], 1):
                md += f"### Step {i}: {step['title']}\n\n"
                md += f"{step['description']}\n\n"

        elif section['type'] == 'comparison_table':
            md += f"## {section['title']}\n\n"
            table = section['table']
            # Create markdown table
            md += "| " + " | ".join(table['headers']) + " |\n"
            md += "|" + " --- |" * len(table['headers']) + "\n"
            for row in table['rows']:
                md += "| " + " | ".join(row) + " |\n"
            md += "\n"

        elif section['type'] == 'tips':
            md += f"## {section['title']}\n\n"
            for tip in section['tips']:
                md += f"- {tip}\n"
            md += "\n"

        elif section['type'] == 'prerequisites':
            md += f"## {section['title']}\n\n"
            for item in section['items']:
                md += f"- {item}\n"
            md += "\n"

        elif section['type'] == 'chapter':
            md += f"## {section['title']}\n\n"
            md += f"{section['content']}\n\n"
            if 'subsections' in section:
                for subsection in section['subsections']:
                    md += f"### {subsection}\n\n"
                    md += "Content for this subsection...\n\n"

        else:
            # Generic section
            if 'title' in section:
                md += f"## {section['title']}\n\n"
            if 'content' in section:
                md += f"{section['content']}\n\n"

        return md