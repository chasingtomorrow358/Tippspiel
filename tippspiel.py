# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 13:48:31 2025

@author: hoeni_wy8o0xn
"""
import streamlit as st
import sieger

st.title("100m Männer Tippspiel")

# Eingabefelder
a = st.text_input("100m M S:")
b = st.text_input("100m M Z:")
c = st.text_input("100m M D:")

# Eingaben in Liste speichern
hmm = [a, b, c]

punkte = 0

if a and b and c:  # Nur auswerten, wenn alle Felder ausgefüllt
    if hmm[0] == sieger.ohmm[0]:
        punkte += 2
    if hmm[1] == sieger.ohmm[1]:
        punkte += 2
    if hmm[2] == sieger.ohmm[2]:
        punkte += 2
    for name in hmm:
        if name in sieger.ohmm:
            punkte += 1

    st.success(f"Du hast {punkte} Punkte!")




