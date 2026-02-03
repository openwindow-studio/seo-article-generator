'use client'

import { useState } from 'react'
import { GeneratedArticle } from '@/types/article'
import { ArticlePreview } from './article-preview'
import { Button } from '@/components/ui/button'
import { Select } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { ArticleFormatter } from '@/lib/formatters'
import { Download, Search, Filter, Grid, List } from 'lucide-react'

interface ArticleListProps {
  articles: GeneratedArticle[]
  onDownloadSingle?: (article: GeneratedArticle, format: string) => void
  onDownloadAll?: (format: string) => void
  className?: string
}

export function ArticleList({
  articles,
  onDownloadSingle,
  onDownloadAll,
  className = ''
}: ArticleListProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState<'title' | 'date' | 'wordCount' | 'seoScore'>('date')
  const [filterTemplate, setFilterTemplate] = useState<string>('')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('list')

  // Filter and sort articles
  const filteredArticles = articles
    .filter(article => {
      const matchesSearch = searchTerm === '' ||
        article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.meta.description.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesTemplate = filterTemplate === '' ||
        article.template_type === filterTemplate

      return matchesSearch && matchesTemplate
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title)
        case 'date':
          return new Date(b.generated_at).getTime() - new Date(a.generated_at).getTime()
        case 'wordCount':
          const aWords = a.word_count || ArticleFormatter.getWordCount(a)
          const bWords = b.word_count || ArticleFormatter.getWordCount(b)
          return bWords - aWords
        case 'seoScore':
          const aScore = ArticleFormatter.getSeoScore(a)
          const bScore = ArticleFormatter.getSeoScore(b)
          return bScore - aScore
        default:
          return 0
      }
    })

  const templateTypes = Array.from(new Set(articles.map(a => a.template_type)))
  const templateOptions = [
    { value: '', label: 'All Templates' },
    ...templateTypes.map(type => ({
      value: type,
      label: type.replace('_', ' ').toUpperCase()
    }))
  ]

  const sortOptions = [
    { value: 'date', label: 'Date Created' },
    { value: 'title', label: 'Title (A-Z)' },
    { value: 'wordCount', label: 'Word Count' },
    { value: 'seoScore', label: 'SEO Score' }
  ]

  if (articles.length === 0) {
    return (
      <div className={`card text-center py-12 ${className}`}>
        <div className="text-gray-400 mb-4">
          <Grid className="w-12 h-12 mx-auto" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No articles generated yet</h3>
        <p className="text-gray-600">
          Configure your settings and generate articles to see them here.
        </p>
      </div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header with Controls */}
      <div className="card">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between space-y-4 lg:space-y-0">
          <div className="flex items-center space-x-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Generated Articles ({filteredArticles.length})
            </h2>

            {/* View Mode Toggle */}
            <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('list')}
                className={`p-1.5 rounded-md transition-colors ${
                  viewMode === 'list'
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <List className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={`p-1.5 rounded-md transition-colors ${
                  viewMode === 'grid'
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Grid className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Bulk Actions */}
          {onDownloadAll && (
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Download All:</span>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownloadAll('markdown')}
              >
                <Download className="w-4 h-4 mr-1" />
                MD
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownloadAll('html')}
              >
                <Download className="w-4 h-4 mr-1" />
                HTML
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onDownloadAll('zip')}
              >
                <Download className="w-4 h-4 mr-1" />
                ZIP
              </Button>
            </div>
          )}
        </div>

        {/* Filters and Search */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search articles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input pl-10"
            />
          </div>

          <Select
            options={templateOptions}
            value={filterTemplate}
            onChange={(e) => setFilterTemplate(e.target.value)}
            placeholder="Filter by template"
          />

          <Select
            options={sortOptions}
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            placeholder="Sort by"
          />
        </div>
      </div>

      {/* Article Grid/List */}
      {filteredArticles.length === 0 ? (
        <div className="card text-center py-8">
          <Filter className="w-8 h-8 text-gray-400 mx-auto mb-3" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No articles match your filters</h3>
          <p className="text-gray-600">Try adjusting your search or filter criteria.</p>
        </div>
      ) : (
        <div className={
          viewMode === 'grid'
            ? 'grid grid-cols-1 xl:grid-cols-2 gap-6'
            : 'space-y-6'
        }>
          {filteredArticles.map((article) => (
            <ArticlePreview
              key={article.id}
              article={article}
              onDownload={onDownloadSingle}
            />
          ))}
        </div>
      )}
    </div>
  )
}