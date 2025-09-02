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
    # Prüfen, ob alle Felder ausgefüllt sind
    required_fields = [
        hmme, hmmz, hmmd, hmwe, hmwz, hmwd,
        m200_1, m200_2, m200_3,
        m1500_1, m1500_2, m1500_3,
        hind_1, hind_2, hind_3,
        diskus_1, diskus_2, diskus_3,
        stab_1, stab_2, stab_3,
        speer_1, speer_2, speer_3,
        zehn_1, zehn_2, zehn_3,
        h100w_1, h100w_2, h100w_3,
        h400w_1, h400w_2, h400w_3,
        f800_1, f800_2, f800_3,
        weitsprung_1, weitsprung_2, weitsprung_3,
        hoch_1, hoch_2, hoch_3,
        kugel_1, kugel_2, kugel_3,
        staffel100m_1, staffel100m_2, staffel100m_3,
        staffel100w_1, staffel100w_2, staffel100w_3,
        staffel400m_1, staffel400m_2, staffel400m_3,
        staffel400w_1, staffel400w_2, staffel400w_3
    ]

    if any(f.strip() == "" for f in required_fields):
        st.error("Bitte alle Felder ausfüllen!")
    else:
        # Alle Tipps in einer Liste zusammenfassen
        neue_zeile = [
            name,
            hmme, hmmz, hmmd,
            hmwe, hmwz, hmwd,
            m200_1, m200_2, m200_3,
            m1500_1, m1500_2, m1500_3,
            hind_1, hind_2, hind_3,
            diskus_1, diskus_2, diskus_3,
            stab_1, stab_2, stab_3,
            speer_1, speer_2, speer_3,
            zehn_1, zehn_2, zehn_3,
            h100w_1, h100w_2, h100w_3,
            h400w_1, h400w_2, h400w_3,
            f800_1, f800_2, f800_3,
            weitsprung_1, weitsprung_2, weitsprung_3,
            hoch_1, hoch_2, hoch_3,
            kugel_1, kugel_2, kugel_3,
            staffel100m_1, staffel100m_2, staffel100m_3,
            staffel100w_1, staffel100w_2, staffel100w_3,
            staffel400m_1, staffel400m_2, staffel400m_3,
            staffel400w_1, staffel400w_2, staffel400w_3,
            0  # Punkte
        ]

        # Prüfen, ob Teilnehmer schon existiert
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if not df.empty and "Name" in df.columns and name in df["Name"].values:
            # Zeile aktualisieren
            idx = df.index[df["Name"] == name][0]
            row_idx = idx + 2
            sheet.update(f"A{row_idx}:BF{row_idx}", [neue_zeile])
        else:
            # Neue Zeile hinzufügen
            sheet.append_row(neue_zeile)

        st.success(f"Danke {name}, dein Tipp wurde gespeichert!")

