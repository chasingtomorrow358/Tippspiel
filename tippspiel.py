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
st.info("Bei Leuten, bei denen der Vorname öfters im Verein vorkommt, bitte noch den Nachnamen oder einen Spitznamen eintragen /n Für das Tippspiel nur die Nachnamen der jeweiligen Personen eintragen! /n Ihr könnt eure Tipps bis 
bis Ende der Deadline jederzeit ändern, müsst aber leider die ganze Eingabe wiederholen /n 🍀 Viel Glück und viel Spaß")

now = datetime.now()
if now >= deadline:
    st.warning("❌ Die Tipp-Abgabe ist vorbei")
else:
    # -------------------------------
    # Benutzereingaben
    # -------------------------------
    name = st.text_input("Dein Name")

    # Disziplinen
    disziplinen = [
        "100m Männer", "100mW", "200mM", "1500mM", "HindernisM",
        "Diskus", "Stab", "Speer", "Zehnkampf", "100mHürdenW",
        "400mHürdenW", "800mW", "Weitsprung", "Hochsprung",
        "Kugel", "Staffel100mM", "Staffel100mW", "Staffel400mM",
        "Staffel400mW"
    ]

    # Tipp-Felder dynamisch erstellen
    tipp_felder = {}
    for d in disziplinen:
        st.markdown(f"### {d}")
        tipp_felder[f"{d}1"] = st.text_input(f"Sieger {d}:")
        tipp_felder[f"{d}2"] = st.text_input(f"Zweiter {d}:")
        tipp_felder[f"{d}3"] = st.text_input(f"Dritter {d}:")

    # Button Tipp abgeben
    if st.button("Tipp abgeben"):
        # Prüfen, ob Name und alle Felder ausgefüllt sind
        if name.strip() == "" or any(f.strip() == "" for f in tipp_felder.values()):
            st.error("Bitte alle Felder ausfüllen!")
        else:
            # Neue Zeile mit allen Tipps + Punkte=0
            neue_zeile = [name] + list(tipp_felder.values()) + [0]

            # Daten aus Google Sheet
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                # Zeile aktualisieren
                idx = df.index[df["Name"] == name][0]
                row_idx = idx + 2  # +2 wegen Header in Sheet
                sheet.update(f"A{row_idx}:BF{row_idx}", [neue_zeile])
            else:
                # Neue Zeile hinzufügen
                sheet.append_row(neue_zeile)

            st.success(f"Danke {name}, dein Tipp wurde gespeichert!")


