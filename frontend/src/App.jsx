import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Layout from './components/Layout/Layout'

// Pages (탭별 모듈)
import MainPage from './pages/MainPage'
import CodingTest from './pages/CodingTest'
import Chatbot from './pages/Chatbot'
import MyPage from './pages/MyPage'
import AdminPanel from './pages/AdminPanel'

import './App.css'

function App() {
  const { isAuthenticated, user } = useSelector((state) => state.auth)

  return (
    <Routes>
      {/* 메인 화면 (로그인/회원가입) */}
      <Route path="/" element={<MainPage />} />
      <Route path="/login" element={<MainPage />} />
      <Route path="/signup" element={<MainPage />} />

      {/* 인증된 사용자만 접근 가능한 페이지 */}
      <Route
        path="/app"
        element={
          isAuthenticated ? (
            <Layout />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      >
        {/* 코딩 테스트 */}
        <Route path="coding-test" element={<CodingTest />} />
        <Route path="coding-test/:problemId" element={<CodingTest />} />

        {/* 문답 챗봇 */}
        <Route path="chatbot" element={<Chatbot />} />

        {/* 마이페이지 */}
        <Route path="mypage" element={<MyPage />} />

        {/* 관리자 페이지 (관리자만) */}
        <Route
          path="admin"
          element={
            user?.role === 'admin' ? (
              <AdminPanel />
            ) : (
              <Navigate to="/app/coding-test" replace />
            )
          }
        />

        {/* 기본 리다이렉트 */}
        <Route index element={<Navigate to="coding-test" replace />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
