<<<<<<< HEAD
# Smart Study Schedule Generator

A beginner-friendly **Streamlit** web app that creates a **weekly study plan** from your subjects and time availability.

## 🎯 What you’ll get
- A simple webpage to enter **subjects** and **difficulty** (Easy/Medium/Hard)
- Enter your **total weekly study hours**
- (Optional) Customize **hours per day** and **session length**
- Click **Generate Schedule** to see:
  - A **detailed schedule** (Day, Start Time, Subject, Duration)
  - A **weekly summary** table
- **Download** both tables as CSV

---

## 🧰 Requirements
- **Python 3.9 or newer** (3.10+ recommended)

---

## 🖥️ Setup (Step-by-step)

> These instructions are for complete beginners. Follow them exactly.

### 1) Get Python (if you don’t have it)
- **Windows**: Download from the official Python website and install (make sure to tick **“Add Python to PATH”** during installation).  
- **Mac**: macOS often includes Python. If not, download from the website or use Homebrew (`brew install python`).  
- **Linux**: Use your package manager (e.g., `sudo apt install python3 python3-venv`).

Verify installation:
```bash
python --version
# or on some systems:
python3 --version
```

### 2) Download this project
- Download the ZIP provided to you (or copy these files).
- Extract the folder (e.g., to Desktop or Documents).

### 3) Open a terminal in the project folder
- **Windows**: Right-click inside the folder → **Open in Terminal** (or open PowerShell and `cd` into the folder).
- **Mac/Linux**: Open **Terminal**, then type `cd` and drag the folder into Terminal to paste its path, press Enter.

### 4) Create and activate a virtual environment (recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

You should now see `(.venv)` at the start of your terminal prompt.

### 5) Install dependencies
```bash
pip install -r requirements.txt
```

### 6) Run the app
```bash
streamlit run app.py
```
Your browser will open automatically (if not, copy the URL shown in the terminal into your browser).

---

## 🧠 How the schedule is created

- Each **difficulty** has a **weight**: Easy=1, Medium=2, Hard=3.  
- Your **total weekly hours** are split across subjects according to these weights.  
  - Example: If you have Math(Hard), English(Medium), Science(Easy), and 14 hours/week → weights = 3,2,1 (total 6).  
    - Math gets 14 * 3/6 = **7h**  
    - English gets 14 * 2/6 = **4.67h**  
    - Science gets 14 * 1/6 = **2.33h**

- Daily hours are split **equally** by default, but you can **customize** them in **Advanced Options**.  
- The app fills each day with **study blocks** of the chosen **session length** (default 1 hour), starting from **08:00**.  
- You can download the **Detailed** and **Summary** CSV files and share them.

---

## 🧪 Troubleshooting

- **Command not found**: Try `python3` instead of `python`.  
- **Streamlit not found**: Run `pip install -r requirements.txt` again (while your venv is active).  
- **Nothing happens after running**: Check the terminal for the URL (usually `http://localhost:8501`), paste it into your browser.  
- **Weird tables**: Ensure you filled the subject names and chose a difficulty.

---

## 📁 Project structure

```
smart-study-scheduler/
├─ app.py              # Streamlit app (main file to run)
├─ requirements.txt    # Python dependencies
├─ README.md           # This guide
├─ run.bat             # One-click run for Windows
└─ run.sh              # One-click run for Mac/Linux
```

---

## ▶️ One‑click run (optional)

### Windows
Double‑click `run.bat` (or run it from Terminal):
```bat
@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Mac/Linux
Make it executable once, then run it:
```bash
chmod +x run.sh
./run.sh
```

Enjoy and good luck with your studies! 📚
=======
# smart-study-scheduler
📚 Smart Study Schedule Generator is a beginner-friendly Streamlit app that creates personalized weekly study timetables. Enter your subjects, difficulty levels, and available hours to get a balanced, color-coded schedule with detailed daily sessions, weekly summaries, and CSV downloads.
>>>>>>> 41e32616b1c4cf754d5dcf095343a0496cea9e37
