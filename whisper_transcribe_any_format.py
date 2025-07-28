import os
import whisper
import sys
import time
from pathlib import Path

def get_file_id(file_path):
    """Extrahiert einen eindeutigen Identifier aus dem Dateinamen"""
    try:
        # Verwende den Dateinamen ohne Erweiterung als ID
        file_name = Path(file_path).stem
        # Entferne Sonderzeichen und ersetze sie durch Unterstriche
        clean_name = "".join(c if c.isalnum() else "_" for c in file_name)
        return clean_name[:50]  # Begrenze auf 50 Zeichen
    except:
        return str(int(time.time()))

def validate_audio_file(file_path):
    """Validiert ob die Datei existiert und ein unterstütztes Audioformat hat"""
    if not os.path.exists(file_path):
        return False, "Datei nicht gefunden"
    
    # Unterstützte Audioformate
    supported_formats = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma', '.mp4', '.mkv', '.avi'}
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension not in supported_formats:
        return False, f"Nicht unterstütztes Dateiformat: {file_extension}"
    
    # Prüfe Dateigröße
    file_size = os.path.getsize(file_path)
    if file_size < 1000:  # Sehr kleine Datei
        return False, "Datei ist zu klein (wahrscheinlich leer)"
    
    return True, "OK"

def transcribe(audio_file, model_name="medium", lang=None, file_id="unknown"):
    print(f"🧠 Lade Whisper-Modell: {model_name}")
    model = whisper.load_model(model_name)

    print(f"🎧 Transkribiere Datei: {audio_file}")
    
    # Automatische Spracherkennung wenn keine Sprache angegeben
    if lang:
        result = model.transcribe(audio_file, language=lang)
        print(f"🌍 Sprache: {lang}")
    else:
        result = model.transcribe(audio_file)
        detected_lang = result.get('language', 'unbekannt')
        print(f"🌍 Erkannte Sprache: {detected_lang}")

    # Eindeutiger Dateiname mit Datei-ID und Timestamp
    timestamp = int(time.time())
    output_txt = f"transkript_{file_id}_{timestamp}.txt"
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Transkript gespeichert unter: {output_txt}")
    return output_txt

def main():
    print("🎵 Audio-Transkriptions-Tool")
    print("Unterstützte Formate: MP3, WAV, M4A, FLAC, AAC, OGG, WMA, MP4, MKV, AVI")
    print()
    
    # Dateipfad eingeben
    file_path = input("📁 Gib den Pfad zur Datei ein: ").strip()
    
    # Anführungszeichen entfernen falls vorhanden (bei Drag & Drop)
    file_path = file_path.strip('"\'')
    
    # Datei validieren
    is_valid, error_msg = validate_audio_file(file_path)
    if not is_valid:
        print(f"❌ Fehler: {error_msg}")
        sys.exit(1)
    
    # Dateiinformationen anzeigen
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"📊 Audiodatei: {file_size_mb:.2f} MB")
    
    # Datei-ID für eindeutige Benennung extrahieren
    file_id = get_file_id(file_path)
    print(f"🎬 Datei-ID: {file_id}")
    
    # Sprachauswahl (optional)
    print("\n🌍 Sprache für Transkription:")
    print("   [Enter] = Automatische Erkennung")
    print("   de = Deutsch")
    print("   en = Englisch") 
    print("   pl = Polnisch")
    print("   fr = Französisch")
    print("   es = Spanisch")
    print("   it = Italienisch")
    print("   (oder andere ISO-639-1 Codes)")
    
    lang_input = input("Sprache (optional): ").strip().lower()
    language = lang_input if lang_input else None
    
    # Modellauswahl (optional)
    print("\n🧠 Whisper-Modell:")
    print("   [Enter] = medium (gute Genauigkeit, Standard)")
    print("   tiny = Sehr schnell, weniger genau")
    print("   base = Schnell, grundlegende Genauigkeit")
    print("   small = Ausgewogen")
    print("   medium = Gute Genauigkeit (Standard)") 
    print("   large = Beste Genauigkeit")
    
    model_input = input("Modell (optional): ").strip().lower()
    model = model_input if model_input in ['tiny', 'base', 'small', 'medium', 'large'] else 'medium'
    
    print(f"\n🚀 Starte Transkription mit Modell '{model}'...")
    
    try:
        output_file = transcribe(file_path, model_name=model, lang=language, file_id=file_id)
        print(f"\n🎉 Fertig! Transkript verfügbar in: {output_file}")
    except Exception as e:
        print(f"❌ Fehler bei der Transkription: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
