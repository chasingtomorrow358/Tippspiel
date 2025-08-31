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
deadline = datetime(2025, 8, 31, 22, 30)
st.title("🏆 VFV Spandau: Das große Tippspiel")
st.info(f"⏰ Tipps können bis **{deadline.strftime('%d.%m.%Y %H:%M')}** eingereicht werden.")

# Aktuelles Datum
now = datetime.now()

# -------------------------------
# AUSWERTUNG MODUS (nach Deadline)
# -------------------------------
if now >= deadline:
    st.subheader("Auswertung nach Ablauf der Deadline")
    import sieger  # Datei mit den Siegern

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and "Name" in df.columns:
        for idx, row in df.iterrows():
            hmm = [row["100mM1"], row["100mM2"], row["100mM3"]]
            hmw = [row["100mW1"], row["100mW2"], row["100mW3"]]
            punkte = 0

            # Punkteberechnung 100m Männer
            for i, val in enumerate(hmm):
                if val == sieger.ohmm[i]:
                    punkte += 2
                elif val in sieger.ohmm:
                    punkte += 1

            # Punkteberechnung 100m Frauen
            for i, val in enumerate(hmw):
                if val == sieger.ohmw[i]:
                    punkte += 2
                elif val in sieger.ohmw:
                    punkte += 1

            # Punkte in Sheet aktualisieren
            row_idx = idx + 2  # Header = 1
            col_idx = df.columns.get_loc("Punkte") + 1
            sheet.update_cell(row_idx, col_idx, punkte)

        st.success("✅ Alle Tipps wurden ausgewertet!")

        # Leaderboard anzeigen
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df["Punkte"] = pd.to_numeric(df["Punkte"], errors="coerce")
        leaderboard = df[["Name", "Punkte"]].sort_values(by="Punkte", ascending=False)
        st.subheader("🏅 Leaderboard")
        st.dataframe(leaderboard)
    else:
        st.write("Noch keine Tipps vorhanden.")

# -------------------------------
# TIP-ABGABE MODUS (vor Deadline)
# -------------------------------
else:
    st.subheader("Tipps abgeben")
    name = st.text_input("Dein Name")

    st.markdown("### 100m Männer")
    hmme = st.text_input("Sieger:")
    hmmz = st.text_input("Zweiter:")
    hmmd = st.text_input("Dritter:")

    st.markdown("### 100m Frauen")
    hmwe = st.text_input("Siegerin:")
    hmwz = st.text_input("Zweite:")
    hmwd = st.text_input("Dritte:")

    if st.button("Tipp abgeben"):
        if name.strip() == "" or hmme.strip() == "" or hmmz.strip() == "" or hmmd.strip() == "" \
           or hmwe.strip() == "" or hmwz.strip() == "" or hmwd.strip() == "":
            st.error("Bitte alle Felder ausfüllen!")
        else:
            # Daten aus Sheet holen
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                # Bestehende Zeile aktualisieren
                idx = df.index[df["Name"] == name][0]
                row_idx = idx + 2  # Header = 1
                sheet.update_cell(row_idx, df.columns.get_loc("100mM1")+1, hmme)
                sheet.update_cell(row_idx, df.columns.get_loc("100mM2")+1, hmmz)
                sheet.update_cell(row_idx, df.columns.get_loc("100mM3")+1, hmmd)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW1")+1, hmwe)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW2")+1, hmwz)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW3")+1, hmwd)
            else:
                # Neue Zeile anfügen
                sheet.append_row([name, hmme, hmmz, hmmd, hmwe, hmwz, hmwd, 0])  # Punkte=0 als Platzhalter

            st.success(f"Danke {name}, dein Tipp wurde gespeichert!")



