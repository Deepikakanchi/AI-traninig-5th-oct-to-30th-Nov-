# Gather — Event Enrollment Manager

A responsive React + Vite frontend for browsing community learning events, registering attendees, and managing registrations. Registrations are stored in the browser with `localStorage`; no backend, account, or external service is required.

## Run locally

Requirements: Node.js 20.19+ or 22.12+.

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. To create and preview a production build:

```bash
npm run build
npm run preview
```

Run the automated checks:

```bash
npm test
npm run lint
```

The tests cover the supplied event data, search and category filters, form validation, duplicate registrations, seat limits, cancellation, and browser storage.

## Features

- Browse six upcoming events with title, category, local date/time, total seats, and available seats.
- Search event titles without case sensitivity and filter by category.
- Register with a required full name and email address; duplicate emails for the same event are blocked regardless of case or surrounding spaces.
- Available seats update immediately based on active registrations.
- View all attendee registrations and cancel a registration after confirmation.
- Persist registration data in browser `localStorage` across page reloads.
- Responsive layout with dedicated Events and Registrations routes.

## Starter event data

The app starts with the six fixed assessment events below, each with zero registrations:

| ID | Event | Category | Date | Time | Seats |
|---|---|---|---|---|---:|
| EV101 | Intro to Cloud Computing | Technology | 10 Nov 2026 | 10:00 | 4 |
| EV102 | Creative Writing Lab | Arts | 12 Nov 2026 | 14:00 | 3 |
| EV103 | Data Visualization Basics | Technology | 14 Nov 2026 | 11:00 | 5 |
| EV104 | Personal Finance Essentials | Life Skills | 16 Nov 2026 | 16:00 | 4 |
| EV105 | Public Speaking Practice | Life Skills | 18 Nov 2026 | 10:30 | 3 |
| EV106 | Digital Illustration Studio | Arts | 20 Nov 2026 | 13:00 | 2 |

Dates and times are displayed in local time. Event data lives in `src/events.json`.

## Adding an event

Add a new object to the `src/events.json` array. Use a unique `id`, a title, category, date in `YYYY-MM-DD` format, time in 24-hour `HH:MM` format, and the total seat capacity:

```json
{
  "id": "EV107",
  "title": "Intro to Gardening",
  "category": "Life Skills",
  "date": "2026-11-22",
  "time": "10:00",
  "seats": 8
}
```

The Events page and category filters read from this file, so you do not need to edit the React components when adding an event. Keep IDs unique; existing registrations refer to events by ID.

## Routes and persistence

- `/` — event listing, search, category filters, and registration form.
- `/registrations` — attendee registrations and cancellation actions.

Registrations are stored under the `community-learning-centre-registrations` localStorage key. Clearing browser site data removes those registrations.

Registration rules and browser storage helpers are in `src/registrationStore.js`; the UI updates only after a registration change is saved successfully.
