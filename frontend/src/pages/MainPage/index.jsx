import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import api from '../../services/api'
import { loginSuccess } from '../../store/authSlice'
import './MainPage.css'

function MainPage() {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isLogin) {
        // 로그인
        const response = await api.post('/auth/login/', {
          username: formData.username,
          password: formData.password,
        })

        const { user, tokens } = response.data.data

        // 토큰 저장
        localStorage.setItem('accessToken', tokens.access)
        localStorage.setItem('refreshToken', tokens.refresh)

        // Redux에 사용자 정보 저장
        dispatch(loginSuccess(user))

        // 대시보드로 이동
        navigate('/app/dashboard')
      } else {
        // 회원가입
        const response = await api.post('/auth/signup/', {
          username: formData.username,
          email: formData.email,
          password: formData.password,
        })

        alert('회원가입이 완료되었습니다. 로그인해주세요.')
        setIsLogin(true)
        setFormData({ username: formData.username, email: '', password: '' })
      }
    } catch (err) {
      console.error('Auth error:', err)
      setError(
        err.response?.data?.message ||
        (isLogin ? '로그인에 실패했습니다.' : '회원가입에 실패했습니다.')
      )
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="main-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Hint System</h1>
          <p className="hero-subtitle">AI 기반 코딩 테스트 학습 플랫폼</p>

          <div className="features">
            <div className="feature-item">
              <h3>🎯 맞춤형 힌트</h3>
              <p>AI가 당신의 학습 성향을 분석하여 최적의 힌트를 제공합니다</p>
            </div>
            <div className="feature-item">
              <h3>💡 단계별 학습</h3>
              <p>대/중/소 3단계 힌트로 스스로 문제를 해결하는 능력을 키웁니다</p>
            </div>
            <div className="feature-item">
              <h3>🤖 RAG 챗봇</h3>
              <p>Python, Git 공식 문서 기반 질의응답으로 학습을 돕습니다</p>
            </div>
            <div className="feature-item">
              <h3>📊 성과 추적</h3>
              <p>문제 풀이 기록과 레이팅으로 성장을 확인하세요</p>
            </div>
          </div>
        </div>

        <div className="auth-section">
          <div className="auth-card">
            <div className="auth-tabs">
              <button
                className={isLogin ? 'active' : ''}
                onClick={() => setIsLogin(true)}
              >
                로그인
              </button>
              <button
                className={!isLogin ? 'active' : ''}
                onClick={() => setIsLogin(false)}
              >
                회원가입
              </button>
            </div>

            <form onSubmit={handleSubmit} className="auth-form">
              {error && <div className="error-message">{error}</div>}

              <div className="form-group">
                <label>아이디</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="아이디를 입력하세요"
                  required
                />
              </div>

              {!isLogin && (
                <div className="form-group">
                  <label>이메일</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="이메일을 입력하세요"
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label>비밀번호</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="비밀번호를 입력하세요"
                  required
                />
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? '처리중...' : (isLogin ? '로그인' : '회원가입')}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MainPage
