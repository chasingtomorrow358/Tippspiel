import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# -------------------------------
# Google Sheets Setup
# -------------------------------
creds_dict = st.secrets["gspread"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["gspread"]["sheet_id"]).sheet1

# -------------------------------
# Abgabeschluss
# -------------------------------
deadline = datetime(2025, 9, 01, 21, 0)
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
            # Prüfen, ob Teilnehmer schon existiert
            data = sheet.get_all_records()
            df = pd.DataFrame(data)

            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                # Zeile aktualisieren
                idx = df.index[df["Name"] == name][0]
                row_idx = idx + 2
                sheet.update_cell(row_idx, df.columns.get_loc("100mM1")+1, hmme)
                sheet.update_cell(row_idx, df.columns.get_loc("100mM2")+1, hmmz)
                sheet.update_cell(row_idx, df.columns.get_loc("100mM3")+1, hmmd)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW1")+1, hmwe)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW2")+1, hmwz)
                sheet.update_cell(row_idx, df.columns.get_loc("100mW3")+1, hmwd)
            else:
                # Neue Zeile
                sheet.append_row([name, hmme, hmmz, hmmd, hmwe, hmwz, hmwd, 0])

            st.success(f"Danke {name}, dein Tipp wurde gespeichert!")


