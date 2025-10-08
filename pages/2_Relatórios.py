import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
from src.utils.recuperar_dados_bd import carregar_dados
from src.utils.autenticacao import exigir_login

# Exigir login para acessar esta página
exigir_login(["admin", "analista", "viewer"])

# Configuração da página
st.set_page_config(
    page_title="Relatórios Comerciais",
    page_icon="📊",
    layout="wide"
)

# Título e descrição
st.title("📊 Dashboard Comercial")
st.markdown("### Análise de Importação e Exportação do Brasil")

# Configuração da sidebar
st.sidebar.markdown("<h3 style='margin-bottom:0'>🔍 Filtros</h3>", unsafe_allow_html=True)

# Filtro de tipo de operação
tipo_operacao = st.sidebar.selectbox('**Tipo de Dados**', ['Importação', 'Exportação', 'Ambos'])

# Filtro de período
hoje = datetime.now()
anos = list(range(1997, hoje.year + 1))
meses = list(range(1, 13))

# Seletor personalizado
st.sidebar.markdown("**Período**")
c1, c2 = st.sidebar.columns(2)
mes_ini_sel = c1.selectbox("Mês inicial", meses, format_func=lambda m: f"{m:02d}", index=hoje.month-2)
ano_ini_sel = c2.selectbox("Ano inicial", anos, index=len(anos)-1)

c3, c4 = st.sidebar.columns(2)
mes_fim_sel = c3.selectbox("Mês final", meses, format_func=lambda m: f"{m:02d}", index=hoje.month-2)
ano_fim_sel = c4.selectbox("Ano final", anos, index=len(anos)-1)

st.sidebar.markdown("---")

# Função para carregar dados
@st.cache_data(ttl=600, show_spinner="Consultando dados...")
def carregar_dados_dashboard(tipo_operacao, mes_ini, mes_fim, ano_ini, ano_fim):
    if tipo_operacao == "Ambos":
        df_imp = carregar_dados("Importacao", mes_ini, mes_fim, ano_ini, ano_fim)
        df_imp["Tipo"] = "Importação"
        
        df_exp = carregar_dados("Exportacao", mes_ini, mes_fim, ano_ini, ano_fim)
        df_exp["Tipo"] = "Exportação"
        
        # Concatenar os dataframes
        df = pd.concat([df_imp, df_exp])
    else:
        tipo_sql = "Importacao" if tipo_operacao == "Importação" else "Exportacao"
        df = carregar_dados(tipo_sql, mes_ini, mes_fim, ano_ini, ano_fim)
        df["Tipo"] = tipo_operacao
    
    # Criar coluna de data para facilitar análises temporais
    df["Data"] = pd.to_datetime(df["year"].astype(str) + "-" + df["monthNumber"].astype(str) + "-01")
    
    return df

# Botão para carregar dados
if st.sidebar.button("Gerar Relatórios", type="primary"):
    # Validar período
    ini_key = int(ano_ini_sel) * 100 + int(mes_ini_sel)
    fim_key = int(ano_fim_sel) * 100 + int(mes_fim_sel)
    
    if ini_key > fim_key:
        st.sidebar.error("Período inválido: Data Inicial maior que Data Final")
        st.stop()
    
    # Carregar dados
    df = carregar_dados_dashboard(tipo_operacao, mes_ini_sel, mes_fim_sel, ano_ini_sel, ano_fim_sel)
    
    if df.empty:
        st.error("Não foram encontrados dados para o período selecionado.")
        st.stop()
    
    # Exibir métricas principais
    st.sidebar.success(f"Dados carregados com sucesso! ({len(df)} registros)")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valor_total = df["metricFOB"].sum()
        st.metric("Valor Total (USD)", f"${valor_total:,.2f}")
    
    with col2:
        paises = df["country"].nunique()
        st.metric("Países", f"{paises}")
    
    with col3:
        produtos = df["chapter"].nunique()
        st.metric("Categorias de Produtos", f"{produtos}")
    
    # Criar abas para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["Tendências Temporais", "Análise Geográfica", "Parceiros Comerciais"])
    
    with tab1:
        st.subheader("Evolução Temporal")
        
        # Gráfico de tendência mensal
        df_mensal = df.groupby([pd.Grouper(key="Data", freq="ME"), "Tipo"])["metricFOB"].sum().reset_index()
        df_mensal["Mês/Ano"] = df_mensal["Data"].dt.strftime("%b/%Y")
        
        fig_tendencia = px.line(
            df_mensal, 
            x="Mês/Ano", 
            y="metricFOB", 
            color="Tipo",
            title="Evolução Mensal do Comércio Exterior",
            labels={"metricFOB": "Valor FOB (USD)", "Mês/Ano": ""},
            markers=True
        )
        
        fig_tendencia.update_layout(
            xaxis_title="",
            yaxis_title="Valor FOB (USD)",
            legend_title="Operação",
            height=500
        )
        
        st.plotly_chart(fig_tendencia, use_container_width=True)
        
        # Gráfico de barras por categoria de produto
        col1, col2 = st.columns(2)
        
        with col1:
            df_produtos = df.groupby(["chapter", "Tipo"])["metricFOB"].sum().reset_index()
            df_produtos = df_produtos.sort_values("metricFOB", ascending=False).head(10)
            
            fig_produtos = px.bar(
                df_produtos,
                x="chapter",
                y="metricFOB",
                color="Tipo",
                title="Top 10 Categorias de Produtos",
                labels={"chapter": "Categoria", "metricFOB": "Valor FOB (USD)"}
            )
            
            fig_produtos.update_layout(
                xaxis_title="Categoria de Produto",
                yaxis_title="Valor FOB (USD)",
                legend_title="Operação"
            )
            
            st.plotly_chart(fig_produtos, use_container_width=True)
        
        with col2:
            # Gráfico de comparação anual
            df_anual = df.groupby([df["Data"].dt.year, "Tipo"])["metricFOB"].sum().reset_index()
            df_anual.rename(columns={"Data": "Ano"}, inplace=True)
            
            fig_anual = px.bar(
                df_anual,
                x="Ano",
                y="metricFOB",
                color="Tipo",
                title="Comparação Anual",
                barmode="group",
                labels={"Ano": "", "metricFOB": "Valor FOB (USD)"}
            )
            
            fig_anual.update_layout(
                xaxis_title="Ano",
                yaxis_title="Valor FOB (USD)",
                legend_title="Operação"
            )
            
            st.plotly_chart(fig_anual, use_container_width=True)
    
    with tab2:
        st.subheader("Distribuição Geográfica")
        
        # Mapa de calor por país
        df_paises = df.groupby(["country", "Tipo"])["metricFOB"].sum().reset_index()
        
        fig_mapa = px.choropleth(
            df_paises,
            locations="country",
            locationmode="country names",
            color="metricFOB",
            hover_name="country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Distribuição Global de Comércio",
            labels={"metricFOB": "Valor FOB (USD)"}
        )
        
        fig_mapa.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type="natural earth"
            )
        )
        
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # Gráficos por região
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 países
            df_top_paises = df_paises.sort_values("metricFOB", ascending=False).head(10)
            
            fig_top_paises = px.bar(
                df_top_paises,
                x="country",
                y="metricFOB",
                color="Tipo",
                title="Top 10 Países",
                labels={"country": "País", "metricFOB": "Valor FOB (USD)"}
            )
            
            fig_top_paises.update_layout(
                xaxis_title="País",
                yaxis_title="Valor FOB (USD)",
                legend_title="Operação"
            )
            
            st.plotly_chart(fig_top_paises, use_container_width=True)
        
        with col2:
            # Distribuição por bloco econômico
            df_blocos = df.groupby(["economicBlock", "Tipo"])["metricFOB"].sum().reset_index()
            df_blocos = df_blocos.sort_values("metricFOB", ascending=False).head(10)
            
            fig_blocos = px.pie(
                df_blocos,
                values="metricFOB",
                names="economicBlock",
                title="Distribuição por Bloco Econômico",
                hole=0.4
            )
            
            fig_blocos.update_layout(
                legend_title="Bloco Econômico"
            )
            
            st.plotly_chart(fig_blocos, use_container_width=True)
    
    with tab3:
        st.subheader("Análise de Parceiros Comerciais")
        
        # Matriz de correlação entre países
        df_matriz = df.pivot_table(
            index="country",
            columns="Tipo",
            values="metricFOB",
            aggfunc="sum"
        ).fillna(0)
        
        # Calcular balança comercial
        if "Importação" in df_matriz.columns and "Exportação" in df_matriz.columns:
            df_matriz["Balança Comercial"] = df_matriz["Exportação"] - df_matriz["Importação"]
        
        # Selecionar top 15 países por volume total
        df_matriz["Total"] = df_matriz.sum(axis=1)
        df_matriz = df_matriz.sort_values("Total", ascending=False).head(15)
        
        # Gráfico de barras horizontais para balança comercial
        if "Balança Comercial" in df_matriz.columns:
            df_balanca = df_matriz.reset_index()[["country", "Balança Comercial"]]
            
            fig_balanca = px.bar(
                df_balanca,
                x="Balança Comercial",
                y="country",
                orientation="h",
                title="Balança Comercial por País (Top 15)",
                labels={"country": "País", "Balança Comercial": "Valor FOB (USD)"},
                color="Balança Comercial",
                color_continuous_scale=["red", "white", "green"]
            )
            
            fig_balanca.update_layout(
                xaxis_title="Balança Comercial (USD)",
                yaxis_title="",
                height=600
            )
            
            st.plotly_chart(fig_balanca, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("Detalhamento por País")
        
        df_detalhado = df_matriz.reset_index()
        df_detalhado = df_detalhado.drop(columns=["Total"], errors="ignore")
        
        # Formatar valores monetários
        for col in df_detalhado.columns:
            if col != "country":
                df_detalhado[col] = df_detalhado[col].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            df_detalhado,
            hide_index=True,
            use_container_width=True
        )
else:
    # Mensagem inicial
    st.info("👈 Selecione os filtros desejados e clique em 'Gerar Relatórios' para visualizar os dashboards.")