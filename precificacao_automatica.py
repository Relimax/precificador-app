"""
Sistema de Precificação INTELIGENTE - Lucro Real
Com Base de Dados Tributária Automática

Para rodar: streamlit run precificacao_automatica.py
"""

import streamlit as st
import sqlite3
from decimal import Decimal
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Calculadora Inteligente - Lucro Real",
    page_icon="🤖",
    layout="wide"
)

# CSS
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #27ae60;
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
    .info-card {
        background-color: #d1ecf1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# BANCO DE DADOS - CONFIGURAÇÃO AUTOMÁTICA
# ============================================

def inicializar_banco():
    """Cria e popula o banco de dados com regras tributárias"""
    
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    
    # Tabela de NCMs
    c.execute('''CREATE TABLE IF NOT EXISTS ncm (
        codigo TEXT PRIMARY KEY,
        descricao TEXT,
        aliquota_pis REAL DEFAULT 1.65,
        aliquota_cofins REAL DEFAULT 7.60,
        aliquota_ipi REAL DEFAULT 0.0,
        gera_credito_pis INTEGER DEFAULT 1,
        gera_credito_cofins INTEGER DEFAULT 1,
        gera_credito_icms INTEGER DEFAULT 1,
        observacoes TEXT
    )''')
    
    # Tabela de ICMS por UF
    c.execute('''CREATE TABLE IF NOT EXISTS icms_uf (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uf_origem TEXT,
        uf_destino TEXT,
        aliquota_interna REAL,
        aliquota_interestadual REAL,
        aliquota_fcp REAL DEFAULT 0.0,
        calcula_difal INTEGER DEFAULT 0
    )''')
    
    # Tabela de Marketplaces
    c.execute('''CREATE TABLE IF NOT EXISTS marketplace (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        comissao_padrao REAL,
        taxa_fixa REAL DEFAULT 0.0,
        taxa_antecipacao REAL DEFAULT 0.0,
        taxa_gateway REAL DEFAULT 0.0,
        ativo INTEGER DEFAULT 1
    )''')
    
    # Tabela de Produtos (histórico de custos)
    c.execute('''CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        ncm TEXT,
        custo_total REAL,
        data_cadastro TEXT,
        FOREIGN KEY (ncm) REFERENCES ncm(codigo)
    )''')
    
    # Inserir NCMs comuns (exemplos)
    ncms_exemplo = [
        ('85171231', 'Smartphones', 1.65, 7.60, 0.0, 1, 1, 1, 'Eletrônicos importados'),
        ('64022000', 'Calçados', 1.65, 7.60, 0.0, 1, 1, 1, 'Calçados diversos'),
        ('61091000', 'Camisetas de algodão', 1.65, 7.60, 0.0, 1, 1, 1, 'Vestuário'),
        ('84713012', 'Notebooks', 1.65, 7.60, 0.0, 1, 1, 1, 'Informática'),
        ('33049900', 'Cosméticos', 1.65, 7.60, 0.0, 1, 1, 1, 'Beleza'),
        ('94036000', 'Móveis de madeira', 1.65, 7.60, 0.0, 1, 1, 1, 'Móveis'),
        ('39269090', 'Produtos de plástico', 1.65, 7.60, 0.0, 1, 1, 1, 'Plásticos'),
        ('73269090', 'Produtos de ferro', 1.65, 7.60, 0.0, 1, 1, 1, 'Metais'),
    ]
    
    c.executemany('''INSERT OR IGNORE INTO ncm 
        (codigo, descricao, aliquota_pis, aliquota_cofins, aliquota_ipi, 
         gera_credito_pis, gera_credito_cofins, gera_credito_icms, observacoes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', ncms_exemplo)
    
    # Inserir ICMS por UF (principais rotas)
    # Formato: (uf_origem, uf_destino, aliq_interna, aliq_inter, fcp, calcula_difal)
    icms_dados = [
        # SP
        ('SP', 'SP', 18.0, 18.0, 0.0, 0),
        ('SP', 'RJ', 18.0, 12.0, 2.0, 1),
        ('SP', 'MG', 18.0, 12.0, 2.0, 1),
        ('SP', 'RS', 18.0, 12.0, 2.0, 1),
        ('SP', 'BA', 18.0, 7.0, 2.0, 1),
        ('SP', 'PR', 18.0, 12.0, 2.0, 1),
        ('SP', 'SC', 18.0, 12.0, 2.0, 1),
        ('SP', 'PE', 18.0, 7.0, 2.0, 1),
        ('SP', 'CE', 18.0, 7.0, 2.0, 1),
        ('SP', 'GO', 18.0, 12.0, 2.0, 1),
        ('SP', 'AM', 18.0, 7.0, 2.0, 1),
        ('SP', 'DF', 18.0, 12.0, 2.0, 1),
        
        # RJ
        ('RJ', 'RJ', 18.0, 18.0, 2.0, 0),
        ('RJ', 'SP', 18.0, 12.0, 0.0, 1),
        ('RJ', 'MG', 18.0, 12.0, 2.0, 1),
        ('RJ', 'RS', 18.0, 12.0, 2.0, 1),
        ('RJ', 'BA', 18.0, 7.0, 2.0, 1),
        
        # MG
        ('MG', 'MG', 18.0, 18.0, 2.0, 0),
        ('MG', 'SP', 18.0, 12.0, 0.0, 1),
        ('MG', 'RJ', 18.0, 12.0, 2.0, 1),
        ('MG', 'RS', 18.0, 12.0, 2.0, 1),
        
        # RS
        ('RS', 'RS', 18.0, 18.0, 2.0, 0),
        ('RS', 'SP', 18.0, 12.0, 0.0, 1),
        ('RS', 'SC', 18.0, 12.0, 2.0, 1),
        ('RS', 'PR', 18.0, 12.0, 2.0, 1),
        
        # BA
        ('BA', 'BA', 18.0, 18.0, 2.0, 0),
        ('BA', 'SP', 18.0, 7.0, 0.0, 1),
        ('BA', 'RJ', 18.0, 7.0, 2.0, 1),
    ]
    
    c.executemany('''INSERT OR IGNORE INTO icms_uf 
        (uf_origem, uf_destino, aliquota_interna, aliquota_interestadual, aliquota_fcp, calcula_difal) 
        VALUES (?, ?, ?, ?, ?, ?)''', icms_dados)
    
    # Inserir Marketplaces
    marketplaces = [
        ('Mercado Livre', 16.0, 5.0, 2.5, 2.5, 1),
        ('Shopee', 14.0, 0.0, 2.0, 2.0, 1),
        ('Amazon', 15.0, 0.0, 2.5, 2.5, 1),
        ('Magalu', 18.0, 0.0, 2.0, 2.0, 1),
        ('Venda Direta', 0.0, 0.0, 0.0, 0.0, 1),
    ]
    
    c.executemany('''INSERT OR IGNORE INTO marketplace 
        (nome, comissao_padrao, taxa_fixa, taxa_antecipacao, taxa_gateway, ativo) 
        VALUES (?, ?, ?, ?, ?, ?)''', marketplaces)
    
    conn.commit()
    conn.close()

# ============================================
# FUNÇÕES DE BUSCA NO BANCO
# ============================================

def buscar_ncm(codigo_ncm):
    """Busca informações do NCM no banco"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ncm WHERE codigo = ?', (codigo_ncm,))
    resultado = c.fetchone()
    conn.close()
    return resultado

def buscar_icms(uf_origem, uf_destino):
    """Busca alíquotas de ICMS entre UFs"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    c.execute('''SELECT aliquota_interna, aliquota_interestadual, aliquota_fcp, calcula_difal 
                 FROM icms_uf 
                 WHERE uf_origem = ? AND uf_destino = ?''', (uf_origem, uf_destino))
    resultado = c.fetchone()
    conn.close()
    return resultado

def buscar_marketplace(nome):
    """Busca configurações do marketplace"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    c.execute('SELECT * FROM marketplace WHERE nome = ?', (nome,))
    resultado = c.fetchone()
    conn.close()
    return resultado

def listar_ncms():
    """Lista todos os NCMs cadastrados"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    c.execute('SELECT codigo, descricao FROM ncm ORDER BY descricao')
    resultados = c.fetchall()
    conn.close()
    return resultados

def listar_marketplaces():
    """Lista todos os marketplaces"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    c.execute('SELECT nome FROM marketplace WHERE ativo = 1 ORDER BY nome')
    resultados = c.fetchall()
    conn.close()
    return [r[0] for r in resultados]

def cadastrar_ncm_customizado(codigo, descricao, pis, cofins, ipi):
    """Cadastra um NCM novo"""
    conn = sqlite3.connect('regras_tributarias.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO ncm (codigo, descricao, aliquota_pis, aliquota_cofins, aliquota_ipi) 
                     VALUES (?, ?, ?, ?, ?)''', (codigo, descricao, pis, cofins, ipi))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# ============================================
# INICIALIZAR BANCO
# ============================================

inicializar_banco()

# ============================================
# INTERFACE
# ============================================

st.title("🤖 Calculadora INTELIGENTE de Precificação")
st.subheader("Com Base de Dados Tributária Automática")

st.info("✨ **Sistema Inteligente:** Basta informar o NCM e a UF de destino - o sistema busca AUTOMATICAMENTE todas as regras tributárias!")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)
    st.title("📊 Menu")
    pagina = st.radio("Navegação:", 
                     ["🤖 Calculadora Automática", 
                      "📝 Cadastrar NCM", 
                      "📚 Base de Dados",
                      "ℹ️ Como Funciona"])
    
    st.markdown("---")
    st.success("""
    **✨ Sistema Inteligente**  
    Regras tributárias automáticas!
    """)

# ============================================
# PÁGINA: CALCULADORA AUTOMÁTICA
# ============================================

if pagina == "🤖 Calculadora Automática":
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📦 Dados do Produto")
        
        # NCM com busca
        ncms_disponiveis = listar_ncms()
        ncm_opcoes = [f"{ncm[0]} - {ncm[1]}" for ncm in ncms_disponiveis]
        
        ncm_selecionado = st.selectbox(
            "🔍 Selecione o NCM do Produto",
            [""] + ncm_opcoes,
            help="Escolha da lista ou cadastre um novo na aba 'Cadastrar NCM'"
        )
        
        if ncm_selecionado:
            ncm_codigo = ncm_selecionado.split(" - ")[0]
            dados_ncm = buscar_ncm(ncm_codigo)
            
            if dados_ncm:
                st.success(f"✅ NCM encontrado: {dados_ncm[1]}")
                
                with st.expander("📋 Regras Tributárias do NCM"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("PIS", f"{dados_ncm[2]}%")
                        st.metric("COFINS", f"{dados_ncm[3]}%")
                    with col_b:
                        st.metric("IPI", f"{dados_ncm[4]}%")
                        st.metric("Gera Crédito", "✅ Sim" if dados_ncm[5] else "❌ Não")
        
        # Custos do produto
        st.subheader("💰 Custos")
        
        col3, col4 = st.columns(2)
        with col3:
            produto_nome = st.text_input("Nome do Produto (opcional)", "")
            custo_aquisicao = st.number_input("Custo de Aquisição (R$)", min_value=0.0, value=100.0, step=1.0)
        
        with col4:
            outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, value=19.0, step=1.0,
                                           help="Frete, armazenagem, despachante, etc")
        
        # IPI e Créditos
        with st.expander("🔧 Ajustes de Impostos (Opcional)"):
            col5, col6 = st.columns(2)
            with col5:
                st.markdown("**Impostos que viram CUSTO:**")
                ipi_nao_recuperavel = st.number_input("IPI não recuperável (R$)", min_value=0.0, value=15.0, step=0.1)
            
            with col6:
                st.markdown("**Créditos Tributários:**")
                credito_icms = st.number_input("Crédito ICMS (R$)", min_value=0.0, value=18.0, step=0.1)
                credito_pis = st.number_input("Crédito PIS (R$)", min_value=0.0, value=1.65, step=0.01)
                credito_cofins = st.number_input("Crédito COFINS (R$)", min_value=0.0, value=7.60, step=0.01)
        
        # Calcular custo total
        custo_total = (
            custo_aquisicao 
            + ipi_nao_recuperavel
            + outros_custos
            - credito_icms
            - credito_pis
            - credito_cofins
        )
        
        st.success(f"✅ **Custo Total Unitário: R$ {custo_total:.2f}**")
    
    with col2:
        st.header("🎯 Venda")
        
        # Origem (automático - pode ser configurável)
        uf_origem = st.selectbox("UF Origem", ["SP", "RJ", "MG", "RS", "BA", "PR", "SC"], index=0)
        
        # Destino
        uf_destino = st.selectbox("UF Destino", 
                                 ["SP", "RJ", "MG", "RS", "BA", "PR", "SC", "PE", "CE", "GO", "AM", "DF"],
                                 index=1)
        
        # Tipo de cliente
        tipo_cliente = st.radio("Cliente", ["Consumidor Final", "Contribuinte ICMS"])
        
        # Marketplace
        marketplaces = listar_marketplaces()
        marketplace_selecionado = st.selectbox("Marketplace", marketplaces)
        
        # Margem
        margem_alvo = st.slider("Margem Desejada (%)", 0.0, 100.0, 20.0, 0.5)
        
        st.markdown("---")
        
        # Botão calcular
        calcular = st.button("🚀 CALCULAR PREÇO", type="primary", use_container_width=True)
    
    # ============================================
    # CÁLCULO AUTOMÁTICO
    # ============================================
    
    if calcular:
        if not ncm_selecionado:
            st.error("❌ Selecione um NCM primeiro!")
        else:
            with st.spinner("🤖 Buscando regras tributárias automaticamente..."):
                
                # Buscar dados do NCM
                dados_ncm = buscar_ncm(ncm_codigo)
                aliq_pis = dados_ncm[2]
                aliq_cofins = dados_ncm[3]
                
                # Buscar dados de ICMS
                dados_icms = buscar_icms(uf_origem, uf_destino)
                
                if dados_icms:
                    aliq_icms_interna = dados_icms[0]
                    aliq_icms_inter = dados_icms[1]
                    aliq_fcp = dados_icms[2]
                    calcula_difal = dados_icms[3]
                    
                    # Se for mesmo estado, usar alíquota interna
                    if uf_origem == uf_destino:
                        aliq_icms = aliq_icms_interna
                        aliq_difal = 0.0
                        aliq_fcp_final = 0.0
                    else:
                        aliq_icms = aliq_icms_inter
                        if tipo_cliente == "Consumidor Final" and calcula_difal:
                            aliq_difal = aliq_icms_interna - aliq_icms_inter
                            aliq_fcp_final = aliq_fcp
                        else:
                            aliq_difal = 0.0
                            aliq_fcp_final = 0.0
                else:
                    st.warning(f"⚠️ Rota {uf_origem} → {uf_destino} não cadastrada. Usando padrões.")
                    aliq_icms = 12.0 if uf_origem != uf_destino else 18.0
                    aliq_difal = 0.0
                    aliq_fcp_final = 0.0
                
                # Buscar dados do marketplace
                dados_marketplace = buscar_marketplace(marketplace_selecionado)
                if dados_marketplace:
                    comissao = dados_marketplace[2]
                    taxa_fixa = dados_marketplace[3]
                    taxa_antecipacao = dados_marketplace[4]
                    taxa_gateway = dados_marketplace[5]
                else:
                    comissao = 0.0
                    taxa_fixa = 0.0
                    taxa_antecipacao = 0.0
                    taxa_gateway = 0.0
                
                # CALCULAR PREÇO
                D = Decimal
                
                custo = D(str(custo_total))
                custos_fixos = D(str(taxa_fixa))
                
                pct_margem = D(str(margem_alvo)) / D('100')
                pct_tributos = (D(str(aliq_pis)) + D(str(aliq_cofins)) + D(str(aliq_icms)) + 
                               D(str(aliq_difal)) + D(str(aliq_fcp_final))) / D('100')
                pct_custos_variaveis = (D(str(comissao)) + D(str(taxa_antecipacao)) + D(str(taxa_gateway))) / D('100')
                
                total_pct = pct_margem + pct_tributos + pct_custos_variaveis
                
                preco_venda = (custo + custos_fixos) / (D('1') - total_pct)
                
                # Detalhamento
                valor_pis = preco_venda * (D(str(aliq_pis)) / D('100'))
                valor_cofins = preco_venda * (D(str(aliq_cofins)) / D('100'))
                valor_icms = preco_venda * (D(str(aliq_icms)) / D('100'))
                valor_difal = preco_venda * (D(str(aliq_difal)) / D('100'))
                valor_fcp = preco_venda * (D(str(aliq_fcp_final)) / D('100'))
                
                total_tributos = valor_pis + valor_cofins + valor_icms + valor_difal + valor_fcp
                
                valor_comissao = preco_venda * (D(str(comissao)) / D('100'))
                valor_antecipacao = preco_venda * (D(str(taxa_antecipacao)) / D('100'))
                valor_gateway = preco_venda * (D(str(taxa_gateway)) / D('100'))
                
                total_custos_canal = valor_comissao + D(str(taxa_fixa)) + valor_antecipacao + valor_gateway
                
                margem_contribuicao = preco_venda - custo - total_tributos - total_custos_canal
                margem_percentual = (margem_contribuicao / preco_venda) * D('100')
                
                irpj_csll = margem_contribuicao * D('0.34')
                lucro_liquido = margem_contribuicao - irpj_csll
                lucro_liquido_pct = (lucro_liquido / preco_venda) * D('100')
                
                # MOSTRAR RESULTADOS
                st.markdown("---")
                st.markdown("## 🎉 RESULTADO")
                
                st.markdown(f'<p class="big-font">R$ {float(preco_venda):.2f}</p>', unsafe_allow_html=True)
                
                margem_float = float(margem_percentual)
                if margem_float >= 20:
                    st.markdown('<div class="success-card"><h3>🟢 MARGEM SAUDÁVEL</h3></div>', unsafe_allow_html=True)
                elif margem_float >= 10:
                    st.markdown('<div class="warning-card"><h3>🟡 MARGEM BAIXA - ATENÇÃO</h3></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-card"><h3>🔴 MARGEM CRÍTICA</h3></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Regras aplicadas
                with st.expander("🤖 Regras Tributárias Aplicadas AUTOMATICAMENTE"):
                    col_r1, col_r2, col_r3 = st.columns(3)
                    with col_r1:
                        st.markdown("**📋 Do NCM:**")
                        st.write(f"• PIS: {aliq_pis}%")
                        st.write(f"• COFINS: {aliq_cofins}%")
                    with col_r2:
                        st.markdown(f"**🗺️ Da Rota {uf_origem}→{uf_destino}:**")
                        st.write(f"• ICMS: {aliq_icms}%")
                        if aliq_difal > 0:
                            st.write(f"• DIFAL: {aliq_difal}%")
                        if aliq_fcp_final > 0:
                            st.write(f"• FCP: {aliq_fcp_final}%")
                    with col_r3:
                        st.markdown(f"**🏪 Do {marketplace_selecionado}:**")
                        st.write(f"• Comissão: {comissao}%")
                        if taxa_fixa > 0:
                            st.write(f"• Taxa Fixa: R$ {taxa_fixa:.2f}")
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📦 Custo", f"R$ {float(custo):.2f}", 
                             f"{float(custo/preco_venda*100):.1f}%")
                
                with col2:
                    st.metric("💸 Tributos", f"R$ {float(total_tributos):.2f}",
                             f"{float(total_tributos/preco_venda*100):.1f}%")
                
                with col3:
                    st.metric("🏪 Custos Canal", f"R$ {float(total_custos_canal):.2f}",
                             f"{float(total_custos_canal/preco_venda*100):.1f}%")
                
                st.markdown("---")
                
                col4, col5 = st.columns(2)
                
                with col4:
                    st.metric("📈 Margem de Contribuição", f"R$ {float(margem_contribuicao):.2f}",
                             f"{float(margem_percentual):.2f}%")
                
                with col5:
                    st.metric("💰 Lucro Líquido Estimado", f"R$ {float(lucro_liquido):.2f}",
                             f"{float(lucro_liquido_pct):.2f}%")

# ============================================
# PÁGINA: CADASTRAR NCM
# ============================================

elif pagina == "📝 Cadastrar NCM":
    st.header("📝 Cadastrar Novo NCM")
    
    st.info("Adicione NCMs personalizados à base de dados")
    
    with st.form("form_ncm"):
        col1, col2 = st.columns(2)
        
        with col1:
            novo_ncm = st.text_input("Código NCM (8 dígitos)", max_chars=8)
            descricao_ncm = st.text_input("Descrição do Produto")
        
        with col2:
            pis_ncm = st.number_input("Alíquota PIS (%)", 0.0, 100.0, 1.65, 0.01)
            cofins_ncm = st.number_input("Alíquota COFINS (%)", 0.0, 100.0, 7.60, 0.01)
            ipi_ncm = st.number_input("Alíquota IPI (%)", 0.0, 100.0, 0.0, 0.1)
        
        submitted = st.form_submit_button("➕ Cadastrar NCM")
        
        if submitted:
            if len(novo_ncm) == 8 and descricao_ncm:
                sucesso = cadastrar_ncm_customizado(novo_ncm, descricao_ncm, pis_ncm, cofins_ncm, ipi_ncm)
                if sucesso:
                    st.success(f"✅ NCM {novo_ncm} cadastrado com sucesso!")
                else:
                    st.error("❌ NCM já existe ou erro ao cadastrar")
            else:
                st.error("❌ Preencha todos os campos corretamente")

# ============================================
# PÁGINA: BASE DE DADOS
# ============================================

elif pagina == "📚 Base de Dados":
    st.header("📚 Base de Dados Tributária")
    
    tab1, tab2, tab3 = st.tabs(["📋 NCMs", "🗺️ ICMS", "🏪 Marketplaces"])
    
    with tab1:
        st.subheader("NCMs Cadastrados")
        ncms = listar_ncms()
        st.dataframe(ncms, column_config={
            0: "Código NCM",
            1: "Descrição"
        }, hide_index=True)
    
    with tab2:
        st.subheader("Rotas de ICMS Cadastradas")
        conn = sqlite3.connect('regras_tributarias.db')
        icms_df = st.dataframe(conn.execute('SELECT uf_origem as Origem, uf_destino as Destino, aliquota_interestadual as "ICMS %", aliquota_fcp as "FCP %", calcula_difal as "DIFAL?" FROM icms_uf').fetchall())
        conn.close()
    
    with tab3:
        st.subheader("Marketplaces Cadastrados")
        conn = sqlite3.connect('regras_tributarias.db')
        mkt_df = st.dataframe(conn.execute('SELECT nome as Nome, comissao_padrao as "Comissão %", taxa_fixa as "Taxa Fixa", taxa_antecipacao as "Antecipação %", taxa_gateway as "Gateway %" FROM marketplace WHERE ativo = 1').fetchall())
        conn.close()

# ============================================
# PÁGINA: COMO FUNCIONA
# ============================================

else:
    st.header("ℹ️ Como Funciona o Sistema Inteligente")
    
    st.markdown("""
    ## 🤖 Inteligência Automática
    
    Este sistema possui uma **base de dados tributária** que elimina 90% do trabalho manual!
    
    ### ✨ O que o sistema faz automaticamente:
    
    1. **Busca PIS/COFINS pelo NCM**
       - Cada NCM tem suas alíquotas pré-configuradas
       - 1,65% PIS e 7,60% COFINS (não cumulativo) para maioria
       
    2. **Busca ICMS pela rota (UF Origem → UF Destino)**
       - Alíquotas interestaduais (7% ou 12%)
       - Alíquotas internas (18% geralmente)
       - DIFAL automático para consumidor final
       - FCP por estado
       
    3. **Busca comissões do Marketplace**
       - Mercado Livre: 16% + R$ 5,00
       - Shopee: 14%
       - Amazon: 15%
       - E outros...
    
    ### 📊 Você só precisa informar:
    
    - ✅ NCM do produto (escolhe da lista)
    - ✅ UF de destino
    - ✅ Tipo de cliente (consumidor ou contribuinte)
    - ✅ Marketplace
    - ✅ Custo do produto
    - ✅ Margem desejada
    
    **O resto é AUTOMÁTICO!** 🎉
    
    ### 🔧 Personalizável
    
    - Cadastre novos NCMs na aba "Cadastrar NCM"
    - Ajuste créditos tributários se necessário
    - Base de dados SQLite local (portátil)
    
    ### ⚠️ Importante
    
    - Base de dados vem com regras padrão
    - Sempre valide com seu contador
    - Legislação muda - mantenha atualizado
    - Sistema é ferramenta de APOIO
    """)
    
    st.success("💡 **Vantagem:** Precificação em segundos sem precisar lembrar de alíquotas!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 Sistema Inteligente de Precificação | Versão 2.0 com Base de Dados Automática</p>
    <p>⚠️ Sempre valide com seu contador antes de aplicar preços!</p>
</div>
""", unsafe_allow_html=True)
