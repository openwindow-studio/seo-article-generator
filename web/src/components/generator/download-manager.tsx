'use client'

import { useState } from 'react'
import { GeneratedArticle } from '@/types/article'
import { Button } from '@/components/ui/button'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { Download, CheckCircle, AlertCircle } from 'lucide-react'

interface DownloadManagerProps {
  articles: GeneratedArticle[]
  className?: string
}

export function DownloadManager({ articles, className = '' }: DownloadManagerProps) {
  const [downloading, setDownloading] = useState<string | null>(null)
  const [downloadStatus, setDownloadStatus] = useState<{
    success: boolean
    message: string
  } | null>(null)

  const downloadFile = async (articles: GeneratedArticle[], format: string, filename?: string) => {
    if (articles.length === 0) {
      setDownloadStatus({
        success: false,
        message: 'No articles to download'
      })
      return
    }

    setDownloading(format)
    setDownloadStatus(null)

    try {
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          articles,
          format,
          filename: filename || `articles.${format === 'zip' ? 'zip' : format}`
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Download failed')
      }

      // Create download link
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = filename || `articles.${format === 'zip' ? 'zip' : format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      setDownloadStatus({
        success: true,
        message: `Successfully downloaded ${articles.length} article${articles.length !== 1 ? 's' : ''} as ${format.toUpperCase()}`
      })
    } catch (error) {
      setDownloadStatus({
        success: false,
        message: error instanceof Error ? error.message : 'Download failed'
      })
    } finally {
      setDownloading(null)
      // Clear status after 5 seconds
      setTimeout(() => setDownloadStatus(null), 5000)
    }
  }

  const downloadSingle = async (article: GeneratedArticle, format: string) => {
    const sanitizedTitle = article.title
      .replace(/[^a-zA-Z0-9\s]/g, '')
      .replace(/\s+/g, '_')
      .substring(0, 50)

    await downloadFile([article], format, `${sanitizedTitle}.${format}`)
  }

  const downloadAll = async (format: string) => {
    await downloadFile(articles, format)
  }

  if (articles.length === 0) {
    return null
  }

  return (
    <div className={`card ${className}`}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Download Articles</h3>
          <span className="text-sm text-gray-600">
            {articles.length} article{articles.length !== 1 ? 's' : ''} ready
          </span>
        </div>

        {/* Download Status */}
        {downloadStatus && (
          <div className={`p-3 rounded-lg flex items-center space-x-2 ${
            downloadStatus.success
              ? 'bg-green-50 border border-green-200'
              : 'bg-red-50 border border-red-200'
          }`}>
            {downloadStatus.success ? (
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
            )}
            <span className={`text-sm ${
              downloadStatus.success ? 'text-green-800' : 'text-red-800'
            }`}>
              {downloadStatus.message}
            </span>
          </div>
        )}

        {/* Download Options */}
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">Download All Articles</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => downloadAll('markdown')}
                loading={downloading === 'markdown'}
                disabled={downloading !== null}
                className="w-full"
              >
                {downloading === 'markdown' ? (
                  <LoadingSpinner size="sm" className="mr-2" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                Markdown
              </Button>

              <Button
                variant="secondary"
                size="sm"
                onClick={() => downloadAll('html')}
                loading={downloading === 'html'}
                disabled={downloading !== null}
                className="w-full"
              >
                {downloading === 'html' ? (
                  <LoadingSpinner size="sm" className="mr-2" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                HTML
              </Button>

              <Button
                variant="secondary"
                size="sm"
                onClick={() => downloadAll('json')}
                loading={downloading === 'json'}
                disabled={downloading !== null}
                className="w-full"
              >
                {downloading === 'json' ? (
                  <LoadingSpinner size="sm" className="mr-2" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                JSON
              </Button>

              <Button
                variant="primary"
                size="sm"
                onClick={() => downloadAll('zip')}
                loading={downloading === 'zip'}
                disabled={downloading !== null}
                className="w-full"
              >
                {downloading === 'zip' ? (
                  <LoadingSpinner size="sm" className="mr-2" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                ZIP Archive
              </Button>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Individual Downloads</h4>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {articles.map((article, index) => (
                <div
                  key={article.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {article.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {article.template_type.replace('_', ' ')} • {article.word_count || 'Calculating...'} words
                    </p>
                  </div>

                  <div className="flex items-center space-x-1 ml-4">
                    <button
                      onClick={() => downloadSingle(article, 'markdown')}
                      disabled={downloading !== null}
                      className="text-xs text-primary-600 hover:text-primary-800 disabled:opacity-50 px-2 py-1 rounded"
                    >
                      MD
                    </button>
                    <button
                      onClick={() => downloadSingle(article, 'html')}
                      disabled={downloading !== null}
                      className="text-xs text-primary-600 hover:text-primary-800 disabled:opacity-50 px-2 py-1 rounded"
                    >
                      HTML
                    </button>
                    <button
                      onClick={() => downloadSingle(article, 'json')}
                      disabled={downloading !== null}
                      className="text-xs text-primary-600 hover:text-primary-800 disabled:opacity-50 px-2 py-1 rounded"
                    >
                      JSON
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Help Text */}
        <div className="text-xs text-gray-500 pt-3 border-t border-gray-200">
          <p><strong>Markdown:</strong> Plain text with formatting for blogs and documentation</p>
          <p><strong>HTML:</strong> Web-ready format with styling for direct publishing</p>
          <p><strong>JSON:</strong> Structured data format for integration with other tools</p>
          <p><strong>ZIP:</strong> All formats bundled together with summary information</p>
        </div>
      </div>
    </div>
  )
}