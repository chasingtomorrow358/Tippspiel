import streamlit as st
import gspread
import pandas as pd
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

st.markdown("### 100m Männer")
hmme = st.text_input("Sieger 100m Männer:")
hmmz = st.text_input("Zweiter 100m Männer:")
hmmd = st.text_input("Dritter 100m Männer:")

st.markdown("### 100m Frauen")
hmwe = st.text_input("Siegerin 100m Frauen:")
hmwz = st.text_input("Zweite 100m Frauen:")
hmwd = st.text_input("Dritte 100m Frauen:")

st.markdown("### 200m Männer")
m200_1 = st.text_input("Sieger 200m Männer:")
m200_2 = st.text_input("Zweiter 200m Männer:")
m200_3 = st.text_input("Dritter 200m Männer:")

st.markdown("### 1500m Männer")
m1500_1 = st.text_input("Sieger 1500m Männer:")
m1500_2 = st.text_input("Zweiter 1500m Männer:")
m1500_3 = st.text_input("Dritter 1500m Männer:")

st.markdown("### 3000m Hindernis Männer")
hind_1 = st.text_input("Sieger Hindernis Männer:")
hind_2 = st.text_input("Zweiter Hindernis Männer:")
hind_3 = st.text_input("Dritter Hindernis Männer:")

st.markdown("### Diskus")
diskus_1 = st.text_input("Sieger Diskus:")
diskus_2 = st.text_input("Zweiter Diskus:")
diskus_3 = st.text_input("Dritter Diskus:")

st.markdown("### Stabhochsprung")
stab_1 = st.text_input("Sieger Stabhochsprung:")
stab_2 = st.text_input("Zweiter Stabhochsprung:")
stab_3 = st.text_input("Dritter Stabhochsprung:")

st.markdown("### Speer")
speer_1 = st.text_input("Sieger Speer:")
speer_2 = st.text_input("Zweiter Speer:")
speer_3 = st.text_input("Dritter Speer:")

st.markdown("### Zehnkampf")
zehn_1 = st.text_input("Sieger Zehnkampf:")
zehn_2 = st.text_input("Zweiter Zehnkampf:")
zehn_3 = st.text_input("Dritter Zehnkampf:")

st.markdown("### 100m Hürden Frauen")
h100w_1 = st.text_input("Siegerin 100m Hürden Frauen:")
h100w_2 = st.text_input("Zweite 100m Hürden Frauen:")
h100w_3 = st.text_input("Dritte 100m Hürden Frauen:")

st.markdown("### 400m Hürden Frauen")
h400w_1 = st.text_input("Siegerin 400m Hürden Frauen:")
h400w_2 = st.text_input("Zweite 400m Hürden Frauen:")
h400w_3 = st.text_input("Dritte 400m Hürden Frauen:")

st.markdown("### 800m Frauen")
f800_1 = st.text_input("Siegerin 800m Frauen:")
f800_2 = st.text_input("Zweite 800m Frauen:")
f800_3 = st.text_input("Dritte 800m Frauen:")

st.markdown("### Weitsprung")
weitsprung_1 = st.text_input("Sieger Weitsprung:")
weitsprung_2 = st.text_input("Zweiter Weitsprung:")
weitsprung_3 = st.text_input("Dritter Weitsprung:")

st.markdown("### Hochsprung")
hoch_1 = st.text_input("Sieger Hochsprung:")
hoch_2 = st.text_input("Zweiter Hochsprung:")
hoch_3 = st.text_input("Dritter Hochsprung:")

st.markdown("### Kugelstoßen")
kugel_1 = st.text_input("Sieger Kugelstoßen:")
kugel_2 = st.text_input("Zweiter Kugelstoßen:")
kugel_3 = st.text_input("Dritter Kugelstoßen:")

st.markdown("### 4x100m Staffel Männer")
staffel100m_1 = st.text_input("Sieger 4x100m Männer:")
staffel100m_2 = st.text_input("Zweiter 4x100m Männer:")
staffel100m_3 = st.text_input("Dritter 4x100m Männer:")

st.markdown("### 4x100m Staffel Frauen")
staffel100w_1 = st.text_input("Sieger 4x100m Frauen:")
staffel100w_2 = st.text_input("Zweite 4x100m Frauen:")
staffel100w_3 = st.text_input("Dritte 4x100m Frauen:")

st.markdown("### 4x400m Staffel Männer")
staffel400m_1 = st.text_input("Sieger 4x400m Männer:")
staffel400m_2 = st.text_input("Zweiter 4x400m Männer:")
staffel400m_3 = st.text_input("Dritter 4x400m Männer:")

st.markdown("### 4x400m Staffel Frauen")
staffel400w_1 = st.text_input("Sieger 4x400m Frauen:")
staffel400w_2 = st.text_input("Zweite 4x400m Frauen:")
staffel400w_3 = st.text_input("Dritte 4x400m Frauen:")


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
                sheet.append_row(sheet.append_row([
    name,
    hmme, hmmz, hmmd,  # 100m Männer
    hmwe, hmwz, hmwd,  # 100m Frauen
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
])
)

            st.success(f"Danke {name}, dein Tipp wurde gespeichert!")







