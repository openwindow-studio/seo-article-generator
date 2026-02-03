'use client'

import { useEffect, useState } from 'react'
import { GenerationProgress } from '@/types/article'
import { ProgressBar } from '@/components/ui/progress-bar'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { CheckCircle, AlertCircle, FileText } from 'lucide-react'

interface ProgressTrackerProps {
  progress: GenerationProgress
  className?: string
}

export function ProgressTracker({ progress, className = '' }: ProgressTrackerProps) {
  const [animatedProgress, setAnimatedProgress] = useState(0)

  useEffect(() => {
    // Animate progress bar
    const timer = setTimeout(() => {
      setAnimatedProgress(progress.progress)
    }, 100)

    return () => clearTimeout(timer)
  }, [progress.progress])

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'generating':
        return <LoadingSpinner size="sm" />
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-600" />
      default:
        return <FileText className="w-5 h-5 text-gray-400" />
    }
  }

  const getStatusColor = () => {
    switch (progress.status) {
      case 'generating':
        return 'text-blue-600'
      case 'completed':
        return 'text-green-600'
      case 'error':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  const getStatusMessage = () => {
    switch (progress.status) {
      case 'idle':
        return 'Ready to generate articles'
      case 'generating':
        return progress.message || 'Generating articles...'
      case 'completed':
        return `Successfully generated ${progress.articles.length} article${progress.articles.length !== 1 ? 's' : ''}`
      case 'error':
        return progress.error || 'An error occurred during generation'
      default:
        return 'Unknown status'
    }
  }

  if (progress.status === 'idle') {
    return (
      <div className={`card ${className}`}>
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <span className={`text-sm ${getStatusColor()}`}>
            {getStatusMessage()}
          </span>
        </div>
      </div>
    )
  }

  return (
    <div className={`card ${className}`}>
      <div className="space-y-4">
        {/* Status Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {getStatusIcon()}
            <span className={`font-medium ${getStatusColor()}`}>
              {progress.status === 'generating' ? 'Generating Articles' :
               progress.status === 'completed' ? 'Generation Complete' : 'Generation Failed'}
            </span>
          </div>

          {progress.status === 'completed' && progress.articles.length > 0 && (
            <div className="text-sm text-gray-600">
              {progress.articles.length} article{progress.articles.length !== 1 ? 's' : ''} generated
            </div>
          )}
        </div>

        {/* Progress Bar */}
        {(progress.status === 'generating' || progress.status === 'completed') && (
          <ProgressBar progress={animatedProgress} />
        )}

        {/* Status Message */}
        <div className={`text-sm ${getStatusColor()}`}>
          {getStatusMessage()}
        </div>

        {/* Article List Preview */}
        {progress.articles.length > 0 && (
          <div className="border-t border-gray-200 pt-4">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Generated Articles</h4>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {progress.articles.map((article, index) => (
                <div
                  key={article.id}
                  className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg"
                >
                  <div className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-xs font-medium">
                    {index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {article.title}
                    </p>
                    <p className="text-xs text-gray-500">
                      {article.template_type.replace('_', ' ')} • {article.word_count || 'Calculating...'} words
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Error Details */}
        {progress.status === 'error' && progress.error && (
          <div className="border-t border-gray-200 pt-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-red-800 mb-2">Error Details</h4>
              <p className="text-sm text-red-600">{progress.error}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}