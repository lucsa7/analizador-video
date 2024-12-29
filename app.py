import streamlit as st
from moviepy.editor import VideoFileClip
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
import tempfile

def calcular_fuerza_tiempo(masa, velocidades, fps):
    tiempos = []
    fuerzas = []

    for i in range(1, len(velocidades)):
        tiempo = i / fps
        tiempos.append(tiempo)

        # Calcular aceleración
        aceleracion = (velocidades[i] - velocidades[i-1]) * fps

        # Calcular fuerza
        fuerza = masa * (aceleracion + 9.81)  # Incluye la gravedad
        fuerzas.append(fuerza)

    return tiempos, fuerzas

def main():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🔍 Analizador de Video y Curva Fuerza-Tiempo</h1>", unsafe_allow_html=True)

    # Subir archivo de video
    st.markdown("### 📂 Subir un archivo de video")
    video_file = st.file_uploader("Carga un archivo de video", type=["mp4", "avi", "mov", "mpeg4"])

    if video_file:
        try:
            # Crear un archivo temporal para guardar el video
            with tempfile.NamedTemporaryFile(delete=False) as temp_video:
                temp_video.write(video_file.read())
                temp_video_path = temp_video.name

            # Procesar el video con MoviePy
            clip = VideoFileClip(temp_video_path)
            fps = clip.fps
            frame_count = int(clip.duration * fps)
            duration = clip.duration

            st.markdown(f"**📊 Propiedades del Video**")
            st.write(f"- **Frames por segundo (FPS):** {fps}")
            st.write(f"- **Número total de fotogramas:** {frame_count}")
            st.write(f"- **Duración del video:** {duration:.2f} segundos")

            # Pedir el peso del usuario
            peso_usuario = st.number_input("Ingrese el peso del usuario (kg):", min_value=1.0, value=70.0)
            masa_usuario = peso_usuario / 9.81  # Convertir peso a masa

            # Simular velocidades (puedes reemplazar con cálculos reales basados en tu análisis)
            velocidades = np.linspace(0, 5, frame_count)  # Velocidades simuladas en m/s

            # Calcular la curva Fuerza-Tiempo
            tiempos, fuerzas = calcular_fuerza_tiempo(masa_usuario, velocidades, fps)

            # Mostrar la curva Fuerza-Tiempo
            st.markdown("### 📈 Curva Fuerza-Tiempo")
            fig, ax = plt.subplots()
            ax.plot(tiempos, fuerzas, label="Fuerza-Tiempo", color="#FF5733")
            ax.axhline(y=masa_usuario * 9.81, color="green", linestyle="--", label="Peso del Usuario")
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Fuerza (N)")
            ax.set_title("Curva Fuerza-Tiempo")
            ax.legend()
            ax.grid()
            st.pyplot(fig)

            # Exportar el gráfico
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="Descargar gráfico como PNG",
                data=buf,
                file_name="curva_fuerza_tiempo.png",
                mime="image/png"
            )

            # Exportar datos de la curva
            st.markdown("### 💾 Exportar Datos de la Curva")
            data = pd.DataFrame({
                "Tiempo (s)": tiempos,
                "Fuerza (N)": fuerzas
            })
            st.download_button(
                label="Descargar datos como CSV",
                data=data.to_csv(index=False, sep=";"),
                file_name="datos_curva_fuerza_tiempo.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"⚠️ Error al procesar el video: {e}")

if __name__ == "__main__":
    main()










