import { NextRequest, NextResponse } from 'next/server'
import { PythonBridge } from '@/lib/python-bridge'

export async function GET() {
  try {
    const bridge = PythonBridge.getInstance()
    const config = await bridge.loadConfig()
    const templates = await bridge.loadTemplates()

    return NextResponse.json({
      config,
      templates
    })
  } catch (error) {
    console.error('Failed to load configuration:', error)
    return NextResponse.json(
      { error: 'Failed to load configuration' },
      { status: 500 }
    )
  }
}