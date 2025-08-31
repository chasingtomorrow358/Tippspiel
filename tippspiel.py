import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# -------------------------------
# Google Sheets Setup über Secrets
# -------------------------------
creds_dict = st.secrets["gspread"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["gspread"]["sheet_id"]).sheet1

# -------------------------------
# Abgabeschluss festlegen
# -------------------------------
deadline = datetime(2025, 9, 13, 0, 15)

st.title("🏆 VFV Spandau: Das große Tippspiel","content")
st.info(f"⏰ Tipps können bis **{deadline.strftime('%d.%m.%Y %H:%M')}** eingereicht werden.")

# -------------------------------
# Benutzereingaben (nur bis Deadline)
# -------------------------------
now = datetime.now()


if now < deadline:
    name = st.text_input("Dein Name")
    st.title("Dein Tip für die 100m Männer")
    hmme = st.text_input("100m Männer Sieger:")
    hmmz = st.text_input("100m Männer Zweiter:")
    hmmd = st.text_input("100m Männer Dritter:") 
    st.title("Dein Tip für die 100m Frauen")
    hmwe = st.text_input("100m Frauen Siegerin:")
    hmwz = st.text_input("100m Frauen Zweite:")
    hmwd = st.text_input("100m Frauen Dritte:")

if st.button("Tipp abgeben"):
    now = datetime.now()

    if now > deadline:
        st.error("⏰ Abgabeschluss ist vorbei! Du kannst keine Tipps mehr abgeben.")
    elif (
        name.strip() == "" 
        or hmme.strip() == "" or hmmz.strip() == "" or hmmd.strip() == ""
        or hmwe.strip() == "" or hmwz.strip() == "" or hmwd.strip() == ""
    ):
        st.error("Bitte alle Felder ausfüllen!")
    else:
        # Tipps speichern: Männer + Frauen, Punkte=0 als Platzhalter
        sheet.append_row([
            name,
            hmme, hmmz, hmmd,   # 100m Männer
            hmwe, hmwz, hmwd,   # 100m Frauen
            0                   # Punkte/ Hier müssen noch die anderen Events hin
        ])
        st.success(f"Danke {name}, dein Tipp wurde gespeichert!")

# -------------------------------
# Punkteberechnung & Leaderboard-Update
# -------------------------------
if st.button("Auswerten"):
    import sieger  # Datei mit den Siegern

    hmm = [hmme, hmmz, hmmd]
    hmw = [hmwe, hmwz, hmwd]
    punkte = 0

    # Punkte 100m Männer
    if hmm[0] == sieger.ohmm[0]: punkte += 2
    if hmm[1] == sieger.ohmm[1]: punkte += 2
    if hmm[2] == sieger.ohmm[2]: punkte += 2
    for x in hmm:
        if x in sieger.ohmm: punkte += 1

    # Punkte 100m Frauen
    if hmw[0] == sieger.ohmw[0]: punkte += 2
    if hmw[1] == sieger.ohmw[1]: punkte += 2
    if hmw[2] == sieger.ohmw[2]: punkte += 2
    for x in hmw:
        if x in sieger.ohmw: punkte += 1

    st.success(f"{name}, du hast {punkte} Punkte!")

    # -------------------------------
    # Leaderboard aktualisieren
    # -------------------------------
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and "Name" in df.columns and name in df["Name"].values:
        # Update vorhandene Punkte
        idx = df.index[df["Name"] == name][0]
        df.at[idx, "Punkte"] = punkte
        # Sheet neu schreiben
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    else:
        # Neuer Eintrag mit Punkten
        sheet.append_row([name, hmme, hmmz, hmmd, punkte])

# -------------------------------
# Leaderboard anzeigen
# -------------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("🏅 Leaderboard")

if not df.empty and "Punkte" in df.columns:
    df["Punkte"] = pd.to_numeric(df["Punkte"], errors="coerce")
    leaderboard = df[["Name", "Punkte"]]  # nur Name + Punkte anzeigen
    st.dataframe(leaderboard.sort_values(by="Punkte", ascending=False))
else:
    st.write("Noch keine Einträge im Leaderboard.")











