#!/usr/bin/env python3
"""
SEO Article Generator CLI
Generate SEO-optimized articles with one command
"""
import os
import sys
import yaml
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import ArticleGenerator
from src.batch_processor import BatchProcessor
from src.html_converter import HTMLConverter
from src.seo_optimizer import SEOOptimizer

console = Console()


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Load templates if separate file
    template_path = os.path.join(os.path.dirname(config_path), 'templates.yaml')
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            config['templates'] = yaml.safe_load(f)

    return config


@click.command()
@click.option('--count', '-n', default=10, help='Number of articles to generate')
@click.option('--config', '-c', default='config/config.yaml', help='Path to configuration file')
@click.option('--output', '-o', default='generated_articles', help='Output directory')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'json', 'all']),
              default='all', help='Output format')
@click.option('--parallel', '-p', is_flag=True, default=True, help='Use parallel processing')
@click.option('--workers', '-w', default=4, help='Number of parallel workers')
@click.option('--template', '-t', help='Specific template type to use')
@click.option('--optimize-seo', is_flag=True, help='Apply SEO optimization')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate(count, config, output, format, parallel, workers, template, optimize_seo, verbose):
    """Generate SEO-optimized articles with one command"""

    console.print(f"[bold blue]SEO Article Generator v1.0.0[/bold blue]")
    console.print(f"[dim]Generating {count} articles...[/dim]\n")

    # Load configuration
    try:
        config_data = load_config(config)
        if verbose:
            console.print(f"[green]✓[/green] Loaded configuration from {config}")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize components
    try:
        generator = ArticleGenerator(config_data)
        batch_processor = BatchProcessor(generator, output)

        if optimize_seo:
            seo_optimizer = SEOOptimizer(config_data.get('seo', {}))
        else:
            seo_optimizer = None

        if format in ['html', 'all']:
            html_converter = HTMLConverter(config_data.get('html', {}).get('template_path'))
        else:
            html_converter = None

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to initialize components: {e}")
        sys.exit(1)

    # Set template distribution
    if template:
        # Use single template type
        template_distribution = {template: 1.0}
    else:
        template_distribution = config_data.get('template_distribution')

    # Generate articles
    start_time = datetime.now()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(f"Generating {count} articles...", total=count)

        try:
            articles = batch_processor.generate_batch(
                count=count,
                template_distribution=template_distribution,
                parallel=parallel,
                max_workers=workers
            )
            progress.update(task, completed=count)
        except Exception as e:
            console.print(f"[red]✗[/red] Generation failed: {e}")
            sys.exit(1)

    # Apply SEO optimization if requested
    if optimize_seo and seo_optimizer:
        console.print("\n[yellow]Optimizing articles for SEO...[/yellow]")
        optimized_articles = []
        for article in articles:
            try:
                optimized = seo_optimizer.optimize_article(article)
                optimized_articles.append(optimized)
            except Exception as e:
                console.print(f"[red]Warning:[/red] Failed to optimize {article.get('title', 'article')}: {e}")
                optimized_articles.append(article)
        articles = optimized_articles

    # Convert to HTML if requested
    if html_converter and format in ['html', 'all']:
        console.print("\n[yellow]Converting to HTML...[/yellow]")
        html_dir = os.path.join(output, 'html')
        os.makedirs(html_dir, exist_ok=True)

        for article in articles:
            try:
                html_content = html_converter.convert_article(article)
                html_path = os.path.join(html_dir, f"{article['slug']}.html")
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            except Exception as e:
                console.print(f"[red]Warning:[/red] Failed to convert {article.get('title', 'article')}: {e}")

    # Calculate statistics
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Display results
    console.print(f"\n[bold green]✓ Generation Complete![/bold green]")

    # Create summary table
    table = Table(title="Generation Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", width=20)
    table.add_column("Value", style="green")

    table.add_row("Articles Generated", str(len(articles)))
    table.add_row("Time Taken", f"{duration:.2f} seconds")
    table.add_row("Articles per Second", f"{len(articles)/duration:.2f}")
    table.add_row("Output Directory", output)

    # Add template distribution
    if template_distribution:
        template_counts = {}
        for article in articles:
            t = article.get('template_type', 'unknown')
            template_counts[t] = template_counts.get(t, 0) + 1

        for template_type, count in template_counts.items():
            table.add_row(f"  - {template_type}", str(count))

    # Add SEO scores if optimization was applied
    if optimize_seo:
        seo_scores = [a.get('seo_score', 0) for a in articles if 'seo_score' in a]
        if seo_scores:
            avg_score = sum(seo_scores) / len(seo_scores)
            table.add_row("Average SEO Score", f"{avg_score:.1f}/100")

    console.print(table)

    # Show sample titles
    console.print("\n[bold]Sample Generated Titles:[/bold]")
    for article in articles[:5]:
        console.print(f"  • {article.get('title', 'Untitled')}")

    if len(articles) > 5:
        console.print(f"  [dim]... and {len(articles) - 5} more[/dim]")

    # Save manifest
    manifest_path = os.path.join(output, f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    console.print(f"\n[dim]Manifest saved to: {manifest_path}[/dim]")

    # Provide next steps
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("  1. Review generated articles in:", output)
    console.print("  2. Customize templates in: config/templates.yaml")
    console.print("  3. Adjust SEO settings in: config/config.yaml")
    console.print("  4. Deploy to your website or CMS")

    if verbose:
        console.print(f"\n[dim]Run with --help for more options[/dim]")


@click.group()
def cli():
    """SEO Article Generator CLI"""
    pass


@cli.command()
@click.option('--config', '-c', default='config/config.yaml', help='Configuration file to validate')
def validate(config):
    """Validate configuration file"""
    try:
        config_data = load_config(config)
        console.print(f"[green]✓[/green] Configuration is valid")

        # Show loaded settings
        console.print("\n[bold]Configuration Summary:[/bold]")
        console.print(f"  Brand: {config_data.get('brand', {}).get('name', 'Not set')}")
        console.print(f"  Products: {len(config_data.get('variable_pools', {}).get('products', []))} configured")
        console.print(f"  Templates: {len(config_data.get('templates', {}))} types available")

    except Exception as e:
        console.print(f"[red]✗[/red] Configuration error: {e}")
        sys.exit(1)


@cli.command()
def init():
    """Initialize a new configuration"""
    console.print("[bold]Initializing SEO Article Generator[/bold]")

    # Check if config exists
    if os.path.exists('config/config.yaml'):
        if not click.confirm("Configuration already exists. Overwrite?"):
            console.print("[yellow]Initialization cancelled[/yellow]")
            return

    # Create directories
    os.makedirs('config', exist_ok=True)
    os.makedirs('templates/html', exist_ok=True)
    os.makedirs('templates/markdown', exist_ok=True)

    # Copy default configuration
    default_config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    default_templates_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'templates.yaml')

    if os.path.exists(default_config_path):
        with open(default_config_path, 'r') as f:
            config_content = f.read()
        with open('config/config.yaml', 'w') as f:
            f.write(config_content)

    if os.path.exists(default_templates_path):
        with open(default_templates_path, 'r') as f:
            templates_content = f.read()
        with open('config/templates.yaml', 'w') as f:
            f.write(templates_content)

    console.print(f"[green]✓[/green] Configuration initialized")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Edit config/config.yaml with your settings")
    console.print("  2. Customize templates in config/templates.yaml")
    console.print("  3. Run: python generate.py --count 10")


if __name__ == '__main__':
    # If no subcommand, run generate
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1].startswith('-')):
        generate()
    else:
        cli()