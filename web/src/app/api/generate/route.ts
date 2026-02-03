import { NextRequest, NextResponse } from 'next/server'
import { ArticleConfig } from '@/types/article'
import { ArticleGenerator } from '@/lib/generator/article-generator'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const config: ArticleConfig = body

    // Validate the configuration
    if (!config.templateType || !config.variables || !config.count) {
      return NextResponse.json(
        { error: 'Invalid configuration provided' },
        { status: 400 }
      )
    }

    // Create the generator with configuration
    const generator = new ArticleGenerator({
      templateType: config.templateType,
      brandName: config.variables.brandName || 'SE0',
      primaryProduct: config.variables.primaryProduct || config.variables.products?.[0] || 'anonymous calling',
      variables: config.variables,
    })

    // Use Server-Sent Events for real-time progress
    const encoder = new TextEncoder()
    const stream = new ReadableStream({
      async start(controller) {
        try {
          const articles = []
          const totalCount = config.count

          // Generate articles with progress updates
          for (let i = 0; i < totalCount; i++) {
            // Generate article
            const article = generator.generateArticle(config.templateType)
            articles.push(article)

            // Send progress update
            const progress = ((i + 1) / totalCount) * 100
            const data = JSON.stringify({
              type: 'progress',
              progress,
              message: `Generated ${i + 1} of ${totalCount} articles...`,
              current: i + 1,
              total: totalCount
            })
            controller.enqueue(
              encoder.encode(`data: ${data}\n\n`)
            )

            // Add small delay to show progress (optional, for UX)
            if (i < totalCount - 1) {
              await new Promise(resolve => setTimeout(resolve, 100))
            }
          }

          // Send completion
          const data = JSON.stringify({
            type: 'complete',
            articles
          })
          controller.enqueue(
            encoder.encode(`data: ${data}\n\n`)
          )

          controller.close()
        } catch (error) {
          // Send error
          const data = JSON.stringify({
            type: 'error',
            error: error instanceof Error ? error.message : 'Generation failed'
          })
          controller.enqueue(
            encoder.encode(`data: ${data}\n\n`)
          )
          controller.close()
        }
      }
    })

    return new NextResponse(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    })

  } catch (error) {
    console.error('Generation error:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Generation failed' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    status: 'ready',
    message: 'Article generation API is ready',
    templates: [
      'listicle',
      'how_to',
      'comparison',
      'ultimate_guide',
      'location_based',
      'crypto_focused',
      'developer_focused'
    ]
  })
}