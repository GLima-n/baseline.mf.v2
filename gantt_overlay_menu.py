"""
Menu de Contexto Overlay para Gráfico Gantt
============================================

Esta solução cria um overlay transparente SOBRE o iframe do Gantt,
permitindo capturar eventos de clique direito SEM problemas de sandbox.

Arquitetura:
-----------
┌─────────────────────────────────────┐
│  Streamlit Container                │
│  ┌───────────────────────────────┐  │
│  │  Overlay Transparente         │  │ <- Captura eventos
│  │  (position: absolute)         │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Iframe Gantt           │  │  │ <- Apenas visualização
│  │  │  (sandbox)              │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│                                     │
│  Menu de Contexto (fora do iframe) │ <- Comunica com Streamlit
└─────────────────────────────────────┘
"""

import streamlit as st
import streamlit.components.v1 as components


def create_gantt_overlay_with_context_menu(iframe_height, selected_empreendimento):
    """
    Cria um overlay transparente sobre o iframe do Gantt com menu de contexto.
    
    Args:
        iframe_height: Altura do iframe do Gantt em pixels
        selected_empreendimento: Nome do empreendimento selecionado
    
    Returns:
        HTML component com overlay e menu
    """
    
    overlay_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                overflow: hidden;
            }}
            
            /* Container do overlay */
            .overlay-container {{
                position: relative;
                width: 100%;
                height: {iframe_height}px;
            }}
            
            /* Overlay transparente que fica SOBRE o iframe */
            .gantt-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10;
                cursor: default;
                /* Transparente mas captura eventos */
                background: transparent;
                pointer-events: auto;
            }}
            
            /* Área de hint (opcional) */
            .overlay-hint {{
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.9);
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 11px;
                color: #666;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s;
            }}
            
            .gantt-overlay:hover .overlay-hint {{
                opacity: 1;
            }}
            
            /* Menu de contexto */
            #context-menu {{
                position: fixed;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                display: none;
                min-width: 220px;
                overflow: hidden;
            }}
            
            .context-menu-item {{
                padding: 12px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                font-size: 14px;
                color: #333;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .context-menu-item:last-child {{
                border-bottom: none;
            }}
            
            .context-menu-item:hover {{
                background: #f8f9fa;
                color: #000;
            }}
            
            .context-menu-item.disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .context-menu-item.disabled:hover {{
                background: transparent;
                color: #333;
            }}
            
            .menu-icon {{
                font-size: 16px;
                width: 20px;
                text-align: center;
            }}
            
            .menu-separator {{
                height: 1px;
                background: #e0e0e0;
                margin: 4px 0;
            }}
            
            /* Loading overlay */
            .loading-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.4);
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 2000;
            }}
            
            .loading-content {{
                background: white;
                padding: 30px 40px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }}
            
            .loading-spinner {{
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            /* Toast notification */
            .toast {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                padding: 16px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 3000;
                display: none;
                min-width: 300px;
                border-left: 4px solid #3498db;
            }}
            
            .toast.success {{
                border-left-color: #2ecc71;
            }}
            
            .toast.error {{
                border-left-color: #e74c3c;
            }}
            
            .toast.show {{
                display: block;
                animation: slideIn 0.3s ease-out;
            }}
            
            @keyframes slideIn {{
                from {{
                    transform: translateX(400px);
                    opacity: 0;
                }}
                to {{
                    transform: translateX(0);
                    opacity: 1;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- Container do overlay -->
        <div class="overlay-container">
            <!-- Overlay transparente que captura eventos -->
            <div class="gantt-overlay" id="gantt-overlay">
                <div class="overlay-hint">
                    Clique direito para opções
                </div>
            </div>
        </div>
        
        <!-- Menu de contexto (fora do iframe) -->
        <div id="context-menu">
            <div class="context-menu-item" data-action="create-baseline">
                <span class="menu-icon">📸</span>
                <span>Criar Linha de Base</span>
            </div>
            <div class="menu-separator"></div>
            <div class="context-menu-item disabled" data-action="restore-baseline">
                <span class="menu-icon">🔄</span>
                <span>Restaurar Baseline</span>
            </div>
            <div class="context-menu-item disabled" data-action="compare-baseline">
                <span class="menu-icon">📊</span>
                <span>Comparar Baselines</span>
            </div>
            <div class="menu-separator"></div>
            <div class="context-menu-item disabled" data-action="delete-baseline">
                <span class="menu-icon">🗑️</span>
                <span>Deletar Baseline</span>
            </div>
        </div>
        
        <!-- Loading overlay -->
        <div class="loading-overlay" id="loading-overlay">
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <h3>Criando Linha de Base</h3>
                <p>Por favor, aguarde...</p>
            </div>
        </div>
        
        <!-- Toast notification -->
        <div class="toast" id="toast">
            <div id="toast-message"></div>
        </div>
        
        <script>
            // Elementos
            const overlay = document.getElementById('gantt-overlay');
            const contextMenu = document.getElementById('context-menu');
            const loadingOverlay = document.getElementById('loading-overlay');
            const toast = document.getElementById('toast');
            const toastMessage = document.getElementById('toast-message');
            
            const selectedEmpreendimento = "{selected_empreendimento}";
            
            // Função para mostrar menu
            function showContextMenu(x, y) {{
                contextMenu.style.left = x + 'px';
                contextMenu.style.top = y + 'px';
                contextMenu.style.display = 'block';
            }}
            
            // Função para esconder menu
            function hideContextMenu() {{
                contextMenu.style.display = 'none';
            }}
            
            // Função para mostrar loading
            function showLoading() {{
                loadingOverlay.style.display = 'flex';
            }}
            
            // Função para esconder loading
            function hideLoading() {{
                loadingOverlay.style.display = 'none';
            }}
            
            // Função para mostrar toast
            function showToast(message, type = 'success') {{
                toastMessage.textContent = message;
                toast.className = 'toast show ' + type;
                
                setTimeout(() => {{
                    toast.classList.remove('show');
                }}, 4000);
            }}
            
            // Função para criar baseline
            function createBaseline() {{
                console.log('Criando baseline para:', selectedEmpreendimento);
                
                showLoading();
                hideContextMenu();
                
                // Redirecionar para Streamlit com query params
                const timestamp = new Date().getTime();
                const url = `?context_action=take_baseline&empreendimento=${{encodeURIComponent(selectedEmpreendimento)}}&t=${{timestamp}}`;
                
                // Usar window.top para sair do iframe do componente
                window.top.location.href = url;
            }}
            
            // Event listener para clique direito no overlay
            overlay.addEventListener('contextmenu', (e) => {{
                e.preventDefault();
                e.stopPropagation();
                
                // Posição do clique
                const x = e.clientX;
                const y = e.clientY;
                
                showContextMenu(x, y);
            }});
            
            // Event listeners para itens do menu
            contextMenu.querySelectorAll('.context-menu-item').forEach(item => {{
                item.addEventListener('click', (e) => {{
                    const action = e.currentTarget.getAttribute('data-action');
                    
                    // Verificar se está desabilitado
                    if (e.currentTarget.classList.contains('disabled')) {{
                        showToast('⚠️ Funcionalidade em desenvolvimento', 'error');
                        hideContextMenu();
                        return;
                    }}
                    
                    // Executar ação
                    switch(action) {{
                        case 'create-baseline':
                            createBaseline();
                            break;
                        case 'restore-baseline':
                        case 'compare-baseline':
                        case 'delete-baseline':
                            showToast('🔄 Em desenvolvimento...', 'error');
                            hideContextMenu();
                            break;
                    }}
                }});
            }});
            
            // Fechar menu ao clicar fora
            document.addEventListener('click', (e) => {{
                if (!contextMenu.contains(e.target) && e.target !== overlay) {{
                    hideContextMenu();
                }}
            }});
            
            // Fechar menu com ESC
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') {{
                    hideContextMenu();
                }}
            }});
            
            // Prevenir menu de contexto padrão
            document.addEventListener('contextmenu', (e) => {{
                e.preventDefault();
            }}, true);
        </script>
    </body>
    </html>
    """
    
    # Renderizar o componente
    components.html(overlay_html, height=iframe_height)


def render_gantt_with_overlay_menu(gantt_html, iframe_height, selected_empreendimento):
    """
    Renderiza o Gantt no iframe e o overlay com menu de contexto SOBRE ele.
    
    Args:
        gantt_html: HTML do gráfico Gantt
        iframe_height: Altura do iframe
        selected_empreendimento: Empreendimento selecionado
    """
    
    # Container que vai ter o iframe E o overlay
    container_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
            
            .gantt-container {{
                position: relative;
                width: 100%;
                height: {iframe_height}px;
            }}
            
            /* Iframe do Gantt */
            .gantt-iframe {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
                z-index: 1;
            }}
            
            /* Overlay transparente SOBRE o iframe */
            .context-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10;
                pointer-events: auto;
            }}
            
            /* Menu de contexto */
            #context-menu {{
                position: fixed;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                display: none;
                min-width: 220px;
                overflow: hidden;
            }}
            
            .context-menu-item {{
                padding: 12px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                font-size: 14px;
                color: #333;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .context-menu-item:hover {{
                background: #f8f9fa;
            }}
            
            .menu-icon {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="gantt-container">
            <!-- Iframe com o Gantt -->
            <iframe class="gantt-iframe" srcdoc='{gantt_html.replace("'", "&apos;")}'>
            </iframe>
            
            <!-- Overlay transparente para capturar eventos -->
            <div class="context-overlay" id="context-overlay"></div>
        </div>
        
        <!-- Menu de contexto (FORA do iframe) -->
        <div id="context-menu">
            <div class="context-menu-item" onclick="createBaseline()">
                <span class="menu-icon">📸</span>
                <span>Criar Linha de Base</span>
            </div>
        </div>
        
        <script>
            const overlay = document.getElementById('context-overlay');
            const menu = document.getElementById('context-menu');
            
            // Capturar clique direito no overlay
            overlay.addEventListener('contextmenu', (e) => {{
                e.preventDefault();
                menu.style.left = e.pageX + 'px';
                menu.style.top = e.pageY + 'px';
                menu.style.display = 'block';
            }});
            
            // Função para criar baseline
            function createBaseline() {{
                // Comunicar com Streamlit via query params
                window.location.href = '?context_action=take_baseline&empreendimento={selected_empreendimento}';
            }}
            
            // Fechar menu
            document.addEventListener('click', () => {{
                menu.style.display = 'none';
            }});
        </script>
    </body>
    </html>
    """
    
    return container_html
