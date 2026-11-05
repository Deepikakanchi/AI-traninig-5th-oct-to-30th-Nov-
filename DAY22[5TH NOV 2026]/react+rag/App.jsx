import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function BookIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4.5 5.5c2.8-.9 5.3-.4 7.5 1.4v12c-2.2-1.8-4.7-2.3-7.5-1.4v-12Z" />
      <path d="M19.5 5.5c-2.8-.9-5.3-.4-7.5 1.4v12c2.2-1.8 4.7-2.3 7.5-1.4v-12Z" />
    </svg>
  )
}

function BotIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="4" y="7" width="16" height="12" rx="4" />
      <path d="M12 4v3M8.5 12h.01M15.5 12h.01M9 16h6" />
    </svg>
  )
}

function SendIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="m21 3-7.2 18-3.7-7.1L3 10.2 21 3Z" />
      <path d="M10.1 13.9 15 9" />
    </svg>
  )
}

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [activeReservation, setActiveReservation] = useState(null)
  const [reservationBusy, setReservationBusy] = useState(false)
  const messageListRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight
    }
  }, [messages, isSending, reservationBusy])

  async function sendMessage(event) {
    event.preventDefault()
    const text = input.trim()
    if (!text || isSending) return

    setInput('')
    setMessages((current) => [...current, { role: 'user', content: text }])

    if (activeReservation && /^(yes|yeah|yep|sure|confirm|confirmed|okay|ok|cancel|no)\b|reserve\s+(it|this|the book)\b/i.test(text)) {
      const declined = /^(cancel|no)\b/i.test(text)
      await respondToReservation(!declined)
      return
    }

    setIsSending(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          history: messages.map(({ role, content }) => ({ role, content })),
          pending_reservation: activeReservation,
        }),
      })

      if (!response.ok) {
        throw new Error(`The library service returned an error (${response.status}).`)
      }

      const data = await response.json()
      if (data.status === 'error') {
        throw new Error(data.response || 'The assistant could not complete that request.')
      }

      const pending = data.pending_reservation || null
      setActiveReservation(pending)
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: data.response || 'I could not find a response for that request.',
          toolUsed: data.tool_used,
          pendingReservation: pending,
        },
      ])
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: error instanceof Error ? error.message : 'Something went wrong while contacting the library service.',
          isError: true,
        },
      ])
    } finally {
      setIsSending(false)
      inputRef.current?.focus()
    }
  }

  async function respondToReservation(confirmed) {
    if (!activeReservation || reservationBusy) return
    setReservationBusy(true)

    try {
      const response = await fetch(`${API_URL}/confirm-reservation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...activeReservation,
          confirmed,
        }),
      })

      if (!response.ok) {
        throw new Error(`The reservation service returned an error (${response.status}).`)
      }

      const data = await response.json()
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: data.response || 'The reservation request has been processed.',
          isError: data.status === 'error',
        },
      ])
      setActiveReservation(null)
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: error instanceof Error ? error.message : 'Something went wrong while processing the reservation.',
          isError: true,
        },
      ])
    } finally {
      setReservationBusy(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <div className="brand-icon"><BookIcon /></div>
        <div>
          <h1>AI Library Assistant</h1>
          <p>Book Search &amp; Reservations</p>
        </div>
      </header>

      <section
        className="conversation"
        ref={messageListRef}
        aria-label="Chat conversation"
        aria-live="polite"
      >
        {messages.length === 0 && (
          <div className="empty-state">
            <BotIcon />
            <p>Ask me to find a book or make a reservation.</p>
          </div>
        )}

        {messages.map((message, index) => (
          <article className={`message-row ${message.role}`} key={`${message.role}-${index}`}>
            {message.role === 'assistant' && (
              <div className="assistant-icon"><BotIcon /></div>
            )}
            <div className={`message-content${message.isError ? ' error' : ''}`}>
              <div className="message-bubble">{message.content}</div>
              {message.toolUsed && (
                <p className="tool-label">Tool used: {message.toolUsed}</p>
              )}
              {message.pendingReservation && activeReservation?.customer_name && (
                <div className="reservation-actions" aria-label="Reservation confirmation">
                  <button
                    type="button"
                    className="confirm-button"
                    onClick={() => respondToReservation(true)}
                    disabled={reservationBusy}
                  >
                    {reservationBusy ? 'Processing…' : 'Confirm'}
                  </button>
                  <button
                    type="button"
                    className="cancel-button"
                    onClick={() => respondToReservation(false)}
                    disabled={reservationBusy}
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>
          </article>
        ))}

        {isSending && (
          <div className="message-row assistant">
            <div className="assistant-icon"><BotIcon /></div>
            <div className="message-bubble typing-indicator" aria-label="Assistant is typing">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}
      </section>

      <form className="composer" onSubmit={sendMessage}>
        <label className="visually-hidden" htmlFor="chat-input">Type your message</label>
        <textarea
          id="chat-input"
          ref={inputRef}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              event.currentTarget.form?.requestSubmit()
            }
          }}
          placeholder="Type your message..."
          rows="1"
          disabled={isSending}
        />
        <button
          className="send-button"
          type="submit"
          aria-label="Send message"
          disabled={!input.trim() || isSending}
        >
          <SendIcon />
        </button>
      </form>
    </main>
  )
}

export default App
