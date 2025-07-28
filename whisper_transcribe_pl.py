import os
import whisper
import subprocess
import sys
import time
from urllib.parse import urlparse, parse_qs
from pyannote.audio import Pipeline
import torch

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
        "--audio-format", "wav",  # WAV für bessere Kompatibilität mit pyannote
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

def perform_speaker_diarization(audio_file):
    """Führt Speaker Diarization mit pyannote.audio durch"""
    print("🎭 Erkenne Sprecher...")
    
    try:
        # Pipeline laden (erfordert Hugging Face Token für erste Nutzung)
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
        
        # GPU verwenden falls verfügbar
        if torch.cuda.is_available():
            pipeline = pipeline.to(torch.device("cuda"))
            print("🚀 GPU-Beschleunigung aktiviert")
        
        # Diarization durchführen
        diarization = pipeline(audio_file)
        
        # Sprecher zählen - API hat sich geändert
        speakers = set()
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            speakers.add(speaker)
        
        print(f"✅ {len(speakers)} Sprecher erkannt")
        return diarization
        
    except Exception as e:
        print(f"⚠️  Sprechererkennung fehlgeschlagen: {e}")
        print("💡 Tipp: Möglicherweise fehlt ein Hugging Face Token oder pyannote.audio ist nicht installiert")
        return None

def transcribe_with_speakers(audio_file, model_name="medium", lang="pl", video_id="unknown", 
                           include_timestamps=False, use_speaker_diarization=True):
    print(f"🧠 Lade Whisper-Modell: {model_name}")
    model = whisper.load_model(model_name)

    # Sprechererkennung durchführen
    diarization = None
    if use_speaker_diarization:
        diarization = perform_speaker_diarization(audio_file)
    
    print(f"🎧 Transkribiere Datei: {audio_file}")
    
    # word_timestamps nur wenn keine GPU-Probleme auftreten
    try:
        if diarization:
            # Für Speaker-Diarization brauchen wir word-level timestamps
            result = model.transcribe(audio_file, language=lang, word_timestamps=True)
        else:
            # Ohne Speaker-Diarization reichen normale timestamps
            result = model.transcribe(audio_file, language=lang)
    except Exception as e:
        print(f"⚠️  Word-Timestamps fehlgeschlagen, verwende Standard-Modus: {e}")
        result = model.transcribe(audio_file, language=lang)

    # Eindeutiger Dateiname mit Video-ID und Timestamp
    timestamp = int(time.time())
    output_txt = f"transkript_{video_id}_{timestamp}.txt"
    
    with open(output_txt, "w", encoding="utf-8") as f:
        if diarization:
            # Mit Sprechererkennung
            write_transcript_with_speakers(f, result, diarization, include_timestamps)
        else:
            # Ohne Sprechererkennung (wie vorher)
            if include_timestamps:
                f.write("=== TRANSKRIPT MIT ZEITSTEMPELN ===\n\n")
                for segment in result["segments"]:
                    start_time = format_timestamp(segment["start"])
                    end_time = format_timestamp(segment["end"])
                    f.write(f"[{start_time} - {end_time}] {segment['text'].strip()}\n")
            else:
                f.write(result["text"])

    print(f"✅ Transkript gespeichert unter: {output_txt}")

def write_transcript_with_speakers(file_handle, whisper_result, diarization, include_timestamps):
    """Schreibt Transkript mit Sprecherzuordnung"""
    file_handle.write("=== TRANSKRIPT MIT SPRECHERERKENNUNG ===\n\n")
    
    # Segmente nach Sprechern organisieren - API Update
    speaker_segments = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        speaker_segments.append({
            'start': segment.start,
            'end': segment.end,
            'speaker': speaker
        })
    
    # Nach Zeit sortieren
    speaker_segments.sort(key=lambda x: x['start'])
    
    # Text zu Segmenten zuordnen
    current_speaker = None
    
    for seg in speaker_segments:
        # Passenden Whisper-Text finden
        segment_text = get_text_for_timespan(whisper_result, seg['start'], seg['end'])
        
        if segment_text.strip():
            # Leerzeile zwischen verschiedenen Sprechern
            if current_speaker is not None and current_speaker != seg['speaker']:
                file_handle.write("\n")
            
            if include_timestamps:
                start_time = format_timestamp(seg['start'])
                end_time = format_timestamp(seg['end'])
                file_handle.write(f"[{start_time} - {end_time}] {seg['speaker']}: {segment_text.strip()}\n")
            else:
                file_handle.write(f"{seg['speaker']}: {segment_text.strip()}\n")
            
            current_speaker = seg['speaker']

def get_text_for_timespan(whisper_result, start_time, end_time):
    """Extrahiert Text für einen bestimmten Zeitbereich"""
    text_parts = []
    
    for segment in whisper_result["segments"]:
        seg_start = segment["start"]
        seg_end = segment["end"]
        
        # Überschneidung prüfen
        if seg_end >= start_time and seg_start <= end_time:
            # Wenn Wort-Timestamps verfügbar sind, genauer filtern
            if "words" in segment:
                for word_info in segment["words"]:
                    word_start = word_info.get("start", seg_start)
                    word_end = word_info.get("end", seg_end)
                    
                    if word_end >= start_time and word_start <= end_time:
                        text_parts.append(word_info["word"])
            else:
                # Fallback: ganzes Segment
                text_parts.append(segment["text"])
    
    return " ".join(text_parts)

def format_timestamp(seconds):
    """Formatiert Sekunden zu MM:SS Format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def transcribe(audio_file, model_name="medium", lang="pl", video_id="unknown"):
    """Legacy-Funktion für Rückwärtskompatibilität"""
    transcribe_with_speakers(audio_file, model_name, lang, video_id, 
                           include_timestamps=False, use_speaker_diarization=False)

def main():
    print("🎬 YouTube Video Transkriptionstool mit Sprechererkennung")
    print("=" * 60)
    
    youtube_url = input("🔗 Gib den YouTube-Link ein: ").strip()
    
    # Konfiguration abfragen
    print("\n⚙️  Konfiguration:")
    use_speakers = input("🎭 Sprechererkennung verwenden? (j/N): ").lower().startswith('j')
    include_timestamps = input("⏰ Zeitstempel einbinden? (j/N): ").lower().startswith('j')
    
    # Modell auswählen
    print("\n🧠 Verfügbare Whisper-Modelle:")
    print("   tiny (schnell, weniger genau)")
    print("   small (ausgewogen)")
    print("   medium (empfohlen)")
    print("   large (sehr genau, langsam)")
    model_choice = input("Modell wählen (Enter für 'medium'): ").strip() or "medium"

    temp_dir = os.path.join(os.getcwd(), "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)

    # Video-ID für eindeutige Dateinamen extrahieren
    video_id = get_video_id(youtube_url)
    print(f"🎬 Video-ID: {video_id}")

    # Audio herunterladen mit Fehlerbehandlung
    if not download_audio(youtube_url, temp_dir):
        print("❌ Download fehlgeschlagen. Programm wird beendet.")
        sys.exit(1)

    audio_path = os.path.join(temp_dir, "audio.wav")  # WAV statt MP3

    if not os.path.exists(audio_path):
        print("❌ Fehler: Audiodatei nicht gefunden.")
        sys.exit(1)

    # Dateigröße und Erstellungszeit prüfen
    file_size = os.path.getsize(audio_path)
    print(f"📊 Audiodatei: {file_size} Bytes")
    
    if file_size < 1000:  # Sehr kleine Datei = wahrscheinlich leer
        print("⚠️  Warnung: Audiodatei ist sehr klein!")

    # Installation Check
    if use_speakers:
        try:
            import pyannote.audio
            print("✅ pyannote.audio verfügbar")
        except ImportError:
            print("❌ pyannote.audio nicht installiert!")
            print("💡 Installation: pip install pyannote.audio")
            print("🔑 Hugging Face Token erforderlich: huggingface-cli login")
            sys.exit(1)

    transcribe_with_speakers(audio_path, model_choice, "pl", video_id, 
                           include_timestamps, use_speakers)

if __name__ == "__main__":
    main()
