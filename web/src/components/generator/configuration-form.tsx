'use client'

import { useState, useEffect } from 'react'
import { ArticleConfig, ConfigData, TemplateConfig } from '@/types/article'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'

interface ConfigurationFormProps {
  onSubmit: (config: ArticleConfig) => void
  loading?: boolean
}

export function ConfigurationForm({ onSubmit, loading = false }: ConfigurationFormProps) {
  const [config, setConfig] = useState<Partial<ArticleConfig>>({
    templateType: '',
    count: 5,
    variables: {},
    outputFormats: ['markdown'],
    brand: {
      name: 'Your Company',
      website: 'https://example.com',
      tagline: 'Your Tagline Here'
    },
    seo: {
      minWordCount: 800,
      maxWordCount: 2500,
      keywordDensity: 0.02
    }
  })

  const [appConfig, setAppConfig] = useState<ConfigData | null>(null)
  const [templates, setTemplates] = useState<TemplateConfig | null>(null)

  useEffect(() => {
    // Load configuration and templates
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        // Handle the response structure correctly
        setAppConfig(data)
        setTemplates(data.templates)

        // Update form with loaded config if available
        if (data.variables) {
          setConfig(prev => ({
            ...prev,
            variables: data.variables,
            brand: {
              name: data.variables.brandName || 'SE0',
              website: 'https://se0.ai',
              tagline: 'Generate 500+ SEO Articles with One Click'
            },
            seo: data.seoSettings || prev.seo
          }))
        }
      })
      .catch(console.error)
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(config as ArticleConfig)
  }

  const handleVariableChange = (key: string, value: string) => {
    setConfig(prev => ({
      ...prev,
      variables: {
        ...prev.variables,
        [key]: value
      }
    }))
  }

  const getTemplateOptions = () => {
    // Handle both array and object structures
    if (!templates && !appConfig?.templates) return []

    const templateData = templates || appConfig?.templates || []

    // If it's an array of template objects
    if (Array.isArray(templateData)) {
      return templateData.map(template => ({
        value: template.id,
        label: `${template.name} - ${template.description || ''}`
      }))
    }

    // If it's an object
    return Object.entries(templateData).map(([key, template]: [string, any]) => ({
      value: key,
      label: `${key.replace(/_/g, ' ').toUpperCase()} - ${template.description || ''}`
    }))
  }

  const getVariableFields = () => {
    // For now, return common variable fields for all templates
    return ['products', 'use_cases', 'audiences', 'benefits']
  }

  const getVariableOptions = (variableType: string) => {
    // Check both possible paths for variables
    const variables = appConfig?.variable_pools?.[variableType] || appConfig?.variables?.[variableType]

    if (!variables || !Array.isArray(variables)) return []

    return variables.map(item => ({
      value: item,
      label: item
    }))
  }

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Configure Article Generation</h2>
        <p className="text-gray-600">
          Set up your article generation parameters and customize the output to your needs.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Template Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Select
            label="Article Template Type"
            options={getTemplateOptions()}
            value={config.templateType}
            onChange={(e) => setConfig(prev => ({ ...prev, templateType: e.target.value }))}
            placeholder="Select a template type"
            required
          />

          <Input
            label="Number of Articles"
            type="number"
            min={1}
            max={50}
            value={config.count}
            onChange={(e) => setConfig(prev => ({ ...prev, count: parseInt(e.target.value) }))}
            helperText="Generate 1-50 articles at once"
            required
          />
        </div>

        {/* Dynamic Variable Fields */}
        {getVariableFields().length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Template Variables</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {getVariableFields().map((variable) => {
                const options = getVariableOptions(variable)

                if (options.length > 0) {
                  return (
                    <Select
                      key={variable}
                      label={variable.replace('_', ' ').toUpperCase()}
                      options={options}
                      value={config.variables?.[variable] || ''}
                      onChange={(e) => handleVariableChange(variable, e.target.value)}
                      placeholder={`Select ${variable}`}
                    />
                  )
                } else {
                  return (
                    <Input
                      key={variable}
                      label={variable.replace('_', ' ').toUpperCase()}
                      value={config.variables?.[variable] || ''}
                      onChange={(e) => handleVariableChange(variable, e.target.value)}
                      placeholder={`Enter ${variable}`}
                    />
                  )
                }
              })}
            </div>
          </div>
        )}

        {/* Brand Configuration */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Brand Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Company Name"
              value={config.brand?.name || ''}
              onChange={(e) => setConfig(prev => ({
                ...prev,
                brand: { ...prev.brand!, name: e.target.value }
              }))}
              placeholder="Your Company Name"
            />
            <Input
              label="Website"
              type="url"
              value={config.brand?.website || ''}
              onChange={(e) => setConfig(prev => ({
                ...prev,
                brand: { ...prev.brand!, website: e.target.value }
              }))}
              placeholder="https://example.com"
            />
            <div className="md:col-span-2">
              <Input
                label="Tagline"
                value={config.brand?.tagline || ''}
                onChange={(e) => setConfig(prev => ({
                  ...prev,
                  brand: { ...prev.brand!, tagline: e.target.value }
                }))}
                placeholder="Your company tagline"
              />
            </div>
          </div>
        </div>

        {/* SEO Configuration */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">SEO Settings</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label="Min Word Count"
              type="number"
              min={100}
              value={config.seo?.minWordCount || 800}
              onChange={(e) => setConfig(prev => ({
                ...prev,
                seo: { ...prev.seo!, minWordCount: parseInt(e.target.value) }
              }))}
            />
            <Input
              label="Max Word Count"
              type="number"
              min={500}
              value={config.seo?.maxWordCount || 2500}
              onChange={(e) => setConfig(prev => ({
                ...prev,
                seo: { ...prev.seo!, maxWordCount: parseInt(e.target.value) }
              }))}
            />
            <Input
              label="Keyword Density"
              type="number"
              step={0.01}
              min={0.01}
              max={0.1}
              value={config.seo?.keywordDensity || 0.02}
              onChange={(e) => setConfig(prev => ({
                ...prev,
                seo: { ...prev.seo!, keywordDensity: parseFloat(e.target.value) }
              }))}
              helperText="Recommended: 0.02 (2%)"
            />
          </div>
        </div>

        {/* Output Formats */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Output Formats</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['markdown', 'html', 'json', 'zip'].map((format) => (
              <label key={format} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={config.outputFormats?.includes(format) || false}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setConfig(prev => ({
                        ...prev,
                        outputFormats: [...(prev.outputFormats || []), format]
                      }))
                    } else {
                      setConfig(prev => ({
                        ...prev,
                        outputFormats: (prev.outputFormats || []).filter(f => f !== format)
                      }))
                    }
                  }}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700 capitalize">{format}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="flex justify-end pt-6 border-t border-gray-200">
          <Button
            type="submit"
            loading={loading}
            disabled={!config.templateType || !config.count}
            size="lg"
          >
            Generate Articles
          </Button>
        </div>
      </form>
    </div>
  )
}