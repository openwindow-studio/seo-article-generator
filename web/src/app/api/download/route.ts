import { NextRequest, NextResponse } from 'next/server'
import { GeneratedArticle } from '@/types/article'
import { ArticleFormatter } from '@/lib/formatters'
import * as JSZip from 'jszip'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { articles, format, filename } = body

    if (!articles || !Array.isArray(articles)) {
      return NextResponse.json(
        { error: 'Articles array is required' },
        { status: 400 }
      )
    }

    const validFormats = ['markdown', 'html', 'json', 'zip']
    if (!validFormats.includes(format)) {
      return NextResponse.json(
        { error: `Invalid format. Supported: ${validFormats.join(', ')}` },
        { status: 400 }
      )
    }

    if (format === 'zip') {
      return await generateZipFile(articles, filename || 'articles.zip')
    } else {
      return await generateSingleFile(articles, format, filename)
    }
  } catch (error) {
    console.error('Download error:', error)
    return NextResponse.json(
      { error: 'Failed to generate download' },
      { status: 500 }
    )
  }
}

async function generateZipFile(articles: GeneratedArticle[], filename: string) {
  const JSZipConstructor = JSZip.default || JSZip
  const zip = new JSZipConstructor()

  articles.forEach((article, index) => {
    const sanitizedTitle = article.title
      .replace(/[^a-zA-Z0-9\s]/g, '')
      .replace(/\s+/g, '_')
      .substring(0, 50)

    // Add files in different formats
    zip.file(`${sanitizedTitle}_${index + 1}.md`, ArticleFormatter.toMarkdown(article))
    zip.file(`${sanitizedTitle}_${index + 1}.html`, ArticleFormatter.toHTML(article))
    zip.file(`${sanitizedTitle}_${index + 1}.json`, ArticleFormatter.toJSON(article))
  })

  // Add a summary file
  const summary = generateSummary(articles)
  zip.file('summary.json', JSON.stringify(summary, null, 2))

  const zipBuffer = await zip.generateAsync({ type: 'nodebuffer' })

  return new Response(zipBuffer as any, {
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${filename}"`
    }
  })
}

async function generateSingleFile(
  articles: GeneratedArticle[],
  format: string,
  filename?: string
) {
  let content: string
  let contentType: string
  let defaultFilename: string

  switch (format) {
    case 'markdown':
      content = articles.map(article => ArticleFormatter.toMarkdown(article)).join('\n\n---\n\n')
      contentType = 'text/markdown'
      defaultFilename = 'articles.md'
      break
    case 'html':
      content = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Generated Articles</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    .article { margin-bottom: 40px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
    h1 { color: #333; }
    h2 { color: #555; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    th { background-color: #f5f5f5; }
    .meta { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
  </style>
</head>
<body>
  <h1>Generated Articles</h1>
  ${articles.map((article, index) => `
    <div class="article">
      <h2>Article ${index + 1}</h2>
      ${ArticleFormatter.toHTML(article)}
      <div class="meta">
        <strong>Template:</strong> ${article.template_type}<br>
        <strong>Generated:</strong> ${new Date(article.generated_at).toLocaleString()}<br>
        <strong>Word Count:</strong> ${article.word_count || ArticleFormatter.getWordCount(article)}<br>
        <strong>SEO Score:</strong> ${ArticleFormatter.getSeoScore(article)}/100
      </div>
    </div>
  `).join('')}
</body>
</html>`
      contentType = 'text/html'
      defaultFilename = 'articles.html'
      break
    case 'json':
      const jsonData = {
        generated_at: new Date().toISOString(),
        total_articles: articles.length,
        summary: generateSummary(articles),
        articles: articles
      }
      content = JSON.stringify(jsonData, null, 2)
      contentType = 'application/json'
      defaultFilename = 'articles.json'
      break
    default:
      throw new Error('Invalid format')
  }

  return new Response(content, {
    headers: {
      'Content-Type': contentType,
      'Content-Disposition': `attachment; filename="${filename || defaultFilename}"`
    }
  })
}

function generateSummary(articles: GeneratedArticle[]) {
  const templateCounts = articles.reduce((acc, article) => {
    acc[article.template_type] = (acc[article.template_type] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  const totalWordCount = articles.reduce((acc, article) =>
    acc + (article.word_count || ArticleFormatter.getWordCount(article)), 0
  )

  const averageSeoScore = articles.reduce((acc, article) =>
    acc + ArticleFormatter.getSeoScore(article), 0
  ) / articles.length

  return {
    total_articles: articles.length,
    template_distribution: templateCounts,
    total_word_count: totalWordCount,
    average_word_count: Math.round(totalWordCount / articles.length),
    average_seo_score: Math.round(averageSeoScore),
    generated_at: new Date().toISOString()
  }
}