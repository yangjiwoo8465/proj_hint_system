import React from 'react'
import './UsersTab.css'

function UsersTab({ users, handleToggleUserStatus, handleDeleteUser }) {
  return (
    <div className="users-section">
      <div className="section-header">
        <h3>사용자 목록 ({users.length}명)</h3>
      </div>

      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>사용자명</th>
              <th>이메일</th>
              <th>레이팅</th>
              <th>가입일</th>
              <th>상태</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td colSpan="6" className="empty-cell">
                  등록된 사용자가 없습니다.
                </td>
              </tr>
            ) : (
              users.map((user) => (
                <tr key={user.id}>
                  <td>{user.username}</td>
                  <td>{user.email || '-'}</td>
                  <td>{user.rating || 0}</td>
                  <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}</td>
                  <td>
                    <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                      {user.is_active ? '활성' : '비활성'}
                    </span>
                  </td>
                  <td>
                    <div className="table-actions">
                      <button
                        className="action-btn toggle"
                        onClick={() => handleToggleUserStatus(user.id, user.is_active)}
                      >
                        {user.is_active ? '비활성화' : '활성화'}
                      </button>
                      <button
                        className="action-btn delete"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        삭제
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default UsersTab
