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
st.title("🏆 VFV Spandau: Das große Tippspiel")

# -------------------------------
# Benutzereingaben
# -------------------------------
name = st.text_input("Dein Name")
hmme = st.text_input("100m Männer Sieger:")
hmmz = st.text_input("100m Männer Zweiter:")
hmmd = st.text_input("100m Männer Dritter:") #100m Männer
hmwe = st.text_input("100m Frauen Siegerin:")
hmwz = st.text_input("100m Frauen Zweite:")
hmwd = st.text_input("100m Frauen Dritte:") #100m Frauen
hzmhme = st.text_input("110m Hürden Männer Sieger:")
hzmhmz = st.text_input("100m M Z:")
hzmhmd = st.text_input("100m M D:") #110m Hürden Männer
hmhwe = st.text_input("100m Hürde Frauen Siegerin:")
hmhwz = st.text_input("100m M Z:")
hmhwd = st.text_input("100m M D:") #100m Hürden Frauen
zmms= st.text_input("100m M S:")
zmmz = st.text_input("100m M Z:")
zmmd = st.text_input("100m M D:") #200m Männer
zmws = st.text_input("100m M S:")
zmwz = st.text_input("100m M Z:")
zmwd = st.text_input("100m M D:") #200m Frauen
vmms = st.text_input("100m M S:")
vmmz = st.text_input("100m M Z:")
vmmd = st.text_input("100m M D:") #400m Männer
vmwe = st.text_input("100m M S:")
vmwz = st.text_input("100m M Z:")
vmwd = st.text_input("100m M D:") #400m Frauen

# -------------------------------
# Punkteberechnung & Leaderboard-Update
# -------------------------------
if st.button("Auswerten"):
    import sieger  # deine Datei mit den Siegern

    hmm = [hmme, hmmz, hmmd]
    hmw = [hmwe, hmwz, hmwd]
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
    #Punkte 100m Frauen
    if hmw[0] == sieger.ohmw[0]:
        punkte += 2
    if hmw[1] == sieger.ohmw[1]:
        punkte += 2
    if hmw[2] == sieger.ohmw[2]:
        punkte += 2
    for x in hmw:
        if x in sieger.ohmw:
            punkte += 1
    #Punkte 110m Hürden Männer
        if hmm[0] == sieger.ohmm[0]:
        punkte += 2
    if hmm[1] == sieger.ohmm[1]:
        punkte += 2
    if hmm[2] == sieger.ohmm[2]:
        punkte += 2
    for x in hmm:
        if x in sieger.ohmm:
            punkte += 1
    #100m Hürden Frauen
        if hmm[0] == sieger.ohmm[0]:
        punkte += 2
    if hmm[1] == sieger.ohmm[1]:
        punkte += 2
    if hmm[2] == sieger.ohmm[2]:
        punkte += 2
    for x in hmm:
        if x in sieger.ohmm:
            punkte += 1
    #100m Hürden Frauen
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




