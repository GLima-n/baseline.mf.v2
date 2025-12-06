import streamlit as st
import base64
import os

def show_welcome_screen():
    """
    Popup de login - sempre aparece quando não há email no session_state
    """
    
    # Processar login do formulário
    if 'popup_name' in st.query_params and 'popup_email' in st.query_params:
        name = st.query_params['popup_name']
        email = st.query_params['popup_email']
        
        if name and email and len(name) >= 3 and '@' in email:
            # Salvar apenas no session_state (temporário)
            st.session_state.user_name = name
            st.session_state.user_email = email
            
            # Limpar params e recarregar
            st.query_params.clear()
            st.rerun()
    
    # Se já tem email no session_state, não mostra popup
    if 'user_email' in st.session_state and st.session_state.user_email:
        return
    
    # Carregar background SVG
    def load_svg_as_base64():
        svg_path = 'Frame (10).svg'
        if os.path.exists(svg_path):
            try:
                with open(svg_path, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            except:
                return ""
        return ""
    
    svg_base64 = load_svg_as_base64()
    bg_style = f"background-image: url('data:image/svg+xml;base64,{svg_base64}');" if svg_base64 else "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"
    
    # CSS e HTML do popup
    popup_html = f"""
    <style>
        /* Esconder conteúdo principal do Streamlit */
        .main > div:not(.block-container) {{
            display: none !important;
        }}
        .block-container {{
            padding: 0 !important;
        }}
        header, .stToolbar, .stDeployButton {{
            display: none !important;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: scale(0.95); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        
        .popup-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            {bg_style}
            background-size: cover;
            background-position: center;
            z-index: 999999;
        }}
        
        .popup-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000000;
            padding: 20px;
        }}
        
        .popup-card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            max-width: 420px;
            width: 100%;
            animation: fadeIn 0.4s ease-out;
        }}
        
        .popup-header {{
            padding: 30px 30px 20px;
            text-align: center;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .popup-header h2 {{
            margin: 0 0 8px 0;
            color: #333;
            font-size: 1.5em;
            font-weight: 600;
        }}
        
        .popup-header p {{
            margin: 0;
            color: #666;
            font-size: 0.95em;
        }}
        
        .popup-body {{
            padding: 30px;
        }}
        
        .input-group {{
            margin-bottom: 18px;
        }}
        
        .popup-input {{
            width: 100%;
            padding: 14px 16px;
            font-size: 1em;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background: #fafafa;
            color: #333;
            outline: none;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}
        
        .popup-input:focus {{
            border-color: #ff8c00;
            background: white;
            box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.1);
        }}
        
        .popup-button {{
            width: 100%;
            padding: 16px;
            font-size: 1.1em;
            font-weight: 600;
            color: white;
            background: linear-gradient(45deg, #ff8c00, #ff6b00);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .popup-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 140, 0, 0.4);
        }}
        
        @media (max-width: 480px) {{
            .popup-card {{
                margin: 20px;
            }}
        }}
    </style>
    
    <div class="popup-overlay"></div>
    <div class="popup-container">
        <div class="popup-card">
            <div class="popup-header">
                <h2>Bem-vindo ao Painel</h2>
                <p>Por favor, preencha seus dados para acessar</p>
            </div>
            <div class="popup-body">
                <form method="get">
                    <div class="input-group">
                        <input type="text" name="popup_name" placeholder="Nome completo" class="popup-input" required minlength="3" />
                    </div>
                    <div class="input-group">
                        <input type="email" name="popup_email" placeholder="Email corporativo" class="popup-input" required />
                    </div>
                    <button type="submit" class="popup-button">Acessar Painel</button>
                </form>
            </div>
        </div>
    </div>
    """
    
    st.markdown(popup_html, unsafe_allow_html=True)
    st.stop()
