'use client'

import { useState } from 'react'
import { GeneratedArticle } from '@/types/article'
import { ArticleFormatter } from '@/lib/formatters'
import { Button } from '@/components/ui/button'
import { Eye, Code, FileText, Download, Star } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface ArticlePreviewProps {
  article: GeneratedArticle
  onDownload?: (article: GeneratedArticle, format: string) => void
  className?: string
}

export function ArticlePreview({ article, onDownload, className = '' }: ArticlePreviewProps) {
  const [viewMode, setViewMode] = useState<'preview' | 'markdown' | 'json'>('preview')
  const [isExpanded, setIsExpanded] = useState(false)

  const wordCount = article.word_count || ArticleFormatter.getWordCount(article)
  const seoScore = ArticleFormatter.getSeoScore(article)

  const getContent = () => {
    switch (viewMode) {
      case 'markdown':
        return (
          <pre className="text-sm bg-gray-100 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
            {ArticleFormatter.toMarkdown(article)}
          </pre>
        )
      case 'json':
        return (
          <pre className="text-sm bg-gray-100 p-4 rounded-lg overflow-x-auto">
            {ArticleFormatter.toJSON(article)}
          </pre>
        )
      default:
        return (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown>{ArticleFormatter.toMarkdown(article)}</ReactMarkdown>
          </div>
        )
    }
  }

  const getSeoScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getSeoScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className={`card ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 pb-4 mb-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {article.title}
            </h3>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span className="flex items-center space-x-1">
                <FileText className="w-4 h-4" />
                <span>{wordCount} words</span>
              </span>
              <span className="capitalize">
                {article.template_type.replace('_', ' ')}
              </span>
              <span>
                {new Date(article.generated_at).toLocaleDateString()}
              </span>
            </div>
          </div>

          {/* SEO Score */}
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${getSeoScoreBg(seoScore)} ${getSeoScoreColor(seoScore)}`}>
            <div className="flex items-center space-x-1">
              <Star className="w-4 h-4" />
              <span>SEO: {seoScore}/100</span>
            </div>
          </div>
        </div>

        {/* Meta Information */}
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <div className="text-sm">
            <p className="text-gray-600 mb-1">
              <strong>Meta Description:</strong> {article.meta.description}
            </p>
            <p className="text-gray-600">
              <strong>Keywords:</strong> {article.meta.keywords.join(', ')}
            </p>
          </div>
        </div>
      </div>

      {/* View Mode Controls */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Button
            variant={viewMode === 'preview' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setViewMode('preview')}
          >
            <Eye className="w-4 h-4 mr-1" />
            Preview
          </Button>
          <Button
            variant={viewMode === 'markdown' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setViewMode('markdown')}
          >
            <FileText className="w-4 h-4 mr-1" />
            Markdown
          </Button>
          <Button
            variant={viewMode === 'json' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setViewMode('json')}
          >
            <Code className="w-4 h-4 mr-1" />
            JSON
          </Button>
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? 'Collapse' : 'Expand'}
          </Button>

          {onDownload && (
            <div className="flex items-center space-x-1">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownload(article, 'markdown')}
              >
                <Download className="w-4 h-4 mr-1" />
                MD
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownload(article, 'html')}
              >
                <Download className="w-4 h-4 mr-1" />
                HTML
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownload(article, 'json')}
              >
                <Download className="w-4 h-4 mr-1" />
                JSON
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className={`${isExpanded ? '' : 'max-h-96 overflow-hidden'} relative`}>
        {getContent()}

        {!isExpanded && (
          <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-white to-transparent pointer-events-none" />
        )}
      </div>

      {/* Key Takeaways */}
      {article.key_takeaways && article.key_takeaways.length > 0 && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Key Takeaways</h4>
          <ul className="space-y-1">
            {article.key_takeaways.map((takeaway, index) => (
              <li key={index} className="flex items-start space-x-2 text-sm text-gray-600">
                <span className="w-1.5 h-1.5 bg-primary-600 rounded-full mt-2 flex-shrink-0" />
                <span>{takeaway}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}