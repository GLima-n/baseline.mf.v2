import streamlit as st
import base64
import os
from datetime import datetime

def show_welcome_screen():
    """
    Popup de login - pede nome e email do usuário
    """
    
    # Processar login do formulário
    if 'popup_email' in st.query_params:
        email = st.query_params['popup_email']
        name = st.query_params.get('popup_name', '')
        
        if email and '@' in email:
            # Salvar email e nome no session_state
            st.session_state.user_email = email
            st.session_state.user_name = name
            
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
    
    # Carregar logo
    def load_logo_as_base64():
        # Tentar carregar o SVG primeiro
        logo_paths = ['logoNova 1.svg', 'logoNova.svg', 'logoNova.png']
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    with open(logo_path, 'rb') as f:
                        logo_data = base64.b64encode(f.read()).decode('utf-8')
                        if logo_path.endswith('.svg'):
                            return f"data:image/svg+xml;base64,{logo_data}"
                        else:
                            return f"data:image/png;base64,{logo_data}"
                except:
                    continue
        return ""
    
    svg_base64 = load_svg_as_base64()
    logo_base64 = load_logo_as_base64()
    bg_style = f"background-image: url('data:image/svg+xml;base64,{svg_base64}');" if svg_base64 else "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"
    
    # Data de última atualização
    last_update = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
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
        
        .last-update-badge {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 12px 20px;
            border-radius: 25px;
            font-size: 0.85em;
            color: #666;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000001;
            font-weight: 500;
        }}
        
        .last-update-badge strong {{
            color: #333;
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
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 440px;
            width: 100%;
            animation: fadeIn 0.4s ease-out;
        }}
        
        .popup-header {{
            padding: 40px 40px 25px;
            text-align: center;
        }}
        
        .logo-container {{
            margin-bottom: 25px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .logo-container img {{
            max-width: 180px;
            height: auto;
        }}
        
        .popup-header h2 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.6em;
            font-weight: 600;
        }}
        
        .popup-header p {{
            margin: 0;
            color: #7f8c8d;
            font-size: 0.95em;
            line-height: 1.5;
        }}
        
        .popup-body {{
            padding: 0 40px 40px;
        }}
        
        .input-group {{
            margin-bottom: 20px;
        }}
        
        .popup-input {{
            width: 100%;
            padding: 16px 18px;
            font-size: 1em;
            border: 2px solid #e8e8e8;
            border-radius: 10px;
            background: #fafafa;
            color: #2c3e50;
            outline: none;
            transition: all 0.3s ease;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        .popup-input::placeholder {{
            color: #95a5a6;
        }}
        
        .popup-input:focus {{
            border-color: #ff8c00;
            background: white;
            box-shadow: 0 0 0 4px rgba(255, 140, 0, 0.08);
        }}
        
        .popup-button {{
            width: 100%;
            padding: 18px;
            font-size: 1.05em;
            font-weight: 600;
            color: white;
            background: #ff8c00;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 10px;
        }}
        
        .popup-button:hover {{
            background: #ff7a00;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 140, 0, 0.35);
        }}
        
        .popup-button:active {{
            transform: translateY(0);
        }}
        
        @media (max-width: 480px) {{
            .popup-card {{
                margin: 15px;
            }}
            .popup-header {{
                padding: 30px 25px 20px;
            }}
            .popup-body {{
                padding: 0 25px 30px;
            }}
            .last-update-badge {{
                top: 10px;
                right: 10px;
                font-size: 0.75em;
                padding: 8px 14px;
            }}
        }}
    </style>
    
    <div class="popup-overlay"></div>
    <div class="last-update-badge">
        <strong>Última atualização:</strong> {last_update}
    </div>
    <div class="popup-container">
        <div class="popup-card">
            <div class="popup-header">
                <div class="logo-container">
                    {'<img src="' + logo_base64 + '" alt="Logo Viana e Moura" />' if logo_base64 else ''}
                </div>
                <h2>Bem-vindo ao Painel</h2>
                <p>Por favor, preencha seus dados para acessar</p>
            </div>
            <div class="popup-body">
                <form method="get">
                    <div class="input-group">
                        <input type="text" name="popup_name" placeholder="Nome completo" class="popup-input" required />
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
