export interface ArticleConfig {
  templateType: string
  variables: Record<string, any>
  count: number
  outputFormats: string[]
  brand: {
    name: string
    website: string
    tagline: string
  }
  seo: {
    minWordCount: number
    maxWordCount: number
    keywordDensity: number
  }
}

export interface ContentSection {
  type: string
  title?: string
  content?: string
  number?: number
  benefits?: string[]
  items?: string[]
  steps?: Step[]
  tips?: string[]
  table?: ComparisonTable
  subsections?: string[] | AnalysisSection[]
  resources?: Resource[]
}

export interface Step {
  title: string
  description: string
}

export interface ComparisonTable {
  headers: string[]
  rows: string[][]
}

export interface AnalysisSection {
  title: string
  content: string
}

export interface Resource {
  type: string
  description: string
}

export interface GeneratedArticle {
  id: string
  title: string
  intro: string
  template_type: string
  generated_at: string
  content_sections: ContentSection[]
  conclusion: string
  key_takeaways: string[]
  meta: {
    description: string
    keywords: string[]
  }
  word_count?: number
}

export interface GenerationProgress {
  status: 'idle' | 'generating' | 'completed' | 'error'
  progress: number
  message: string
  articles: GeneratedArticle[]
  error?: string
}

export interface TemplateConfig {
  [key: string]: {
    title_patterns: string[]
    intro_patterns: string[]
    description: string
    variables: string[]
  }
}

export interface ConfigData {
  brand: {
    name: string
    website: string
    logo_url: string
    tagline: string
  }
  seo: {
    min_word_count: number
    max_word_count: number
    keyword_density: number
    meta_description_length: number
  }
  generation: {
    default_count: number
    max_parallel_workers: number
    output_dir: string
  }
  template_distribution: Record<string, number>
  variable_pools: Record<string, string[]>
  content_blocks: {
    conclusions: string[]
    takeaways: string[]
    [key: string]: any
  }
  output_formats: string[]
}