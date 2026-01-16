# Script para reescrever a secao da tab3 de forma limpa
lines = open('app.py', 'r', encoding='utf-8').readlines()

# Encontrar onde começa a seção problemática (após selected_empreendimento_baseline)
# e reescrever tudo de forma limpa

# Deletar linhas 6200-6277 (todo o código problemático)
del lines[6199:6277]

# Inserir código limpo
novo_codigo = '''            
            # === CRIAR NOVA BASELINE ===
            st.markdown("---")
            st.markdown("### 📝 Criar Nova Linha de Base")
            
            with st.container(border=True):
                user_email = st.session_state.get('user_email', '')
                user_name = st.session_state.get('user_name', '')
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Empreendimento:** {selected_empreendimento_baseline}")
                    if user_name and user_email:
                        st.write(f"**Criado por:** {user_name} ({user_email})")
                
                with col2:
                    if st.button("🎯 Criar Baseline", use_container_width=True, type="primary", key="create_baseline_main"):
                        try:
                            version_name = take_gantt_baseline(
                                df_data, 
                                selected_empreendimento_baseline, 
                                tipo_visualizacao,
                                created_by=user_email if user_email else "usuario"
                            )
                            st.success(f"✅ Baseline **{version_name}** criada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao criar baseline: {e}")
            
            # === APLICAR BASELINE NO GRÁFICO ===
            st.markdown("---")
            st.markdown("### 📊 Aplicar Baseline no Gráfico")
            
'''

lines.insert(6199, novo_codigo)

open('app.py', 'w', encoding='utf-8').writelines(lines)
print("Tab3 reescrita com sucesso!")
