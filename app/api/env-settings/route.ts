import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const ENV_FILE_PATH = path.join(process.cwd(), '.env')

// Environment variables we want to expose for editing
const EDITABLE_VARS = [
  'AGENT_TEST_MODE',
  'ROLE_TEST_MODE', 
  'TEST_MODE',
  'ENABLE_HITL',
  'AUTO_ACTION',
  // Enhanced 10-step Workflow Configuration
  'WORKFLOW_REQUIREMENTS_GATHERING_ENABLED',
  'WORKFLOW_REQUIREMENTS_MAX_QUESTIONS',
  'WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES',
  'WORKFLOW_REQUIREMENTS_AUTO_PROCEED',
  'WORKFLOW_HITL_ANALYZE_REQUIRED',
  'WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES',
  'WORKFLOW_HITL_DESIGN_REQUIRED',
  'WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES',
  'WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS',
  'WORKFLOW_ARTIFACT_UI_INTEGRATION'
]

interface EnvVariable {
  key: string
  value: string | boolean | number
  description: string
  category?: string
  type: 'string' | 'boolean' | 'number'
}

const getVariableDescription = (key: string): string => {
  const descriptions: Record<string, string> = {
    'AGENT_TEST_MODE': 'Enable agent test mode to return static confirmations',
    'ROLE_TEST_MODE': 'Enable role test mode for LLM role confirmation', 
    'TEST_MODE': 'Enable overall test mode for mock LLM responses',
    'ENABLE_HITL': 'Enable Human-in-the-Loop functionality',
    'AUTO_ACTION': 'Default auto action (approve/reject)',
    // Enhanced 10-step Workflow Configuration
    'WORKFLOW_REQUIREMENTS_GATHERING_ENABLED': 'Enable interactive requirements gathering in workflows',
    'WORKFLOW_REQUIREMENTS_MAX_QUESTIONS': 'Maximum number of requirements gathering questions',
    'WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES': 'Timeout for requirements gathering (minutes)',
    'WORKFLOW_REQUIREMENTS_AUTO_PROCEED': 'Automatically proceed when requirements gathering times out',
    'WORKFLOW_HITL_ANALYZE_REQUIRED': 'Require human approval at Analyze stage',
    'WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES': 'Timeout for Analyze stage approval (minutes)',
    'WORKFLOW_HITL_DESIGN_REQUIRED': 'Require human approval at Design stage',
    'WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES': 'Timeout for Design stage approval (minutes)',
    'WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS': 'Automatically create artifact placeholders',
    'WORKFLOW_ARTIFACT_UI_INTEGRATION': 'Enable UI integration for artifact scaffolding'
  }
  return descriptions[key] || 'Configuration setting'
}

const parseEnvFile = (): Record<string, string> => {
  try {
    if (!fs.existsSync(ENV_FILE_PATH)) {
      return {}
    }
    
    const content = fs.readFileSync(ENV_FILE_PATH, 'utf8')
    const env: Record<string, string> = {}
    
    content.split('\n').forEach(line => {
      const trimmed = line.trim()
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const [key, ...valueParts] = trimmed.split('=')
        const value = valueParts.join('=').trim()
        env[key.trim()] = value
      }
    })
    
    return env
  } catch (error) {
    console.error('Error reading .env file:', error)
    return {}
  }
}

const updateEnvFile = (updates: Record<string, string>): boolean => {
  try {
    if (!fs.existsSync(ENV_FILE_PATH)) {
      console.error('.env file not found')
      return false
    }
    
    let content = fs.readFileSync(ENV_FILE_PATH, 'utf8')
    
    // Update each variable
    Object.entries(updates).forEach(([key, value]) => {
      if (EDITABLE_VARS.includes(key)) {
        const regex = new RegExp(`^${key}=.*$`, 'm')
        const newLine = `${key}=${value}`
        
        if (regex.test(content)) {
          content = content.replace(regex, newLine)
        } else {
          // If variable doesn't exist, add it to the end
          content += `\n${newLine}`
        }
      }
    })
    
    fs.writeFileSync(ENV_FILE_PATH, content, 'utf8')
    return true
  } catch (error) {
    console.error('Error updating .env file:', error)
    return false
  }
}

const convertValue = (key: string, value: string): string | boolean | number => {
  const booleanVars = [
    'AGENT_TEST_MODE', 'ROLE_TEST_MODE', 'TEST_MODE', 'ENABLE_HITL',
    'WORKFLOW_REQUIREMENTS_GATHERING_ENABLED', 'WORKFLOW_REQUIREMENTS_AUTO_PROCEED',
    'WORKFLOW_HITL_ANALYZE_REQUIRED', 'WORKFLOW_HITL_DESIGN_REQUIRED',
    'WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS', 'WORKFLOW_ARTIFACT_UI_INTEGRATION'
  ]
  const numberVars = [
    'WORKFLOW_REQUIREMENTS_MAX_QUESTIONS', 'WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES',
    'WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES', 'WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES'
  ]
  
  if (booleanVars.includes(key)) {
    return value.toLowerCase() === 'true'
  }
  if (numberVars.includes(key)) {
    return parseInt(value) || 0
  }
  return value
}

const getVariableType = (key: string): 'string' | 'boolean' | 'number' => {
  const booleanVars = [
    'AGENT_TEST_MODE', 'ROLE_TEST_MODE', 'TEST_MODE', 'ENABLE_HITL',
    'WORKFLOW_REQUIREMENTS_GATHERING_ENABLED', 'WORKFLOW_REQUIREMENTS_AUTO_PROCEED',
    'WORKFLOW_HITL_ANALYZE_REQUIRED', 'WORKFLOW_HITL_DESIGN_REQUIRED',
    'WORKFLOW_ARTIFACT_AUTO_PLACEHOLDERS', 'WORKFLOW_ARTIFACT_UI_INTEGRATION'
  ]
  const numberVars = [
    'WORKFLOW_REQUIREMENTS_MAX_QUESTIONS', 'WORKFLOW_REQUIREMENTS_TIMEOUT_MINUTES',
    'WORKFLOW_HITL_ANALYZE_TIMEOUT_MINUTES', 'WORKFLOW_HITL_DESIGN_TIMEOUT_MINUTES'
  ]
  
  if (booleanVars.includes(key)) {
    return 'boolean'
  }
  if (numberVars.includes(key)) {
    return 'number'
  }
  return 'string'
}

export async function GET() {
  try {
    const envData = parseEnvFile()
    
    const variables: EnvVariable[] = EDITABLE_VARS.map(key => ({
      key,
      value: convertValue(key, envData[key] || (getVariableType(key) === 'number' ? '0' : getVariableType(key) === 'boolean' ? 'false' : '')),
      description: getVariableDescription(key),
      category: key.startsWith('WORKFLOW_') ? 'Workflow Configuration' : 'Testing Configuration',
      type: getVariableType(key)
    }))
    
    return NextResponse.json({ success: true, variables })
  } catch (error) {
    console.error('Error reading environment variables:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to read environment variables' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { variables } = body
    
    if (!variables || !Array.isArray(variables)) {
      return NextResponse.json(
        { success: false, error: 'Invalid request format' },
        { status: 400 }
      )
    }
    
    // Convert variables array to updates object
    const updates: Record<string, string> = {}
    variables.forEach((variable: EnvVariable) => {
      if (EDITABLE_VARS.includes(variable.key)) {
        updates[variable.key] = String(variable.value)
      }
    })
    
    const success = updateEnvFile(updates)
    
    if (success) {
      return NextResponse.json({ success: true, message: 'Environment variables updated successfully' })
    } else {
      return NextResponse.json(
        { success: false, error: 'Failed to update .env file' },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Error updating environment variables:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to update environment variables' },
      { status: 500 }
    )
  }
}