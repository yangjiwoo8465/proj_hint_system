import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Layout from './components/Layout/Layout'

// Pages (탭별 모듈)
import MainPage from './pages/MainPage'
import Dashboard from './pages/Dashboard'
import Problems from './pages/Problems'
import CodingTest from './pages/CodingTest'
import Chatbot from './pages/Chatbot'
import MyPage from './pages/MyPage'
import AdminPanel from './pages/AdminPanel'
import TestCaseProposal from './pages/TestCaseProposal'
import SolutionProposal from './pages/SolutionProposal'
import ProblemProposal from './pages/ProblemProposal'

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
        {/* 대시보드 */}
        <Route index element={<Dashboard />} />
        <Route path="dashboard" element={<Dashboard />} />

        {/* 코딩 테스트 문제 선택 */}
        <Route path="problems" element={<Problems />} />

        {/* 테스트 케이스 제안 */}
        <Route path="test-case-proposal" element={<TestCaseProposal />} />

        {/* 솔루션 제안 */}
        <Route path="solution-proposal" element={<SolutionProposal />} />

        {/* 문제 제안 */}
        <Route path="problem-proposal" element={<ProblemProposal />} />

        {/* 문답 챗봇 */}
        <Route path="chatbot" element={<Chatbot />} />

        {/* 마이페이지 */}
        <Route path="mypage" element={<MyPage />} />

        {/* 관리자 페이지 (관리자만) */}
        <Route
          path="admin"
          element={
            user?.is_staff || user?.is_superuser ? (
              <AdminPanel />
            ) : (
              <Navigate to="/app/dashboard" replace />
            )
          }
        />
      </Route>

      {/* 코딩 테스트 - 사이드바 없이 독립 실행 */}
      <Route
        path="/app/coding-test/:problemId"
        element={
          isAuthenticated ? (
            <CodingTest />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
