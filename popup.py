import streamlit as st
import base64
import os
import json

def show_welcome_screen():
    """
    Popup bonito usando overlay CSS puro sem iframe.
    """
    
    print("="*80)
    print("🔍 show_welcome_screen() CHAMADO!")
    print(f"📧 Session state user_email: '{st.session_state.get('user_email', 'VAZIO')}'")
    print(f"👤 Session state user_name: '{st.session_state.get('user_name', 'VAZIO')}'")
    print(f"🔗 Query params: {dict(st.query_params)}")
    
    # === LIMPEZA FORÇADA VIA URL ===
    # Se a URL contiver ?clear_login=1, limpa TUDO e mostra o popup
    if 'clear_login' in st.query_params:
        print("🧹 LIMPEZA FORÇADA ATIVADA!")
        
        # Deletar arquivo
        config_file = '.streamlit_user_config.json'
        if os.path.exists(config_file):
            try:
                os.remove(config_file)
                print(f"✅ Arquivo {config_file} DELETADO!")
            except Exception as e:
                print(f"❌ Erro ao deletar arquivo: {e}")
        
        # Limpar session_state
        if 'user_email' in st.session_state:
            del st.session_state['user_email']
            print("✅ user_email removido do session_state")
        if 'user_name' in st.session_state:
            del st.session_state['user_name']
            print("✅ user_name removido do session_state")
        
        # Limpar query params e recarregar
        st.query_params.clear()
        print("✅ Query params limpos, fazendo rerun...")
        st.rerun()
    
    # PRIMEIRO: Processar query params se existirem (antes de qualquer verificação)
    if 'popup_name' in st.query_params and 'popup_email' in st.query_params:
        print("✅ QUERY PARAMS DETECTADOS - Processando login...")
        name = st.query_params['popup_name']
        email = st.query_params['popup_email']
        
        if name and email and len(name) >= 3 and '@' in email:
            print(f"✅ Salvando: name='{name}', email='{email}'")
            st.session_state.user_name = name
            st.session_state.user_email = email
            
            # Salvar no arquivo
            try:
                with open('.streamlit_user_config.json', 'w') as f:
                    json.dump({'user_name': name, 'user_email': email}, f)
                print("✅ Arquivo .streamlit_user_config.json CRIADO")
            except Exception as e:
                print(f"❌ Erro ao salvar arquivo: {e}")
            
            # IMPORTANTE: Limpar params e recarregar IMEDIATAMENTE
            st.query_params.clear()
            print("🔄 Query params limpos, fazendo rerun...")
            st.rerun()
    else:
        print("⚠️ Nenhum query param detectado")
    
    # SEGUNDO: Verificar se já tem email no session_state
    if 'user_email' in st.session_state and st.session_state.user_email:
        print(f"🚫 JÁ TEM EMAIL NO SESSION_STATE: '{st.session_state.user_email}' - POPUP NÃO SERÁ EXIBIDO")
        print("="*80)
        return  # Já tem email
    else:
        print("✅ Session_state NÃO tem email ainda")
    
    # TERCEIRO: Tentar carregar do arquivo
    try:
        config_file = '.streamlit_user_config.json'
        print(f"🔍 Verificando se existe arquivo '{config_file}'...")
        if os.path.exists(config_file):
            print(f"❌ ARQUIVO EXISTE! Carregando...")
            with open(config_file, 'r') as f:
                config = json.load(f)
                print(f"📄 Conteúdo do arquivo: {config}")
                if config.get('user_email'):
                    st.session_state.user_name = config.get('user_name', '')
                    st.session_state.user_email = config['user_email']
                    print(f"🚫 EMAIL CARREGADO DO ARQUIVO: '{config['user_email']}' - POPUP NÃO SERÁ EXIBIDO")
                    print("="*80)
                    return
        else:
            print(f"✅ Arquivo NÃO existe - Popup DEVE ser exibido")
    except Exception as e:
        print(f"⚠️ Erro ao carregar arquivo: {e}")
    
    print("🎯 TODAS AS VERIFICAÇÕES PASSARAM - EXIBINDO POPUP!")
    print("="*80)
    
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
    
    # CSS e HTML do popup (sem iframe!)
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
