import pandas as pd
import duckdb
from datetime import datetime

# Conectar ao banco
con = duckdb.connect("data/spotify.duckdb")

# Detecta o mês atual
hoje = datetime.now()
ano_mes = hoje.strftime("%Y-%m")

# Consulta dados do mês atual
query = f"""
SELECT 
    track_id,
    track_name,
    artist_id,
    artist_name,
    all_artists,
    genres,
    popularity,
    played_at,
    CAST(played_at AS DATE) AS date,
    EXTRACT(HOUR FROM played_at) AS hour,
    duration_ms / 60000.0 AS duration_min
FROM recent_tracks
WHERE STRFTIME(played_at, '%Y-%m') = '{ano_mes}'
"""

df = con.execute(query).fetchdf()

if df.empty:
    print("⚠️ Nenhum dado encontrado para o mês atual.")
    exit()

# Conversões
df["date"] = pd.to_datetime(df["date"])
df["weekday"] = df["date"].dt.day_name()

# 🎧 Faixas
tempo_total = df["duration_min"].sum()
tempo_medio = df["duration_min"].mean()
dias_unicos = df["date"].nunique()
media_dia = len(df) / dias_unicos if dias_unicos else 0

print(f"🎧 Faixas únicas: {len(df)}")
print(f"🕒 Tempo total: {int(tempo_total // 60)}h {int(tempo_total % 60)}min")
print(f"⏱️ Tempo médio por faixa: {tempo_medio:.2f} min")
print(f"📅 Média por dia: {media_dia:.1f} faixas")

# 🎶 Top músicas
top_tracks = df.groupby("track_name").size().reset_index(name="quantidade") \
               .sort_values(by="quantidade", ascending=False)

# 🎤 Top artistas
top_artists = df.groupby("artist_name").size().reset_index(name="quantidade") \
                .sort_values(by="quantidade", ascending=False)

# 🎧 Top gêneros
df_genres = df[["genres"]].dropna()
df_genres = df_genres[df_genres["genres"] != ""]  # remove vazios
df_genres = df_genres.assign(genre_list=df_genres["genres"].str.split(", "))
df_genres = df_genres.explode("genre_list")
top_genres = df_genres["genre_list"].value_counts().reset_index()
top_genres.columns = ["gênero", "quantidade"]

# ⏰ Faixas por hora
hourly = df.groupby("hour").size().reindex(range(24), fill_value=0).reset_index()
hourly.columns = ["hora", "quantidade"]

# 📈 Faixas por dia
daily = df.groupby("date").size().reset_index(name="quantidade")

# 📅 Faixas por dia da semana
weekday = df.groupby("weekday").size().reset_index(name="quantidade") \
            .sort_values(by="quantidade", ascending=False)

# 💾 Exporta CSVs
df.to_csv("data/cleaned_tracks.csv", index=False)
top_tracks.to_csv("data/top_tracks.csv", index=False)
top_artists.to_csv("data/top_artists.csv", index=False)
top_genres.to_csv("data/top_genres.csv", index=False)
hourly.to_csv("data/hourly_distribution.csv", index=False)
daily.to_csv("data/daily_trend.csv", index=False)
weekday.to_csv("data/weekday_distribution.csv", index=False)

print("✅ Dados transformados e salvos:")
print(" - cleaned_tracks.csv")
print(" - top_tracks.csv")
print(" - top_artists.csv")
print(" - top_genres.csv")
print(" - hourly_distribution.csv")
print(" - daily_trend.csv")
print(" - weekday_distribution.csv")
