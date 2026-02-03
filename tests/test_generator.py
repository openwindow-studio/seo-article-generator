"""
Tests for SEO Article Generator
"""
import sys
import os
import unittest
import yaml

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import ArticleGenerator
from src.batch_processor import BatchProcessor
from src.html_converter import HTMLConverter
from src.seo_optimizer import SEOOptimizer


class TestArticleGenerator(unittest.TestCase):
    """Test article generation functionality"""

    def setUp(self):
        """Set up test configuration"""
        self.config = {
            'brand': {
                'name': 'TestBrand',
                'website': 'https://test.com'
            },
            'templates': {
                'listicle': {
                    'title_patterns': [
                        '{number} Best {product} for {use_case}'
                    ],
                    'intro_patterns': [
                        'Looking for {product}? Here are {number} options.'
                    ]
                },
                'how_to': {
                    'title_patterns': [
                        'How to {action} in {year}'
                    ],
                    'intro_patterns': [
                        'Learn how to {action} effectively.'
                    ]
                }
            },
            'variable_pools': {
                'products': ['Product A', 'Product B'],
                'use_cases': ['business', 'personal'],
                'actions': ['get started', 'optimize'],
            },
            'content_blocks': {
                'conclusions': ['In conclusion, this is great.'],
                'takeaways': ['Key point 1', 'Key point 2']
            }
        }
        self.generator = ArticleGenerator(self.config)

    def test_generate_title(self):
        """Test title generation"""
        variables = {
            'number': 5,
            'product': 'Test Product',
            'use_case': 'testing',
            'year': 2024
        }
        title = self.generator.generate_title('listicle', variables)
        self.assertIn('5', title)
        self.assertIn('Test Product', title)

    def test_generate_intro(self):
        """Test intro generation"""
        variables = {
            'number': 10,
            'product': 'Test Product',
            'action': 'test things'
        }
        intro = self.generator.generate_intro('listicle', variables)
        self.assertIn('Test Product', intro)

    def test_generate_content(self):
        """Test full content generation"""
        variables = {
            'number': 5,
            'product': 'Test Product',
            'use_case': 'testing',
            'year': 2024
        }
        title = "Test Article"
        intro = "Test introduction"

        article = self.generator.generate_content('listicle', title, intro, variables)

        self.assertEqual(article['title'], title)
        self.assertEqual(article['intro'], intro)
        self.assertIn('content_sections', article)
        self.assertIn('key_takeaways', article)
        self.assertIn('conclusion', article)

    def test_invalid_template(self):
        """Test handling of invalid template type"""
        with self.assertRaises(ValueError):
            self.generator.generate_title('invalid_template', {})


class TestBatchProcessor(unittest.TestCase):
    """Test batch processing functionality"""

    def setUp(self):
        """Set up test configuration"""
        config = {
            'templates': {
                'listicle': {
                    'title_patterns': ['{number} Test Articles'],
                    'intro_patterns': ['Test intro']
                }
            },
            'variable_pools': {
                'products': ['Product'],
                'use_cases': ['testing']
            }
        }
        generator = ArticleGenerator(config)
        self.processor = BatchProcessor(generator, 'test_output')

    def test_generate_batch(self):
        """Test batch generation"""
        articles = self.processor.generate_batch(
            count=2,
            template_distribution={'listicle': 1.0},
            parallel=False
        )

        self.assertEqual(len(articles), 2)
        for article in articles:
            self.assertIn('title', article)
            self.assertIn('slug', article)

    def test_slug_generation(self):
        """Test slug generation from title"""
        slug = self.processor._generate_slug("Test Article Title!")
        self.assertEqual(slug, "test-article-title")

        slug = self.processor._generate_slug("10 Best Products for 2024")
        self.assertEqual(slug, "10-best-products-for-2024")


class TestHTMLConverter(unittest.TestCase):
    """Test HTML conversion functionality"""

    def setUp(self):
        """Set up HTML converter"""
        self.converter = HTMLConverter()

    def test_markdown_to_html(self):
        """Test markdown to HTML conversion"""
        markdown = "# Heading\n\n**Bold** and *italic* text."
        html = self.converter.markdown_to_html(markdown)

        self.assertIn('<h1>Heading</h1>', html)
        self.assertIn('<strong>Bold</strong>', html)
        self.assertIn('<em>italic</em>', html)

    def test_escape_html(self):
        """Test HTML escaping"""
        text = '<script>alert("test")</script>'
        escaped = self.converter._escape_html(text)

        self.assertNotIn('<script>', escaped)
        self.assertIn('&lt;script&gt;', escaped)

    def test_article_to_html(self):
        """Test article dict to HTML conversion"""
        article = {
            'title': 'Test Article',
            'intro': 'Test intro',
            'key_takeaways': ['Point 1', 'Point 2'],
            'content_sections': [],
            'conclusion': 'Test conclusion'
        }

        html = self.converter._article_to_html(article)

        self.assertIn('Test Article', html)
        self.assertIn('Point 1', html)
        self.assertIn('Test conclusion', html)


class TestSEOOptimizer(unittest.TestCase):
    """Test SEO optimization functionality"""

    def setUp(self):
        """Set up SEO optimizer"""
        self.optimizer = SEOOptimizer({
            'keyword_density': 0.02,
            'min_word_count': 300,
            'max_word_count': 2000
        })

    def test_analyze_seo(self):
        """Test SEO analysis"""
        text = "This is a test article about SEO optimization. " * 50
        keywords = ['test', 'SEO', 'optimization']

        analysis = self.optimizer.analyze_seo(text, keywords)

        self.assertIn('word_count', analysis)
        self.assertIn('keyword_density', analysis)
        self.assertIn('readability', analysis)
        self.assertGreater(analysis['word_count'], 0)

    def test_calculate_seo_score(self):
        """Test SEO score calculation"""
        analysis = {
            'word_count': 1000,
            'keyword_density': {
                'test': {'count': 5, 'density': 2.0}
            },
            'heading_structure': {
                'has_h1': True,
                'h2_count': 3,
                'proper_hierarchy': True
            },
            'readability': {
                'flesch_score': 65
            },
            'has_meta_description': True,
            'average_sentence_length': 18
        }

        score = self.optimizer._calculate_seo_score(analysis)

        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)

    def test_count_syllables(self):
        """Test syllable counting"""
        self.assertEqual(self.optimizer._count_syllables('hello'), 2)
        self.assertEqual(self.optimizer._count_syllables('a'), 1)
        self.assertEqual(self.optimizer._count_syllables('optimization'), 5)


if __name__ == '__main__':
    unittest.main()