# DEPLOY TO GITHUB + STREAMLIT CLOUD
# Complete step-by-step guide
# ============================================================

# ── STEP 1: Initialise git in C:\Projects\MoPhones ──────────────
cd C:\Projects\MoPhones

# Copy these files into C:\Projects\MoPhones:
#   app.py
#   requirements.txt
#   README.md
#   .gitignore
#   .streamlit\config.toml   (create the .streamlit folder first)

git init
git add app.py requirements.txt README.md .streamlit/config.toml
# NOTE: Do NOT git add the data files — .gitignore excludes them
git commit -m "Initial commit: MoPhones Credit Intelligence Dashboard"


# ── STEP 2: Create GitHub repo ───────────────────────────────────
# Option A: GitHub CLI (if installed)
gh repo create mophones-credit-dashboard --public --push --source=.

# Option B: Manual
# 1. Go to https://github.com/new
# 2. Name it:  mophones-credit-dashboard
# 3. Keep it PUBLIC (required for free Streamlit Cloud)
# 4. Do NOT initialise with README (you already have one)
# 5. Then run:
git remote add origin https://github.com/YOUR_USERNAME/mophones-credit-dashboard.git
git branch -M main
git push -u origin main


# ── STEP 3: Handle data files for Streamlit Cloud ────────────────
# The data files are too large / sensitive for git.
# Best approach: add a file uploader fallback to app.py
# (already handled — the app will prompt for uploads if files are missing)
#
# OR: Use Streamlit Secrets to store a download URL
# OR: Commit a small anonymised sample for demo purposes


# ── STEP 4: Deploy to Streamlit Community Cloud ──────────────────
# 1. Go to https://share.streamlit.io
# 2. Sign in with GitHub
# 3. Click "New app"
# 4. Repository:  YOUR_USERNAME/mophones-credit-dashboard
# 5. Branch:      main
# 6. Main file:   app.py
# 7. Click "Deploy!"
#
# Your app will be live at:
# https://YOUR_USERNAME-mophones-credit-dashboard-app-XXXX.streamlit.app


# ── STEP 5: Add data upload support (for Streamlit Cloud) ────────
# The app already tries to load files from disk first.
# If running on Streamlit Cloud (no local files), add this to your
# app.py sidebar to let users upload their own data:
#
# with st.sidebar:
#     st.markdown("### Upload Data")
#     credit_zip = st.file_uploader("Credit Data.zip", type="zip")
#     sales_xl   = st.file_uploader("Sales & Customer Data.xlsx", type="xlsx")
#     nps_xl     = st.file_uploader("NPS Data.xlsx", type="xlsx")


# ── QUICK REFERENCE ──────────────────────────────────────────────
# Local run:
#   cd C:\Projects\MoPhones
#   streamlit run app.py

# Update and re-deploy:
#   git add app.py
#   git commit -m "Update: <description>"
#   git push
#   (Streamlit Cloud auto-deploys on push)
