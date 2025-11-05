import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import './Dashboard.css'

function Dashboard() {
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)

  const navigationCards = [
    {
      id: 'problems',
      title: '코딩 테스트 문제 선택',
      icon: '📝',
      description: '난이도별, 태그별 문제를 선택하여 풀어보세요',
      path: '/app/problems',
      color: '#667eea'
    },
    {
      id: 'chatbot',
      title: '문답 챗봇',
      icon: '🤖',
      description: 'Python, Git 문서 기반 질의응답',
      path: '/app/chatbot',
      color: '#f093fb'
    },
    {
      id: 'mypage',
      title: '마이페이지',
      icon: '👤',
      description: '내 정보 및 학습 기록 확인',
      path: '/app/mypage',
      color: '#4facfe'
    }
  ]

  // 관리자 권한이 있는 경우 관리자 탭 추가
  if (user?.is_staff || user?.is_superuser) {
    navigationCards.push({
      id: 'admin',
      title: '관리자',
      icon: '⚙️',
      description: '시스템 관리 및 설정',
      path: '/app/admin',
      color: '#fa709a'
    })
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>대시보드</h1>
        <p className="welcome-message">환영합니다, {user?.username}님!</p>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">{user?.rating || 0}</div>
            <div className="stat-label">레이팅 점수</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{user?.solved_count || 0}</div>
            <div className="stat-label">해결한 문제</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <div className="stat-value">{user?.attempted_count || 0}</div>
            <div className="stat-label">시도한 문제</div>
          </div>
        </div>
      </div>

      <div className="navigation-grid">
        {navigationCards.map((card) => (
          <div
            key={card.id}
            className="nav-card"
            onClick={() => navigate(card.path)}
            style={{ borderTopColor: card.color }}
          >
            <div className="nav-card-icon">{card.icon}</div>
            <h3 className="nav-card-title">{card.title}</h3>
            <p className="nav-card-description">{card.description}</p>
            <button
              className="nav-card-button"
              style={{ background: card.color }}
            >
              시작하기 →
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard
