"""
🧹 Cleaning Tool - Redukcja kolorów i usuwanie tła
Wersja web (Streamlit) bazowana na image_processor_gui.py
"""

import streamlit as st
from PIL import Image
import numpy as np
import io

# ============================================================================
# FUNKCJE CORE
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

def process_image(img, threshold=128):
    """Pełny proces: redukcja kolorów + usunięcie tła"""
    # Krok 1: Redukcja do 2 kolorów
    img = reduce_to_2_colors(img, threshold=threshold)
    
    # Krok 2: Biały -> przezroczysty
    img = remove_white_to_transparent(img)
    
    return img

def convert_image_to_bytes(img):
    """Konwertuje obraz do bytes do pobrania"""
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()

# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(
    page_title="Cleaning Tool",
    page_icon="🧹",
    layout="wide"
)

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='color: white; margin: 0;'>🧹 Cleaning Tool</h1>
    <p style='color: #f0f0f0; margin: 10px 0 0 0;'>
        Redukcja kolorów + Usuwanie tła
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - instrukcje
with st.sidebar:
    st.header("📖 Jak używać?")
    
    st.markdown("""
    ### Krok 1: Upload
    Wgraj obraz (JPG, PNG)
    
    ### Krok 2: Reguluj threshold
    - **Wyższy (180+)** = więcej białego
    - **Średni (128)** = balans
    - **Niższy (80-)** = więcej czarnego
    
    ### Krok 3: Pobierz
    Zapisz PNG z przezroczystym tłem
    
    ---
    
    ### 💡 Wskazówki
    
    **Dla napisów/logo:**
    - Threshold 150-180
    - Ostry kontrast
    
    **Dla rysunków:**
    - Threshold 100-130
    - Więcej detali
    
    **Dla skanów:**
    - Threshold 160-200
    - Usuwa szare tło
    """)
    
    st.divider()
    
    st.markdown("""
    ### 🎯 Co robi narzędzie?
    
    1. **Redukcja kolorów**  
       Obraz → 2 kolory (czarny/biały)
    
    2. **Usuwanie tła**  
       Biały → Przezroczysty
    
    3. **Export PNG**  
       Gotowy do użycia!
    """)

# Main area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload obrazu")
    
    uploaded_file = st.file_uploader(
        "Wybierz plik (JPG, PNG)",
        type=['jpg', 'jpeg', 'png'],
        help="Maksymalnie 200MB"
    )
    
    if uploaded_file:
        # Wczytaj obraz
        original_img = Image.open(uploaded_file)
        
        st.success(f"✅ Wczytano: {uploaded_file.name}")
        st.info(f"📐 Wymiary: {original_img.size[0]} x {original_img.size[1]} px")
        
        # Pokaż oryginał
        st.markdown("**Oryginał:**")
        st.image(original_img, use_container_width=True)

with col2:
    if uploaded_file:
        st.subheader("⚙️ Parametry")
        
        # Threshold slider
        threshold = st.slider(
            "Próg binaryzacji (0-255)",
            min_value=0,
            max_value=255,
            value=128,
            step=5,
            help="Wyższy = więcej białego, Niższy = więcej czarnego"
        )
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: #f0f2f6; 
                    border-radius: 5px; margin-bottom: 20px;'>
            <strong>Aktualna wartość:</strong> {threshold}
        </div>
        """, unsafe_allow_html=True)
        
        # Process button
        if st.button("🚀 Przetwórz obraz", type="primary", use_container_width=True):
            with st.spinner("Przetwarzam..."):
                # Process
                processed_img = process_image(original_img.copy(), threshold=threshold)
                
                # Save to session state
                st.session_state.processed_img = processed_img
                st.session_state.original_filename = uploaded_file.name
            
            st.success("✅ Gotowe!")
        
        # Show processed if exists
        if 'processed_img' in st.session_state:
            st.markdown("**Po obróbce:**")
            
            # Display with checkered background (żeby pokazać przezroczystość)
            st.image(st.session_state.processed_img, use_container_width=True)
            
            # Download button
            st.divider()
            
            processed_bytes = convert_image_to_bytes(st.session_state.processed_img)
            
            # Generate filename
            original_name = st.session_state.original_filename
            new_filename = original_name.rsplit('.', 1)[0] + '_cleaned.png'
            
            st.download_button(
                label="💾 Pobierz PNG",
                data=processed_bytes,
                file_name=new_filename,
                mime="image/png",
                use_container_width=True
            )
            
            st.success(f"📁 Nazwa pliku: {new_filename}")

# Info section
if not uploaded_file:
    st.info("👈 Zacznij od wgrania obrazu po lewej stronie")
    
    # Example section
    st.markdown("---")
    st.subheader("📸 Przykłady użycia")
    
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    
    with ex_col1:
        st.markdown("""
        **Napisy/Logo**
        - Ostre kontury
        - Czytelny tekst
        - Threshold: 150-180
        """)
    
    with ex_col2:
        st.markdown("""
        **Rysunki**
        - Zachowanie detali
        - Linie i kształty
        - Threshold: 100-130
        """)
    
    with ex_col3:
        st.markdown("""
        **Skany**
        - Usuwanie szarego tła
        - Czysty wynik
        - Threshold: 160-200
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px;'>
    <strong>💡 Potrzebujesz pomocy?</strong><br>
    Jeśli masz pytania lub sugestie, daj znać!
</div>
""", unsafe_allow_html=True)
