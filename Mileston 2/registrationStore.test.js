import assert from 'node:assert/strict'
import test from 'node:test'
import EVENTS from '../src/events.json' with { type: 'json' }
import {
  cancelRegistration,
  createRegistration,
  filterEvents,
  getAvailableSeats,
  loadRegistrations,
  saveRegistrations,
  STORAGE_KEY,
  validateAttendee,
} from '../src/registrationStore.js'

function createMemoryStorage() {
  const values = new Map()
  return {
    getItem(key) {
      return values.get(key) ?? null
    },
    setItem(key, value) {
      values.set(key, value)
    },
  }
}

test('starter data contains the six assessment events with valid fields', () => {
  assert.equal(EVENTS.length, 6)
  const ids = EVENTS.map((event) => event.id)
  assert.equal(new Set(ids).size, ids.length)
  assert.deepEqual(EVENTS.map(({ id, seats }) => [id, seats]), [
    ['EV101', 4],
    ['EV102', 3],
    ['EV103', 5],
    ['EV104', 4],
    ['EV105', 3],
    ['EV106', 2],
  ])
  assert.ok(EVENTS.every((event) =>
    event.title.trim()
    && event.category.trim()
    && /^\d{4}-\d{2}-\d{2}$/.test(event.date)
    && /^([01]\d|2[0-3]):[0-5]\d$/.test(event.time)
    && Number.isInteger(event.seats)
    && event.seats > 0,
  ))
})

test('search ignores case and category filtering returns the matching events', () => {
  assert.equal(filterEvents(EVENTS, 'VISUAL', 'All')[0].id, 'EV103')
  assert.deepEqual(filterEvents(EVENTS, '', 'Arts').map((event) => event.id), ['EV102', 'EV106'])
  assert.deepEqual(filterEvents(EVENTS, 'not an event', 'All'), [])
})

test('attendee validation requires a name and a valid email address', () => {
  assert.deepEqual(validateAttendee({ name: ' ', email: '' }), {
    name: 'Please enter your full name.',
    email: 'Please enter your email address.',
  })
  assert.deepEqual(validateAttendee({ name: 'Taylor Reed', email: 'invalid' }), {
    email: 'Please enter a valid email address.',
  })
  assert.deepEqual(validateAttendee({ name: ' Taylor Reed ', email: ' taylor@example.com ' }), {})
})

test('registration reduces available seats and persists for a reload', () => {
  const event = EVENTS[0]
  const storage = createMemoryStorage()
  const result = createRegistration(event, { name: 'Taylor Reed', email: 'taylor@example.com' }, [])

  assert.equal(result.error, '')
  assert.equal(getAvailableSeats(event, [result.registration]), event.seats - 1)
  assert.equal(saveRegistrations([result.registration], storage), '')
  assert.deepEqual(loadRegistrations(storage, EVENTS).registrations, [result.registration])
})

test('duplicate email is rejected regardless of case and spaces', () => {
  const event = EVENTS[0]
  const existing = { id: 'existing', eventId: event.id, name: 'Taylor Reed', email: 'taylor@example.com' }
  const result = createRegistration(
    event,
    { name: 'Taylor Reed', email: ' TAYLOR@example.com ' },
    [existing],
  )

  assert.equal(result.registration, null)
  assert.match(result.error, /already registered/)
})

test('the same email can register for a different event', () => {
  const [firstEvent, secondEvent] = EVENTS
  const existing = { id: 'existing', eventId: firstEvent.id, name: 'Taylor Reed', email: 'taylor@example.com' }
  const result = createRegistration(
    secondEvent,
    { name: 'Taylor Reed', email: 'TAYLOR@example.com' },
    [existing],
  )

  assert.equal(result.error, '')
  assert.equal(result.registration.eventId, secondEvent.id)
})

test('full events reject new registrations and cancelling restores a seat', () => {
  const event = EVENTS[0]
  const registrations = Array.from({ length: event.seats }, (_, index) => ({
    id: `registration-${index}`,
    eventId: event.id,
    name: `Attendee ${index}`,
    email: `attendee${index}@example.com`,
  }))

  assert.equal(getAvailableSeats(event, registrations), 0)
  assert.match(createRegistration(event, { name: 'New attendee', email: 'new@example.com' }, registrations).error, /fully booked/)

  const activeRegistrations = cancelRegistration(registrations, registrations[0].id)
  assert.equal(activeRegistrations.length, event.seats - 1)
  assert.equal(getAvailableSeats(event, activeRegistrations), 1)
})

test('loading ignores registrations for removed events and reports malformed data', () => {
  const storage = createMemoryStorage()
  storage.setItem(STORAGE_KEY, JSON.stringify([
    { id: 'valid', eventId: EVENTS[0].id, name: 'Taylor Reed', email: 'taylor@example.com' },
    { id: 'removed', eventId: 'EV-REMOVED', name: 'Old attendee', email: 'old@example.com' },
  ]))

  assert.equal(loadRegistrations(storage, EVENTS).registrations.length, 1)

  storage.setItem(STORAGE_KEY, '{invalid')
  assert.equal(loadRegistrations(storage, EVENTS).registrations.length, 0)
  assert.match(loadRegistrations(storage, EVENTS).error, /could not be read/)
})

test('storage write failures return an error without throwing', () => {
  const brokenStorage = {
    setItem() {
      throw new Error('Storage quota exceeded')
    },
  }

  assert.match(saveRegistrations([], brokenStorage), /could not be saved/)
})
