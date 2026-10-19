import os, glob, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config
from audio_visualizer import AudioSpectrumVisualizer

def get_rotating_images(images_dir: str) -> list:
    """Scans the images folder and returns all valid image paths sorted."""
    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp")
    all_files = []
    for ext in valid_exts:
        all_files.extend(glob.glob(os.path.join(images_dir, ext)))
        all_files.extend(glob.glob(os.path.join(images_dir, ext.upper())))

    all_files = sorted(list(set(all_files)))
    if not all_files:
        if os.path.exists(config.DEFAULT_IMAGE_PATH):
            all_files = [config.DEFAULT_IMAGE_PATH]
        else:
            raise FileNotFoundError(f"No background images found in {images_dir}")
    return all_files

def prepare_base_image(img_path: str, logo_img: Image.Image, font_brand: ImageFont.ImageFont, font_path: str) -> Image.Image:
    """Loads an image, resizes to 1920x1080 with cinematic grading, and stamps permanent static branding and the Wisdom Slate."""
    raw = Image.open(img_path).convert("RGBA")
    if raw.size != (config.VIDEO_WIDTH, config.VIDEO_HEIGHT):
        raw = raw.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)

    # Right-side shadow gradient for depth
    overlay = Image.new("RGBA", (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for x in range(800, config.VIDEO_WIDTH):
        alpha = int(min(160, (x - 800) / (config.VIDEO_WIDTH - 800) * 160))
        ov_draw.line([(x, 0), (x, config.VIDEO_HEIGHT)], fill=(6, 8, 12, alpha))
    raw = Image.alpha_composite(raw, overlay)

    draw = ImageDraw.Draw(raw)

    # 1. Circular Channel Logo Badge with Gold Rim (Top-Left)
    logo_size = 104
    logo_x, logo_y = 50, 35
    if logo_img:
        try:
            resized_logo = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            mask = Image.new("L", (logo_size * 4, logo_size * 4), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.ellipse((0, 0, logo_size * 4, logo_size * 4), fill=255)
            mask = mask.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            circular_logo = Image.new("RGBA", (logo_size, logo_size), (0, 0, 0, 0))
            circular_logo.paste(resized_logo, (0, 0), mask)
            raw.paste(circular_logo, (logo_x, logo_y), circular_logo)

            draw.ellipse(
                [(logo_x - 2, logo_y - 2), (logo_x + logo_size + 2, logo_y + logo_size + 2)],
                outline=(218, 165, 32, 240),
                width=3
            )
        except Exception:
            pass

    # 2. Top Branding Pill: [Amber Dot] THE DIONYSIAN ABYSS
    bbox = draw.textbbox((0, 0), config.CHANNEL_NAME, font=font_brand)
    text_w = bbox[2] - bbox[0]
    pill_start_x = 168
    text_start_x = pill_start_x + 46
    pill_end_x = text_start_x + text_w + 32

    draw.rounded_rectangle(
        [(pill_start_x, 50), (pill_end_x, 112)],
        radius=30,
        fill=(14, 16, 24, 230),
        outline=(218, 165, 32, 220),
        width=2
    )
    dot_cx = pill_start_x + 23
    draw.ellipse([(dot_cx - 8, 81 - 8), (dot_cx + 8, 81 + 8)], fill=(245, 175, 40))
    draw.text((text_start_x, 66), config.CHANNEL_NAME, fill=(255, 255, 255), font=font_brand)

    # 3. Footer Divider and Tagline
    draw.line([(0, 1025), (config.VIDEO_WIDTH, 1025)], fill=(40, 42, 54), width=2)
    f_footer = ImageFont.truetype(font_path, 24)
    draw.text((config.SUBTITLE_CENTER_X, 1052), config.TAGLINE, fill=(215, 205, 185), font=f_footer, anchor="mm")

    # 4. Stamp the Unified Wisdom Slate Frame onto Base Image
    p_left = getattr(config, "PANEL_LEFT", 930)
    p_top = getattr(config, "PANEL_TOP", 180)
    p_right = getattr(config, "PANEL_RIGHT", 1830)
    p_bot = getattr(config, "PANEL_BOT", 860)

    # Dark Obsidian Slate Body
    draw.rounded_rectangle([(p_left, p_top), (p_right, p_bot)], radius=24, fill=(10, 12, 18, 230), outline=(218, 165, 32, 200), width=2)

    # Slate Header Pill
    f_header = ImageFont.truetype(font_path, 22)
    draw.rounded_rectangle([(p_left + 28, p_top + 20), (p_right - 28, p_top + 68)], radius=12, fill=(18, 22, 32, 240), outline=(218, 165, 32, 120), width=1)
    draw.text(((p_left + p_right) // 2, p_top + 44), "• THE DIONYSIAN ABYSS • PHILOSOPHY OF NIETZSCHE •", fill=(245, 205, 90), font=f_header, anchor="mm")

    return raw

def layout_sentence_chunk(words: list, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw, space_w: int) -> list:
    """Wraps words of a sentence into balanced lines fitting within max_width."""
    lines = []
    curr_line = []
    curr_w = 0

    for w in words:
        w_text = w["word"]
        w_len = draw.textbbox((0, 0), w_text, font=font)[2]
        add_w = w_len if not curr_line else (space_w + w_len)

        if curr_line and (curr_w + add_w > max_width):
            lines.append(curr_line)
            curr_line = [{**w, "width": w_len}]
            curr_w = w_len
        else:
            curr_line.append({**w, "width": w_len})
            curr_w += add_w

    if curr_line:
        lines.append(curr_line)
    return lines

def render_podcast_video(audio_path: str, subtitle_chunks: list, output_video_path: str, fps: int = 30, preview_seconds: float = None) -> str:
    print(f"[VideoComposer] Initializing video render: {output_video_path}...")
    visualizer = AudioSpectrumVisualizer(audio_path, fps=fps)
    total_frames = visualizer.total_frames
    if preview_seconds:
        total_frames = min(total_frames, int(preview_seconds * fps))
        print(f"[VideoComposer] Preview active: rendering {total_frames} frames ({preview_seconds:.1f}s)...")

    # Discover rotating background images
    images_dir = config.IMAGES_DIR
    image_paths = get_rotating_images(images_dir)
    print(f"[VideoComposer] Found {len(image_paths)} rotating images in {images_dir}:")
    for i, ipath in enumerate(image_paths):
        print(f"  [{i+1}] {os.path.basename(ipath)}")

    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH
    font_quote = ImageFont.truetype(font_path, 34)
    font_brand = ImageFont.truetype(font_path, 28)

    # Load logo if available
    logo_img = None
    if os.path.exists(config.LOGO_PATH):
        try:
            logo_img = Image.open(config.LOGO_PATH).convert("RGBA")
        except Exception:
            logo_img = None

    # Pre-render base images for all rotating portraits
    print("[VideoComposer] Pre-processing rotating background frames with Unified Wisdom Slate...")
    prepared_bases = [prepare_base_image(p, logo_img, font_brand, font_path) for p in image_paths]
    num_images = len(prepared_bases)

    # Rotation timing parameters
    rotation_period = getattr(config, "IMAGE_ROTATION_SECONDS", 30.0)
    trans_duration = getattr(config, "IMAGE_TRANSITION_SECONDS", 1.5)

    # Pre-render & layout sentence chunks within the Wisdom Slate reading chamber
    p_left = getattr(config, "PANEL_LEFT", 930)
    p_top = getattr(config, "PANEL_TOP", 180)
    p_right = getattr(config, "PANEL_RIGHT", 1830)
    p_bot = getattr(config, "PANEL_BOT", 860)

    center_x = (p_left + p_right) // 2
    chamber_top = p_top + 90
    chamber_bot = getattr(config, "VIS_BASE_Y", 780) - 50
    chamber_mid_y = (chamber_top + chamber_bot) // 2
    max_reading_w = (p_right - p_left) - 90  # 810px usable width

    dummy_draw = ImageDraw.Draw(prepared_bases[0])
    space_w = dummy_draw.textbbox((0, 0), " ", font=font_quote)[2]
    line_height = 50

    processed_chunks = []
    for c in subtitle_chunks:
        words = c["words"]
        if not words:
            continue

        wrapped_lines = layout_sentence_chunk(words, font_quote, max_reading_w, dummy_draw, space_w)
        total_text_h = len(wrapped_lines) * line_height
        start_y = chamber_mid_y - (total_text_h // 2)

        positioned_lines = []
        for l_idx, line_words in enumerate(wrapped_lines):
            line_w = sum(w["width"] for w in line_words) + max(0, len(line_words) - 1) * space_w
            curr_x = center_x - (line_w // 2)
            y_pos = start_y + l_idx * line_height

            word_positions = []
            for w in line_words:
                word_positions.append({
                    "word": w["word"],
                    "start": w["start"],
                    "end": w["end"],
                    "width": w["width"],
                    "x": curr_x,
                    "y": y_pos
                })
                curr_x += w["width"] + space_w

            positioned_lines.append(word_positions)

        processed_chunks.append({
            "start": c["start"],
            "end": c["end"],
            "lines": positioned_lines
        })

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video_path
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    total_audio_sec = total_frames / float(fps)
    active_chunk_idx = 0
    num_chunks = len(processed_chunks)

    # Frame rendering loop with dynamic image rotation & unified slate
    for f_idx in range(total_frames):
        t_sec = f_idx / float(fps)

        # 1. Determine rotating background image
        if num_images == 1:
            current_base = prepared_bases[0]
        else:
            cycle_idx = int(t_sec // rotation_period)
            curr_img_idx = cycle_idx % num_images
            next_img_idx = (cycle_idx + 1) % num_images
            time_in_period = t_sec % rotation_period

            if time_in_period > (rotation_period - trans_duration):
                blend_ratio = (time_in_period - (rotation_period - trans_duration)) / trans_duration
                current_base = Image.blend(prepared_bases[curr_img_idx], prepared_bases[next_img_idx], blend_ratio)
            else:
                current_base = prepared_bases[curr_img_idx]

        frame_img = current_base.copy()
        draw = ImageDraw.Draw(frame_img)

        # 2. Draw audio spectrum visualizer (Anchored in bottom of Wisdom Slate)
        visualizer.draw_frame(draw, f_idx)

        # 3. Draw gold progress line
        ratio = min(1.0, t_sec / max(1.0, total_audio_sec))
        draw.line([(0, 1025), (int(config.VIDEO_WIDTH * ratio), 1025)], fill=(218, 165, 32), width=4)

        # 4. Locate active sentence chunk smoothly (persist during natural pauses)
        while active_chunk_idx < num_chunks - 1 and t_sec >= processed_chunks[active_chunk_idx + 1]["start"]:
            active_chunk_idx += 1

        curr_c = processed_chunks[active_chunk_idx] if active_chunk_idx < num_chunks else None
        chunk = None
        if curr_c and (curr_c["start"] <= t_sec <= (curr_c["end"] + 1.0)):
            chunk = curr_c

        # 5. Draw sentence words inside Wisdom Slate with radiant gold active highlighting
        if chunk:
            for line_words in chunk["lines"]:
                for wm in line_words:
                    is_active = (wm["start"] <= t_sec <= wm["end"])
                    color = (255, 215, 0) if is_active else (245, 240, 230)
                    # Drop shadow
                    draw.text((wm["x"] + 2, wm["y"] + 2), wm["word"], fill=(0, 0, 0, 220), font=font_quote)
                    draw.text((wm["x"], wm["y"]), wm["word"], fill=color, font=font_quote)

        raw_bgr = np.array(frame_img.convert("RGB"))[:, :, ::-1].tobytes()
        pipe.stdin.write(raw_bgr)

        if (f_idx + 1) % (fps * 30) == 0:
            print(f"  [Video Render] Progress: {f_idx + 1}/{total_frames} frames ({(f_idx+1)/fps:.1f}s / {total_audio_sec:.1f}s)")

    pipe.stdin.close()
    pipe.wait()
    print(f"[VideoComposer] Video rendered successfully: {output_video_path}")
    return output_video_path
