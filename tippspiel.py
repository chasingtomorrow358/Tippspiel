import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# -------------------------------
# Google Sheets Setup
# -------------------------------
creds_dict = st.secrets["gspread"]
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["gspread"]["sheet_id"]).sheet1

# -------------------------------
# Abgabeschluss
# -------------------------------
deadline = datetime(2025, 9, 12, 23, 59)
st.title("🏆 VFV Spandau Tippspiel - Tipps abgeben")
st.info(f"⏰ Tipps können bis **{deadline.strftime('%d.%m.%Y %H:%M')}** eingereicht werden.")

now = datetime.now()
if now >= deadline:
    st.warning("Die Tipp-Abgabe ist vorbei. Dieses Skript ist nur für die Eingabe vor Deadline.")
else:
    # -------------------------------
    # Benutzereingaben
    # -------------------------------
    name = st.text_input("Dein Name")

    # Disziplinen (nur Tippfelder)
    disziplinen = [
        "100mM", "100mW", "200mM", "1500mM", "HindernisM",
        "Diskus", "Stab", "Speer", "Zehnkampf", "100mHürdenW",
        "400mHürdenW", "800mW", "Weitsprung", "Hochsprung",
        "Kugel", "Staffel100mM", "Staffel100mW", "Staffel400mM",
        "Staffel400mW"
    ]

    tipp_felder = {}
    for d in disziplinen:
        st.markdown(f"### {d}")
        tipp_felder[f"{d}1"] = st.text_input(f"Sieger {d}:")
        tipp_felder[f"{d}2"] = st.text_input(f"Zweiter {d}:")
        tipp_felder[f"{d}3"] = st.text_input(f"Dritter {d}:")

    if st.button("Tipp abgeben"):
        # Alle Felder prüfen
        if name.strip() == "" or any(v.strip() == "" for v in tipp_felder.values()):
            st.error("Bitte alle Felder ausfüllen!")
        else:
            # Google Sheet auslesen
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            # Prüfen, ob Teilnehmer schon existiert
            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                idx = df.index[df["Name"] == name][0]
                row_idx = idx + 2  # Sheet-Zeilen beginnen bei 1 und Kopfzeile bei 1
                for col, val in tipp_felder.items():
                    col_idx = df.columns.get_loc(col) + 1
                    sheet.update_cell(row_idx, col_idx, val)
            else:
                # Neue Zeile erstellen
                neue_zeile = [name] + list(tipp_felder.values()) + [0]  # Punkte = 0
                sheet.append_row(neue_zeile)

            st.success(f"Danke {name}, dein Tipp wurde gespeichert!")
