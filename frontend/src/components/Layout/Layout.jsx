/**
 * 메인 레이아웃 컴포넌트
 */
import React from 'react'
import { Outlet, NavLink } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { logout } from '@store/authSlice'
import './Layout.css'

const Layout = () => {
  const { user } = useSelector((state) => state.auth)
  const dispatch = useDispatch()

  const handleLogout = () => {
    dispatch(logout())
  }

  return (
    <div className="layout">
      <nav className="sidebar">
        <div className="sidebar-header">
          <h2>Hint System</h2>
          <p className="user-info">{user?.username}</p>
        </div>

        <div className="nav-links">
          <NavLink to="/app/coding-test" className="nav-link">
            코딩 테스트
          </NavLink>
          <NavLink to="/app/chatbot" className="nav-link">
            문답 챗봇
          </NavLink>
          <NavLink to="/app/mypage" className="nav-link">
            마이페이지
          </NavLink>
          {user?.role === 'admin' && (
            <NavLink to="/app/admin" className="nav-link admin">
              관리자
            </NavLink>
          )}
        </div>

        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            로그아웃
          </button>
        </div>
      </nav>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
