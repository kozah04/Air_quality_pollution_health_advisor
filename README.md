# Air Quality & Pollution Health Advisor

A Python + Streamlit app where you type in a location and it shows the current air quality, the cleanest time of day to go outside, and plain-English health advice written by Google's Gemini AI. The advice pays special attention to children, the elderly, and people with asthma or other breathing problems.

## What it does

- **Check a location:** shows the AQI and the main pollutants (PM2.5, PM10, ozone, nitrogen dioxide), then asks Gemini to explain what the numbers mean and whether it is safe to be outside.
- **Cleanest time to go out:** shows the cleanest hour of the whole day, and the cleanest hour between 6 AM and 10 PM, since almost nobody goes out at 1 AM.
- **Protective advice:** masks, windows, indoor air, based on how bad the air is.
- **Compare two locations:** puts two places side by side and tells you which has cleaner air.
- **Favourites and history:** saves favourite locations and every reading to local JSON files so you can look back at past checks.

Air quality data comes from the free [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) (no key needed). The AI advice comes from the Gemini API (free key needed, see Step 4).

## Project structure

```
air_quality_app/
├── main.py                     # The Streamlit app (the screen you see)
├── air_quality_client.py       # Talks to Open-Meteo, finds the cleanest hours
├── air_reading.py              # AirReading class, holds one reading's data
├── health_risk_analyzer.py     # Sends the numbers to Gemini for health advice
├── location_history_store.py   # Saves and loads history and favourites (JSON)
├── validators.py               # Regex checks on user input
├── requirements.txt            # Python packages the app needs
├── .env.example                # Template for your API key file
├── .gitignore
├── data/                       # history.json and favourites.json live here
└── README.md
```

You will also create a file called `.env` in this same folder. It holds your API key and is never uploaded to GitHub.

## Before you start

You need:

- **Python 3.10 or newer**
- **Git** (Git Bash on Windows is fine)
- **Anaconda or Miniconda** (recommended), or plain Python with `venv` (see the note in Step 2)
- **A Google account**, to get the free Gemini API key
- **An internet connection**, since the app calls two online APIs

## Step 1: Get the code

Open a terminal (Git Bash, Anaconda Prompt, or Terminal on macOS/Linux) and run:

```
git clone https://github.com/kozah04/air_quality_app.git
cd air_quality_app
```

If you are working on your own branch, switch to it now with `git checkout your-branch-name`.

## Step 2: Create an environment and install the packages

An environment keeps this project's packages separate from everything else on your computer.

```
conda create -n air_quality python=3.10
conda activate air_quality
pip install -r requirements.txt
```

Type `y` if conda asks whether to proceed. After `conda activate`, your terminal prompt should start with `(air_quality)`.

**Not using conda?** Use Python's built-in `venv` instead:

```
python -m venv venv
```

Then activate it:

- Windows (Git Bash): `source venv/Scripts/activate`
- Windows (Command Prompt): `venv\Scripts\activate`
- macOS / Linux: `source venv/bin/activate`

Then run `pip install -r requirements.txt`.

**Git Bash and conda:** if `conda activate` gives an error like `CommandNotFoundError`, run `conda init bash` once, close Git Bash, open it again, and retry. Using the Anaconda Prompt instead also avoids this.

## Step 3: Check the install worked

```
pip list
```

You should see `streamlit`, `requests`, `google-generativeai`, and `python-dotenv` in the list.

## Step 4: Get your Gemini API key

The AI health advice needs a key from Google. It is free to get and does not need a credit card. Google can change the exact wording on these pages, but the steps look like this:

1. Go to **Google AI Studio** at [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys). 
2. Sign in with your Google account and accept the terms if asked.
3. Click **Create API key**.
4. Choose an existing project or let it create a new one for you. Either is fine.
5. Copy the key that appears. Treat it like a password.

Google's own instructions are here if the page looks different: [ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)

The free tier has usage limits (a limited number of requests per minute and per day), and Google changes them from time to time. For this project this is normally plenty. If you hit the limit, wait a minute and try again.

## Step 5: Put your API key in the `.env` file

The key goes in a file named `.env`, in the project's main folder (the same folder as `main.py`). **Do not** type it into `main.py` or any other `.py` file.

1. Make a copy of the template:
   - Git Bash, macOS, Linux: `cp .env.example .env`
   - Windows Command Prompt: `copy .env.example .env`
2. Open the new `.env` file in any text editor.
3. Replace the placeholder so the file contains exactly one line:

```
GEMINI_API_KEY=paste_your_real_key_here
```

- No quotes around the key.
- No spaces around the `=`.
- The file must be named exactly `.env`, not `.env.txt`. On Windows, turn on "File name extensions" in File Explorer to check.

The `.env` file is listed in `.gitignore`, so Git will never upload it. That is the whole point: your key stays on your machine even though the code is on a public GitHub repo.

**If you ever paste a key into a file that gets pushed to GitHub, treat that key as leaked.** Go back to Google AI Studio, delete it, and create a new one.

## Step 6: Run the app

Make sure your environment is active (you see `(air_quality)` in the prompt) and you are in the project folder, then run:

```
streamlit run main.py
```

Streamlit opens the app in your browser, usually at `http://localhost:8501`. If it does not open by itself, paste that address into your browser. To stop the app, go back to the terminal and press `Ctrl + C`.

**Always start it with `streamlit run main.py`.** Running `python main.py` will not show the interface.

## Python concepts used in this project

- **OOP:** `AirQualityClient`, `AirReading`, `HealthRiskAnalyzer`, `LocationHistoryStore`
- **File handling:** saving and loading `history.json` and `favourites.json`
- **Exception handling:** bad locations, network errors, missing data, failed AI calls
- **Regular expressions:** checking location names, coordinates and dates in `validators.py`
- **Date and time handling:** timestamps on readings, formatting forecast hours, finding the cleanest hour of the day
- **External APIs:** Open-Meteo for air quality data, Gemini for the health advice
- **GUI:** Streamlit
