import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Problems.css'

function Problems() {
  const navigate = useNavigate()
  const [problems, setProblems] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    level: 'all',
    tag: 'all',
    search: ''
  })

  useEffect(() => {
    // JSON 파일에서 문제 로드
    fetch('/problems.json')
      .then(response => response.json())
      .then(data => {
        setProblems(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Failed to load problems:', error)
        setLoading(false)
      })
  }, [])

  const handleProblemClick = (problemId) => {
    navigate(`/app/coding-test/${problemId}`)
  }

  const filteredProblems = problems.filter(problem => {
    const matchesLevel = filters.level === 'all' || problem.level === parseInt(filters.level)
    const matchesTag = filters.tag === 'all' || problem.tags?.includes(filters.tag)
    const matchesSearch = !filters.search ||
      problem.title?.toLowerCase().includes(filters.search.toLowerCase()) ||
      problem.step_title?.toLowerCase().includes(filters.search.toLowerCase())

    return matchesLevel && matchesTag && matchesSearch
  })

  const getLevelColor = (level) => {
    if (level <= 5) return '#4caf50'  // Easy (Green)
    if (level <= 10) return '#ff9800' // Medium (Orange)
    return '#f44336' // Hard (Red)
  }

  const getLevelLabel = (level) => {
    if (level <= 5) return 'Easy'
    if (level <= 10) return 'Medium'
    return 'Hard'
  }

  const allTags = [...new Set(problems.flatMap(p => p.tags || []))]
  const allLevels = [...new Set(problems.map(p => p.level))].sort((a, b) => a - b)

  const handleProposeTestCase = () => {
    navigate('/app/test-case-proposal')
  }

  const handleProposeSolution = () => {
    navigate('/app/solution-proposal')
  }

  const handleProposeProblem = () => {
    navigate('/app/problem-proposal')
  }

  return (
    <div className="problems-page">
      <div className="problems-header">
        <div className="header-content">
          <div className="header-text">
            <h1>코딩 테스트 문제 선택</h1>
            <p>난이도와 태그를 선택하여 원하는 문제를 찾아보세요</p>
          </div>
          <div className="header-buttons">
            <button
              className="propose-problem-btn"
              onClick={handleProposeProblem}
            >
              새로운 문제를 제안하고 싶으신가요?
            </button>
            <button
              className="propose-test-case-btn"
              onClick={handleProposeTestCase}
            >
              테스트 케이스가 이상한가요? 추가해보세요!
            </button>
            <button
              className="propose-solution-btn"
              onClick={handleProposeSolution}
            >
              참조 솔루션을 제안하고 싶으신가요?
            </button>
          </div>
        </div>
      </div>

      <div className="problems-filters">
        <div className="filter-group">
          <label>레벨</label>
          <select
            value={filters.level}
            onChange={(e) => setFilters({...filters, level: e.target.value})}
          >
            <option value="all">전체</option>
            {allLevels.map(level => (
              <option key={level} value={level}>Level {level}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>태그</label>
          <select
            value={filters.tag}
            onChange={(e) => setFilters({...filters, tag: e.target.value})}
          >
            <option value="all">전체</option>
            {allTags.map(tag => (
              <option key={tag} value={tag}>{tag}</option>
            ))}
          </select>
        </div>

        <div className="filter-group search-group">
          <label>검색</label>
          <input
            type="text"
            placeholder="문제 제목으로 검색..."
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
          />
        </div>
      </div>

      <div className="problems-stats">
        <span>총 {problems.length}개의 문제</span>
        <span>필터링된 결과: {filteredProblems.length}개</span>
      </div>

      <div className="problems-list">
        {filteredProblems.length === 0 ? (
          <div className="no-problems">
            <p>조건에 맞는 문제가 없습니다.</p>
          </div>
        ) : (
          filteredProblems.map((problem) => (
            <div
              key={problem.problem_id}
              className="problem-card"
              onClick={() => handleProblemClick(problem.problem_id)}
            >
              <div className="problem-header-row">
                <div className="problem-number">#{problem.problem_id}</div>
                <span
                  className="difficulty-badge"
                  style={{ backgroundColor: getLevelColor(problem.level) }}
                >
                  {getLevelLabel(problem.level)} (Lv.{problem.level})
                </span>
              </div>

              <h3 className="problem-title">{problem.title}</h3>
              {problem.step_title && (
                <div className="problem-category">{problem.step_title}</div>
              )}

              <p className="problem-description">
                {problem.description}
              </p>

              <div className="problem-tags">
                {(problem.tags || []).map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>

              <div className="problem-footer">
                <span>풀이 수: {problem.solutions?.length || 0}개</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Problems
