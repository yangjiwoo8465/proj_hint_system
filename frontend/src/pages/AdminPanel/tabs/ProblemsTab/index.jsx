import React from 'react'
import './ProblemsTab.css'

function ProblemsTab({ problems }) {
  return (
    <div className="problems-section">
      <div className="section-header">
        <h3>문제 목록 ({problems.length}개)</h3>
      </div>

      <div className="problems-grid">
        {problems.length === 0 ? (
          <div className="empty-state">
            <p>등록된 문제가 없습니다.</p>
          </div>
        ) : (
          problems.map((problem) => (
            <div key={problem.id} className="problem-card">
              <div className="problem-header">
                <h4>{problem.title}</h4>
                <span className={`difficulty-badge ${problem.difficulty?.toLowerCase()}`}>
                  {problem.difficulty}
                </span>
              </div>
              <p className="problem-description">{problem.description}</p>
              <div className="problem-stats">
                <span>제출: {problem.submissions || 0}</span>
                <span>정답률: {problem.acceptance_rate || 0}%</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default ProblemsTab
