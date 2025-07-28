import os
import whisper
import subprocess
import sys
import time
from urllib.parse import urlparse, parse_qs

def cleanup_temp_files(temp_dir):
    """Löscht alle alten Audio-Dateien im temp-Verzeichnis"""
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"🗑️  Alte Datei gelöscht: {file}")

def get_video_id(youtube_url):
    """Extrahiert Video-ID aus YouTube-URL für eindeutige Dateinamen"""
    try:
        parsed_url = urlparse(youtube_url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed_url.query)['v'][0]
        else:
            # Fallback: Zeitstempel verwenden
            return str(int(time.time()))
    except:
        return str(int(time.time()))

def download_audio(youtube_url, output_path):
    print("📥 Lade Audio mit yt-dlp herunter...")
    
    # Erst alte Dateien löschen
    cleanup_temp_files(output_path)
    
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", os.path.join(output_path, "audio.%(ext)s"),
        youtube_url
    ]
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ Audio erfolgreich heruntergeladen")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Download: {e}")
        print(f"Fehlerausgabe: {e.stderr}")
        return False

def transcribe(audio_file, model_name="medium", lang="pl", video_id="unknown"):
    print(f"🧠 Lade Whisper-Modell: {model_name}")
    model = whisper.load_model(model_name)

    print(f"🎧 Transkribiere Datei: {audio_file}")
    result = model.transcribe(audio_file, language=lang)

    # Eindeutiger Dateiname mit Video-ID und Timestamp
    timestamp = int(time.time())
    output_txt = f"transkript_{video_id}_{timestamp}.txt"
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Transkript gespeichert unter: {output_txt}")

def main():
    youtube_url = input("🔗 Gib den YouTube-Link ein: ").strip()

    temp_dir = os.path.join(os.getcwd(), "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)

    # Video-ID für eindeutige Dateinamen extrahieren
    video_id = get_video_id(youtube_url)
    print(f"🎬 Video-ID: {video_id}")

    # Audio herunterladen mit Fehlerbehandlung
    if not download_audio(youtube_url, temp_dir):
        print("❌ Download fehlgeschlagen. Programm wird beendet.")
        sys.exit(1)

    audio_path = os.path.join(temp_dir, "audio.mp3")

    if not os.path.exists(audio_path):
        print("❌ Fehler: Audiodatei nicht gefunden.")
        sys.exit(1)

    # Dateigröße und Erstellungszeit prüfen
    file_size = os.path.getsize(audio_path)
    print(f"📊 Audiodatei: {file_size} Bytes")
    
    if file_size < 1000:  # Sehr kleine Datei = wahrscheinlich leer
        print("⚠️  Warnung: Audiodatei ist sehr klein!")

    transcribe(audio_path, video_id=video_id)

if __name__ == "__main__":
    main()
