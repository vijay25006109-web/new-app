# 🔐 Password Strength Checker

A simple Streamlit web app that estimates password strength using rule-based security checks.

## Features

- Password length check
- Uppercase/lowercase checks
- Number and special-character checks
- Common-password detection
- Repeated-character detection
- Obvious sequence detection
- Strength score
- Improvement suggestions

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Open Streamlit Cloud.
4. Select your GitHub repository.
5. Set the main file to `app.py`.
6. Deploy.

## Privacy

The app does not save or send passwords to an external service. The password is processed by the Streamlit application for the current session only.

## Disclaimer

This is an educational password-strength estimator, not a guarantee of password security.
