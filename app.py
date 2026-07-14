import streamlit as st
import pandas as pd

# Ustawienia strony dla urządzeń mobilnych
st.set_page_config(
    page_title="MaksStandard",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLIZACJA I ANIMOWANE TŁO (Szybki deszcz jedzenia + własna ikona iOS) ---
st.markdown("""
<head>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="MaksStandard">
    <link rel="apple-touch-icon" href="https://img.icons8.com/emoji/192/hamburger-emoji.png">
    <link rel="apple-touch-icon" sizes="152x152" href="https://img.icons8.com/emoji/152/hamburger-emoji.png">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.icons8.com/emoji/180/hamburger-emoji.png">
    <link rel="icon" type="image/png" href="https://img.icons8.com/emoji/192/hamburger-emoji.png">
</head>
<style>
    /* Tło aplikacji */
    .stApp {
        background: linear-gradient(135deg, #1e1e24 0%, #2a2a35 100%);
        color: #ffffff;
        overflow: hidden;
    }
    
    /* Animacja deszczu jedzenia */
    @keyframes foodRain {
        0% { transform: translateY(-20vh) rotate(0deg); opacity: 0; }
        5% { opacity: 0.8; }
        90% { opacity: 0.8; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }
    
    .food-particle {
        position: fixed;
        top: -15%;
        font-size: 26px;
        user-select: none;
        pointer-events: none;
        animation: foodRain 9s linear infinite;
        animation-fill-mode: backwards;
        z-index: 0;
    }
    
    /* Nagłówek aplikacji */
    .main-title {
        text-align: center;
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto;
        font-weight: 800;
        font-size: 32px;
        margin-bottom: 30px;
        color: #ff9f43;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
</style>

<div class="food-particle" style="left: 5%; animation-delay: 0s; animation-duration: 7s;">🍔</div>
<div class="food-particle" style="left: 15%; animation-delay: 1.2s; animation-duration: 9s;">🍽️</div>
<div class="food-particle" style="left: 25%; animation-delay: 0.2s; animation-duration: 10s;">🍣</div>
<div class="food-particle" style="left: 35%; animation-delay: 2.5s; animation-duration: 8s;">🥤</div>
<div class="food-particle" style="left: 45%; animation-delay: 0s; animation-duration: 9s;">🥪</div>
<div class="food-particle" style="left: 55%; animation-delay: 1.8s; animation-duration: 11s;">🍴</div>
<div class="food-particle" style="left: 65%; animation-delay: 0.5s; animation-duration: 9s;">🍔</div>
<div class="food-particle" style="left: 75%; animation-delay: 3s; animation-duration: 7s;">🍽️</div>
<div class="food-particle" style="left: 85%; animation-delay: 0.1s; animation-duration: 10s;">🍣</div>
<div class="food-particle" style="left: 95%; animation-delay: 1.5s; animation-duration: 8s;">🥤</div>
""", unsafe_allow_html=True)

# --- TYTUŁ GŁÓWNY ---
st.markdown('<div class="main-title">MaksStandard</div>', unsafe_allow_html=True)

# --- LINK DO TWOJEGO ARKUSZA GOOGLE ---
LINK_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQM0vjCm1BiSiMejP38yW62cFTH7YpnIQDlXI3Tt3Ip0yJ5yF2scsH4kFpCkMSPXIqvLZogwT7uQFry/pub?gid=0&single=true&output=csv"

# --- STAN APLIKACJI (Session State dla nawigacji) ---
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Główne"

# Funkcja powrotu
def go_back():
    st.session_state.current_menu = "Główne"
    st.rerun()

# --- MENU GŁÓWNE ---
if st.session_state.current_menu == "Główne":
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛠️\n\nPracownia", use_container_width=True):
            st.session_state.current_menu = "Pracownia"
            st.rerun()
            
        if st.button("🍳\n\nKuchnia", use_container_width=True):
            st.session_state.current_menu = "Kuchnia"
            st.rerun()
            
    with col2:
        if st.button("📦\n\nMagazyn", use_container_width=True):
            st.session_state.current_menu = "Magazyn"
            st.rerun()
            
        if st.button("👔\n\nZarząd", use_container_width=True):
            st.session_state.current_menu = "Zarząd"
            st.rerun()

# --- PODMENU: PRACOWNIA (Pobiera dane z Excela w czasie rzeczywistym) ---
elif st.session_state.current_menu == "Pracownia":
    st.subheader("🛠️ Pracownia – Standardy Dań")
    if st.button("⬅️ Powrót", on_click=go_back): pass
    
    st.write("Wybierz danie z listy, aby zobaczyć standard i recepturę:")
    
    try:
        # Pobieranie danych z obsługą średników (sep=None automatycznie wykrywa przecinek lub średnik)
        df = pd.read_csv(LINK_CSV, sep=None, engine='python')
        
        # Oczyszczenie nazw kolumn ze spacji i wielkości liter
        df.columns = df.columns.str.strip()
        
        # Sprawdzamy czy kolumny istnieją pod różnymi nazwami (z polskimi znakami lub bez)
        col_danie = [c for c in df.columns if c.lower() in ['danie', 'nazwa']][0]
        col_skladniki = [c for c in df.columns if c.lower() in ['skladniki', 'składniki', 'receptura']][0]
        
        # Tworzenie przycisku dla każdego dania z tabeli
        for index, row in df.iterrows():
            danie_nazwa = row[col_danie]
            skladniki_tekst = row[col_skladniki]
            
            # Jeśli wiersz jest pusty, pomiń go
            if pd.isna(danie_nazwa) or pd.isna(skladniki_tekst):
                continue
                
            with st.expander(f"🍔 {danie_nazwa}"):
                st.markdown("**Składniki i standard przygotowania:**")
                # Rozdzielenie składników po przecinku lub średniku
                if ";" in str(skladniki_tekst):
                    skladniki_list = str(skladniki_tekst).split(";")
                else:
                    skladniki_list = str(skladniki_tekst).split(",")
                    
                for item in skladniki_list:
                    if item.strip():
                        st.write(f"- {item.strip()}")
                    
    except Exception as e:
        st.error("Nie udało się pobrać danych z Arkusza Google.")
        st.info(f"Szczegóły błędu: {e}")

# --- PODMENU: KUCHNIA (Hasło: 0000) ---
elif st.session_state.current_menu == "Kuchnia":
    st.subheader("🍳 Kuchnia – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    
    if pin == "0000":
        st.success("Dostęp przyznany!")
        st.button("Dodatkowe menu Kuchni 1")
        st.button("Dodatkowe menu Kuchni 2")
    elif pin != "":
        st.error("Błędny kod PIN!")
        
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: MAGAZYN (Hasło: 1111) ---
elif st.session_state.current_menu == "Magazyn":
    st.subheader("📦 Magazyn – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    
    if pin == "1111":
        st.success("Dostęp przyznany!")
        st.button("Dodatkowe menu Magazynu 1")
    elif pin != "":
        st.error("Błędny kod PIN!")
        
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: ZARZĄD (Hasło: 2222) ---
elif st.session_state.current_menu == "Zarząd":
    st.subheader("👔 Zarząd – Strefa Ściśle Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    
    if pin == "2222":
        st.success("Dostęp przyznany!")
        st.button("Statystyki finansowe")
        st.button("Zarządzanie użytkownikami")
    elif pin != "":
        st.error("Błędny kod PIN!")
        
    if st.button("⬅️ Powrót", on_click=go_back): pass
