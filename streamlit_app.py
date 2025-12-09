"""
PapercraftTools - Multi-Tool Web App
Zestaw narzędzi do obróbki obrazów dla papercraft
"""

import streamlit as st
from PIL import Image
import numpy as np
import io

# ============================================================================
# FUNKCJE POMOCNICZE
# ============================================================================

def reduce_to_2_colors(img, threshold=128):
    """Redukuje obraz do 2 kolorów (czarny i biały)"""
    if img.mode != 'L':
        img = img.convert('L')
    
    img_array = np.array(img)
    binary = (img_array > threshold).astype(np.uint8) * 255
    
    return Image.fromarray(binary, mode='L')

def remove_white_to_transparent(img):
    """Zamienia biały kolor na przezroczystość"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    data = np.array(img)
    white_mask = (data[:,:,0] > 250) & (data[:,:,1] > 250) & (data[:,:,2] > 250)
    data[white_mask] = [255, 255, 255, 0]
    
    return Image.fromarray(data, mode='RGBA')

def flatten_to_white_background(img):
    """Spłaszcza obraz na białe tło (dla PBM)"""
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    return img

def convert_image_to_bytes(img, format='PNG'):
    """Konwertuje obraz do bytes do pobrania"""
    buf = io.BytesIO()
    
    if format == 'PBM':
        img_flat = flatten_to_white_background(img)
        img_bw = img_flat.convert('L').convert('1')
        img_bw.save(buf, format='PPM')
    else:  # PNG
        img.save(buf, format='PNG')
    
    buf.seek(0)
    return buf.getvalue()

# ============================================================================
# KONFIGURACJA STRONY
# ============================================================================

st.set_page_config(
    page_title="PapercraftTools",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
    <h1 style='color: white; margin: 0; font-size: 42px;'>🛠️ PapercraftTools</h1>
    <p style='color: #f0f0f0; margin: 10px 0 0 0; font-size: 18px;'>
        Darmowe narzędzia do obróbki obrazów dla papercraft
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - NAWIGACJA
# ============================================================================

with st.sidebar:
    st.markdown("### 🧭 Narzędzia")
    
    tool = st.radio(
        "Wybierz narzędzie:",
        options=[
            "🏠 Strona główna",
            "✂️ Czyszczenie i wycinanie",
            "🎨 Wektoryzacja (wkrótce)",
            "📐 Zmiana rozmiaru (wkrótce)",
            "🔄 Batch processing (wkrótce)"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Mini info
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; font-size: 14px;'>
        <strong>💡 Tip:</strong><br>
        Wszystkie narzędzia działają lokalnie w Twojej przeglądarce - Twoje pliki są bezpieczne!
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# STRONA GŁÓWNA
# ============================================================================

if tool == "🏠 Strona główna":
    st.markdown("## 👋 Witaj w PapercraftTools!")
    
    st.markdown("""
    Ta aplikacja oferuje **darmowe narzędzia** do przetwarzania obrazów, 
    stworzone specjalnie z myślą o projektach papercraft.
    """)
    
    st.divider()
    
    # Karty z narzędziami
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 25px; background-color: #f8f9fa; border-radius: 15px; 
                    border-left: 5px solid #667eea; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #667eea;'>✂️ Czyszczenie i wycinanie</h3>
            <p style='color: #666; line-height: 1.6;'>
                • Redukcja kolorów do czarno-białego<br>
                • Usuwanie białego tła<br>
                • Wycinanie fragmentów obrazu<br>
                • Export do PNG lub PBM
            </p>
            <span style='background-color: #4ade80; color: white; padding: 5px 12px; 
                         border-radius: 20px; font-size: 12px; font-weight: bold;'>
                ✓ DOSTĘPNE
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 25px; background-color: #f8f9fa; border-radius: 15px; 
                    border-left: 5px solid #fbbf24; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #fbbf24;'>🎨 Wektoryzacja</h3>
            <p style='color: #666; line-height: 1.6;'>
                • Konwersja obrazu rastrowego na wektor<br>
                • Export do SVG<br>
                • Regulacja dokładności<br>
                • Podgląd na żywo
            </p>
            <span style='background-color: #fbbf24; color: white; padding: 5px 12px; 
                         border-radius: 20px; font-size: 12px; font-weight: bold;'>
                🚧 WKRÓTCE
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style='padding: 25px; background-color: #f8f9fa; border-radius: 15px; 
                    border-left: 5px solid #a78bfa; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #a78bfa;'>📐 Zmiana rozmiaru</h3>
            <p style='color: #666; line-height: 1.6;'>
                • Skalowanie z zachowaniem proporcji<br>
                • Zmiana DPI<br>
                • Batch processing wielu plików<br>
                • Predefiniowane rozmiary
            </p>
            <span style='background-color: #6b7280; color: white; padding: 5px 12px; 
                         border-radius: 20px; font-size: 12px; font-weight: bold;'>
                📅 PLANOWANE
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='padding: 25px; background-color: #f8f9fa; border-radius: 15px; 
                    border-left: 5px solid #f472b6; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #f472b6;'>🔄 Batch processing</h3>
            <p style='color: #666; line-height: 1.6;'>
                • Przetwarzanie wielu plików naraz<br>
                • Automatyczne nazewnictwo<br>
                • Zapis do ZIP<br>
                • Podgląd wszystkich
            </p>
            <span style='background-color: #6b7280; color: white; padding: 5px 12px; 
                         border-radius: 20px; font-size: 12px; font-weight: bold;'>
                📅 PLANOWANE
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # FAQ
    st.markdown("### ❓ Często zadawane pytania")
    
    with st.expander("💰 Czy to naprawdę darmowe?"):
        st.markdown("""
        Tak! Wszystkie narzędzia są **całkowicie darmowe**. 
        Jeśli chcesz wesprzeć rozwój projektu, możesz to zrobić dobrowolnie 
        przez sekcję wsparcia na dole strony.
        """)
    
    with st.expander("🔒 Czy moje pliki są bezpieczne?"):
        st.markdown("""
        **Absolutnie!** Wszystkie operacje wykonywane są lokalnie w Twojej przeglądarce. 
        Pliki **nie są wysyłane** na żaden serwer. Pozostają tylko u Ciebie.
        """)
    
    with st.expander("🐛 Znalazłem błąd, jak zgłosić?"):
        st.markdown("""
        Jeśli znajdziesz błąd lub masz sugestię, możesz:
        - Skontaktować się przez formularz kontaktowy
        - Napisać na e-mail: twoj-email@example.com
        """)

# ============================================================================
# NARZĘDZIE 1: CZYSZCZENIE I WYCINANIE
# ============================================================================

elif tool == "✂️ Czyszczenie i wycinanie":
    st.markdown("## ✂️ Czyszczenie i wycinanie obrazu")
    st.markdown("Usuń tło, zredukuj kolory i wytnij potrzebny fragment")
    
    st.divider()
    
    # Upload
    uploaded_file = st.file_uploader(
        "📁 Wgraj obraz",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Obsługiwane formaty: PNG, JPG, BMP"
    )
    
    if uploaded_file is not None:
        original_img = Image.open(uploaded_file)
        
        # Parametry
        with st.expander("⚙️ Ustawienia", expanded=True):
            col_set1, col_set2 = st.columns(2)
            
            with col_set1:
                threshold = st.slider(
                    "Próg binaryzacji (0-255)",
                    min_value=0,
                    max_value=255,
                    value=128,
                    help="Wyższy = więcej białego, Niższy = więcej czarnego"
                )
            
            with col_set2:
                output_format = st.radio(
                    "Format wyjściowy",
                    options=["PNG", "PBM"],
                    horizontal=True,
                    help="PNG - z przezroczystością, PBM - do wektoryzacji"
                )
        
        # Przetwarzanie
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📥 Oryginał")
            st.image(original_img, use_container_width=True)
            st.caption(f"📏 {original_img.width} x {original_img.height} px")
        
        with col2:
            st.markdown("### ✨ Po obróbce")
            
            with st.spinner("Przetwarzam..."):
                # Redukcja kolorów
                processed_img = reduce_to_2_colors(original_img, threshold=threshold)
                # Usunięcie białego tła
                processed_img = remove_white_to_transparent(processed_img)
            
            st.image(processed_img, use_container_width=True)
            st.caption(f"✅ {processed_img.width} x {processed_img.height} px")
        
        # Opcjonalne wycinanie
        st.divider()
        
        enable_crop = st.checkbox("✂️ Wytnij fragment obrazu", value=False)
        
        if enable_crop:
            st.info("💡 Wpisz współrzędne prostokąta do wycięcia")
            
            col_x1, col_y1, col_x2, col_y2 = st.columns(4)
            
            with col_x1:
                x1 = st.number_input("X1 (lewy)", min_value=0, max_value=processed_img.width, value=0)
            with col_y1:
                y1 = st.number_input("Y1 (górny)", min_value=0, max_value=processed_img.height, value=0)
            with col_x2:
                x2 = st.number_input("X2 (prawy)", min_value=0, max_value=processed_img.width, value=processed_img.width)
            with col_y2:
                y2 = st.number_input("Y2 (dolny)", min_value=0, max_value=processed_img.height, value=processed_img.height)
            
            if x2 > x1 and y2 > y1:
                cropped_img = processed_img.crop((x1, y1, x2, y2))
                st.image(cropped_img, caption=f"Przycięty: {cropped_img.width} x {cropped_img.height} px", width=400)
                processed_img = cropped_img  # Użyj przyciętego do pobrania
            else:
                st.error("❌ Nieprawidłowe współrzędne!")
        
        # Pobieranie
        st.divider()
        st.markdown("### 💾 Pobierz wynik")
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            output_bytes = convert_image_to_bytes(processed_img, format=output_format)
            file_extension = '.png' if output_format == 'PNG' else '.pbm'
            file_name = uploaded_file.name.rsplit('.', 1)[0] + f'_processed{file_extension}'
            
            st.download_button(
                label=f"⬇️ Pobierz {output_format}",
                data=output_bytes,
                file_name=file_name,
                mime=f"image/{output_format.lower()}",
                use_container_width=True,
                type="primary"
            )
        
        with col_download2:
            # Zawsze oferuj też drugi format
            alt_format = "PBM" if output_format == "PNG" else "PNG"
            alt_bytes = convert_image_to_bytes(processed_img, format=alt_format)
            alt_extension = '.pbm' if alt_format == 'PBM' else '.png'
            alt_name = uploaded_file.name.rsplit('.', 1)[0] + f'_processed{alt_extension}'
            
            st.download_button(
                label=f"⬇️ Pobierz {alt_format}",
                data=alt_bytes,
                file_name=alt_name,
                mime=f"image/{alt_format.lower()}",
                use_container_width=True
            )
    
    else:
        st.info("👆 Wgraj obraz powyżej, aby rozpocząć")

# ============================================================================
# NARZĘDZIE 2: WEKTORYZACJA (PLACEHOLDER)
# ============================================================================

elif tool == "🎨 Wektoryzacja (wkrótce)":
    st.markdown("## 🎨 Wektoryzacja obrazu")
    
    st.info("""
    ### 🚧 To narzędzie jest w przygotowaniu!
    
    **Planowane funkcje:**
    - Konwersja z PNG/JPG do SVG
    - Regulacja poziomu detali
    - Wybór metody wektoryzacji
    - Podgląd na żywo
    - Export do różnych formatów wektorowych
    
    **Przewidywana data uruchomienia:** Wkrótce!
    """)
    
    st.markdown("---")
    st.markdown("💡 **Chcesz być powiadomiony o uruchomieniu?** Obserwuj tę stronę!")

# ============================================================================
# INNE NARZĘDZIA (PLACEHOLDERS)
# ============================================================================

else:
    st.markdown(f"## {tool}")
    
    st.info("""
    ### 🚧 To narzędzie jest w przygotowaniu!
    
    Wkrótce pojawi się tutaj nowa funkcjonalność. 
    
    Śledź aktualizacje i bądź na bieżąco z nowymi narzędziami!
    """)

# ============================================================================
# SEKCJA WSPARCIA (zawsze na dole)
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

# Wyśrodkowana sekcja wsparcia
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);'>
        <h3 style='color: white; margin-bottom: 10px; font-size: 24px;'>☕ Podobają Ci się darmowe narzędzia?</h3>
        <p style='color: #f0f0f0; margin-bottom: 0; font-size: 16px;'>
            Jeśli to co tutaj znajdujesz jest dla Ciebie pomocne, możesz wesprzeć rozwój projektu.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Przycisk Crypto
    if st.button("🪙 **Wesprzyj Crypto**", use_container_width=True, type="primary"):
        st.session_state.show_crypto = True
    
    # Modal z crypto
    if 'show_crypto' in st.session_state and st.session_state.show_crypto:
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
                    border-left: 4px solid #667eea; margin-top: 15px;'>
            <h4 style='margin-top: 0; color: #667eea;'>🪙 Adresy Kryptowalut</h4>
        </div>
        """, unsafe_allow_html=True)
        
        crypto_col1, crypto_col2 = st.columns(2)
        
        with crypto_col1:
            st.markdown("**Bitcoin (BTC):**")
            st.code("bc1qvw7zl88s9a88cydqxzxxfcyqapsv5ks3yk689z", language="text")
            
            st.markdown("**Ethereum (ETH):**")
            st.code("0x6B084eF6E8389Ba8013087cfFE1ed96c7eE41E9F", language="text")
        
        with crypto_col2:
            st.markdown("**USDC (ERC20):**")
            st.code("0x6B084eF6E8389Ba8013087cfFE1ed96c7eE41E9F", language="text")
            
            st.markdown("**💡 Tip:**")
            st.info("Każda kwota pomaga w rozwoju darmowych narzędzi!")
        
        if st.button("✖️ Zamknij", use_container_width=True):
            st.session_state.show_crypto = False
            st.rerun()

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px; margin-top: 40px;'>
    Made with ❤️ | PapercraftTools © 2024
</div>
""", unsafe_allow_html=True)
