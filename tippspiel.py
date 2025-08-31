import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# Google Sheets Setup über Secrets
# -------------------------------
creds_dict = st.secrets["gspread"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["gspread"]["sheet_id"]).sheet1

# -------------------------------
# App-Titel
# -------------------------------
st.title("🏆 100m Männer Tippspiel mit Leaderboard")

# -------------------------------
# Benutzereingaben
# -------------------------------
name = st.text_input("Dein Name")
a = st.text_input("100m M S:")
b = st.text_input("100m M Z:")
c = st.text_input("100m M D:")

# -------------------------------
# Punkteberechnung & Leaderboard-Update
# -------------------------------
if st.button("Auswerten"):
    import sieger  # deine Datei mit den Siegern

    hmm = [a, b, c]
    punkte = 0

    # Punkteberechnung
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

    # -------------------------------
    # Leaderboard aktualisieren
    # -------------------------------
    # Bestehende Daten laden
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Prüfen, ob der User schon existiert
    if not df.empty and "Name" in df.columns and name in df["Name"].values:
        # Zeile aktualisieren
        idx = df.index[df["Name"] == name][0]
        df.at[idx, "Punkte"] = punkte
        # Sheet leeren und aktualisieren
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    else:
        # Neuer Eintrag
        sheet.append_row([name, punkte])

# -------------------------------
# Leaderboard anzeigen
# -------------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("🏅 Leaderboard")

if not df.empty and "Punkte" in df.columns:
    df["Punkte"] = pd.to_numeric(df["Punkte"], errors="coerce")
    st.dataframe(df.sort_values(by="Punkte", ascending=False))
else:
    st.write("Noch keine Einträge im Leaderboard.")



