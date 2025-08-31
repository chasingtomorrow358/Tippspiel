import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup über Streamlit Secrets
# st.secrets["gspread"] ist bereits ein dict, kein JSON
creds_dict = st.secrets["gspread"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Öffne das Sheet
sheet = client.open_by_key(st.secrets["sheet_id"]).sheet1  # sheet_id ebenfalls in Secrets speichern

st.title("🏆 100m Männer Tippspiel mit Leaderboard")

# Eingaben
name = st.text_input("Dein Name")
a = st.text_input("100m M S:")
b = st.text_input("100m M Z:")
c = st.text_input("100m M D:")

if st.button("Auswerten"):
    import sieger  # deine Datei mit den Siegern

    hmm = [a, b, c]
    punkte = 0

    if hmm[0] == sieger.ohmm[0]:
        punkte += 2
    if hmm[1] == sieger.ohmm[1]:
        punkte += 2
    if hmm[2] == sieger.ohmm[2]:
        punkte += 2
    for x in hmm:
        if x in sieger.ohmm:
            punkte += 1

    st.success(f"{name}, du hast {punkte} Punkte!")

    # Punkte in Google Sheet eintragen
    sheet.append_row([name, punkte])

# Leaderboard aus Google Sheet laden
data = sheet.get_all_records()
df = pd.DataFrame(data)
st.subheader("🏅 Leaderboard")
st.dataframe(df.sort_values(by="Punkte", ascending=False))

