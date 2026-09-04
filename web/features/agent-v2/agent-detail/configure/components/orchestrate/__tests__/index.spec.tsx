import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vite-plus/test'
import { AgentOrchestratePanel } from '../index'

vi.mock('../header', () => ({
  AgentOrchestrateHeader: () => null,
}))

vi.mock('../model-config/field', () => ({
  AgentModelField: () => null,
}))

vi.mock('../prompt-editor', () => ({
  AgentPromptEditor: () => null,
}))

vi.mock('../skills', () => ({
  AgentSkills: () => <div>Skills</div>,
}))

vi.mock('../files', () => ({
  AgentFiles: () => <div>Files</div>,
}))

vi.mock('../tools', () => ({
  AgentTools: () => <div>Tools</div>,
}))

vi.mock('../knowledge', () => ({
  AgentKnowledgeRetrieval: () => (
    <section aria-label="agentV2.agentDetail.configure.knowledgeRetrieval.label">
      <button type="button" aria-label="agentV2.agentDetail.configure.knowledgeRetrieval.add">
        Add knowledge retrieval
      </button>
    </section>
  ),
}))

vi.mock('../advanced', () => ({
  AgentAdvancedSettings: () => null,
}))

describe('AgentOrchestratePanel', () => {
  it('should show the Knowledge Retrieval add section on the configure page', () => {
    render(
      <AgentOrchestratePanel
        agentId="agent-1"
        textGenerationModelList={[]}
        showHeader={false}
        showPublishBar={false}
        onSelectModel={vi.fn()}
      />,
    )

    expect(
      screen.getByRole('region', {
        name: 'agentV2.agentDetail.configure.knowledgeRetrieval.label',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', {
        name: 'agentV2.agentDetail.configure.knowledgeRetrieval.add',
      }),
    ).toBeInTheDocument()
  })
})
