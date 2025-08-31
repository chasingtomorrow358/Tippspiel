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

            # Prüfen, ob Name bereits existiert
            if not df.empty and "Name" in df.columns and name in df["Name"].values:
                idx = df.index[df["Name"] == name][0]
                df.at[idx, "100mM1"] = hmme
                df.at[idx, "100mM2"] = hmmz
                df.at[idx, "100mM3"] = hmmd
                df.at[idx, "100mW1"] = hmwe
                df.at[idx, "100mW2"] = hmwz
                df.at[idx, "100mW3"] = hmwd
                # Punkte bleiben unverändert
                values = df.where(pd.notnull(df), None)
                sheet.clear()
                sheet.update([values.columns.values.tolist()] + values.values.tolist())
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
    import sieger  # deine Datei mit den Siegern

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

    # Leaderboard aktualisieren
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and "Name" in df.columns and name in df["Name"].values:
        idx = df.index[df["Name"] == name][0]
        df.at[idx, "Punkte"] = punkte
        values = df.where(pd.notnull(df), None)
        sheet.clear()
        sheet.update([values.columns.values.tolist()] + values.values.tolist())
    else:
        sheet.append_row([
            name,
            hmme, hmmz, hmmd,
            hmwe, hmwz, hmwd,
            punkte
        ])

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











