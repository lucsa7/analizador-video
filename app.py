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
        aceleracion = (velocidades[i] - velocidades[i - 1]) * fps

        # Calcular fuerza
        fuerza = masa * (aceleracion + 9.81)  # Incluye la gravedad
        fuerzas.append(fuerza)

    return tiempos, fuerzas

def main():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🔍 Analizador de Video y Métricas Físicas</h1>", unsafe_allow_html=True)

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

            # Deslizador para seleccionar un fotograma
            st.markdown("### 🎞️ Selecciona un fotograma")
            frame_idx = st.slider("Selecciona un fotograma", 0, frame_count - 1, 0)

            # Obtener y mostrar el fotograma seleccionado
            frame_time = frame_idx / fps
            frame = clip.get_frame(frame_time)
            st.image(frame, caption=f"Fotograma {frame_idx}", use_container_width=True)

            # Pedir el peso de la persona
            st.markdown("### ⚖️ Datos del atleta")
            peso_persona = st.number_input("Ingresa el peso de la persona (kg):", min_value=1.0, value=70.0)

            # Seleccionar fotogramas clave
            st.markdown("### 📌 Selección de fotogramas clave")
            inicio_contacto = st.number_input("Fotograma de inicio del contacto inicial (caída):", min_value=0, max_value=frame_count - 1, value=0)
            final_contacto = st.number_input("Fotograma de final del contacto inicial (despegue):", min_value=0, max_value=frame_count - 1, value=0)
            aterrizaje = st.number_input("Fotograma de aterrizaje (fin del vuelo):", min_value=0, max_value=frame_count - 1, value=0)

            # Validar el orden de los fotogramas clave
            if inicio_contacto >= final_contacto or final_contacto >= aterrizaje:
                st.error("⚠️ Asegúrate de que los fotogramas clave están en el orden correcto: inicio_contacto < final_contacto < aterrizaje.")
                return

            # Calcular tiempos y métricas
            if st.button("📐 Calcular tiempos y métricas"):
                tiempo_contacto = (final_contacto - inicio_contacto) / fps
                tiempo_vuelo = (aterrizaje - final_contacto) / fps
                altura = (tiempo_vuelo ** 2 * 9.81) / 8
                velocidad_pico = (2 * altura * 9.81) ** 0.5  # Fórmula para calcular la velocidad pico en el despegue

                # Cálculo de fuerza media
                masa_persona = peso_persona / 9.81  # Masa en kg
                aceleracion_media = velocidad_pico / tiempo_contacto
                fuerza_media = masa_persona * (aceleracion_media + 9.81)  # Newtons

                # Cálculo de potencia promedio
                potencia_promedio = fuerza_media * velocidad_pico  # Watts

                # Mostrar resultados
                st.markdown("### 📈 Resultados")
                st.write(f"- **Tiempo de contacto inicial:** {tiempo_contacto:.2f} segundos")
                st.write(f"- **Tiempo de vuelo:** {tiempo_vuelo:.2f} segundos")
                st.write(f"- **Altura estimada del salto:** {altura:.2f} metros")
                st.write(f"- **Velocidad pico en el despegue:** {velocidad_pico:.2f} m/s")
                st.write(f"- **Fuerza media durante el contacto:** {fuerza_media:.2f} N")
                st.write(f"- **Potencia promedio durante el salto:** {potencia_promedio:.2f} W")

                # Curva Fuerza-Tiempo
                velocidades = np.linspace(0, velocidad_pico, int(tiempo_contacto * fps))  # Velocidades simuladas
                tiempos, fuerzas = calcular_fuerza_tiempo(masa_persona, velocidades, fps)

                st.markdown("### 📈 Curva Fuerza-Tiempo")
                fig, ax = plt.subplots()
                ax.plot(tiempos, fuerzas, label="Fuerza-Tiempo", color="#FF5733")
                ax.axhline(y=masa_persona * 9.81, color="green", linestyle="--", label="Peso del Usuario")
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("Fuerza (N)")
                ax.set_title("Curva Fuerza-Tiempo")
                ax.legend()
                ax.grid()
                st.pyplot(fig)

                # Exportar datos de la curva
                st.markdown("### 💾 Exportar Datos de la Curva")
                data_curva = pd.DataFrame({
                    "Tiempo (s)": tiempos,
                    "Fuerza (N)": fuerzas
                })
                st.download_button(
                    label="Descargar datos como CSV",
                    data=data_curva.to_csv(index=False, sep=";"),
                    file_name="curva_fuerza_tiempo.csv",
                    mime="text/csv"
                )

                # Exportar resultados generales
                st.markdown("### 💾 Exportar Resultados Generales")
                data_resultados = pd.DataFrame({
                    "Métrica": ["Tiempo de contacto (s)", "Tiempo de vuelo (s)", "Altura (m)", "Velocidad pico (m/s)",
                                "Fuerza media (N)", "Potencia promedio (W)"],
                    "Valor": [tiempo_contacto, tiempo_vuelo, altura, velocidad_pico, fuerza_media, potencia_promedio]
                })
                st.download_button(
                    label="Descargar resultados como CSV",
                    data=data_resultados.to_csv(index=False, sep=";"),
                    file_name="resultados_generales.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"⚠️ Error al procesar el video: {e}")

if __name__ == "__main__":
    main()












