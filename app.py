import cv2
import streamlit as st
import numpy as np

def main():
    st.title("Analizador de Video por Fotogramas")

    # Subir el archivo de video
    video_file = st.file_uploader("Carga un archivo de video", type=["mp4", "avi", "mov"])

    if video_file:
        # Guardar el video cargado
        video_path = f"temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.read())

        # Abrir el video con OpenCV
        cap = cv2.VideoCapture(video_path)

        # Obtener propiedades del video
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        st.write(f"**Frames por segundo (FPS):** {fps}")
        st.write(f"**Número total de fotogramas:** {frame_count}")
        st.write(f"**Duración del video:** {duration:.2f} segundos")

        # Crear un deslizador para navegar por los fotogramas
        frame_idx = st.slider("Selecciona un fotograma", 0, frame_count - 1, 0)

        # Ir al fotograma seleccionado
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if ret:
            # Mostrar el fotograma actual
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, channels="RGB", caption=f"Fotograma {frame_idx}")

        # Seleccionar fotogramas clave
        st.write("### Selecciona los fotogramas clave")
        inicio_contacto = st.number_input("Fotograma de inicio del contacto inicial (caída):", min_value=0, max_value=frame_count - 1, value=0)
        final_contacto = st.number_input("Fotograma de final del contacto inicial (despegue):", min_value=0, max_value=frame_count - 1, value=0)
        aterrizaje = st.number_input("Fotograma de aterrizaje (fin del vuelo):", min_value=0, max_value=frame_count - 1, value=0)

        # Calcular tiempos
        if st.button("Calcular tiempos y altura"):
            tiempo_contacto = (final_contacto - inicio_contacto) / fps
            tiempo_vuelo = (aterrizaje - final_contacto) / fps
            altura = (tiempo_vuelo ** 2 * 9.81) / 8

            st.write(f"**Tiempo de contacto inicial:** {tiempo_contacto:.2f} segundos")
            st.write(f"**Tiempo de vuelo:** {tiempo_vuelo:.2f} segundos")
            st.write(f"**Altura estimada del salto:** {altura:.2f} metros")

        cap.release()

if __name__ == "__main__":
    main()

