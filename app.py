import streamlit as st
from moviepy.editor import VideoFileClip
import pandas as pd
import tempfile

def main():
    # Título del analizador
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🔍 Analizador de Video por Fotogramas</h1>", unsafe_allow_html=True)

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
            st.image(frame, caption=f"Fotograma {frame_idx}", use_column_width=True)

            # Seleccionar fotogramas clave
            st.markdown("### 📌 Selección de fotogramas clave")
            inicio_contacto = st.number_input("Fotograma de inicio del contacto inicial (caída):", min_value=0, max_value=frame_count - 1, value=0)
            final_contacto = st.number_input("Fotograma de final del contacto inicial (despegue):", min_value=0, max_value=frame_count - 1, value=0)
            aterrizaje = st.number_input("Fotograma de aterrizaje (fin del vuelo):", min_value=0, max_value=frame_count - 1, value=0)

            # Calcular tiempos y altura
            if st.button("📐 Calcular tiempos y altura"):
                tiempo_contacto = (final_contacto - inicio_contacto) / fps
                tiempo_vuelo = (aterrizaje - final_contacto) / fps
                altura = (tiempo_vuelo ** 2 * 9.81) / 8

                st.markdown("### 📈 Resultados")
                st.write(f"- **Tiempo de contacto inicial:** {tiempo_contacto:.2f} segundos")
                st.write(f"- **Tiempo de vuelo:** {tiempo_vuelo:.2f} segundos")
                st.write(f"- **Altura estimada del salto:** {altura:.2f} metros")

                # Exportar resultados
                st.markdown("### 💾 Exportar resultados")
                data = {
                    "Tiempo de contacto inicial (s)": [tiempo_contacto],
                    "Tiempo de vuelo (s)": [tiempo_vuelo],
                    "Altura estimada (m)": [altura]
                }
                df = pd.DataFrame(data)
                st.download_button(
                    label="Descargar resultados como CSV",
                    data=df.to_csv(index=False),
                    file_name="resultados_salto.csv",
                    mime="text/csv"
                )

            # Explicación de la lógica
            st.markdown("### 📚 Lógica de cálculo")
            st.markdown("""
            La altura del salto se calcula utilizando la fórmula de la caída libre:
            
            \[
            h = \frac{(t_{vuelo})^2 \cdot g}{8}
            \]
            
            Donde:
            - \(t_{vuelo}\): Es el tiempo de vuelo, calculado como la diferencia entre el fotograma de aterrizaje y el fotograma de despegue dividido por los FPS del video.
            - \(g = 9.81 \, \text{m/s}^2\): Es la aceleración debido a la gravedad.
            
            La fórmula asume un movimiento parabólico ideal del salto, y el factor \(1/8\) ajusta la fórmula para considerar la simetría del vuelo en dos mitades iguales (ascenso y descenso).
            """)

        except Exception as e:
            st.error(f"⚠️ Error al procesar el video: {e}")

if __name__ == "__main__":
    main()



