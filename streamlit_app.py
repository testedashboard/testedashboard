import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard - Centro Auditivo",
    page_icon="📈",
    layout="wide",
)
####################################

dataset_url = "https://raw.githubusercontent.com/testedashboard/testedashboard/main/info.csv"

# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

list_of_campaigns = pd.unique(df["Campanha"])

colEspaco1, col, colEspaco2 = st.columns([1, 3, 1], gap="small")
with col:
    st.title("Dashboard - Centro Auditivo", anchor=False)

    selected_campaign = st.selectbox("Selecione a campanha", list_of_campaigns, placeholder="Selecione a campanha", label_visibility="collapsed")

    st.header("Taxa de investimento e faturamento", anchor=False)

colEspaco1, colA, colB, colC, colEspaco2 = st.columns([4, 6, 6, 4, 3], gap="small")
colEspaco1, colD, colE, colF, colG, colEspaco2 = st.columns([4, 4, 4, 4, 4, 3], gap="small")


with colA:
    st.metric(
    label="Valor investido",
    value=f'R${float(df[df["Campanha"] == selected_campaign]["Valor investido"].iloc[0]):20,.2f}',
    )

with colB:
    st.metric(
    label="Custo por Click",
    value=f'R${float(df[df["Campanha"] == selected_campaign]["CPC"].iloc[0]):.2f}',
    )

with colC:
    st.metric(
        label="Custo por Aquisição",
        value=f'R${float(df[df["Campanha"] == selected_campaign]["CPA"].iloc[0]):20,.2f}',
    )

with colD:
    st.metric(
    label="Clicks no link",
    value=df[df["Campanha"] == selected_campaign]["Cliques"],
    )



with colE:
    st.metric(
    label="Visualizou Página",
    value="---",
    )

with colF:
    st.metric(
    label="Checkouts",
    value="---",
    )

with colG:
    st.metric(
        label="Aquisições",
        value=int(df[df["Campanha"] == selected_campaign]["Conversões"].iloc[0]),
    )

colEspaco1, colH, colI, colJ, colEspaco2 = st.columns([4, 6, 6, 4, 3], gap="small")

with colI:
    st.metric(
            label="Conversões",
            value=f'{(100 * df[df["Campanha"] == selected_campaign]["Conversões"].iloc[0] / df[df["Campanha"] == selected_campaign]["Cliques"].iloc[0]):.2f}%',
        )

st.write("---")

options = st.multiselect(label="Comparar Campanhas", options=list_of_campaigns)

if len(options) > 0:

    ### Criando colunas para os gráficos
    colGraphA, colGraphB = st.columns(2, gap="large")

    lista_dfs = []
    for item in options:
        lista_dfs.append(df[df["Campanha"] == item])
    result = pd.concat(lista_dfs, axis=0, ignore_index=True, sort=False)

    with colGraphA:
        fig = px.bar(result, x="Campanha", y="Valor investido", color="Campanha", title="Valor investido")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

    with colGraphB:
        fig = px.bar(result, x="Campanha", y="CPC", color="Campanha", title="Custo por Click")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

    ### Criando colunas para os gráficos
    colGraphC, colGraphD = st.columns(2, gap="large")

    with colGraphC:
        fig = px.bar(result, x="Campanha", y="CPA", color="Campanha", title="Custo por Aquisição")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

    with colGraphD:
        result["Porcentagem de conversão"] = 100 * result["Conversões"] / result["Cliques"]
        fig = px.bar(result, x="Campanha", y="Porcentagem de conversão", color="Campanha", title="Porcentagem de conversão")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

st.write("---")

# cliques = df[df["Campanha"] == selected_campaign]["Cliques"].iloc[0]
# conver = df[df["Campanha"] == selected_campaign]["Conversões"].iloc[0]
# data = dict(
#     number=[cliques, cliques/2, conver*2, conver],
#     stage=["Clicks no link", "Visualizou a Página", "Checkouts", "Aquisições"],
# )
#
# fig = px.funnel(data, x='number', y='stage')
# st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
