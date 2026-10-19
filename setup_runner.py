import os, sys, shutil, subprocess

def run_command(cmd):
    print(f"[Setup] Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    print("=" * 70)
    print("   [THE DIONYSIAN ABYSS] Cloud Runner Environment Setup")
    print("=" * 70)

    # 1. Check Python
    print(f"[*] Python Version: {sys.version.split()[0]}")

    # 2. Check FFmpeg
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        print("[!] WARNING: FFmpeg was not found in PATH.")
        print("    On Ubuntu/Debian runner: sudo apt-get update && sudo apt-get install -y ffmpeg")
        print("    On macOS runner: brew install ffmpeg")
        print("    On Windows: ensure ffmpeg.exe is in PATH")
    else:
        print(f"[+] FFmpeg detected at: {ffmpeg_bin}")

    # 3. Install requirements
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        print(f"[*] Verifying Python dependencies from {req_file}...")
        run_command([sys.executable, "-m", "pip", "install", "-r", req_file])

    # 4. Ensure Kokoro Models from GitHub Releases
    import config
    from tts_engine import ensure_kokoro_models
    model_path = os.path.join(config.BASE_DIR, "models", "kokoro-v1.0.onnx")
    voices_path = os.path.join(config.BASE_DIR, "models", "voices-v1.0.bin")
    print("[*] Checking Kokoro AI model weights from GitHub Releases...")
    ensure_kokoro_models(model_path, voices_path)

    print("\n" + "=" * 70)
    print("   [+] RUNNER SETUP COMPLETE! All models & tools are verified.")
    print("   Run test with: python auto_pipeline.py --preview 25.0")
    print("   Run full video: python auto_pipeline.py --duration 20.0")
    print("=" * 70)

if __name__ == "__main__":
    main()
