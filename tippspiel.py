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

st.title("🏆 VFV Spandau: Das große Tippspiel")
st.info(f"⏰ Tipps können bis **{deadline.strftime('%d.%m.%Y %H:%M')}** eingereicht werden.")

# -------------------------------
# Benutzereingaben (nur bis Deadline)
# -------------------------------
now = datetime.now()

if now < deadline:
    name = st.text_input("Dein Name")

    st.subheader("Dein Tipp für die 100m Männer")
    hmme = st.text_input("100m Männer Sieger:")
    hmmz = st.text_input("100m Männer Zweiter:")
    hmmd = st.text_input("100m Männer Dritter:")

    st.subheader("Dein Tipp für die 100m Frauen")
    hmwe = st.text_input("100m Frauen Siegerin:")
    hmwz = st.text_input("100m Frauen Zweite:")
    hmwd = st.text_input("100m Frauen Dritte:")

    # -------------------------------
    # Tipp abgeben
    # -------------------------------
    if st.button("Tipp abgeben"):
        if name.strip() == "" or hmme.strip() == "" or hmmz.strip() == "" or hmmd.strip() == "" \
           or hmwe.strip() == "" or hmwz.strip() == "" or hmwd.strip() == "":
            st.error("⚠️ Bitte alle Felder ausfüllen!")
        else:
            # Bestehende Daten laden
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                # Zeile aktualisieren
                idx = df.index[df["Name"] == name][0]
                row_idx = idx + 2  # Header = 1, df index 0-basiert
                # Spalten für Tipps
                tips_columns = ["100mM1", "100mM2", "100mM3", "100mW1", "100mW2", "100mW3"]
                tips_values = [hmme, hmmz, hmmd, hmwe, hmwz, hmwd]
                for i, col_name in enumerate(tips_columns):
                    col_idx = df.columns.get_loc(col_name) + 1  # gspread 1-basiert
                    sheet.update_cell(row_idx, col_idx, tips_values[i])
                st.success(f"{name}, dein Tipp wurde aktualisiert!")
            else:
                # Neuer Eintrag
                sheet.append_row([
                    name,
                    hmme, hmmz, hmmd,   # 100m Männer
                    hmwe, hmwz, hmwd,   # 100m Frauen
                    0                    # Punkte
                ])
                st.success(f"Danke {name}, dein Tipp wurde gespeichert!")

# -------------------------------
# Punkteberechnung & Leaderboard-Update
# -------------------------------
if st.button("Auswerten"):
    import sieger  # Datei mit den Siegern

    # Werte aus den Inputs
    hmm = [hmme, hmmz, hmmd]
    hmw = [hmwe, hmwz, hmwd]
    punkte = 0

    # Punkte 100m Männer
    for i, val in enumerate(hmm):
        if val == sieger.ohmm[i]:
            punkte += 2
        elif val in sieger.ohmm:
            punkte += 1

    # Punkte 100m Frauen
    for i, val in enumerate(hmw):
        if val == sieger.ohmw[i]:
            punkte += 2
        elif val in sieger.ohmw:
            punkte += 1

    st.success(f"{name}, du hast {punkte} Punkte!")

    # -------------------------------
    # Nur die Punkte-Zelle aktualisieren
    # -------------------------------
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and "Name" in df.columns and name in df["Name"].values:
        idx = df.index[df["Name"] == name][0]
        row_idx = idx + 2  # Header = 1
        col_idx = df.columns.get_loc("Punkte") + 1
        sheet.update_cell(row_idx, col_idx, punkte)
    else:
        st.error("Fehler: Name nicht im Sheet gefunden. Bitte zuerst Tipp abgeben.")

# -------------------------------
# Leaderboard anzeigen
# -------------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("🏅 Leaderboard")

if not df.empty and "Punkte" in df.columns:
    df["Punkte"] = pd.to_numeric(df["Punkte"], errors="coerce")
    leaderboard = df[["Name", "Punkte"]]  # nur Name + Punkte
    st.dataframe(leaderboard.sort_values(by="Punkte", ascending=False))
else:
    st.write("Noch keine Einträge im Leaderboard.")



