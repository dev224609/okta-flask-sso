# okta-flask-sso

A sample Python 3 Flask web application demonstrating how to integrate Okta Single Sign-On (SSO) using the OAuth 2.0 Authorization Code flow.  

This app:  
- Fetches both an **ID Token** and an **Access Token** from Okta  
- Parses and displays OIDC claims in a Bootstrap-styled profile page  
- Provides a clean **Login** / **Logout** UX that clears both your application session and the Okta SSO session  

---

## Features

- OAuth 2.0 Authorization Code grant with Authlib  
- Automatic parsing & display of OIDC ID Token claims  
- Access Token retrieval & display  
- Home page with **Login** button  
- Profile page with **Logout** button  
- Clears both app session and Okta session on logout  
- Bootstrap-powered UI  

---

## Prerequisites

- Python 3.7 or newer  
- [Okta Developer account](https://developer.okta.com/)  
- An Okta OIDC Web application (Authorization Code grant enabled)  

---

## Project Structure
okta-flask-sso/ ├── .env ├── app.py ├── requirements.txt └── templates/ ├── base.html ├── index.html └── profile.htm


---

## Installation

1. Clone this repo (or create a new folder and copy files)  
2. Create and activate a virtual environment  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\Activate.ps1

### Install dependencies
1. Run below cmd to install dependencies
   ```bash
   pip install -r requirements.txt


### Configuration
- Create a .env file in your project root with
```
OKTA_CLIENT_ID=your_client_id
OKTA_CLIENT_SECRET=your_client_secret
OKTA_ISSUER=https://{yourOktaDomain}/oauth2/default
FLASK_SECRET_KEY=a-very-random-secret
```
- Ensure FLASK_SECRET_KEY is a strong, random string (used to sign session cookies).
