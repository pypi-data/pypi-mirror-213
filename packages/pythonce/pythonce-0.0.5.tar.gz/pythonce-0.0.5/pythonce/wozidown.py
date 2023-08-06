import cv2
import subprocess

def save_rtsp_stream(rtsp_url, duration):
    # Definir o tempo de gravação em segundos
    duration_seconds = duration * 60

    # Iniciar a captura do fluxo RTSP usando o OpenCV
    cap = cv2.VideoCapture(rtsp_url)

    # Obter as informações do vídeo para configurações de gravação
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Definir o comando FFmpeg para gravar o fluxo
    output_file = 'output.mp4'
    command = ['ffmpeg', '-y', '-i', '-', '-c:v', 'copy', '-t', str(duration_seconds), '-an', output_file]

    # Iniciar o processo FFmpeg
    ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    # Ler frames do fluxo RTSP e gravar no processo FFmpeg
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        ffmpeg_process.stdin.write(frame.tobytes())

    # Finalizar o processo FFmpeg
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()

    # Liberar recursos
    cap.release()

    print(f'Gravação concluída. Vídeo salvo em {output_file}.')

# Exemplo de uso
rtsp_url = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'  # Substitua pela sua URL RTSP
duration_minutes = 3  # Duração da gravação em minutos

save_rtsp_stream(rtsp_url, duration_minutes)
