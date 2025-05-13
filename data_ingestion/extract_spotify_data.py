import os
import spotipy
import pandas as pd
import duckdb
import pytz
from tqdm import tqdm
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime, timezone

# Carrega variáveis do .env
load_dotenv()
os.makedirs("data", exist_ok=True)

# Timezones
utc = pytz.UTC
brt = pytz.timezone("America/Sao_Paulo")

# Autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# Início do mês atual (BRT)
agora = datetime.now(brt)
inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
inicio_mes_utc = inicio_mes.astimezone(utc)

# Lista de faixas novas
new_data = []
before = None

print(f"📅 Coletando dados desde {inicio_mes.strftime('%d/%m/%Y')}...\n")

while True:
    try:
        results = sp.current_user_recently_played(limit=50, before=before)
    except spotipy.SpotifyException as e:
        print(f"❌ Erro ao acessar API: {e}")
        break

    items = results.get("items", [])
    if not items:
        break

    for item in tqdm(items, desc="🔄 Processando faixas"):
        played_at_utc = datetime.fromisoformat(item["played_at"].replace("Z", "+00:00")).astimezone(brt)
        if played_at_utc < inicio_mes:
            break

        track = item["track"]
        artist = track["artists"][0]

        # Coleta gêneros do artista
        try:
            artist_data = sp.artist(artist["id"])
            genres = ", ".join(artist_data.get("genres", []))
        except Exception:
            genres = ""

        new_data.append({
            "track_id": track["id"],
            "track_name": track["name"],
            "artist_id": artist["id"],
            "artist_name": artist["name"],
            "all_artists": ", ".join([a["name"] for a in track["artists"]]),
            "genres": genres,
            "popularity": track["popularity"],
            "played_at": played_at_utc,
            "date": played_at_utc.date(),
            "hour": played_at_utc.hour,
            "duration_ms": track["duration_ms"]
        })

    oldest_timestamp = min(
        datetime.fromisoformat(i["played_at"].replace("Z", "+00:00"))
        for i in items
    )
    before = int(oldest_timestamp.timestamp() * 1000)
    if oldest_timestamp < inicio_mes_utc:
        break

# Criação do DataFrame
df_new = pd.DataFrame(new_data)
df_new.drop_duplicates(subset=["track_id", "played_at"], inplace=True)

# Conexão com banco DuckDB
db_path = "data/spotify.duckdb"
con = duckdb.connect(db_path)

# Verifica base existente e concatena
if "recent_tracks" in con.execute("SHOW TABLES").fetchdf()["name"].values:
    df_old = con.execute("SELECT * FROM recent_tracks").fetchdf()
    df_all = pd.concat([df_old, df_new], ignore_index=True)
    df_all.drop_duplicates(subset=["track_id", "played_at"], inplace=True)
    novas = len(df_all) - len(df_old)
    print(f"📈 Novas faixas adicionadas: {novas}")
else:
    df_all = df_new
    print(f"📥 Inicializando base com {len(df_all)} faixas.")

# Atualiza tabela DuckDB
con.execute("CREATE OR REPLACE TABLE recent_tracks AS SELECT * FROM df_all")
print("✅ Banco atualizado com sucesso.")

# Atualiza arquivo .parquet
parquet_path = f"data/raw_tracks_{agora.strftime('%Y_%m')}.parquet"
if os.path.exists(parquet_path):
    df_parquet_old = pd.read_parquet(parquet_path)
    df_parquet = pd.concat([df_parquet_old, df_new], ignore_index=True)
    df_parquet.drop_duplicates(subset=["track_id", "played_at"], inplace=True)
else:
    df_parquet = df_new

df_parquet.to_parquet(parquet_path, index=False)
print(f"✅ Arquivo '{parquet_path}' salvo com dados atualizados.")

# Visualização final
if not df_new.empty:
    print("\n🆕 Faixas novas:")
    print(df_new[["played_at", "track_name", "artist_name"]].sort_values(by="played_at", ascending=False).tail(10).to_string(index=False))
else:
    print("⚠️ Nenhuma faixa nova foi adicionada.")
