# 🤖 VERSÃO INTELIGENTE - COM BASE DE DADOS AUTOMÁTICA!

## ✨ NOVIDADE: Sistema Busca TUDO Automaticamente!

Esta versão tem um **banco de dados SQLite** com regras tributárias pré-cadastradas.

---

## 🎯 O QUE MUDOU?

### ❌ Versão Anterior:
- Você precisava digitar TODAS as alíquotas
- PIS, COFINS, ICMS, DIFAL, FCP...
- Comissões de marketplace...
- MUITO trabalho manual!

### ✅ Versão Nova (INTELIGENTE):
- Você só escolhe o **NCM** da lista
- Você só escolhe a **UF destino**
- **Sistema busca TUDO automaticamente!**
- PIS, COFINS, ICMS, DIFAL, FCP, comissões...
- **90% menos trabalho!**

---

## 🗄️ BASE DE DADOS INCLUSA

O sistema já vem com:

### 📋 NCMs Pré-Cadastrados:
- 85171231 - Smartphones
- 64022000 - Calçados
- 61091000 - Camisetas
- 84713012 - Notebooks
- 33049900 - Cosméticos
- 94036000 - Móveis
- E mais...

Cada NCM tem:
- Alíquota PIS (geralmente 1,65%)
- Alíquota COFINS (geralmente 7,60%)
- Se gera crédito ou não

### 🗺️ Rotas de ICMS:
Principais rotas entre estados:
- SP → RJ, MG, RS, BA, PR, SC, PE, CE, GO, AM, DF
- RJ → SP, MG, RS, BA
- MG → SP, RJ, RS
- RS → SP, SC, PR
- BA → SP, RJ

Cada rota tem:
- ICMS interestadual (7% ou 12%)
- ICMS interno (18%)
- FCP quando aplicável (2%)
- Cálculo automático de DIFAL

### 🏪 Marketplaces:
- Mercado Livre: 16% + R$ 5,00
- Shopee: 14%
- Amazon: 15%
- Magalu: 18%
- Venda Direta: 0%

---

## 🚀 COMO USAR

### 1. Instale
```bash
pip install streamlit
```

### 2. Rode
```bash
streamlit run precificacao_automatica.py
```

### 3. Use!
1. **Escolha o NCM** da lista dropdown
2. **Escolha UF de destino**
3. **Escolha marketplace**
4. Informe apenas o **custo** e **margem desejada**
5. Clique em **"CALCULAR"**

**Pronto!** Sistema busca todas as regras automaticamente! 🎉

---

## ✨ EXEMPLO PRÁTICO

**Antes (Manual):**
```
Digite PIS: 1.65
Digite COFINS: 7.60
Digite ICMS: 12
Digite DIFAL: 6
Digite FCP: 2
Digite comissão ML: 16
Digite taxa fixa: 5
...
```

**Agora (Automático):**
```
Selecione NCM: Smartphones
Selecione UF: Rio de Janeiro
Selecione Marketplace: Mercado Livre
Custo: R$ 100
Margem: 20%
[CALCULAR] ← Um clique!
```

Sistema busca automaticamente:
- ✅ PIS: 1,65%
- ✅ COFINS: 7,60%
- ✅ ICMS: 12%
- ✅ DIFAL: 6%
- ✅ FCP: 2%
- ✅ Comissão: 16%
- ✅ Taxa fixa: R$ 5,00

**Resultado: R$ 379,99** 🎯

---

## 📝 CADASTRAR NOVOS NCMs

Tem um NCM que não está na base?

1. Vá na aba **"📝 Cadastrar NCM"**
2. Digite o código (8 dígitos)
3. Digite descrição
4. Configure alíquotas
5. Clique em **"Cadastrar"**

Pronto! Agora ele aparece na lista!

---

## 🔍 VER BASE DE DADOS

Na aba **"📚 Base de Dados"** você vê:
- Todos os NCMs cadastrados
- Todas as rotas de ICMS
- Todos os marketplaces

---

## 💾 BANCO DE DADOS

O sistema cria um arquivo: **regras_tributarias.db**

É um banco SQLite:
- ✅ Leve (poucos KB)
- ✅ Portátil (leva pra qualquer PC)
- ✅ Sem precisar servidor
- ✅ Rápido
- ✅ Confiável

**Importante:** Leve o arquivo .db junto com o .py!

---

## 🆚 COMPARAÇÃO

| Recurso | Versão Manual | Versão Automática |
|---------|---------------|-------------------|
| **Preencher alíquotas** | ❌ Todas (10+ campos) | ✅ Nenhuma |
| **Escolher NCM** | ❌ Digitar código | ✅ Selecionar da lista |
| **Alíquotas ICMS** | ❌ Consultar tabela | ✅ Automático |
| **DIFAL** | ❌ Calcular manual | ✅ Automático |
| **Comissões** | ❌ Lembrar de cada | ✅ Automático |
| **Tempo para calcular** | ⏱️ 5 minutos | ⏱️ 30 segundos |

---

## 🎓 RECURSOS

### ✅ Tem nesta versão:
- Base de dados SQLite integrada
- NCMs pré-cadastrados
- Rotas ICMS pré-cadastradas
- Marketplaces pré-cadastrados
- Busca automática de regras
- Cadastro de novos NCMs
- Interface limpa e simples
- Cálculos precisos (Decimal)
- Exportação de resultados

### 🔮 Futuras melhorias:
- Importar NCMs de CSV
- Atualização automática de alíquotas
- Histórico de cálculos
- Comparação entre marketplaces
- API REST
- Multi-usuário

---

## ⚠️ IMPORTANTE

**Este sistema continua sendo ferramenta de APOIO!**

- ✅ Base de dados vem com regras padrão (2024/2025)
- ✅ Pode precisar ajustes para casos específicos
- ✅ Legislação muda - mantenha atualizado
- ❌ NÃO substitui contador
- ❌ Sempre valide antes de usar em produção

---

## 🔧 CUSTOMIZAÇÃO

Você pode:
- Adicionar novos NCMs
- Editar alíquotas no banco (SQLite Browser)
- Adicionar novas rotas de ICMS
- Adicionar novos marketplaces
- Ajustar para casos especiais

O banco é **seu** - customize à vontade!

---

## 📥 DOWNLOAD

Arquivo único: `precificacao_automatica.py`

Dependências:
```bash
pip install streamlit
```

Só isso! O SQLite já vem no Python.

---

## 🎉 RESUMO

**Antes:** 10 campos para preencher, 5 minutos  
**Agora:** 4 campos para preencher, 30 segundos

**Diferença:** Sistema inteligente com base de dados! 🤖

---

**🚀 Versão:** 2.0 Inteligente  
**📅 Data:** Novembro 2025  
**✨ Destaque:** Base de dados automática!  

Muito mais prático! 🎯
