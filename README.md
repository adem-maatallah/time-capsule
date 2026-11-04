# Digital Time Capsule

A one-page web app where you write messages to the future. Each capsule
has an "open date", and the Flask API keeps its content locked until that
date arrives. Before then, you can only see the title and a countdown.

## Features
- Write a capsule: title, message, your name, and an open date
- See all capsules in a list, marked 🔒 locked or 🔓 unlocked
- Live countdown for locked capsules ("Opens in 12 days")
- Open an unlocked capsule to read the message
- Delete a capsule

## The key rule
The API itself enforces the lock. If a capsule is still locked, the server
never sends its message, even if someone calls the API directly.

## Data model (Capsule)
| Field      | Type     | Notes                          |
|------------|----------|--------------------------------|
| id         | integer  | auto-generated                 |
| title      | text     | required, visible when locked  |
| message    | text     | required, hidden until open    |
| author     | text     | required                       |
| open_date  | date     | required, must be in the future|
| created_at | datetime | set automatically              |

## API endpoints
| Method | Endpoint             | Description                                  |
|--------|----------------------|----------------------------------------------|
| GET    | /api/capsules        | List all capsules (no messages included)     |
| POST   | /api/capsules        | Create a new capsule                         |
| GET    | /api/capsules/<id>   | Get one capsule; message only if unlocked    |
| DELETE | /api/capsules/<id>   | Delete a capsule                             |

## Tech stack
- Backend: Python, Flask
- Database: SQLite
- Frontend: one HTML page with CSS and JavaScript (fetch API)