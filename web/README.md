# SEO Article Generator - Web Interface

A modern, responsive web interface for the SEO Article Generator built with Next.js, React, and Tailwind CSS.

## Features

- **🚀 Modern UI**: Clean, responsive design with Tailwind CSS
- **⚡ Real-time Generation**: Live progress tracking during article generation
- **📝 Rich Preview**: Interactive article previews with multiple view modes
- **💾 Multi-format Downloads**: Export articles as Markdown, HTML, JSON, or ZIP
- **🔧 Configurable**: Extensive configuration options for templates and SEO settings
- **📱 Responsive**: Works seamlessly on desktop, tablet, and mobile devices

## Getting Started

### Prerequisites

- Node.js 18 or later
- npm or yarn
- The SEO Article Generator Python backend (in parent directory)

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** and navigate to [http://localhost:3000](http://localhost:3000)

### Building for Production

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Start the production server**:
   ```bash
   npm start
   ```

## Architecture

### Project Structure

```
web/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── api/            # API routes
│   │   ├── globals.css     # Global styles
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home page
│   ├── components/         # React components
│   │   ├── ui/             # Reusable UI components
│   │   ├── generator/      # Generation-specific components
│   │   └── article/        # Article display components
│   ├── lib/                # Utility libraries
│   ├── types/              # TypeScript type definitions
│   └── ...
├── public/                 # Static assets
├── package.json
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── vercel.json           # Vercel deployment configuration
```

### Key Components

#### Configuration Form (`/src/components/generator/configuration-form.tsx`)
- Dynamic form generation based on available templates
- Real-time validation and configuration
- Brand and SEO settings management

#### Progress Tracker (`/src/components/generator/progress-tracker.tsx`)
- Real-time progress updates via Server-Sent Events
- Visual progress indicators and status messages
- Error handling and recovery

#### Article Preview (`/src/components/article/article-preview.tsx`)
- Multiple view modes (Preview, Markdown, JSON)
- SEO score calculation and display
- Individual article download functionality

#### Download Manager (`/src/components/generator/download-manager.tsx`)
- Bulk download operations
- Multiple format support
- Progress tracking and error handling

### API Routes

#### `/api/config` - Configuration Management
- **GET**: Retrieve application configuration and templates
- Returns merged configuration from YAML files

#### `/api/generate` - Article Generation
- **POST**: Start article generation process
- Uses Server-Sent Events for real-time progress
- Accepts `ArticleConfig` object with generation parameters

#### `/api/download` - File Downloads
- **POST**: Generate and download articles in various formats
- Supports single article or bulk downloads
- Formats: Markdown, HTML, JSON, ZIP

### Integration with Python Backend

The web interface integrates with the Python SEO Article Generator through:

1. **Configuration Loading**: Reads YAML configuration files from the parent directory
2. **Article Generation**: Simulates Python script execution (can be replaced with actual Python integration)
3. **Template Processing**: Uses the same template structure as the Python backend

## Deployment

### Vercel Deployment

This application is optimized for deployment on Vercel:

1. **Connect your repository** to Vercel
2. **Set the root directory** to `web`
3. **Configure environment variables** in the Vercel dashboard
4. **Deploy** - Vercel will automatically build and deploy your application

### Environment Variables

Configure these environment variables for production:

```bash
NODE_ENV=production
API_BASE_URL=https://your-domain.com
MAX_ARTICLES_PER_REQUEST=50
MAX_WORD_COUNT=5000
```

### Custom Deployment

For custom deployment:

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Start with a process manager** like PM2:
   ```bash
   pm2 start npm --name "seo-generator" -- start
   ```

## Configuration

### Templates

Template configurations are loaded from `/config/templates.yaml` in the parent directory. The web interface automatically generates form fields based on available templates and their variables.

### Brand Settings

Customize your brand information in the configuration form:
- Company name and website
- Tagline and branding
- SEO preferences

### Output Formats

The application supports multiple output formats:
- **Markdown**: Clean, readable format for blogs
- **HTML**: Web-ready with embedded styles
- **JSON**: Structured data for API integration
- **ZIP**: Bundle containing all formats

## Development

### Adding New Components

1. Create component files in `/src/components/`
2. Use the established patterns for props and styling
3. Include TypeScript interfaces for type safety

### Styling Guidelines

- Use Tailwind CSS utility classes
- Follow the established design system
- Maintain responsive design patterns
- Use the predefined color palette

### API Integration

To replace the simulation with real Python integration:

1. Update `/src/lib/python-bridge.ts`
2. Implement actual Python script execution
3. Handle real-time output streaming
4. Maintain the existing interface contracts

## Performance

### Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Image Optimization**: Built-in Next.js image optimization
- **Caching**: Aggressive caching for static assets
- **Bundle Analysis**: Use `npm run analyze` to examine bundle size

### Monitoring

- Built-in Next.js performance monitoring
- Vercel Analytics integration (when deployed to Vercel)
- Error boundary components for graceful error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the SEO Article Generator and follows the same license terms.