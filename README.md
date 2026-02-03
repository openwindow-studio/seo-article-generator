# SEO Article Generator

Generate 500+ SEO-optimized articles with one click. A powerful, configurable tool for content generation at scale.

## Features

- **One-Click Generation**: Generate hundreds of SEO-optimized articles with a single command
- **Multiple Templates**: Listicles, how-tos, comparisons, guides, and more
- **SEO Optimization**: Built-in keyword density analysis, meta descriptions, and schema markup
- **Configurable**: Easy YAML configuration for any industry or niche
- **Multiple Formats**: Export to Markdown, HTML, or JSON
- **Parallel Processing**: Generate articles quickly with multi-threading
- **Content Variety**: Smart randomization ensures unique, engaging content

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-article-generator.git
cd seo-article-generator

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Generate 10 articles with default settings
python scripts/generate.py --count 10

# Generate 500 articles with parallel processing
python scripts/generate.py --count 500 --parallel --workers 8

# Generate articles with specific template
python scripts/generate.py --count 50 --template listicle

# Generate with SEO optimization
python scripts/generate.py --count 100 --optimize-seo
```

## Configuration

### 1. Edit `config/config.yaml`

Customize the generator for your specific needs:

```yaml
brand:
  name: "Your Company"
  website: "https://yoursite.com"

variable_pools:
  products:
    - "Your Product"
    - "Product Feature 1"
    - "Product Feature 2"

  use_cases:
    - "small businesses"
    - "enterprise teams"
    - "remote workers"
```

### 2. Customize Templates

Edit `config/templates.yaml` to define article patterns:

```yaml
listicle:
  title_patterns:
    - "{number} Best {product} for {use_case} in {year}"
    - "Top {number} {product} Solutions for {audience}"

  intro_patterns:
    - "Looking for {product} solutions? We've tested {number} options..."
```

### 3. Set Distribution

Control how many of each article type to generate:

```yaml
template_distribution:
  listicle: 0.30        # 30% listicles
  how_to: 0.25          # 25% how-to guides
  comparison: 0.20      # 20% comparisons
  ultimate_guide: 0.15  # 15% ultimate guides
  location_based: 0.10  # 10% location-based
```

## Advanced Features

### SEO Optimization

The generator includes powerful SEO features:

- **Keyword Density Analysis**: Ensures optimal keyword usage
- **Meta Descriptions**: Auto-generated, keyword-optimized
- **Schema Markup**: Structured data for better search visibility
- **Readability Scoring**: Flesch reading ease analysis
- **Content Length Optimization**: Configurable min/max word counts

```bash
# Generate with full SEO optimization
python scripts/generate.py --count 100 --optimize-seo --format all
```

### Batch Processing

Generate articles in batches for large-scale content production:

```bash
# Generate 1000 articles in batches
python scripts/generate.py --count 1000 --parallel --workers 10
```

### Custom Industries

Easy to adapt for any industry:

1. **E-commerce**: Product comparisons, buying guides
2. **SaaS**: Feature guides, integration tutorials
3. **Finance**: Investment guides, market analysis
4. **Health**: Wellness tips, treatment comparisons
5. **Technology**: Developer guides, API documentation

## Output Formats

### Markdown
Perfect for static site generators (Hugo, Jekyll, Gatsby):

```markdown
# 10 Best Solutions for Remote Teams in 2024

Looking for tools that enhance productivity...

## Key Takeaways
- Point 1
- Point 2
```

### HTML
Ready-to-publish HTML with SEO optimization:

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="description" content="...">
    <title>Article Title</title>
</head>
<body>
    <article>...</article>
</body>
</html>
```

### JSON
Structured data for headless CMS integration:

```json
{
  "title": "Article Title",
  "slug": "article-title",
  "content_sections": [...],
  "meta": {...},
  "seo_score": 85
}
```

## Template Types

### 1. Listicles
- "10 Best [Product] for [Use Case]"
- "Top 7 Ways to [Achieve Goal]"
- Perfect for: Product roundups, tips, features

### 2. How-To Guides
- "How to [Action] in 5 Steps"
- "Complete Guide to [Task]"
- Perfect for: Tutorials, setup guides, processes

### 3. Comparisons
- "[Product A] vs [Product B]: Which is Better?"
- "Detailed Comparison of Top Solutions"
- Perfect for: Product comparisons, alternatives

### 4. Ultimate Guides
- "Ultimate Guide to [Topic]"
- "Everything You Need to Know About [Subject]"
- Perfect for: Comprehensive resources, pillar content

### 5. Location-Based
- "[Service] in [City]: Complete Guide"
- "Best [Product] for [Location] Residents"
- Perfect for: Local SEO, geographic targeting

## CLI Commands

```bash
# Initialize new configuration
python scripts/generate.py init

# Validate configuration
python scripts/generate.py validate --config config/config.yaml

# Generate with specific output directory
python scripts/generate.py --count 50 --output my_articles/

# Generate specific format only
python scripts/generate.py --count 20 --format html

# Verbose mode for debugging
python scripts/generate.py --count 10 --verbose
```

## Project Structure

```
seo-article-generator/
├── config/
│   ├── config.yaml         # Main configuration
│   └── templates.yaml      # Article templates
├── src/
│   ├── generator.py        # Core generation logic
│   ├── batch_processor.py  # Batch processing
│   ├── html_converter.py   # HTML conversion
│   └── seo_optimizer.py    # SEO optimization
├── scripts/
│   └── generate.py         # CLI interface
├── examples/               # Example configurations
└── tests/                  # Unit tests
```

## Examples

### E-commerce Configuration

```yaml
variable_pools:
  products:
    - "wireless headphones"
    - "noise-cancelling earbuds"
    - "bluetooth speakers"

  use_cases:
    - "working from home"
    - "commuting"
    - "exercise"
    - "travel"
```

### SaaS Configuration

```yaml
variable_pools:
  products:
    - "project management software"
    - "team collaboration tool"
    - "task tracking system"

  audiences:
    - "startups"
    - "agencies"
    - "enterprise teams"
```

### Crypto/Web3 Configuration

```yaml
variable_pools:
  products:
    - "DeFi protocol"
    - "NFT marketplace"
    - "blockchain platform"

  use_cases:
    - "yield farming"
    - "liquidity provision"
    - "NFT trading"
```

## Performance

- **Speed**: Generate 100 articles in ~30 seconds
- **Scalability**: Tested with 1000+ article batches
- **Memory**: Efficient memory usage with streaming
- **Parallel**: Multi-threaded for faster generation

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root directory
2. **Config Not Found**: Run `python scripts/generate.py init` first
3. **Slow Generation**: Increase workers with `--workers 8`
4. **Memory Issues**: Generate in smaller batches

### Debug Mode

```bash
# Run with verbose output
python scripts/generate.py --count 10 --verbose

# Validate configuration
python scripts/generate.py validate
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/seo-article-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/seo-article-generator/discussions)

## Roadmap

- [ ] WordPress integration
- [ ] AI-powered content enhancement
- [ ] Image generation support
- [ ] Multi-language support
- [ ] Content scheduling
- [ ] Analytics integration

---

Built with ❤️ for content creators and SEO professionals