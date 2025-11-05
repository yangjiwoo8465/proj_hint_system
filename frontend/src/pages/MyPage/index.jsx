import React, { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { updateUser, logout } from '../../store/authSlice'
import api from '../../services/api'
import './MyPage.css'

function MyPage() {
  const dispatch = useDispatch()
  const user = useSelector((state) => state.auth.user)
  const [activeTab, setActiveTab] = useState('profile')
  const [stats, setStats] = useState(null)
  const [solvedProblems, setSolvedProblems] = useState([])
  const [bookmarks, setBookmarks] = useState([])
  const [editMode, setEditMode] = useState(false)
  const [formData, setFormData] = useState({
    email: user?.email || '',
    bio: user?.bio || ''
  })
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  const [allUsers, setAllUsers] = useState([])
  const [loadingUsers, setLoadingUsers] = useState(false)

  useEffect(() => {
    fetchUserStats()
    fetchSolvedProblems()
    fetchBookmarks()
    if (user?.is_staff || user?.is_superuser) {
      fetchAllUsers()
    }
  }, [])

  const fetchUserStats = async () => {
    try {
      const response = await api.get('/auth/user/')
      setStats(response.data.data)
    } catch (error) {
      console.error('Failed to fetch user stats:', error)
    }
  }

  const fetchSolvedProblems = async () => {
    try {
      const response = await api.get('/coding-test/solved/')
      setSolvedProblems(response.data.data || [])
    } catch (error) {
      console.error('Failed to fetch solved problems:', error)
    }
  }

  const fetchBookmarks = async () => {
    try {
      const response = await api.get('/chatbot/bookmarks/')
      setBookmarks(response.data.data || [])
    } catch (error) {
      console.error('Failed to fetch bookmarks:', error)
    }
  }

  const handleUpdateProfile = async (e) => {
    e.preventDefault()

    try {
      const response = await api.put('/auth/user/update/', formData)
      dispatch(updateUser(response.data.data))
      setEditMode(false)
      alert('프로필이 업데이트되었습니다.')
    } catch (error) {
      console.error('Failed to update profile:', error)
      alert('프로필 업데이트에 실패했습니다.')
    }
  }

  const handleChangePassword = async (e) => {
    e.preventDefault()

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert('새 비밀번호가 일치하지 않습니다.')
      return
    }

    try {
      await api.post('/auth/user/password/', {
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      })

      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })

      alert('비밀번호가 변경되었습니다.')
    } catch (error) {
      console.error('Failed to change password:', error)
      alert('비밀번호 변경에 실패했습니다.')
    }
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
      return
    }

    try {
      await api.delete('/auth/user/delete/')
      dispatch(logout())
      alert('계정이 삭제되었습니다.')
    } catch (error) {
      console.error('Failed to delete account:', error)
      alert('계정 삭제에 실패했습니다.')
    }
  }

  const fetchAllUsers = async () => {
    setLoadingUsers(true)
    try {
      const response = await api.get('/auth/users/')
      setAllUsers(response.data.data || [])
    } catch (error) {
      console.error('Failed to fetch users:', error)
    } finally {
      setLoadingUsers(false)
    }
  }

  const handleToggleUserPermission = async (userId, field, currentValue) => {
    if (!window.confirm(`정말로 이 사용자의 ${field === 'is_staff' ? '관리자' : '슈퍼유저'} 권한을 ${currentValue ? '제거' : '부여'}하시겠습니까?`)) {
      return
    }

    try {
      await api.patch(`/auth/users/${userId}/permissions/`, {
        [field]: !currentValue
      })
      await fetchAllUsers()
      alert('권한이 변경되었습니다.')
    } catch (error) {
      console.error('Failed to update permissions:', error)
      alert('권한 변경에 실패했습니다.')
    }
  }

  return (
    <div className="mypage">
      <div className="mypage-header">
        <h1>마이페이지</h1>
        <p>{user?.username}님의 프로필 및 학습 기록</p>
      </div>

      <div className="mypage-tabs">
        <button
          className={activeTab === 'profile' ? 'active' : ''}
          onClick={() => setActiveTab('profile')}
        >
          프로필
        </button>
        <button
          className={activeTab === 'stats' ? 'active' : ''}
          onClick={() => setActiveTab('stats')}
        >
          통계
        </button>
        <button
          className={activeTab === 'solved' ? 'active' : ''}
          onClick={() => setActiveTab('solved')}
        >
          해결한 문제
        </button>
        <button
          className={activeTab === 'bookmarks' ? 'active' : ''}
          onClick={() => setActiveTab('bookmarks')}
        >
          북마크
        </button>
        {(user?.is_staff || user?.is_superuser) && (
          <button
            className={activeTab === 'users' ? 'active' : ''}
            onClick={() => setActiveTab('users')}
          >
            사용자 관리
          </button>
        )}
      </div>

      <div className="mypage-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <div className="profile-card">
              <div className="profile-header">
                <div className="profile-avatar">
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <div className="profile-info">
                  <h2>{user?.username}</h2>
                  <p className="rating">레이팅: {user?.rating || 0}점</p>
                </div>
              </div>

              {!editMode ? (
                <div className="profile-details">
                  <div className="detail-item">
                    <strong>이메일:</strong>
                    <span>{user?.email || '등록되지 않음'}</span>
                  </div>
                  <div className="detail-item">
                    <strong>가입일:</strong>
                    <span>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}</span>
                  </div>
                  <div className="detail-item">
                    <strong>소개:</strong>
                    <span>{user?.bio || '소개글이 없습니다.'}</span>
                  </div>

                  <button
                    className="edit-btn"
                    onClick={() => setEditMode(true)}
                  >
                    프로필 수정
                  </button>
                </div>
              ) : (
                <form onSubmit={handleUpdateProfile} className="edit-form">
                  <div className="form-group">
                    <label>이메일</label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      placeholder="이메일을 입력하세요"
                    />
                  </div>

                  <div className="form-group">
                    <label>소개</label>
                    <textarea
                      value={formData.bio}
                      onChange={(e) => setFormData({...formData, bio: e.target.value})}
                      placeholder="자기소개를 입력하세요"
                      rows="4"
                    />
                  </div>

                  <div className="form-actions">
                    <button type="submit" className="save-btn">저장</button>
                    <button
                      type="button"
                      className="cancel-btn"
                      onClick={() => setEditMode(false)}
                    >
                      취소
                    </button>
                  </div>
                </form>
              )}
            </div>

            <div className="password-section">
              <h3>비밀번호 변경</h3>
              <form onSubmit={handleChangePassword} className="password-form">
                <div className="form-group">
                  <label>현재 비밀번호</label>
                  <input
                    type="password"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>새 비밀번호</label>
                  <input
                    type="password"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>새 비밀번호 확인</label>
                  <input
                    type="password"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                    required
                  />
                </div>

                <button type="submit" className="save-btn">비밀번호 변경</button>
              </form>
            </div>

            <div className="danger-zone">
              <h3>위험 구역</h3>
              <p>계정을 삭제하면 모든 데이터가 영구적으로 삭제됩니다.</p>
              <button className="delete-btn" onClick={handleDeleteAccount}>
                계정 삭제
              </button>
            </div>
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="stats-section">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">⭐</div>
                <div className="stat-value">{stats?.rating || user?.rating || 0}</div>
                <div className="stat-label">레이팅</div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">✅</div>
                <div className="stat-value">{stats?.solved_count || user?.solved_count || 0}</div>
                <div className="stat-label">해결한 문제</div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">📝</div>
                <div className="stat-value">{stats?.attempted_count || user?.attempted_count || 0}</div>
                <div className="stat-label">시도한 문제</div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-value">
                  {stats?.solved_count && stats?.attempted_count
                    ? Math.round((stats.solved_count / stats.attempted_count) * 100)
                    : 0}%
                </div>
                <div className="stat-label">정답률</div>
              </div>
            </div>

            <div className="activity-chart">
              <h3>최근 활동</h3>
              <p className="coming-soon">활동 차트는 곧 제공됩니다.</p>
            </div>
          </div>
        )}

        {activeTab === 'solved' && (
          <div className="solved-section">
            <h3>해결한 문제 ({solvedProblems.length}개)</h3>
            {solvedProblems.length === 0 ? (
              <div className="empty-state">
                <p>아직 해결한 문제가 없습니다.</p>
                <p className="hint">문제를 풀어보세요!</p>
              </div>
            ) : (
              <div className="problems-grid">
                {solvedProblems.map((problem) => (
                  <div key={problem.id} className="problem-item">
                    <h4>{problem.title}</h4>
                    <div className="problem-meta">
                      <span className={`difficulty ${problem.difficulty?.toLowerCase()}`}>
                        {problem.difficulty}
                      </span>
                      <span className="solved-date">
                        {problem.solved_at ? new Date(problem.solved_at).toLocaleDateString() : ''}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'bookmarks' && (
          <div className="bookmarks-section">
            <h3>북마크 ({bookmarks.length}개)</h3>
            {bookmarks.length === 0 ? (
              <div className="empty-state">
                <p>저장된 북마크가 없습니다.</p>
                <p className="hint">챗봇 응답을 북마크해보세요!</p>
              </div>
            ) : (
              <div className="bookmarks-grid">
                {bookmarks.map((bookmark) => (
                  <div key={bookmark.id} className="bookmark-item">
                    <p>{bookmark.content}</p>
                    <div className="bookmark-date">
                      {bookmark.created_at ? new Date(bookmark.created_at).toLocaleDateString() : ''}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'users' && (user?.is_staff || user?.is_superuser) && (
          <div className="users-management-section">
            <h3>사용자 관리 ({allUsers.length}명)</h3>

            {loadingUsers ? (
              <div className="loading-state">
                <p>사용자 목록을 불러오는 중...</p>
              </div>
            ) : allUsers.length === 0 ? (
              <div className="empty-state">
                <p>사용자가 없습니다.</p>
              </div>
            ) : (
              <div className="users-table-container">
                <table className="users-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>사용자명</th>
                      <th>이메일</th>
                      <th>가입일</th>
                      <th>관리자</th>
                      <th>슈퍼유저</th>
                      <th>활성</th>
                    </tr>
                  </thead>
                  <tbody>
                    {allUsers.map((u) => (
                      <tr key={u.id} className={u.id === user?.id ? 'current-user' : ''}>
                        <td>{u.id}</td>
                        <td>
                          {u.username}
                          {u.id === user?.id && <span className="badge-me">본인</span>}
                        </td>
                        <td>{u.email || '-'}</td>
                        <td>{u.created_at ? new Date(u.created_at).toLocaleDateString() : '-'}</td>
                        <td>
                          <button
                            className={`permission-toggle ${u.is_staff ? 'active' : ''}`}
                            onClick={() => handleToggleUserPermission(u.id, 'is_staff', u.is_staff)}
                            disabled={u.id === user?.id}
                          >
                            {u.is_staff ? '✓' : '✗'}
                          </button>
                        </td>
                        <td>
                          <button
                            className={`permission-toggle ${u.is_superuser ? 'active' : ''}`}
                            onClick={() => handleToggleUserPermission(u.id, 'is_superuser', u.is_superuser)}
                            disabled={u.id === user?.id}
                          >
                            {u.is_superuser ? '✓' : '✗'}
                          </button>
                        </td>
                        <td>
                          <span className={`status-badge ${u.is_active ? 'active' : 'inactive'}`}>
                            {u.is_active ? '활성' : '비활성'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default MyPage
