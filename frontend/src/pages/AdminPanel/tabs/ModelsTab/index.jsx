import React from 'react'
import './ModelsTab.css'

function ModelsTab({
  aiMode,
  setAiMode,
  apiKey,
  setApiKey,
  modelName,
  isModelLoaded,
  aiConfigLoading,
  handleUpdateAIConfig,
  handleLoadModel,
  handleUnloadModel
}) {
  return (
    <div className="models-section">
      <div className="section-card">
        <h3>AI 모델 사용 방식</h3>
        <p className="section-description">
          힌트 챗봇에 사용할 AI 모델의 사용 방식을 선택하세요. 모든 사용자에게 적용됩니다.
        </p>

        <div className="mode-selector">
          <label className={`mode-option ${aiMode === 'api' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="aiMode"
              value="api"
              checked={aiMode === 'api'}
              onChange={(e) => setAiMode(e.target.value)}
            />
            <div className="mode-content">
              <div className="mode-title">API 방식 (Hugging Face)</div>
              <div className="mode-description">
                외부 API를 사용하여 모델을 호출합니다. 별도의 GPU 없이 사용 가능하며, 월 30,000회 무료 제공됩니다.
              </div>
            </div>
          </label>

          <label className={`mode-option ${aiMode === 'local' ? 'selected' : ''}`}>
            <input
              type="radio"
              name="aiMode"
              value="local"
              checked={aiMode === 'local'}
              onChange={(e) => setAiMode(e.target.value)}
            />
            <div className="mode-content">
              <div className="mode-title">로컬 로드 방식</div>
              <div className="mode-description">
                모델을 서버 메모리에 로드하여 사용합니다. 고성능 GPU(16GB+ VRAM)가 필요하지만 무제한 사용 가능합니다.
              </div>
            </div>
          </label>
        </div>
      </div>

      {aiMode === 'api' && (
        <div className="section-card">
          <h3>Hugging Face API 키</h3>
          <p className="section-description">
            Hugging Face 계정의 API 키를 입력하세요. 입력한 키는 .env 파일에 저장됩니다.
          </p>

          <div className="api-key-input">
            <input
              type="password"
              placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <a
              href="https://huggingface.co/settings/tokens"
              target="_blank"
              rel="noopener noreferrer"
              className="get-api-key-link"
            >
              API 키 발급받기
            </a>
          </div>
        </div>
      )}

      {aiMode === 'local' && (
        <div className="section-card">
          <h3>로컬 모델 관리</h3>
          <p className="section-description">
            모델을 메모리에 로드하거나 언로드할 수 있습니다. 로드 완료까지 수 분이 걸릴 수 있습니다.
          </p>

          <div className="model-status">
            <div className="status-item">
              <span className="status-label">모델 상태:</span>
              <span className={`status-value ${isModelLoaded ? 'loaded' : 'unloaded'}`}>
                {isModelLoaded ? '로드됨' : '언로드됨'}
              </span>
            </div>
          </div>

          <div className="model-actions">
            {!isModelLoaded ? (
              <button
                className="load-model-btn"
                onClick={handleLoadModel}
                disabled={aiConfigLoading}
              >
                {aiConfigLoading ? '로드 중...' : '모델 로드'}
              </button>
            ) : (
              <button
                className="unload-model-btn"
                onClick={handleUnloadModel}
                disabled={aiConfigLoading}
              >
                {aiConfigLoading ? '언로드 중...' : '모델 언로드'}
              </button>
            )}
          </div>
        </div>
      )}

      <div className="section-card">
        <h3>모델 정보</h3>
        <p className="section-description">
          사용 중인 모델: {modelName}
        </p>
      </div>

      <button
        className="save-config-btn"
        onClick={handleUpdateAIConfig}
        disabled={aiConfigLoading}
      >
        {aiConfigLoading ? '저장 중...' : 'AI 설정 저장'}
      </button>
    </div>
  )
}

export default ModelsTab
