<h1 align="center">Spotify Wrapped: Análise Personalizada com Python, DuckDB e Streamlit</h1>
<p align="center">
  <img src="https://img.shields.io/badge/python-3.10-blue" />
  <img src="https://img.shields.io/badge/duckdb-%2300B4CC" />
  <img src="https://img.shields.io/badge/streamlit-%23FF4B4B" />
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/c11e0134-5bbf-4999-9809-777bc77f72cd" alt="inicio"  />
</p>

<p>
Este projeto tem como objetivo apresentar uma análise interativa e visual dos seus hábitos musicais no Spotify, similar ao Spotify Wrapped oficial, mas com controle total sobre os dados. Utilizando Python, DuckDB e Streamlit, a aplicação coleta e processa as faixas reproduzidas no mês atual e exibe dashboards personalizados com os estilos, artistas, horários e perfis musicais do usuário.

<h2>⚠️ Limitação da API do Spotify:</h2>
A API do Spotify permite acessar apenas as últimas 50 faixas reproduzidas. Para contornar essa limitação, o sistema foi projetado para armazenar os dados localmente e realizar apenas inserções incrementais, evitando duplicações.

Como melhoria futura, recomenda-se hospedar a aplicação em ambiente em nuvem, utilizando serviços como EC2, Cloud Run, Railway ou similares, juntamente com um agendador de tarefas como o Apache Airflow ou cron, executando a coleta a cada 5 minutos. Isso permite capturar continuamente os dados de reprodução e ultrapassar a limitação de 50 faixas, garantindo um histórico completo e mais preciso para análises aprofundadas.

Assim, ao transformar o sistema em uma solução persistente e escalável, é possível construir uma base robusta de comportamento musical do usuário, com insights mais ricos ao longo do tempo.
</p>

<h2>🛠️ Tecnologias Utilizadas</h2>
<ul>
  <li><strong>Spotify API:</strong> Para acesso ao histórico de reproduções recentes e metadados das faixas.</li>
  <li><strong>Python:</strong> Para scripts de extração, transformação e backend do dashboard.</li>
  <li><strong>Spotipy:</strong> Wrapper para comunicação com a API do Spotify.</li>
  <li><strong>DuckDB:</strong> Banco de dados analítico para armazenamento local e consulta SQL.</li>
  <li><strong>Pandas:</strong> Manipulação e análise de dados.</li>
  <li><strong>Streamlit:</strong> Criação de uma interface web interativa e leve para explorar os dados.</li>
</ul>

<h2>📊 Funcionalidades</h2>
<ul>
  <li>🔄 Botão interativo para atualizar os dados diretamente da API</li>
  <li>🎶 Listagem das músicas mais escutadas</li>
  <li>🎤 Artistas favoritos</li>
  <li>🎧 Estilos musicais mais presentes</li>
  <li>⏰ Horários mais ativos (00h - 23h)</li>
  <li>📅 Dias da semana mais musicais</li>
  <li>📈 Evolução temporal da audição</li>
  <li>📥 Botões para download dos dados em CSV</li>
</ul>

<h2>🎨 Interface</h2>
<p align="center">
  <img src="https://github.com/user-attachments/assets/d894485d-cc2a-4a1e-a0ed-6fd3ee7e38dd" alt="dashboard preview"/>
  <img src="https://github.com/user-attachments/assets/99612382-b8c2-43ed-b44d-09c89dd557bc" alt="dashboard preview"/>
  <p>Por favor, ignorem as musicas...</p>
</p>

<h2>📂 Estrutura de Pastas</h2>
<pre><code>.
├── data_ingestion/
│   └── extract_spotify_data.py
├── data_processing/
│   └── transform_data.py
├── data/
│   ├── cleaned_tracks.csv
│   ├── top_tracks.csv
│   ├── top_artists.csv
│   ├── top_genres.csv
│   └── spotify.duckdb
├── app.py
└── .env
</code></pre>

<h2>⚙️ Executando o Projeto</h2>
<ol>
  <li>Clone o repositório</li>
  <li>Configure o arquivo <code>.env</code> com suas credenciais do Spotify API:</li>
  <pre><code>SPOTIPY_CLIENT_ID=...
SPOTIPY_CLIENT_SECRET=...
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback</code></pre>
  <li>Ative seu ambiente virtual:</li>
  <pre><code>python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac</code></pre>
  <li>Instale as dependências:</li>
  <pre><code>pip install -r requirements.txt</code></pre>
  <li>Rode o dashboard:</li>
  <pre><code>streamlit run app.py</code></pre>
</ol>

<h2>👤 Desenvolvido por</h2>
<p><strong>Mateus Vicentin</strong> - Projeto pessoal de visualização de dados com foco em música e engenharia de dados.</p>
