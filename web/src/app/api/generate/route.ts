import { NextRequest, NextResponse } from 'next/server'
import { PythonBridge } from '@/lib/python-bridge'
import { ArticleConfig } from '@/types/article'

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

    const bridge = PythonBridge.getInstance()

    // Use Server-Sent Events for real-time progress
    const encoder = new TextEncoder()
    const stream = new ReadableStream({
      async start(controller) {
        try {
          const articles = await bridge.generateArticles(
            config,
            (progress, message) => {
              // Send progress updates
              const data = JSON.stringify({
                type: 'progress',
                progress,
                message
              })
              controller.enqueue(
                encoder.encode(`data: ${data}\n\n`)
              )
            }
          )

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
          const errorData = JSON.stringify({
            type: 'error',
            error: error instanceof Error ? error.message : 'Unknown error'
          })
          controller.enqueue(
            encoder.encode(`data: ${errorData}\n\n`)
          )
          controller.close()
        }
      }
    })

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    })
  } catch (error) {
    console.error('Generation error:', error)
    return NextResponse.json(
      { error: 'Failed to generate articles' },
      { status: 500 }
    )
  }
}