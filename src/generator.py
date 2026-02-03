"""
Core article generation module
"""
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ArticleGenerator:
    """Generate SEO-optimized articles based on templates and configuration"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration"""
        self.config = config
        self.templates = config.get('templates', {})
        self.keywords = config.get('keywords', {})
        self.brand = config.get('brand', {})

    def generate_title(self, template_type: str, variables: Dict[str, Any]) -> str:
        """Generate article title based on template"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")

        title_pattern = random.choice(self.templates[template_type]['title_patterns'])

        # Replace variables in pattern
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            if placeholder in title_pattern:
                title_pattern = title_pattern.replace(placeholder, str(value))

        return title_pattern

    def generate_intro(self, template_type: str, variables: Dict[str, Any]) -> str:
        """Generate article introduction"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")

        intro_pattern = random.choice(self.templates[template_type]['intro_patterns'])

        # Replace variables
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            if placeholder in intro_pattern:
                intro_pattern = intro_pattern.replace(placeholder, str(value))

        return intro_pattern

    def generate_content(self, template_type: str, title: str, intro: str,
                        variables: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete article content"""

        # Build article structure
        article = {
            'title': title,
            'intro': intro,
            'template_type': template_type,
            'generated_at': datetime.now().isoformat(),
            'content_sections': [],
            'meta': {
                'description': self._generate_meta_description(title, intro),
                'keywords': self._extract_keywords(title, intro),
            }
        }

        # Generate content based on template type
        if template_type == 'listicle':
            article['content_sections'] = self._generate_listicle_content(variables)
        elif template_type == 'how_to':
            article['content_sections'] = self._generate_howto_content(variables)
        elif template_type == 'comparison':
            article['content_sections'] = self._generate_comparison_content(variables)
        elif template_type == 'ultimate_guide':
            article['content_sections'] = self._generate_guide_content(variables)
        else:
            article['content_sections'] = self._generate_generic_content(variables)

        # Add conclusion
        article['conclusion'] = self._generate_conclusion(template_type, variables)

        # Add key takeaways
        article['key_takeaways'] = self._generate_takeaways(variables)

        return article

    def _generate_listicle_content(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content sections for listicle format"""
        sections = []
        num_items = variables.get('number', 10)

        # Get list items from config or generate defaults
        list_items = self.config.get('content_blocks', {}).get('listicle_items', [])

        for i in range(min(num_items, len(list_items))):
            item = list_items[i] if i < len(list_items) else self._generate_default_item(i)
            sections.append({
                'type': 'list_item',
                'number': i + 1,
                'title': item.get('title', f'Item {i+1}'),
                'content': item.get('content', ''),
                'benefits': item.get('benefits', [])
            })

        return sections

    def _generate_howto_content(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content sections for how-to format"""
        sections = []

        # Prerequisites section
        sections.append({
            'type': 'prerequisites',
            'title': 'What You\'ll Need',
            'items': self._generate_prerequisites(variables)
        })

        # Step-by-step instructions
        steps = self._generate_steps(variables)
        sections.append({
            'type': 'steps',
            'title': 'Step-by-Step Instructions',
            'steps': steps
        })

        # Tips section
        sections.append({
            'type': 'tips',
            'title': 'Pro Tips',
            'tips': self._generate_tips(variables)
        })

        return sections

    def _generate_comparison_content(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content sections for comparison format"""
        sections = []

        # Feature comparison table
        sections.append({
            'type': 'comparison_table',
            'title': 'Feature Comparison',
            'table': self._generate_comparison_table(variables)
        })

        # Detailed analysis
        sections.append({
            'type': 'analysis',
            'title': 'Detailed Analysis',
            'subsections': self._generate_analysis_sections(variables)
        })

        # Verdict
        sections.append({
            'type': 'verdict',
            'title': 'Final Verdict',
            'content': self._generate_verdict(variables)
        })

        return sections

    def _generate_guide_content(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content sections for ultimate guide format"""
        sections = []

        # Overview
        sections.append({
            'type': 'overview',
            'title': 'Overview',
            'content': self._generate_overview(variables)
        })

        # Main chapters
        chapters = self._generate_chapters(variables)
        for chapter in chapters:
            sections.append({
                'type': 'chapter',
                'title': chapter['title'],
                'content': chapter['content'],
                'subsections': chapter.get('subsections', [])
            })

        # Resources
        sections.append({
            'type': 'resources',
            'title': 'Additional Resources',
            'resources': self._generate_resources(variables)
        })

        return sections

    def _generate_generic_content(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate generic content sections"""
        sections = []

        # Add 3-5 main sections
        num_sections = random.randint(3, 5)
        for i in range(num_sections):
            sections.append({
                'type': 'section',
                'title': self._generate_section_title(i, variables),
                'content': self._generate_section_content(i, variables)
            })

        return sections

    def _generate_conclusion(self, template_type: str, variables: Dict[str, Any]) -> str:
        """Generate article conclusion"""
        conclusions = self.config.get('content_blocks', {}).get('conclusions', [
            "In conclusion, {product} offers a comprehensive solution for {use_case}.",
            "With these features and benefits, it's clear why {product} is leading the way.",
            "The future of {topic} is here, and it's more accessible than ever."
        ])

        conclusion = random.choice(conclusions)
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            if placeholder in conclusion:
                conclusion = conclusion.replace(placeholder, str(value))

        return conclusion

    def _generate_takeaways(self, variables: Dict[str, Any]) -> List[str]:
        """Generate key takeaways"""
        takeaways = self.config.get('content_blocks', {}).get('takeaways', [])

        if not takeaways:
            # Generate default takeaways
            takeaways = [
                f"{variables.get('product', 'The solution')} offers unmatched privacy protection",
                "No downloads or installations required",
                "Pay-per-use model ensures cost efficiency",
                "Enterprise-grade security for all users",
                "Works on any device with a modern browser"
            ]

        return takeaways[:5]  # Return max 5 takeaways

    def _generate_meta_description(self, title: str, intro: str) -> str:
        """Generate SEO meta description"""
        # Take first 150 chars of intro, clean it up
        meta = intro[:150].strip()
        if len(intro) > 150:
            meta = meta.rsplit(' ', 1)[0] + '...'
        return meta

    def _extract_keywords(self, title: str, intro: str) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction - in production, use NLP
        text = f"{title} {intro}".lower()

        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = [w for w in text.split() if w not in stopwords and len(w) > 3]

        # Return unique keywords
        return list(set(words))[:10]

    def _generate_prerequisites(self, variables: Dict[str, Any]) -> List[str]:
        """Generate prerequisites for how-to articles"""
        return [
            "A modern web browser (Chrome, Firefox, Safari, or Edge)",
            "Stable internet connection",
            "Microphone access (will be requested by browser)",
            "5 minutes of your time"
        ]

    def _generate_steps(self, variables: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate steps for how-to articles"""
        return [
            {
                'title': 'Access the Platform',
                'description': 'Navigate to the website using any modern browser'
            },
            {
                'title': 'Create Your Room',
                'description': 'Click the create button to generate a unique, encrypted room'
            },
            {
                'title': 'Share the Link',
                'description': 'Send the secure link to your call participants'
            },
            {
                'title': 'Start Calling',
                'description': 'Both parties join and start the encrypted conversation'
            }
        ]

    def _generate_tips(self, variables: Dict[str, Any]) -> List[str]:
        """Generate pro tips"""
        return [
            "Use headphones for better audio quality",
            "Test your microphone before important calls",
            "Close unnecessary browser tabs for better performance",
            "Use a wired connection for more stable calls"
        ]

    def _generate_comparison_table(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison table data"""
        return {
            'headers': ['Feature', variables.get('product1', 'Product A'),
                       variables.get('product2', 'Product B')],
            'rows': [
                ['Privacy Protection', 'Complete', 'Partial'],
                ['Browser-Based', 'Yes', 'No'],
                ['No Download Required', 'Yes', 'No'],
                ['Pay-Per-Use', 'Yes', 'Monthly Only'],
                ['Anonymous Usage', 'Yes', 'Requires Account']
            ]
        }

    def _generate_analysis_sections(self, variables: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate analysis sections for comparisons"""
        return [
            {
                'title': 'Privacy Features',
                'content': 'When it comes to privacy, the differences are clear...'
            },
            {
                'title': 'Ease of Use',
                'content': 'User experience is crucial for adoption...'
            },
            {
                'title': 'Pricing Model',
                'content': 'The pricing structure reveals different philosophies...'
            }
        ]

    def _generate_verdict(self, variables: Dict[str, Any]) -> str:
        """Generate comparison verdict"""
        return f"While both options have their merits, {variables.get('product1', 'our solution')} " \
               f"stands out for users who prioritize {variables.get('priority', 'privacy and convenience')}."

    def _generate_overview(self, variables: Dict[str, Any]) -> str:
        """Generate guide overview"""
        return f"This comprehensive guide covers everything you need to know about " \
               f"{variables.get('topic', 'the subject')}. From basics to advanced techniques."

    def _generate_chapters(self, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate guide chapters"""
        return [
            {
                'title': 'Getting Started',
                'content': 'The fundamentals you need to know...',
                'subsections': ['Basic Concepts', 'First Steps', 'Common Mistakes']
            },
            {
                'title': 'Advanced Techniques',
                'content': 'Once you master the basics...',
                'subsections': ['Pro Strategies', 'Optimization Tips', 'Expert Secrets']
            },
            {
                'title': 'Best Practices',
                'content': 'Industry standards and recommendations...',
                'subsections': ['Security', 'Performance', 'Scalability']
            }
        ]

    def _generate_resources(self, variables: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate additional resources"""
        return [
            {'type': 'Documentation', 'description': 'Complete API documentation'},
            {'type': 'Tutorial', 'description': 'Step-by-step video guides'},
            {'type': 'Community', 'description': 'Join our user community'},
            {'type': 'Support', 'description': '24/7 customer support'}
        ]

    def _generate_section_title(self, index: int, variables: Dict[str, Any]) -> str:
        """Generate generic section title"""
        titles = [
            'Understanding the Basics',
            'Key Features and Benefits',
            'How It Works',
            'Getting the Most Value',
            'Common Use Cases'
        ]
        return titles[index % len(titles)]

    def _generate_section_content(self, index: int, variables: Dict[str, Any]) -> str:
        """Generate generic section content"""
        return f"This section explores important aspects of {variables.get('topic', 'the topic')}..."

    def _generate_default_item(self, index: int) -> Dict[str, Any]:
        """Generate default list item"""
        return {
            'title': f'Feature {index + 1}',
            'content': 'This feature provides significant value...',
            'benefits': ['Benefit 1', 'Benefit 2', 'Benefit 3']
        }