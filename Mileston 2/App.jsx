import { useState } from 'react'
import { BrowserRouter, Link, NavLink, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import EVENTS from './events.json'
import {
  cancelRegistration,
  createRegistration,
  filterEvents,
  getAvailableSeats,
  loadRegistrations,
  saveRegistrations,
  validateAttendee,
} from './registrationStore'
import './App.css'

const CATEGORIES = ['All', ...new Set(EVENTS.map((event) => event.category))]

function formatDate(date) {
  return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(`${date}T00:00:00`))
}

function formatTime(time) {
  return new Intl.DateTimeFormat('en', { hour: 'numeric', minute: '2-digit' }).format(new Date(`2026-01-01T${time}:00`))
}

function AppLayout({ registrations, onRegister, onCancel, storageError, onClearStorageError }) {
  const location = useLocation()
  const registrationCount = registrations.length

  return (
    <div className="app-shell">
      <header className="site-header">
        <Link className="brand" to="/" aria-label="Gather home">
          Gather
        </Link>
        <nav className="main-nav" aria-label="Main navigation">
          <NavLink to="/" end>Events</NavLink>
          <NavLink to="/registrations">
            Registrations <span className="nav-count">{registrationCount}</span>
          </NavLink>
        </nav>
      </header>

      <main>
        {storageError && (
          <div className="storage-alert" role="alert">
            {storageError}
            <button type="button" onClick={onClearStorageError} aria-label="Dismiss message">×</button>
          </div>
        )}
        <Routes>
          <Route
            path="/"
            element={<EventsPage registrations={registrations} onRegister={onRegister} />}
          />
          <Route
            path="/registrations"
            element={<RegistrationsPage registrations={registrations} onCancel={onCancel} />}
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      <footer className="site-footer">
        <span>© 2026 Gather Community Centre</span>
      </footer>
      {location.pathname !== '/registrations' && <span className="sr-only" aria-live="polite">{registrationCount} active registrations</span>}
    </div>
  )
}

function EventsPage({ registrations, onRegister }) {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('All')
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [notice, setNotice] = useState('')

  const filteredEvents = filterEvents(EVENTS, query, category)

  const availableSeats = (event) => getAvailableSeats(event, registrations)

  function submitRegistration(attendee) {
    const result = onRegister(selectedEvent, attendee)
    if (result.error) {
      return result
    }
    setSelectedEvent(null)
    setNotice(`You're registered for ${selectedEvent.title}. See you there!`)
    return result
  }

  return (
    <>
      <section className="events-section" id="events">
        <div className="section-heading">
          <h1>Upcoming events</h1>
        </div>

        <div className="event-tools">
          <label className="search-field">
            <span className="sr-only">Search events by title</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search events..." />
            {query && <button type="button" onClick={() => setQuery('')} aria-label="Clear search">×</button>}
          </label>
          <div className="category-filters" aria-label="Filter by category">
            {CATEGORIES.map((item) => (
              <button
                className={category === item ? 'filter-chip active' : 'filter-chip'}
                key={item}
                onClick={() => setCategory(item)}
                type="button"
                aria-pressed={category === item}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {notice && <div className="success-alert" role="status">{notice}<button type="button" onClick={() => setNotice('')} aria-label="Dismiss confirmation">×</button></div>}

        <div className="event-grid">
          {filteredEvents.map((event) => (
            <EventCard
              event={event}
              available={availableSeats(event)}
              key={event.id}
              onRegister={() => { setNotice(''); setSelectedEvent(event) }}
            />
          ))}
        </div>
        {filteredEvents.length === 0 && (
          <div className="empty-state">
            <p>No events found. Try another search.</p>
            <button type="button" className="button button-outline" onClick={() => { setQuery(''); setCategory('All') }}>Clear filters</button>
          </div>
        )}
      </section>
      {selectedEvent && (
        <RegistrationModal
          event={selectedEvent}
          available={availableSeats(selectedEvent)}
          onClose={() => setSelectedEvent(null)}
          onSubmit={submitRegistration}
        />
      )}
    </>
  )
}

function EventCard({ event, available, onRegister }) {
  const full = available === 0
  return (
    <article className="event-card">
      <div className="event-meta">
        <span className="category-label">{event.category}</span>
        <span className={full ? 'seats-label full' : 'seats-label'}>{available} of {event.seats} seats available</span>
      </div>
      <h3>{event.title}</h3>
      <div className="event-details">
        <span>{formatDate(event.date)}</span>
        <span>{formatTime(event.time)}</span>
      </div>
      <button className={full ? 'button button-disabled' : 'button button-dark'} type="button" disabled={full} onClick={onRegister}>
        {full ? 'Fully booked' : 'Register'}
      </button>
    </article>
  )
}

function RegistrationModal({ event, available, onClose, onSubmit }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')

  function submit(eventObject) {
    eventObject.preventDefault()
    const nextErrors = validateAttendee({ name, email })
    setErrors(nextErrors)
    setFormError('')
    if (Object.keys(nextErrors).length > 0) return
    const result = onSubmit({ name: name.trim(), email: email.trim() })
    if (result?.error) setFormError(result.error)
  }

  return (
    <div className="modal-backdrop" onMouseDown={(eventObject) => { if (eventObject.target === eventObject.currentTarget) onClose() }}>
      <section className="registration-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <button className="modal-close" type="button" onClick={onClose} aria-label="Close registration form">×</button>
        <h2 id="modal-title">{event.title}</h2>
        <p className="modal-date">{formatDate(event.date)} <span>·</span> {formatTime(event.time)} <span>·</span> {available} {available === 1 ? 'seat' : 'seats'} remaining</p>
        {formError && <p className="form-error form-error-summary" role="alert">{formError}</p>}
        {available === 0 ? (
          <div className="empty-state compact"><p>This event is fully booked.</p></div>
        ) : (
          <form onSubmit={submit} noValidate>
            <label className="form-field">
              <span>Full name</span>
              <input autoFocus value={name} onChange={(eventObject) => setName(eventObject.target.value)} aria-invalid={Boolean(errors.name)} aria-describedby={errors.name ? 'name-error' : undefined} placeholder="e.g. Alex Morgan" />
              {errors.name && <span className="form-error" id="name-error">{errors.name}</span>}
            </label>
            <label className="form-field">
              <span>Email address</span>
              <input type="email" value={email} onChange={(eventObject) => setEmail(eventObject.target.value)} aria-invalid={Boolean(errors.email)} aria-describedby={errors.email ? 'email-error' : undefined} placeholder="you@example.com" />
              {errors.email && <span className="form-error" id="email-error">{errors.email}</span>}
            </label>
            <button className="button button-dark submit-button" type="submit">Confirm registration <span aria-hidden="true">↗</span></button>
          </form>
        )}
      </section>
    </div>
  )
}

function RegistrationsPage({ registrations, onCancel }) {
  const navigate = useNavigate()
  return (
    <section className="registrations-section">
      <div className="registrations-heading">
        <h1>My registrations</h1>
        <Link className="button button-outline" to="/">Events</Link>
      </div>
      {registrations.length > 0 ? (
        <div className="registration-list">
          {registrations.map((registration) => {
            const event = EVENTS.find((item) => item.id === registration.eventId)
            if (!event) return null
            return (
              <article className="registration-row" key={registration.id}>
                <div className="registration-info"><span className="category-label">{event.category}</span><h2>{event.title}</h2><p>{formatDate(event.date)} · {formatTime(event.time)}</p></div>
                <div className="attendee-info"><span>Attendee</span><strong>{registration.name}</strong><p>{registration.email}</p></div>
                <button className="cancel-button" type="button" onClick={() => onCancel(registration)}>Cancel registration</button>
              </article>
            )
          })}
        </div>
      ) : (
        <div className="empty-state registrations-empty">
          <h2>No registrations yet</h2>
          <button type="button" className="button button-dark" onClick={() => navigate('/')}>Browse events</button>
        </div>
      )}
    </section>
  )
}

function NotFoundPage() {
  return (
    <div className="empty-state registrations-empty">
      <h2>Page not found</h2>
      <Link className="button button-dark" to="/">Back to events</Link>
    </div>
  )
}

function App() {
  const [initialState] = useState(() => loadRegistrations(undefined, EVENTS))
  const [registrations, setRegistrations] = useState(initialState.registrations)
  const [storageError, setStorageError] = useState(initialState.error)

  function updateRegistrations(nextRegistrations) {
    const error = saveRegistrations(nextRegistrations)
    if (error) {
      setStorageError(error)
      return error
    }

    setRegistrations(nextRegistrations)
    setStorageError('')
    return ''
  }

  function register(event, attendee) {
    const result = createRegistration(event, attendee, registrations)
    if (result.error) return result

    const updated = [...registrations, result.registration]
    const error = updateRegistrations(updated)
    return { registration: error ? null : result.registration, error }
  }

  function cancel(registration) {
    if (!window.confirm(`Cancel ${registration.name}'s registration for ${EVENTS.find((event) => event.id === registration.eventId)?.title}?`)) return
    updateRegistrations(cancelRegistration(registrations, registration.id))
  }

  return (
    <BrowserRouter>
      <AppLayout
        registrations={registrations}
        onRegister={register}
        onCancel={cancel}
        storageError={storageError}
        onClearStorageError={() => setStorageError('')}
      />
    </BrowserRouter>
  )
}

export default App
