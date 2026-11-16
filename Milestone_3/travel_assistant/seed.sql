INSERT OR IGNORE INTO trips
    (id, employee_id, destination, start_date, end_date, purpose, status)
VALUES
    (104, 'EMP104', 'Jaipur',  '2026-11-20', '2026-11-22', 'Client meeting',    'planned'),
    (205, 'EMP205', 'Mumbai',  '2026-11-22', '2026-11-24', 'Training workshop', 'planned'),
    (310, 'EMP310', 'Chennai', '2026-11-25', '2026-11-27', 'Audit visit',       'planned');

INSERT OR IGNORE INTO session_trips (session_id, trip_id)
VALUES ('demo-session', 104);