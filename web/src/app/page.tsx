'use client'

import { useState } from 'react'
import { ArticleConfig, GeneratedArticle, GenerationProgress } from '@/types/article'
import { ConfigurationForm } from '@/components/generator/configuration-form'
import { ProgressTracker } from '@/components/generator/progress-tracker'
import { ArticleList } from '@/components/article/article-list'
import { DownloadManager } from '@/components/generator/download-manager'
import { FileText, Sparkles, Settings, Download } from 'lucide-react'

export default function HomePage() {
  const [progress, setProgress] = useState<GenerationProgress>({
    status: 'idle',
    progress: 0,
    message: '',
    articles: []
  })

  const [currentTab, setCurrentTab] = useState<'configure' | 'articles' | 'download'>('configure')

  const handleGenerate = async (config: ArticleConfig) => {
    setProgress({
      status: 'generating',
      progress: 0,
      message: 'Starting generation...',
      articles: []
    })

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
      })

      if (!response.ok) {
        throw new Error('Failed to start generation')
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('No response body')
      }

      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))

              if (data.type === 'progress') {
                setProgress(prev => ({
                  ...prev,
                  progress: data.progress,
                  message: data.message
                }))
              } else if (data.type === 'complete') {
                setProgress({
                  status: 'completed',
                  progress: 100,
                  message: 'Generation completed!',
                  articles: data.articles
                })
                // Switch to articles tab when complete
                setCurrentTab('articles')
              } else if (data.type === 'error') {
                setProgress(prev => ({
                  ...prev,
                  status: 'error',
                  error: data.error
                }))
              }
            } catch (e) {
              // Ignore JSON parsing errors for incomplete chunks
            }
          }
        }
      }
    } catch (error) {
      setProgress(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      }))
    }
  }

  const downloadSingle = async (article: GeneratedArticle, format: string) => {
    try {
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          articles: [article],
          format,
          filename: `${article.title.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_')}.${format}`
        })
      })

      if (!response.ok) {
        throw new Error('Download failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${article.title.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_')}.${format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const downloadAll = async (format: string) => {
    try {
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          articles: progress.articles,
          format,
          filename: `articles.${format === 'zip' ? 'zip' : format}`
        })
      })

      if (!response.ok) {
        throw new Error('Download failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `articles.${format === 'zip' ? 'zip' : format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">
                SEO Article Generator
              </h1>
            </div>

            <div className="text-sm text-gray-500">
              Generate high-quality, SEO-optimized articles with AI
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setCurrentTab('configure')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                currentTab === 'configure'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Settings className="w-4 h-4" />
                <span>Configure</span>
              </div>
            </button>

            <button
              onClick={() => setCurrentTab('articles')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                currentTab === 'articles'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>Articles ({progress.articles.length})</span>
              </div>
            </button>

            <button
              onClick={() => setCurrentTab('download')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                currentTab === 'download'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
              disabled={progress.articles.length === 0}
            >
              <div className="flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Download</span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Progress Tracker - Always visible when generating or completed */}
          {(progress.status !== 'idle') && (
            <ProgressTracker progress={progress} />
          )}

          {/* Tab Content */}
          {currentTab === 'configure' && (
            <ConfigurationForm
              onSubmit={handleGenerate}
              loading={progress.status === 'generating'}
            />
          )}

          {currentTab === 'articles' && (
            <ArticleList
              articles={progress.articles}
              onDownloadSingle={downloadSingle}
              onDownloadAll={downloadAll}
            />
          )}

          {currentTab === 'download' && (
            <DownloadManager articles={progress.articles} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>SEO Article Generator - Powered by AI</p>
            <p className="mt-1">Generate high-quality, SEO-optimized content for your business</p>
          </div>
        </div>
      </footer>
    </div>
  )
}