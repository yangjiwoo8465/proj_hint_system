import React, { useState, useRef, useEffect } from 'react'
import api from '../../services/api'
import './Chatbot.css'

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요! Python과 Git 관련 질문에 답변해드립니다. 무엇을 도와드릴까요?'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [bookmarks, setBookmarks] = useState([])
  const messagesEndRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    fetchBookmarks()
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchBookmarks = async () => {
    try {
      const response = await api.get('/chatbot/bookmarks/')
      setBookmarks(response.data.data || [])
    } catch (error) {
      console.error('Failed to fetch bookmarks:', error)
    }
  }

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/chatbot/chat/', {
        message: input,
        history: messages
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.data.response,
        sources: response.data.data.sources
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage = {
        role: 'assistant',
        content: '죄송합니다. 응답을 생성하는 중 오류가 발생했습니다.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleBookmark = async (messageIndex) => {
    const message = messages[messageIndex]
    if (message.role !== 'assistant') return

    try {
      await api.post('/chatbot/bookmark/', {
        content: message.content,
        sources: message.sources
      })

      alert('북마크에 추가되었습니다.')
      fetchBookmarks()
    } catch (error) {
      console.error('Failed to bookmark:', error)
      alert('북마크 추가에 실패했습니다.')
    }
  }

  const handleCopy = (content) => {
    navigator.clipboard.writeText(content)
    alert('클립보드에 복사되었습니다.')
  }

  const handleDeleteBookmark = async (bookmarkId) => {
    try {
      await api.delete(`/chatbot/bookmark/${bookmarkId}/`)
      fetchBookmarks()
    } catch (error) {
      console.error('Failed to delete bookmark:', error)
      alert('북마크 삭제에 실패했습니다.')
    }
  }

  return (
    <div className="chatbot-page">
      <div className="chat-section">
        <div className="chat-header">
          <h2>RAG 챗봇</h2>
          <p>Python 및 Git 공식 문서 기반 질의응답</p>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-avatar">
                {message.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <strong>참고 문서:</strong>
                    <ul>
                      {message.sources.map((source, idx) => (
                        <li key={idx}>{source}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {message.role === 'assistant' && (
                  <div className="message-actions">
                    <button
                      className="action-btn"
                      onClick={() => handleBookmark(index)}
                      title="북마크"
                    >
                      ⭐ 북마크
                    </button>
                    <button
                      className="action-btn"
                      onClick={() => handleCopy(message.content)}
                      title="복사"
                    >
                      📋 복사
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Python이나 Git에 대해 질문하세요... (Shift+Enter: 줄바꿈, Enter: 전송)"
            rows="3"
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            {loading ? '전송 중...' : '전송'}
          </button>
        </div>
      </div>

      <div className="bookmarks-section">
        <div className="bookmarks-header">
          <h3>북마크</h3>
          <span className="bookmark-count">{bookmarks.length}개</span>
        </div>

        <div className="bookmarks-list">
          {bookmarks.length === 0 ? (
            <div className="no-bookmarks">
              <p>저장된 북마크가 없습니다.</p>
              <p className="hint">챗봇 응답에서 ⭐ 버튼을 눌러 북마크를 추가하세요.</p>
            </div>
          ) : (
            bookmarks.map((bookmark) => (
              <div key={bookmark.id} className="bookmark-item">
                <div className="bookmark-content">{bookmark.content}</div>
                <div className="bookmark-actions">
                  <button
                    className="action-btn small"
                    onClick={() => handleCopy(bookmark.content)}
                  >
                    📋
                  </button>
                  <button
                    className="action-btn small delete"
                    onClick={() => handleDeleteBookmark(bookmark.id)}
                  >
                    🗑️
                  </button>
                </div>
                {bookmark.created_at && (
                  <div className="bookmark-date">
                    {new Date(bookmark.created_at).toLocaleDateString()}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default Chatbot
