# 🎬 YouTube Video Transcription Tool mit Sprechererkennung

Ein leistungsstarkes Python-Tool, das Audio aus YouTube-Videos herunterlädt und mit **OpenAI Whisper** transkribiert. **NEU:** Automatische **Sprechererkennung** mit pyannote.audio - erkenne wer gerade spricht!

## ✨ Features

- 📥 **YouTube Audio Download** mit `yt-dlp`
- 🧠 **KI-Transkription** mit OpenAI Whisper (alle Modelle verfügbar)
- 🎭 **Sprechererkennung** - Identifiziert verschiedene Sprecher automatisch
- ⏰ **Optionale Zeitstempel** - An/Aus nach Wunsch
- 🌍 **Multi-Language Support** (Standard: Polnisch)
- 🚀 **GPU-Beschleunigung** für schnellere Verarbeitung
- 🧹 **Automatische Cleanup** von temporären Dateien
- 📝 **Intelligente Formatierung** mit Leerzeilen zwischen Sprechern

## 📋 Beispiel-Ausgabe

**Mit Sprechererkennung:**

```
=== TRANSKRIPT MIT SPRECHERERKENNUNG ===

SPEAKER_00: Witam wszystkich na naszym kanale YouTube
SPEAKER_01: Dzisiaj będziemy rozmawiać o sztucznej inteligencji

SPEAKER_00: To bardzo fascynujący temat
SPEAKER_01: Zgadzam się, szczególnie w kontekście...
```

**Mit Zeitstempeln:**

```
[02:15 - 02:22] SPEAKER_00: Witam wszystkich na naszym kanale YouTube
[02:23 - 02:30] SPEAKER_01: Dzisiaj będziemy rozmawiać o...
```

## 🛠️ Installation

### System-Dependencies

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
sudo apt install yt-dlp
```

**macOS (Homebrew):**

```bash
brew install ffmpeg
brew install yt-dlp
```

**Windows:**

- Installiere [ffmpeg](https://ffmpeg.org/download.html)
- Installiere [yt-dlp](https://github.com/yt-dlp/yt-dlp)

### Python-Setup

```bash
# Repository klonen
git clone <repository-url>
cd transcribe-YouTube-videos

# Virtual Environment erstellen
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Für Sprechererkennung zusätzlich:
pip install pyannote.audio
```

### 🔑 Hugging Face Setup (für Sprechererkennung)

1. **Account erstellen:** [huggingface.co](https://huggingface.co)

2. **Access Token erstellen:**

   - Gehe zu [Settings → Access Tokens](https://huggingface.co/settings/tokens)
   - **Token type:** `Read`
   - **Permissions:** `Read access to contents of all public gated repos you can access`

3. **Nutzungsbedingungen akzeptieren:**

   - Besuche: [pyannote/speaker-diarization-3.1](https://hf.co/pyannote/speaker-diarization-3.1)
   - Klicke "Accept and access repository"

4. **Login:**
   ```bash
   huggingface-cli login
   # Oder: hf auth login
   ```

## 🚀 Verwendung

```bash
# Virtual Environment aktivieren
source .venv/bin/activate

# Script starten
python whisper_transcribe_pl.py
```

**Interaktive Konfiguration:**

```
🎬 YouTube Video Transkriptionstool mit Sprechererkennung
============================================================
🔗 Gib den YouTube-Link ein: https://youtu.be/VIDEO_ID

⚙️  Konfiguration:
🎭 Sprechererkennung verwenden? (j/N): j
⏰ Zeitstempel einbinden? (j/N): N

🧠 Verfügbare Whisper-Modelle:
   tiny (schnell, weniger genau)
   small (ausgewogen)
   medium (empfohlen)
   large (sehr genau, langsam)
Modell wählen (Enter für 'medium'):
```

## ⚙️ Konfiguration

### Whisper-Modelle

| Modell   | Geschwindigkeit | Genauigkeit | Empfehlung               |
| -------- | --------------- | ----------- | ------------------------ |
| `tiny`   | ⚡⚡⚡⚡        | ⭐          | Sehr schnelle Tests      |
| `small`  | ⚡⚡⚡          | ⭐⭐        | Schnelle Verarbeitung    |
| `medium` | ⚡⚡            | ⭐⭐⭐      | **Standard (empfohlen)** |
| `large`  | ⚡              | ⭐⭐⭐⭐    | Beste Qualität           |

### Sprachen

Standardmäßig auf **Polnisch** (`pl`) konfiguriert. Andere Sprachen:

- `en` - Englisch
- `de` - Deutsch
- `fr` - Französisch
- `es` - Spanisch
- etc.

### GPU-Beschleunigung

- **Automatische CUDA-Erkennung** für Whisper und pyannote.audio
- Deutlich schnellere Verarbeitung mit kompatiblen NVIDIA-GPUs
- Fallback auf CPU falls keine GPU verfügbar

## 📁 Ausgabe

- **Transkript:** `transkript_{video_id}_{timestamp}.txt`
- **Temporäre Dateien:** `temp_audio/` (automatisch bereinigt)
- **Eindeutige Dateinamen** verhindern Überschreibungen

## ❗ Troubleshooting

### Häufige Probleme

**Sprechererkennung fehlgeschlagen:**

```bash
# Prüfe Hugging Face Login
hf auth whoami

# Nochmal einloggen falls nötig
hf auth login
```

**"yt-dlp not found":**

```bash
# Installation prüfen
which yt-dlp
pip install yt-dlp
```

**GPU-Probleme:**

- Script fällt automatisch auf CPU zurück
- Keine Aktion erforderlich

**Sehr kleine Audio-Datei:**

- Möglicherweise ist das Video privat/gelöscht
- Prüfe YouTube-URL

### Performance-Tipps

- **GPU verwenden** für deutlich schnellere Verarbeitung
- **Kleinere Whisper-Modelle** für schnellere Tests
- **Sprechererkennung deaktivieren** für einfache Transkription

## 🔄 Updates

```bash
# Dependencies aktualisieren
pip install --upgrade whisper pyannote.audio

# Neueste Whisper-Modelle laden
python -c "import whisper; whisper.load_model('medium')"
```

## 📄 Lizenz

Dieses Projekt steht für Bildungs- und persönliche Zwecke zur Verfügung. Bitte respektiere YouTubes Nutzungsbedingungen.

## 🤝 Contributing

Issues und Pull Requests sind willkommen!

---

**💡 Tipp:** Starte mit Sprechererkennung AUS und Zeitstempel AUS für die ersten Tests, dann erweitere die Funktionen nach Bedarf.
