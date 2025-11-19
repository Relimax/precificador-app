"""
Sistema de Precificação para E-commerce - Lucro Real
Versão Simplificada em Python com Interface Web

Para rodar: streamlit run precificacao_app.py
"""

import streamlit as st
from decimal import Decimal
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Preço - Lucro Real",
    page_icon="💰",
    layout="wide"
)

# CSS customizado para melhorar visual
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #27ae60;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    .success-card {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #27ae60;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .danger-card {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("💰 Calculadora de Precificação")
st.subheader("Sistema para E-commerce no Lucro Real")

# Aviso importante
with st.expander("⚠️ IMPORTANTE - Leia antes de usar"):
    st.warning("""
    **Este sistema é uma ferramenta de APOIO!**
    
    - ❌ NÃO substitui seu contador
    - ❌ NÃO substitui sistema fiscal oficial
    - ✅ Use para simulações e estudos
    - ✅ Sempre valide com seu contador antes de aplicar preços
    
    A legislação tributária muda frequentemente. Mantenha as alíquotas atualizadas!
    """)

# Separador
st.markdown("---")

# Sidebar com informações
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)
    st.title("📊 Menu")
    pagina = st.radio("Navegação:", ["🧮 Calculadora", "📚 Como Usar", "ℹ️ Sobre"])
    
    st.markdown("---")
    st.info("""
    **Versão:** 1.0  
    **Atualizado:** Nov/2025  
    **Status:** ✅ Online
    """)

# PÁGINA: CALCULADORA
if pagina == "🧮 Calculadora":
    
    # Criar abas para organizar melhor
    tab1, tab2, tab3 = st.tabs(["📝 Dados do Produto", "🏪 Marketplace", "📊 Resultado"])
    
    # ABA 1: DADOS DO PRODUTO
    with tab1:
        st.header("📦 Dados do Produto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            produto_nome = st.text_input("Nome do Produto", "Smartphone Samsung Galaxy A54", help="Apenas para identificação")
            custo_aquisicao = st.number_input("💵 Custo de Aquisição (R$)", min_value=0.0, value=100.0, step=1.0)
            
            st.subheader("Impostos na Compra (que viram CUSTO)")
            ipi_compra = st.number_input("IPI não recuperável (R$)", min_value=0.0, value=15.0, step=0.1, 
                                        help="IPI que não gera crédito (comércio)")
            
        with col2:
            st.subheader("Créditos Tributários (REDUZEM custo)")
            credito_icms = st.number_input("Crédito ICMS (R$)", min_value=0.0, value=18.0, step=0.1,
                                          help="ICMS que você recupera na compra")
            credito_pis = st.number_input("Crédito PIS (R$)", min_value=0.0, value=1.65, step=0.01,
                                         help="PIS não cumulativo - 1,65% geralmente")
            credito_cofins = st.number_input("Crédito COFINS (R$)", min_value=0.0, value=7.60, step=0.01,
                                            help="COFINS não cumulativo - 7,60% geralmente")
        
        st.subheader("Outros Custos")
        col3, col4 = st.columns(2)
        with col3:
            custo_frete = st.number_input("Frete (R$)", min_value=0.0, value=5.0, step=0.1)
            custo_armazenagem = st.number_input("Armazenagem (R$)", min_value=0.0, value=1.0, step=0.1)
        with col4:
            custo_despachante = st.number_input("Despachante/Outros (R$)", min_value=0.0, value=10.0, step=0.1)
            custo_seguro = st.number_input("Seguro (R$)", min_value=0.0, value=3.0, step=0.1)
        
        # Calcular custo total
        custo_total = (
            custo_aquisicao 
            + ipi_compra 
            - credito_icms 
            - credito_pis 
            - credito_cofins 
            + custo_frete 
            + custo_armazenagem 
            + custo_despachante 
            + custo_seguro
        )
        
        st.success(f"✅ **Custo Total Unitário: R$ {custo_total:.2f}**")
    
    # ABA 2: MARKETPLACE E VENDA
    with tab2:
        st.header("🏪 Condições de Venda")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Destino da Venda")
            uf_destino = st.selectbox("UF de Destino", 
                                     ["SP", "RJ", "MG", "RS", "BA", "PR", "SC", "PE", "CE", "DF", "GO", "AM"],
                                     index=1)
            
            tipo_cliente = st.radio("Tipo de Cliente", 
                                   ["Consumidor Final", "Contribuinte ICMS"],
                                   help="Consumidor Final = tem DIFAL")
            
            st.subheader("Alíquotas de Tributos (%)")
            aliq_pis = st.number_input("PIS", min_value=0.0, max_value=100.0, value=1.65, step=0.01)
            aliq_cofins = st.number_input("COFINS", min_value=0.0, max_value=100.0, value=7.60, step=0.01)
            aliq_icms = st.number_input("ICMS", min_value=0.0, max_value=100.0, value=12.0, step=0.1,
                                       help="Interestadual geralmente 12%")
            
            if tipo_cliente == "Consumidor Final":
                aliq_difal = st.number_input("DIFAL", min_value=0.0, max_value=100.0, value=6.0, step=0.1,
                                            help="Diferença entre ICMS interno e interestadual")
                aliq_fcp = st.number_input("FCP", min_value=0.0, max_value=100.0, value=2.0, step=0.1,
                                          help="Fundo de Combate à Pobreza")
            else:
                aliq_difal = 0.0
                aliq_fcp = 0.0
        
        with col2:
            st.subheader("Marketplace")
            marketplace = st.selectbox("Qual marketplace?", 
                                      ["Nenhum (Venda Direta)", "Mercado Livre", "Shopee", "Amazon", "Magalu", "Outro"])
            
            if marketplace != "Nenhum (Venda Direta)":
                comissao = st.number_input("Comissão (%)", min_value=0.0, max_value=100.0, value=16.0, step=0.1)
                taxa_fixa = st.number_input("Taxa Fixa (R$)", min_value=0.0, value=5.0, step=0.1)
                taxa_antecipacao = st.number_input("Taxa Antecipação (%)", min_value=0.0, max_value=100.0, value=2.5, step=0.1)
                taxa_gateway = st.number_input("Taxa Gateway (%)", min_value=0.0, max_value=100.0, value=2.5, step=0.1)
            else:
                comissao = 0.0
                taxa_fixa = 0.0
                taxa_antecipacao = 0.0
                taxa_gateway = 0.0
            
            st.subheader("Margem Desejada")
            margem_alvo = st.slider("Margem de Contribuição Alvo (%)", 
                                   min_value=0.0, max_value=100.0, value=20.0, step=0.5,
                                   help="Quanto % você quer de margem?")
    
    # ABA 3: RESULTADO
    with tab3:
        st.header("📊 Resultado do Cálculo")
        
        if st.button("🔄 CALCULAR PREÇO", type="primary", use_container_width=True):
            
            with st.spinner("Calculando..."):
                # Usar Decimal para precisão
                D = Decimal
                
                custo = D(str(custo_total))
                custos_fixos = D(str(taxa_fixa))
                
                # Percentuais em decimal
                pct_margem = D(str(margem_alvo)) / D('100')
                pct_tributos = (D(str(aliq_pis)) + D(str(aliq_cofins)) + D(str(aliq_icms)) + 
                               D(str(aliq_difal)) + D(str(aliq_fcp))) / D('100')
                pct_custos_variaveis = (D(str(comissao)) + D(str(taxa_antecipacao)) + D(str(taxa_gateway))) / D('100')
                
                # Total de percentuais
                total_pct = pct_margem + pct_tributos + pct_custos_variaveis
                
                # Fórmula: Preço = (Custo + Fixos) / (1 - Total%)
                preco_venda = (custo + custos_fixos) / (D('1') - total_pct)
                
                # Calcular detalhamento
                valor_pis = preco_venda * (D(str(aliq_pis)) / D('100'))
                valor_cofins = preco_venda * (D(str(aliq_cofins)) / D('100'))
                valor_icms = preco_venda * (D(str(aliq_icms)) / D('100'))
                valor_difal = preco_venda * (D(str(aliq_difal)) / D('100'))
                valor_fcp = preco_venda * (D(str(aliq_fcp)) / D('100'))
                
                total_tributos = valor_pis + valor_cofins + valor_icms + valor_difal + valor_fcp
                
                valor_comissao = preco_venda * (D(str(comissao)) / D('100'))
                valor_antecipacao = preco_venda * (D(str(taxa_antecipacao)) / D('100'))
                valor_gateway = preco_venda * (D(str(taxa_gateway)) / D('100'))
                
                total_custos_canal = valor_comissao + D(str(taxa_fixa)) + valor_antecipacao + valor_gateway
                
                margem_contribuicao = preco_venda - custo - total_tributos - total_custos_canal
                margem_percentual = (margem_contribuicao / preco_venda) * D('100')
                
                # IRPJ/CSLL estimado (34%)
                irpj_csll = margem_contribuicao * D('0.34')
                lucro_liquido = margem_contribuicao - irpj_csll
                lucro_liquido_pct = (lucro_liquido / preco_venda) * D('100')
                
                # MOSTRAR RESULTADOS
                st.markdown("### 💵 PREÇO DE VENDA SUGERIDO")
                st.markdown(f'<p class="big-font">R$ {float(preco_venda):.2f}</p>', unsafe_allow_html=True)
                
                # Determinar status da margem
                margem_float = float(margem_percentual)
                if margem_float >= 20:
                    status_cor = "success-card"
                    status_texto = "🟢 MARGEM SAUDÁVEL"
                elif margem_float >= 10:
                    status_cor = "warning-card"
                    status_texto = "🟡 MARGEM BAIXA - ATENÇÃO"
                else:
                    status_cor = "danger-card"
                    status_texto = "🔴 MARGEM CRÍTICA"
                
                st.markdown(f'<div class="{status_cor}"><h3>{status_texto}</h3></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Breakdown em colunas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📦 Custo do Produto", f"R$ {float(custo):.2f}", 
                             f"{float(custo/preco_venda*100):.1f}% do preço")
                
                with col2:
                    st.metric("💸 Tributos Total", f"R$ {float(total_tributos):.2f}",
                             f"{float(total_tributos/preco_venda*100):.1f}% do preço")
                
                with col3:
                    st.metric("🏪 Custos de Canal", f"R$ {float(total_custos_canal):.2f}",
                             f"{float(total_custos_canal/preco_venda*100):.1f}% do preço")
                
                st.markdown("---")
                
                col4, col5 = st.columns(2)
                
                with col4:
                    st.metric("📈 Margem de Contribuição", f"R$ {float(margem_contribuicao):.2f}",
                             f"{float(margem_percentual):.2f}%")
                
                with col5:
                    st.metric("💰 Lucro Líquido Estimado", f"R$ {float(lucro_liquido):.2f}",
                             f"{float(lucro_liquido_pct):.2f}%",
                             help="Após IRPJ/CSLL estimado (34%)")
                
                st.markdown("---")
                
                # Tabela detalhada
                st.subheader("📋 Detalhamento Completo")
                
                st.markdown("**💸 Tributos:**")
                tributos_data = {
                    "Tributo": ["PIS", "COFINS", "ICMS", "DIFAL", "FCP"],
                    "Alíquota": [f"{aliq_pis}%", f"{aliq_cofins}%", f"{aliq_icms}%", f"{aliq_difal}%", f"{aliq_fcp}%"],
                    "Valor": [f"R$ {float(valor_pis):.2f}", f"R$ {float(valor_cofins):.2f}", 
                             f"R$ {float(valor_icms):.2f}", f"R$ {float(valor_difal):.2f}", 
                             f"R$ {float(valor_fcp):.2f}"]
                }
                st.table(tributos_data)
                
                if marketplace != "Nenhum (Venda Direta)":
                    st.markdown("**🏪 Custos do Marketplace:**")
                    marketplace_data = {
                        "Item": ["Comissão", "Taxa Fixa", "Antecipação", "Gateway"],
                        "Percentual/Valor": [f"{comissao}%", f"R$ {taxa_fixa:.2f}", 
                                            f"{taxa_antecipacao}%", f"{taxa_gateway}%"],
                        "Valor": [f"R$ {float(valor_comissao):.2f}", f"R$ {taxa_fixa:.2f}",
                                 f"R$ {float(valor_antecipacao):.2f}", f"R$ {float(valor_gateway):.2f}"]
                    }
                    st.table(marketplace_data)
                
                # Botão para baixar resultado
                resultado_texto = f"""
RESULTADO DA PRECIFICAÇÃO
=========================

Produto: {produto_nome}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

CUSTO:
- Custo Total Unitário: R$ {float(custo):.2f}

VENDA:
- Destino: {uf_destino}
- Cliente: {tipo_cliente}
- Marketplace: {marketplace}

PREÇO DE VENDA SUGERIDO: R$ {float(preco_venda):.2f}

COMPOSIÇÃO:
- Custo do Produto: R$ {float(custo):.2f} ({float(custo/preco_venda*100):.1f}%)
- Tributos: R$ {float(total_tributos):.2f} ({float(total_tributos/preco_venda*100):.1f}%)
- Custos Canal: R$ {float(total_custos_canal):.2f} ({float(total_custos_canal/preco_venda*100):.1f}%)

MARGEM:
- Margem de Contribuição: R$ {float(margem_contribuicao):.2f} ({float(margem_percentual):.2f}%)
- Lucro Líquido Est.: R$ {float(lucro_liquido):.2f} ({float(lucro_liquido_pct):.2f}%)

STATUS: {status_texto}

AVISO: Sempre valide com seu contador!
                """
                
                st.download_button(
                    label="📥 Baixar Resultado (TXT)",
                    data=resultado_texto,
                    file_name=f"precificacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

# PÁGINA: COMO USAR
elif pagina == "📚 Como Usar":
    st.header("📚 Como Usar Este Sistema")
    
    st.markdown("""
    ### 🎯 Passo a Passo
    
    #### 1️⃣ **Dados do Produto** (Aba 1)
    
    **Informe os custos:**
    - **Custo de Aquisição:** Quanto você pagou pelo produto
    - **IPI não recuperável:** IPI que não gera crédito (se for comércio)
    - **Créditos Tributários:** Impostos que você recupera na compra
      - ICMS: Geralmente 18% do valor
      - PIS: 1,65% do valor (Lucro Real)
      - COFINS: 7,60% do valor (Lucro Real)
    - **Outros Custos:** Frete, armazenagem, despachante, etc.
    
    ✅ O sistema calcula automaticamente o **Custo Total Unitário**
    
    ---
    
    #### 2️⃣ **Marketplace e Venda** (Aba 2)
    
    **Configure a venda:**
    - **UF de Destino:** Para onde vai vender
    - **Tipo de Cliente:** 
      - Consumidor Final → calcula DIFAL
      - Contribuinte ICMS → não calcula DIFAL
    
    **Alíquotas de Tributos:**
    - PIS: Geralmente 1,65%
    - COFINS: Geralmente 7,60%
    - ICMS: 12% (interestadual) ou 18% (interno)
    - DIFAL: Diferença entre ICMS interno e interestadual
    - FCP: 2% (alguns estados)
    
    **Se vender em Marketplace:**
    - Escolha o marketplace
    - Informe comissão (ex: Mercado Livre = 16%)
    - Informe taxas (fixa, antecipação, gateway)
    
    **Defina a Margem:**
    - Quanto % de lucro você quer? (ex: 20%)
    
    ---
    
    #### 3️⃣ **Resultado** (Aba 3)
    
    Clique em **"CALCULAR PREÇO"**
    
    O sistema mostra:
    - ✅ Preço de venda sugerido
    - ✅ Status da margem (saudável/atenção/crítica)
    - ✅ Breakdown completo de custos
    - ✅ Detalhamento de tributos
    - ✅ Lucro líquido estimado
    
    Você pode **baixar o resultado** em TXT!
    
    ---
    
    ### 💡 Dicas Importantes
    
    1. **Valide alíquotas** com seu contador
    2. **ICMS varia por UF** - consulte tabelas oficiais
    3. **Comissões mudam** - verifique no marketplace
    4. **Sempre teste** antes de aplicar preços
    5. **Margem saudável:** Acima de 20% 🟢
    
    ---
    
    ### 📊 Exemplo Prático
    
    **Produto:** Smartphone Samsung Galaxy A54
    - Custo de compra: R$ 100,00
    - IPI: R$ 15,00 (não recupera)
    - Crédito ICMS: R$ 18,00
    - Crédito PIS/COFINS: R$ 9,25
    - Outros custos: R$ 19,00
    - **Custo Total: R$ 107,75**
    
    **Venda para RJ via Mercado Livre:**
    - PIS: 1,65%
    - COFINS: 7,60%
    - ICMS: 12%
    - DIFAL: 6%
    - FCP: 2%
    - Comissão ML: 16%
    - Margem alvo: 20%
    
    **Resultado: R$ 379,99** ✅
    """)

# PÁGINA: SOBRE
else:
    st.header("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### 💰 Sistema de Precificação - Lucro Real
    
    Este sistema foi desenvolvido para ajudar **empresas de e-commerce** que estão no regime de **Lucro Real** a calcular preços de venda considerando:
    
    - ✅ Custos de aquisição
    - ✅ Tributos (débitos e créditos)
    - ✅ Custos de marketplaces
    - ✅ Margem de lucro desejada
    
    ---
    
    ### 🎯 Funcionalidades
    
    - 📊 Cálculo automático de preço
    - 💸 Consideração de PIS/COFINS não cumulativo
    - 🏪 Suporte a múltiplos marketplaces
    - 📈 Análise de margem e lucro líquido
    - 📥 Exportação de resultados
    
    ---
    
    ### ⚠️ IMPORTANTE
    
    **Este sistema é uma FERRAMENTA DE APOIO!**
    
    - ❌ NÃO substitui contador
    - ❌ NÃO substitui sistema fiscal
    - ✅ Use para simulações
    - ✅ Valide TUDO com seu contador
    
    A legislação tributária brasileira é complexa e muda frequentemente.
    
    ---
    
    ### 📚 Conceitos Básicos
    
    **Lucro Real:**
    - Regime tributário onde IRPJ e CSLL incidem sobre o lucro real
    - PIS/COFINS não cumulativos (geram créditos)
    - Obrigatório para faturamento > R$ 78 milhões/ano
    
    **Débito:**
    - Impostos que você deve pagar na venda
    - Ex: PIS, COFINS, ICMS sobre a venda
    
    **Crédito:**
    - Impostos que você recupera na compra
    - Ex: PIS, COFINS, ICMS da nota de compra
    - Reduzem o custo efetivo do produto
    
    **DIFAL:**
    - Diferencial de Alíquota
    - Aplicável em vendas interestaduais para consumidor final
    - Diferença entre ICMS interno e interestadual
    
    ---
    
    ### 🔧 Tecnologia
    
    - **Linguagem:** Python 3
    - **Framework:** Streamlit
    - **Precisão:** Decimal (cálculos financeiros)
    
    ---
    
    ### 📞 Suporte
    
    Para dúvidas sobre:
    - **Sistema:** Consulte a aba "Como Usar"
    - **Tributação:** Consulte seu contador
    - **Legislação:** Consulte Receita Federal / SEFAZ
    
    ---
    
    **Versão:** 1.0  
    **Desenvolvido em:** Novembro 2025  
    **Licença:** Uso livre (validar com contador)
    """)
    
    st.info("💡 **Dica:** Use este sistema para estudar e simular diferentes cenários de precificação!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Sistema de Precificação para E-commerce - Lucro Real | Versão 1.0 | 2025</p>
    <p>⚠️ Sempre valide com seu contador antes de aplicar preços em produção!</p>
</div>
""", unsafe_allow_html=True)
