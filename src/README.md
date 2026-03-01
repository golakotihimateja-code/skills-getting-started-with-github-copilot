# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. (Optional) Run the test suite to verify behavior:

   ```
   pip install -r ../requirements.txt
   pytest
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

*(A `tests/` directory accompanies this project.  The tests use `pytest` with the
Arrange–Act–Assert pattern to exercise all routes.  Add new tests there when
expanding functionality.)*


| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup` (body: `{"email": "student@mergington.edu"}`) | Sign up for an activity; returns **201 Created**                     |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

**Note:**
- `POST` returns 201 on success; supply the student email in the JSON body.
- `DELETE` also expects a JSON body and returns 204 No Content when a signup
  is removed.  Both endpoints use the same `SignupRequest` model.