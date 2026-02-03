import { NextRequest, NextResponse } from 'next/server'
import { TEMPLATES } from '@/lib/generator/templates'
import { DEFAULT_VARIABLES } from '@/lib/generator/variables'

export async function GET() {
  try {
    // Return configuration based on our TypeScript templates
    const config = {
      templates: Object.keys(TEMPLATES).map(key => ({
        id: key,
        name: key.split('_').map(word =>
          word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' '),
        description: getTemplateDescription(key)
      })),
      variables: {
        products: DEFAULT_VARIABLES.products,
        competitors: DEFAULT_VARIABLES.competitors,
        use_cases: DEFAULT_VARIABLES.use_cases,
        audiences: DEFAULT_VARIABLES.audiences,
        problems: DEFAULT_VARIABLES.problems,
        goals: DEFAULT_VARIABLES.goals,
        benefits: DEFAULT_VARIABLES.benefits,
        actions: DEFAULT_VARIABLES.actions,
        topics: DEFAULT_VARIABLES.topics,
        locations: DEFAULT_VARIABLES.locations.slice(0, 10), // Limit for UI
        services: DEFAULT_VARIABLES.services,
        // Brand settings
        brandName: 'SE0',
        primaryProduct: 'SEO Article Generator',
      },
      outputFormats: ['markdown', 'html', 'json', 'zip'],
      seoSettings: {
        minWordCount: 800,
        maxWordCount: 2500,
        targetKeywordDensity: 0.02
      }
    }

    return NextResponse.json(config)
  } catch (error) {
    console.error('Failed to load config:', error)
    return NextResponse.json(
      {
        error: 'Configuration is now built-in to the application',
        templates: Object.keys(TEMPLATES).map(key => ({
          id: key,
          name: key.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
          ).join(' ')
        }))
      },
      { status: 200 } // Return 200 since we have fallback data
    )
  }
}

function getTemplateDescription(templateType: string): string {
  const descriptions: Record<string, string> = {
    listicle: 'Numbered lists and roundup articles (e.g., "10 Best Tools for...")',
    how_to: 'Step-by-step tutorials and guides',
    comparison: 'Product or service comparisons',
    ultimate_guide: 'Comprehensive, in-depth guides',
    location_based: 'Location-specific content for local SEO',
    crypto_focused: 'Web3, DeFi, and cryptocurrency content',
    developer_focused: 'Technical content for developers'
  }
  return descriptions[templateType] || 'General article template'
}