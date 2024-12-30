mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
# setup.sh
# Instalar ffmpeg y otras librerías necesarias
apt-get update && apt-get install -y ffmpeg libsm6 libxext6
