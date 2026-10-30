export const STORAGE_KEY = 'community-learning-centre-registrations'

export function filterEvents(events, query, category) {
  const searchTerm = query.trim().toLowerCase()
  return events.filter((event) =>
    event.title.toLowerCase().includes(searchTerm)
    && (category === 'All' || event.category === category),
  )
}

export function validateAttendee(attendee) {
  const errors = {}
  const email = attendee.email.trim()

  if (!attendee.name.trim()) errors.name = 'Please enter your full name.'
  if (!email) errors.email = 'Please enter your email address.'
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Please enter a valid email address.'
  }

  return errors
}

export function getAvailableSeats(event, registrations) {
  const activeCount = registrations.filter((registration) => registration.eventId === event.id).length
  return Math.max(0, event.seats - activeCount)
}

export function createRegistration(event, attendee, registrations) {
  if (getAvailableSeats(event, registrations) === 0) {
    return { registration: null, error: 'This event is now fully booked.' }
  }

  const normalizedEmail = attendee.email.trim().toLowerCase()
  const alreadyRegistered = registrations.some((registration) =>
    registration.eventId === event.id
    && registration.email.trim().toLowerCase() === normalizedEmail,
  )

  if (alreadyRegistered) {
    return { registration: null, error: 'This email is already registered for this event.' }
  }

  return {
    registration: {
      id: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
      eventId: event.id,
      name: attendee.name,
      email: attendee.email,
    },
    error: '',
  }
}

export function cancelRegistration(registrations, registrationId) {
  return registrations.filter((registration) => registration.id !== registrationId)
}

export function loadRegistrations(storage, events) {
  try {
    const storageArea = storage ?? window.localStorage
    const saved = storageArea.getItem(STORAGE_KEY)
    if (!saved) return { registrations: [], error: '' }

    const parsed = JSON.parse(saved)
    if (!Array.isArray(parsed)) throw new Error('Stored registrations are not a list.')

    const registrations = parsed.filter((registration) =>
      registration
      && typeof registration.id === 'string'
      && typeof registration.eventId === 'string'
      && events.some((event) => event.id === registration.eventId)
      && typeof registration.name === 'string'
      && typeof registration.email === 'string',
    )
    return { registrations, error: '' }
  } catch {
    return {
      registrations: [],
      error: 'Saved registrations could not be read. New registrations will still work in this session.',
    }
  }
}

export function saveRegistrations(registrations, storage) {
  try {
    const storageArea = storage ?? window.localStorage
    storageArea.setItem(STORAGE_KEY, JSON.stringify(registrations))
    return ''
  } catch {
    return 'Your registration could not be saved in this browser. Check your browser storage settings.'
  }
}
