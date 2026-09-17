# Lost & Found HWP

Mobile-first Lost & Found web application for Horwang Pathumthani School, built with Python and Streamlit.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit. The app now supports personal email sign-in, OTP verification, and first-time student linking.

## Included

- Personal email authentication using standard public domains such as gmail.com, outlook.com, and hotmail.com
- 2-step OTP verification flow with validation for malformed email input
- First-time linking of personal email to Student ID and Class
- Session-backed login state and user profile mapping to behavior score and item return history
- Mobile-friendly report form, search filters, and clear logout controls in both the sidebar and profile dashboard

Data is stored in Streamlit session state for this prototype and resets when the session restarts.
