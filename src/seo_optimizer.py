"""
SEO optimization module for generated articles
"""
import re
from typing import Dict, List, Any, Optional
from collections import Counter


class SEOOptimizer:
    """Optimize articles for search engines"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize SEO optimizer with configuration"""
        self.config = config or {}
        self.target_keyword_density = config.get('keyword_density', 0.02)  # 2% default
        self.min_word_count = config.get('min_word_count', 800)
        self.max_word_count = config.get('max_word_count', 2500)

    def optimize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Apply SEO optimizations to article"""
        # Extract text content
        text_content = self._extract_text(article)

        # Analyze current state
        analysis = self.analyze_seo(text_content, article.get('meta', {}).get('keywords', []))

        # Apply optimizations
        optimized = article.copy()

        # Optimize meta description
        if 'meta' not in optimized:
            optimized['meta'] = {}

        optimized['meta']['description'] = self._optimize_meta_description(
            article.get('title', ''),
            article.get('intro', ''),
            analysis['primary_keywords']
        )

        # Add schema markup suggestions
        optimized['schema_markup'] = self._generate_schema_markup(article)

        # Add internal linking suggestions
        optimized['internal_links'] = self._suggest_internal_links(article)

        # Add SEO score
        optimized['seo_score'] = self._calculate_seo_score(analysis)

        # Add optimization suggestions
        optimized['seo_suggestions'] = self._generate_suggestions(analysis)

        return optimized

    def analyze_seo(self, text: str, target_keywords: List[str]) -> Dict[str, Any]:
        """Analyze SEO metrics for text content"""
        words = text.lower().split()
        word_count = len(words)

        # Calculate keyword density
        keyword_density = {}
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = text.lower().count(keyword_lower)
            density = (count / word_count) * 100 if word_count > 0 else 0
            keyword_density[keyword] = {
                'count': count,
                'density': round(density, 2)
            }

        # Find most common words (potential keywords)
        word_frequency = Counter(words)
        # Remove common stop words
        stop_words = self._get_stop_words()
        filtered_words = {w: c for w, c in word_frequency.items()
                         if w not in stop_words and len(w) > 3}
        primary_keywords = [w for w, c in Counter(filtered_words).most_common(10)]

        # Check heading structure
        heading_analysis = self._analyze_headings(text)

        # Check readability metrics
        readability = self._calculate_readability(text)

        return {
            'word_count': word_count,
            'keyword_density': keyword_density,
            'primary_keywords': primary_keywords,
            'heading_structure': heading_analysis,
            'readability': readability,
            'has_meta_description': bool(text),  # Simplified check
            'average_sentence_length': self._calculate_avg_sentence_length(text)
        }

    def _extract_text(self, article: Dict[str, Any]) -> str:
        """Extract all text content from article"""
        text_parts = []

        # Add title
        if 'title' in article:
            text_parts.append(article['title'])

        # Add intro
        if 'intro' in article:
            text_parts.append(article['intro'])

        # Add content sections
        for section in article.get('content_sections', []):
            text_parts.append(self._extract_section_text(section))

        # Add conclusion
        if 'conclusion' in article:
            text_parts.append(article['conclusion'])

        # Add takeaways
        for takeaway in article.get('key_takeaways', []):
            text_parts.append(takeaway)

        return ' '.join(text_parts)

    def _extract_section_text(self, section: Dict[str, Any]) -> str:
        """Extract text from a section"""
        text_parts = []

        if 'title' in section:
            text_parts.append(str(section['title']))

        if 'content' in section:
            text_parts.append(str(section['content']))

        if 'description' in section:
            text_parts.append(str(section['description']))

        # Handle lists
        for key in ['benefits', 'tips', 'items', 'steps']:
            if key in section:
                items = section[key]
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            text_parts.extend(item.values())
                        else:
                            text_parts.append(str(item))

        return ' '.join(str(part) for part in text_parts)

    def _optimize_meta_description(self, title: str, intro: str,
                                  keywords: List[str]) -> str:
        """Generate optimized meta description"""
        # Start with intro
        meta = intro[:150] if intro else title[:150]

        # Ensure primary keyword is included
        if keywords and keywords[0].lower() not in meta.lower():
            # Try to naturally include the keyword
            meta = f"{keywords[0].title()}: {meta}"[:160]

        # Clean up
        meta = meta.strip()
        if len(meta) > 160:
            meta = meta[:157] + '...'

        return meta

    def _generate_schema_markup(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Generate schema.org markup for article"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article.get('title', ''),
            "description": article.get('meta', {}).get('description', ''),
            "datePublished": article.get('generated_at', ''),
            "dateModified": article.get('generated_at', ''),
            "author": {
                "@type": "Organization",
                "name": self.config.get('organization', 'Your Company')
            },
            "publisher": {
                "@type": "Organization",
                "name": self.config.get('organization', 'Your Company'),
                "logo": {
                    "@type": "ImageObject",
                    "url": self.config.get('logo_url', 'https://example.com/logo.png')
                }
            }
        }

        # Add FAQ schema if applicable
        if article.get('template_type') == 'how_to':
            schema['@type'] = 'HowTo'
            if 'content_sections' in article:
                steps = []
                for section in article['content_sections']:
                    if section.get('type') == 'steps' and 'steps' in section:
                        for step in section['steps']:
                            steps.append({
                                "@type": "HowToStep",
                                "name": step.get('title', ''),
                                "text": step.get('description', '')
                            })
                if steps:
                    schema['step'] = steps

        return schema

    def _suggest_internal_links(self, article: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest internal linking opportunities"""
        suggestions = []

        # Extract keywords and topics
        keywords = article.get('meta', {}).get('keywords', [])
        template_type = article.get('template_type', '')

        # Suggest related article types
        if template_type == 'how_to':
            suggestions.append({
                'anchor_text': 'complete guide',
                'suggested_url': '/ultimate-guide-[topic]',
                'reason': 'Link to comprehensive guide on same topic'
            })

        if template_type == 'comparison':
            suggestions.append({
                'anchor_text': 'detailed review',
                'suggested_url': '/review-[product]',
                'reason': 'Link to individual product reviews'
            })

        # Suggest links based on keywords
        for keyword in keywords[:3]:  # Top 3 keywords
            suggestions.append({
                'anchor_text': keyword,
                'suggested_url': f'/{keyword.replace(" ", "-").lower()}',
                'reason': f'Link to pillar content about {keyword}'
            })

        return suggestions

    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 0
        max_score = 100

        # Word count (20 points)
        word_count = analysis['word_count']
        if word_count >= self.min_word_count:
            if word_count <= self.max_word_count:
                score += 20
            else:
                score += 10  # Too long
        else:
            score += 5  # Too short

        # Keyword density (20 points)
        ideal_density_achieved = False
        for keyword, data in analysis['keyword_density'].items():
            density = data['density']
            if 1.5 <= density <= 3.0:  # Ideal range
                ideal_density_achieved = True
                break

        if ideal_density_achieved:
            score += 20
        elif analysis['keyword_density']:
            score += 10  # Keywords present but not ideal

        # Heading structure (15 points)
        heading_structure = analysis['heading_structure']
        if heading_structure.get('has_h1', False):
            score += 5
        if heading_structure.get('h2_count', 0) >= 3:
            score += 5
        if heading_structure.get('proper_hierarchy', True):
            score += 5

        # Readability (20 points)
        readability = analysis['readability']
        if readability.get('flesch_score', 0) >= 60:  # Easy to read
            score += 20
        elif readability.get('flesch_score', 0) >= 40:
            score += 10

        # Meta description (10 points)
        if analysis.get('has_meta_description', False):
            score += 10

        # Sentence length (15 points)
        avg_sentence_length = analysis.get('average_sentence_length', 20)
        if 15 <= avg_sentence_length <= 20:
            score += 15
        elif 10 <= avg_sentence_length <= 25:
            score += 8

        return min(score, max_score)

    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate SEO improvement suggestions"""
        suggestions = []

        # Word count suggestions
        word_count = analysis['word_count']
        if word_count < self.min_word_count:
            suggestions.append(f"Increase word count to at least {self.min_word_count} words")
        elif word_count > self.max_word_count:
            suggestions.append(f"Consider reducing word count to under {self.max_word_count} words")

        # Keyword density suggestions
        for keyword, data in analysis['keyword_density'].items():
            density = data['density']
            if density < 1.0:
                suggestions.append(f"Increase usage of keyword '{keyword}' (current: {density}%)")
            elif density > 3.0:
                suggestions.append(f"Reduce keyword stuffing for '{keyword}' (current: {density}%)")

        # Heading suggestions
        heading_structure = analysis['heading_structure']
        if not heading_structure.get('has_h1', False):
            suggestions.append("Add a clear H1 heading")
        if heading_structure.get('h2_count', 0) < 3:
            suggestions.append("Add more H2 subheadings to improve structure")

        # Readability suggestions
        readability = analysis['readability']
        if readability.get('flesch_score', 0) < 40:
            suggestions.append("Simplify language to improve readability")

        # Sentence length
        avg_sentence_length = analysis.get('average_sentence_length', 20)
        if avg_sentence_length > 25:
            suggestions.append("Use shorter sentences for better readability")
        elif avg_sentence_length < 10:
            suggestions.append("Vary sentence length for better flow")

        return suggestions

    def _analyze_headings(self, text: str) -> Dict[str, Any]:
        """Analyze heading structure"""
        lines = text.split('\n')
        h1_count = sum(1 for line in lines if line.startswith('# '))
        h2_count = sum(1 for line in lines if line.startswith('## '))
        h3_count = sum(1 for line in lines if line.startswith('### '))

        return {
            'has_h1': h1_count > 0,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'proper_hierarchy': h1_count <= 1  # Only one H1
        }

    def _calculate_readability(self, text: str) -> Dict[str, float]:
        """Calculate readability metrics"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)

        # Flesch Reading Ease
        if len(sentences) > 0 and len(words) > 0:
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = syllables / len(words)
            flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        else:
            flesch_score = 0

        return {
            'flesch_score': max(0, min(100, flesch_score)),
            'sentence_count': len(sentences),
            'word_count': len(words),
            'syllable_count': syllables
        }

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simple approximation)"""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        # Ensure at least 1 syllable
        return max(1, count)

    def _calculate_avg_sentence_length(self, text: str) -> float:
        """Calculate average sentence length"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0

        total_words = sum(len(s.split()) for s in sentences)
        return total_words / len(sentences)

    def _get_stop_words(self) -> set:
        """Get common stop words to filter"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
            'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'same', 'so', 'than', 'too', 'very', 'just', 'there'
        }