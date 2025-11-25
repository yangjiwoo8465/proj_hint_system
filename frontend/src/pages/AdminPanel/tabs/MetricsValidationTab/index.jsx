import React, { useState, useEffect } from 'react'
import api from '../../../../services/api'
import './MetricsValidationTab.css'

export default function MetricsValidationTab() {
  // localStorage 키
  const STORAGE_KEY = 'metrics_validation_sessions'
  const STORAGE_ACTIVE_ID = 'metrics_validation_active_session'
  const STORAGE_NEXT_ID = 'metrics_validation_next_session_id'

  // localStorage에서 세션 불러오기
  const loadSessionsFromStorage = () => {
    try {
      const savedSessions = localStorage.getItem(STORAGE_KEY)
      const savedActiveId = localStorage.getItem(STORAGE_ACTIVE_ID)
      const savedNextId = localStorage.getItem(STORAGE_NEXT_ID)

      if (savedSessions) {
        return {
          sessions: JSON.parse(savedSessions),
          activeSessionId: savedActiveId ? parseInt(savedActiveId) : 1,
          nextSessionId: savedNextId ? parseInt(savedNextId) : 2
        }
      }
    } catch (error) {
      console.error('Failed to load sessions from localStorage:', error)
    }
    return null
  }

  // 문제 목록
  const [problems, setProblems] = useState([])
  const [loadingProblems, setLoadingProblems] = useState(true)

  // 여러 문제 세션 관리 (localStorage에서 복원 시도)
  const initialData = loadSessionsFromStorage() || {
    sessions: [
      {
        id: 1,
        code: '',
        problemId: '',
        problemTitle: '',
        preset: '초급',
        hintPurpose: 'completion',  // 'completion' or 'optimization'
        customComponents: {
          summary: true,  // 항상 포함
          libraries: true,
          code_example: true,
          step_by_step: false,
          complexity_hint: false,
          edge_cases: false,
          improvements: false
        },
        history: []
      }
    ],
    activeSessionId: 1,
    nextSessionId: 2
  }

  const [sessions, setSessions] = useState(initialData.sessions)
  const [activeSessionId, setActiveSessionId] = useState(initialData.activeSessionId)
  const [nextSessionId, setNextSessionId] = useState(initialData.nextSessionId)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const activeSession = sessions.find(s => s.id === activeSessionId)

  // 세션 데이터가 변경될 때마다 localStorage에 저장
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
      localStorage.setItem(STORAGE_ACTIVE_ID, activeSessionId.toString())
      localStorage.setItem(STORAGE_NEXT_ID, nextSessionId.toString())
    } catch (error) {
      console.error('Failed to save sessions to localStorage:', error)
    }
  }, [sessions, activeSessionId, nextSessionId])

  // 문제 목록 불러오기
  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await api.get('/coding-test/problems/')
        if (response.data.success) {
          setProblems(response.data.data)
        }
      } catch (err) {
        console.error('Failed to fetch problems:', err)
      } finally {
        setLoadingProblems(false)
      }
    }
    fetchProblems()
  }, [])

  // 문제 선택 핸들러
  const handleProblemSelect = (e) => {
    const selectedProblemId = e.target.value
    const selectedProblem = problems.find(p => p.problem_id === selectedProblemId)

    updateSession({
      problemId: selectedProblemId,
      problemTitle: selectedProblem ? selectedProblem.title : ''
    })
  }

  // 프리셋 변경 (요약 설명 방식만 변경, 선택사항은 사용자가 직접 제어)
  const handlePresetChange = (preset) => {
    updateSession({
      preset
    })
  }

  // 커스텀 구성 변경 (프리셋은 유지)
  const handleComponentToggle = (component) => {
    updateSession({
      customComponents: {
        ...activeSession.customComponents,
        [component]: !activeSession.customComponents[component]
      }
    })
  }

  // 세션 추가
  const handleAddSession = () => {
    const newSession = {
      id: nextSessionId,
      code: '',
      problemId: '',
      problemTitle: '',
      preset: '초급',
      hintPurpose: 'completion',  // 'completion' or 'optimization'
      customComponents: {
        summary: true,  // 항상 포함
        libraries: true,
        code_example: true,
        step_by_step: false,
        complexity_hint: false,
        edge_cases: false,
        improvements: false
      },
      history: []
    }
    setSessions([...sessions, newSession])
    setActiveSessionId(nextSessionId)
    setNextSessionId(nextSessionId + 1)
  }

  // 세션 삭제
  const handleDeleteSession = (sessionId) => {
    if (sessions.length === 1) {
      alert('최소 1개의 세션은 유지해야 합니다.')
      return
    }

    const newSessions = sessions.filter(s => s.id !== sessionId)
    setSessions(newSessions)

    if (activeSessionId === sessionId) {
      setActiveSessionId(newSessions[0].id)
    }
  }

  // 세션 데이터 업데이트
  const updateSession = (updates) => {
    setSessions(sessions.map(s =>
      s.id === activeSessionId ? { ...s, ...updates } : s
    ))
  }

  // 검증 실행
  const handleValidate = async () => {
    if (!activeSession.code.trim()) {
      setError('코드를 입력해주세요.')
      return
    }

    if (!activeSession.problemId) {
      setError('문제를 선택해주세요.')
      return
    }

    setLoading(true)
    setError('')

    try {
      // 이전 힌트 이력 생성 (Chain of Hints)
      const previousHints = activeSession.history.map((item, index) => ({
        hint_text: item.hint,
        level: item.preset,
        timestamp: item.timestamp
      }))

      const payload = {
        code: activeSession.code,
        problem_id: activeSession.problemId,
        preset: activeSession.preset,
        hint_purpose: activeSession.hintPurpose,  // 'completion' or 'optimization'
        custom_components: activeSession.customComponents,  // 항상 전송 (사용자가 체크박스로 수정 가능)
        previous_hints: previousHints
      }

      const response = await api.post('/coding-test/admin/validate-metrics/', payload)

      if (response.data.success) {
        const result = response.data.data

        // 히스토리에 추가
        const newHistoryItem = {
          static_metrics: result.static_metrics,
          llm_metrics: result.llm_metrics,
          hint: result.hint,
          hint_purpose: result.hint_purpose,  // 'completion' or 'optimization'
          weak_metrics: result.weak_metrics || null,  // optimization인 경우만
          hint_components: result.hint_components || null,
          totalScore: result.total_score,
          preset: result.preset || activeSession.preset,
          timestamp: new Date().toLocaleString('ko-KR')
        }

        updateSession({
          history: [...activeSession.history, newHistoryItem]
        })
      } else {
        setError(response.data.error || '검증 실패')
      }
    } catch (err) {
      console.error('Validation error:', err)
      setError(err.response?.data?.error || '검증 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  // 세션 초기화
  const handleClearSession = () => {
    updateSession({
      code: '',
      history: []
    })
    setError('')
  }

  const getScoreColor = (score) => {
    if (score >= 80) return '#4caf50'
    if (score >= 60) return '#ff9800'
    return '#f44336'
  }

  const getMetricColor = (value, max = 5) => {
    const percentage = (value / max) * 100
    if (percentage >= 80) return '#4caf50'
    if (percentage >= 60) return '#ff9800'
    return '#f44336'
  }

  // 최신 검증 결과 (맨 마지막 항목)
  const latestResult = activeSession.history.length > 0
    ? activeSession.history[activeSession.history.length - 1]
    : null

  return (
    <div className="metrics-validation-tab">
      <div className="validation-header">
        <h2>📊 메트릭 & 힌트 검증</h2>
        <p>12개 지표 생성 검증 · 지표 기반 힌트 퀄리티 검증 · Chain of Hints 동작 검증</p>
      </div>

      {/* 세션 탭 */}
      <div className="session-tabs">
        {sessions.map(session => (
          <div
            key={session.id}
            className={`session-tab ${activeSessionId === session.id ? 'active' : ''}`}
            onClick={() => setActiveSessionId(session.id)}
          >
            <span>{session.problemTitle || `세션 ${session.id}`}</span>
            {sessions.length > 1 && (
              <button
                className="session-delete-btn"
                onClick={(e) => {
                  e.stopPropagation()
                  handleDeleteSession(session.id)
                }}
              >
                ×
              </button>
            )}
          </div>
        ))}
        <button className="session-add-btn" onClick={handleAddSession}>
          + 새 세션
        </button>
      </div>

      <div className="validation-container">
        {/* 좌측: 입력 영역 */}
        <div className="input-section">
          <h3>힌트 요청 설정</h3>

          <div className="input-group">
            <label>문제 선택 *</label>
            <select
              value={activeSession.problemId}
              onChange={handleProblemSelect}
              className="input-field"
              disabled={loadingProblems}
            >
              <option value="">문제를 선택하세요</option>
              {problems.map(problem => (
                <option key={problem.problem_id} value={problem.problem_id}>
                  {problem.problem_id}. {problem.title}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label>작성 코드 *</label>
            <textarea
              value={activeSession.code}
              onChange={(e) => updateSession({ code: e.target.value })}
              placeholder="Python 코드를 입력하세요..."
              className="code-input"
              rows={12}
            />
          </div>

          <div className="input-group">
            <label>힌트 목적 *</label>
            <select
              value={activeSession.hintPurpose}
              onChange={(e) => updateSession({ hintPurpose: e.target.value })}
              className="input-field"
            >
              <option value="completion">완료 (코드를 동작하게 만들기)</option>
              <option value="optimization">최적화 (코드를 효율적으로 만들기)</option>
            </select>
            <small style={{ color: '#666', fontSize: '12px', marginTop: '4px', display: 'block' }}>
              {activeSession.hintPurpose === 'completion'
                ? '💡 문법 오류 수정 또는 다음 단계 로직 힌트 제공'
                : '⚡ 약한 메트릭을 개선하는 최적화 힌트 제공'}
            </small>
          </div>

          <div className="preset-section">
            <label>힌트 프리셋 (💡 요약 설명 방식만 변경됩니다)</label>
            <div className="preset-buttons">
              {['초급', '중급', '고급'].map(preset => (
                <button
                  key={preset}
                  className={`preset-btn ${activeSession.preset === preset ? 'active' : ''}`}
                  onClick={() => handlePresetChange(preset)}
                >
                  {preset}
                </button>
              ))}
            </div>
          </div>

          <div className="custom-components-section">
            <label>힌트 구성 요소 (💡 요약은 항상 포함됩니다)</label>
            <div className="component-checkboxes">
              {Object.entries({
                libraries: '라이브러리',
                code_example: '코드 예시',
                step_by_step: '단계별 설명',
                complexity_hint: '복잡도',
                edge_cases: '엣지 케이스',
                improvements: '개선사항'
              }).map(([key, label]) => (
                <div key={key} className="component-checkbox">
                  <input
                    type="checkbox"
                    id={`${activeSessionId}-${key}`}
                    checked={activeSession.customComponents[key]}
                    onChange={() => handleComponentToggle(key)}
                  />
                  <label htmlFor={`${activeSessionId}-${key}`}>{label}</label>
                </div>
              ))}
            </div>
          </div>

          <div className="action-buttons">
            <button
              onClick={handleValidate}
              disabled={loading || !activeSession.code.trim() || !activeSession.problemId}
              className="btn-validate"
            >
              {loading ? '검증 중...' : '💡 힌트 생성'}
            </button>
            <button
              onClick={handleClearSession}
              disabled={loading}
              className="btn-clear"
            >
              🗑️ 초기화
            </button>
          </div>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}
        </div>

        {/* 우측: 결과 & 힌트 영역 */}
        <div className="results-wrapper">
          {/* 검증 결과 */}
          <div className="result-section">
            <h3>검증 결과</h3>

            {!latestResult ? (
              <div className="result-empty">
                <p>검증 결과가 없습니다.</p>
                <p>코드를 입력하고 검증을 시작하세요.</p>
              </div>
            ) : (
              <>
                {/* 종합 점수 */}
                <div className="total-score-card">
                  <h4>종합 점수</h4>
                  <div className="score-display" style={{ color: getScoreColor(latestResult.totalScore) }}>
                    {latestResult.totalScore.toFixed(1)}
                    <span className="score-suffix">/100</span>
                  </div>
                  <div className="score-bar">
                    <div
                      className="score-fill"
                      style={{
                        width: `${latestResult.totalScore}%`,
                        backgroundColor: getScoreColor(latestResult.totalScore)
                      }}
                    />
                  </div>
                </div>

                {/* 12개 지표 */}
                <div className="metrics-card">
                  <h4>📋 정적 지표 (6개)</h4>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <span className="metric-label">문법 오류</span>
                      <span
                        className="metric-value"
                        style={{ color: latestResult.static_metrics.syntax_errors === 0 ? '#4caf50' : '#f44336' }}
                      >
                        {latestResult.static_metrics.syntax_errors}개
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">테스트 통과율</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.static_metrics.test_pass_rate, 100) }}
                      >
                        {latestResult.static_metrics.test_pass_rate}%
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">실행 시간</span>
                      <span
                        className="metric-value"
                        style={{ color: (latestResult.static_metrics.execution_time || 0) <= 100 ? '#4caf50' : '#ff9800' }}
                      >
                        {(latestResult.static_metrics.execution_time || 0).toFixed(2)}ms
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">메모리 사용량</span>
                      <span
                        className="metric-value"
                        style={{ color: (latestResult.static_metrics.memory_usage || 0) <= 1000 ? '#4caf50' : '#ff9800' }}
                      >
                        {(latestResult.static_metrics.memory_usage || 0).toFixed(2)}KB
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">코드 품질</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.static_metrics.code_quality_score, 100) }}
                      >
                        {latestResult.static_metrics.code_quality_score}/100
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">PEP8 위반</span>
                      <span
                        className="metric-value"
                        style={{ color: latestResult.static_metrics.pep8_violations === 0 ? '#4caf50' : '#ff9800' }}
                      >
                        {latestResult.static_metrics.pep8_violations}개
                      </span>
                    </div>
                  </div>
                </div>

                <div className="metrics-card">
                  <h4>🤖 LLM 지표 (6개)</h4>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <span className="metric-label">알고리즘 효율성</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.algorithm_efficiency) }}
                      >
                        {latestResult.llm_metrics.algorithm_efficiency}/5
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">코드 가독성</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.code_readability) }}
                      >
                        {latestResult.llm_metrics.code_readability}/5
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">엣지 케이스</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.edge_case_handling) }}
                      >
                        {latestResult.llm_metrics.edge_case_handling}/5
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">코드 간결성</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.code_conciseness) }}
                      >
                        {latestResult.llm_metrics.code_conciseness}/5
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">테스트 커버리지</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.test_coverage_estimate || 3) }}
                      >
                        {latestResult.llm_metrics.test_coverage_estimate || 3}/5
                      </span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-label">보안 인식</span>
                      <span
                        className="metric-value"
                        style={{ color: getMetricColor(latestResult.llm_metrics.security_awareness || 3) }}
                      >
                        {latestResult.llm_metrics.security_awareness || 3}/5
                      </span>
                    </div>
                  </div>
                </div>

                {/* 힌트 목적 및 약한 메트릭 (optimization인 경우만) */}
                {latestResult.hint_purpose && (
                  <div className="hint-purpose-card">
                    <h4>
                      {latestResult.hint_purpose === 'completion' ? '💡 완료 목적' : '⚡ 최적화 목적'}
                    </h4>
                    <p style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>
                      {latestResult.hint_purpose === 'completion'
                        ? '코드를 동작하게 만들기 (문법 오류 수정 또는 다음 단계 로직)'
                        : '코드를 효율적으로 만들기 (약한 메트릭 개선)'}
                    </p>

                    {latestResult.hint_purpose === 'optimization' && latestResult.weak_metrics && latestResult.weak_metrics.length > 0 && (
                      <div style={{ marginTop: '12px' }}>
                        <strong style={{ fontSize: '13px' }}>약한 메트릭 (개선 필요):</strong>
                        <ul style={{ marginTop: '8px', paddingLeft: '20px', fontSize: '13px', color: '#f44336' }}>
                          {latestResult.weak_metrics.map((wm, idx) => (
                            <li key={idx}>
                              {wm.description} (점수: {wm.score.toFixed(2)})
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>

          {/* 힌트 영역 */}
          <div className="hint-section">
            <h3>생성된 힌트</h3>

            {!latestResult ? (
              <div className="hint-empty">
                <p>아직 생성된 힌트가 없습니다.</p>
                <p>문제와 코드를 입력하고 힌트를 생성하세요.</p>
              </div>
            ) : (
              <>
                {/* 최신 힌트 */}
                <div className="hint-card">
                  <div className="hint-header">
                    <h4>💡 최신 힌트</h4>
                    <span className="hint-preset-badge">{latestResult.preset}</span>
                  </div>
                  <div className="hint-content">
                    {latestResult.hint.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>

                {/* 힌트 히스토리 */}
                {activeSession.history.length > 1 && (
                  <div className="history-card">
                    <h4>📜 이전 힌트 ({activeSession.history.length - 1}개)</h4>
                    <div className="history-list-compact">
                      {activeSession.history.slice(0, -1).reverse().map((item, index) => (
                        <div key={index} className="history-item-compact">
                          <div className="history-item-compact-header">
                            <span className="history-number">#{activeSession.history.length - 1 - index}</span>
                            <span className="history-preset-tag">{item.preset}</span>
                            <span className="history-timestamp">{item.timestamp}</span>
                            <span
                              className="history-score-badge"
                              style={{ backgroundColor: getScoreColor(item.totalScore) }}
                            >
                              {item.totalScore.toFixed(0)}점
                            </span>
                          </div>
                          <div className="history-hint-preview">
                            {item.hint.split('\n')[0].substring(0, 60)}...
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
