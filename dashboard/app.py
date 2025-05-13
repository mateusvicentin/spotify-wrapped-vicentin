import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import sys

# Adiciona raiz ao path para importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações internas
from data_ingestion.extract_spotify_data import extrair_dados
from data_processing.transform_data import transformar_dados

# Configuração da página
st.set_page_config(page_title="Meu Spotify Wrapped", page_icon="🎷", layout="wide")
st.title("🎷 Meu Spotify Wrapped - Mês Atual")

# Botão de atualização
if st.button("🔄 Atualizar Dados"):
    with st.spinner("Atualizando dados..."):
        extrair_dados()
        transformar_dados()
        st.success("✅ Dados atualizados com sucesso!")

# Verifica arquivos essenciais
arquivos = [
    "data/cleaned_tracks.csv", "data/top_tracks.csv", "data/top_artists.csv",
    "data/top_genres.csv", "data/hourly_distribution.csv",
    "data/daily_trend.csv", "data/weekday_distribution.csv"
]
if not all(os.path.exists(arq) for arq in arquivos):
    st.warning("🚧 Os dados ainda não foram gerados. Clique em 'Atualizar Dados'.")
    st.stop()

# Carregamento dos dados
df = pd.read_csv("data/cleaned_tracks.csv")
top_tracks = pd.read_csv("data/top_tracks.csv")
top_artists = pd.read_csv("data/top_artists.csv")
top_genres = pd.read_csv("data/top_genres.csv")
hourly = pd.read_csv("data/hourly_distribution.csv")
daily = pd.read_csv("data/daily_trend.csv")
weekday = pd.read_csv("data/weekday_distribution.csv")

# Conversões
df["date"] = pd.to_datetime(df["date"])
df["played_at"] = pd.to_datetime(df["played_at"])
mes_atual = datetime.now().month
df_mes = df[df["date"].dt.month == mes_atual]

# 🎛️ Filtros
with st.sidebar:
    st.header("🎧 Filtros")
    artistas = df_mes["artist_name"].unique()
    artista_sel = st.selectbox("🎼 Artista", ["Todos"] + sorted(artistas))
    if artista_sel != "Todos":
        df_mes = df_mes[df_mes["artist_name"] == artista_sel]
    min_date = df_mes["date"].min()
    max_date = df_mes["date"].max()
    data_ini, data_fim = st.date_input("🗓️ Período", [min_date, max_date])
    df_mes = df_mes[(df_mes["date"] >= pd.to_datetime(data_ini)) & (df_mes["date"] <= pd.to_datetime(data_fim))]

# 📊 Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("🎵 Faixas Únicas", len(df_mes))
col2.metric("⏱️ Tempo Médio", f"{df_mes['duration_min'].mean():.2f} min")
col3.metric("🗓️ Média Diária", f"{len(df_mes)/df_mes['date'].nunique():.1f} faixas/dia")

tempo_total = df_mes["duration_min"].sum()
st.success(f"🕒 Tempo total ouvido: {int(tempo_total // 60)}h {int(tempo_total % 60)}min")

st.markdown("---")

# 📋 Tabelas principais
top_tracks.columns = ["Música", "Tocadas"]
top_artists.columns = ["Artista", "Tocadas"]
top_genres.columns = ["Estilo", "Tocadas"]

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("🎶 Músicas Mais Escutadas")
    st.dataframe(top_tracks, use_container_width=True, height=400)
with col2:
    st.subheader("🎤 Artistas Mais Escutados")
    st.dataframe(top_artists, use_container_width=True, height=400)
with col3:
    st.subheader("🎧 Estilos Mais Escutados")
    st.dataframe(top_genres, use_container_width=True, height=400)

st.markdown("---")

# 📈 Gráficos
st.subheader("📈 Evolução Diária de Faixas")
fig_daily = px.line(daily, x="date", y="quantidade", markers=True,
                    labels={"date": "Data", "quantidade": "Faixas"},
                    color_discrete_sequence=["#2ecc71"])
fig_daily.update_layout(plot_bgcolor="white", hovermode="x unified")
st.plotly_chart(fig_daily, use_container_width=True)

st.subheader("⏰ Faixas por Hora do Dia")
fig_hour = px.bar(hourly, x="hora", y="quantidade",
                  labels={"hora": "Hora", "quantidade": "Faixas"},
                  color_discrete_sequence=["#2ecc71"])
fig_hour.update_layout(plot_bgcolor="white", xaxis=dict(dtick=1))
st.plotly_chart(fig_hour, use_container_width=True)

st.subheader("📅 Faixas por Dia da Semana")
fig_week = px.bar(weekday, x="weekday", y="quantidade",
                  labels={"weekday": "Dia", "quantidade": "Faixas"},
                  color_continuous_scale="greens")
fig_week.update_layout(plot_bgcolor="white")
st.plotly_chart(fig_week, use_container_width=True)

# 📋 Tabela formatada
st.markdown("---")
st.subheader("📋 Faixas Tocadas no Mês")

df_mes = df_mes.sort_values(by="played_at", ascending=False)
df_limpo = df_mes[["date", "played_at", "track_name", "artist_name", "duration_min", "weekday"]].copy()
df_limpo["played_at"] = df_limpo["played_at"].dt.strftime("%H:%M")
df_limpo["date"] = df_limpo["date"].dt.strftime("%d/%m/%Y")
df_limpo["weekday"] = df_limpo["weekday"].map({
    "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
}).fillna(df_limpo["weekday"])

df_limpo["Duração"] = df_limpo["duration_min"].apply(lambda x: f"{int(x)}:{int(x*60)%60:02d}")
df_limpo = df_limpo.rename(columns={
    "date": "Data", "played_at": "Hora",
    "track_name": "Música", "artist_name": "Artista",
    "weekday": "Dia da Semana"
})[["Data", "Hora", "Dia da Semana", "Música", "Artista", "Duração"]]

df_limpo = df_limpo.drop_duplicates(subset=["Data", "Hora", "Música", "Artista"])
st.dataframe(df_limpo, use_container_width=True)

# 📥 Downloads
st.markdown("### 📥 Baixar Arquivos CSV")
col3, col4, col5 = st.columns(3)
with col3:
    with open("data/cleaned_tracks.csv", "rb") as f:
        st.download_button("🎵 Faixas completas", f, file_name="cleaned_tracks.csv")
with col4:
    with open("data/top_tracks.csv", "rb") as f:
        st.download_button("🎶 Top músicas", f, file_name="top_tracks.csv")
with col5:
    with open("data/top_artists.csv", "rb") as f:
        st.download_button("🎴 Top artistas", f, file_name="top_artists.csv")

st.markdown("---")
st.caption(f"🗓️ Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("🧠 Desenvolvido por Mateus Vicentin")
