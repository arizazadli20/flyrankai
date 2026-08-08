# FlyRank Auth API - Week 2 (A4)

This is a secure backend API built with FastAPI and Supabase Auth. It handles user registration, login, logout, and protects specific routes using JWT (JSON Web Token) verification.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your_github_repo_link>
    ```
2.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn supabase python-dotenv pydantic
    ```
3.  **Environment Variables:**
    *   Create a `.env` file in the root directory.
    *   Copy the variables from `.env.example` and replace them with your actual Supabase project URL and anon key.
4.  **Run the Server:**
    ```bash
    uvicorn main:app --reload
    ```

## Endpoints Overview

| Route | Method | Purpose | Auth Required |
| :--- | :--- | :--- | :--- |
| `/auth/signup` | POST | Create a new user account | No |
| `/auth/login` | POST | Authenticate & return a JWT | No |
| `/public/info` | GET | Read public, open data | No |
| `/protected/profile` | GET | Read private profile data | Yes (Bearer Token) |

## Swagger UI
You can interact with the API and test the authentication flow directly through the Swagger UI at `http://localhost:8000/docs`. A lock icon indicates protected routes.