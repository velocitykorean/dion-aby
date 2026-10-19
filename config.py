import os, sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

for d in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR, IMAGES_DIR]:
    os.makedirs(d, exist_ok=True)

# Channel Identity & Branding
CHANNEL_NAME = "THE DIONYSIAN ABYSS"
CHANNEL_HANDLE = "@TheDionysianAbyss"
TAGLINE = "Nietzsche, Human Nature & The Unspoken Truths"
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
DEFAULT_IMAGE_PATH = os.path.join(IMAGES_DIR, "nietzsche_portrait_1.jpg")

# Dynamic Rotating Backgrounds
IMAGE_ROTATION_SECONDS = 30.0    # Duration each portrait is featured
IMAGE_TRANSITION_SECONDS = 1.5   # Smooth cross-fade transition between portraits

# Video Dimensions & Frame Rate
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

IS_SOLO = True

# Subtitle Position & Typography (Large, bold, single-line in open right zone)
SUBTITLE_CENTER_X = 1360
SUBTITLE_Y = 500
MAX_SUBTITLE_WIDTH = 880
SUBTITLE_FONT_SIZE = 48

# Audio Spectrum Visualizer (Directly below single-line subtitle, no box container)
VIS_CENTER_X = 1360
VIS_BASE_Y = 600
VIS_NUM_BARS = 24
VIS_BAR_WIDTH = 10
VIS_BAR_SPACING = 8
VIS_MIN_HEIGHT = 4
VIS_MAX_HEIGHT = 50
VIS_COLOR = (245, 197, 66, 240)  # Luminous Antique Gold

# Voiceover Engine & Model Selection
# Options for TTS_ENGINE:
#   - "kokoro": Hyper-realistic local AI voice (ElevenLabs quality, 100% free, 100% on GitHub, runs on CPU runners)
#   - "elevenlabs": ElevenLabs Cloud API (requires ELEVENLABS_API_KEY in GitHub secrets / .env)
#   - "edge": Microsoft Edge Neural TTS
TTS_ENGINE = "kokoro"

# Available Kokoro Languages & Voices (54 voices total, all on GitHub):
#   - American English (en-us): am_adam (recommended deep philosopher), am_michael, am_echo, am_eric, am_fenrir, am_liam, am_onyx, am_puck, af_bella, af_sarah, af_nicole, af_sky
#   - British English (en-gb):  bm_george (recommended Oxford scholar), bm_daniel, bm_fable, bm_lewis, bf_emma, bf_isabella, bf_alice, bf_lily
#   - Spanish (es):             em_alex, ef_dora
#   - French (fr-fr):          ff_siwis
#   - Hindi (hi):              hm_omega, hm_psi, hf_alpha, hf_beta
#   - Italian (it):            im_nicola, if_sara
#   - Japanese (ja):           jm_kumo, jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro
#   - Brazilian Portuguese (pt): pm_alex, pf_dora
#   - Mandarin Chinese (zh):   zm_yunjian, zm_yunxi, zm_yunxia, zm_yunyang, zf_xiaobei, zf_xiaoni, zf_xiaoxiao, zf_xiaoyi
KOKORO_VOICE = "bm_lewis"
KOKORO_LANG = None             # Auto-detects en-gb from bm_ prefix
KOKORO_SPEED = 0.85            # Slowed-down aristocratic philosophical cadence

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam / deep narrator

# Edge-TTS Fallback Settings
VOICE_HOST1 = "en-US-GuyNeural"
VOICE_HOST2 = "en-US-GuyNeural"
HOST1_NAME = "The Dionysian"
HOST2_NAME = "The Dionysian"
HOST1_SPEAKER = "male"
HOST2_SPEAKER = "male"
HOST1_PITCH = "+0Hz"
HOST2_PITCH = "+0Hz"
TTS_RATE = "+0%"
PAUSE_BETWEEN_TURNS = 0.45

# Subtitle Sentence Chunking
MAX_WORDS_PER_CHUNK = 14
MAX_CHARS_PER_LINE = 28

# AI Generation Settings
POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY", "sk_B0I1QMA8hWP14sICrnx1S1pt8riQdpLZ")
POLLINATIONS_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"
POLLINATIONS_MODEL = "gemini-fast"
NICHE_PROMPT = "Deep philosophical exploration of Friedrich Nietzsche's aphorisms, human psychology, the nature of women and love, will to power, and the illusions of modern morality, narrated with profound wisdom, intellectual rigor, and poetic gravitas."

# Typography Candidates
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\georgiab.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\timesbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), "arial.ttf")
FALLBACK_FONT_PATH = FONT_PATH
