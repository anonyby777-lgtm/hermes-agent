#!/usr/bin/env python3
"""Skill MOLDURA 1 - aplica moldura + logo NUAKEY num video (padrao aprovado v6).
Uso:
  python3 molduras/apply_moldura.py VIDEO.mp4 -o SAIDA.mp4
  python3 molduras/apply_moldura.py VIDEO.mp4 --moldura molduras/nova_moldura.png -o SAIDA.mp4
"""
import argparse, os, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

def find_ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    cand = "/home/user/ffenv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
    return cand if os.path.exists(cand) else "ffmpeg"

def video_size(path, ffmpeg):
    out = subprocess.run([ffmpeg, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", out)
    if not m: sys.exit("nao consegui ler o tamanho do video")
    return int(m.group(1)), int(m.group(2))

def with_opacity(img, op):
    """Normaliza alpha (max->255) e aplica a opacidade alvo."""
    r, g, b, a = img.split()
    mx = a.getextrema()[1] or 1
    a = a.point(lambda v: int(v / mx * 255 * op))
    return Image.merge("RGBA", (r, g, b, a))

def draw_moldura(W, H, margem=8, linha=2, raio=12, gap=0.40, op=0.5):
    """Desenha a moldura MOLDURA 1 no tamanho do video."""
    S = 2
    f = Image.new("RGBA", (W*S, H*S), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)
    m, lw, r = margem*S, linha*S, raio*S
    d.rounded_rectangle([m, m, W*S-m, H*S-m], radius=r, outline=(255, 255, 255, 255), width=lw)
    g0, g1 = int(W*S*gap/2), int(W*S*(1-gap/2))
    d.rectangle([g0, H*S-m-lw-2, g1, H*S-m+lw+2], fill=(0, 0, 0, 0))
    f = f.resize((W, H), Image.LANCZOS)
    return with_opacity(f, op)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--moldura", default=None, help="PNG da moldura (se omitido, desenha a MOLDURA 1)")
    p.add_argument("--logo", default="logos/nuaky_crop.png")
    p.add_argument("--moldura-op", type=float, default=0.5)
    p.add_argument("--logo-op", type=float, default=0.5)
    p.add_argument("--logo-w", type=float, default=0.39)
    p.add_argument("--logo-y", type=float, default=0.89)
    p.add_argument("--margem", type=int, default=8)
    a = p.parse_args()

    repo = Path(__file__).resolve().parent.parent
    ffmpeg = find_ffmpeg()
    W, H = video_size(a.video, ffmpeg)
    print(f"video: {W}x{H}")

    if a.moldura:
        mold = Image.open(a.moldura).convert("RGBA")
        if mold.size != (W, H):
            print(f"moldura redimensionada {mold.size} -> ({W},{H})")
            mold = mold.resize((W, H), Image.LANCZOS)
        mold = with_opacity(mold, a.moldura_op)
    else:
        mold = draw_moldura(W, H, margem=a.margem, op=a.moldura_op)
    mold_p = "/tmp/_moldura_skill.png"
    mold.save(mold_p)

    logo_p = a.logo if os.path.isabs(a.logo) else str(repo / a.logo)
    logo = with_opacity(Image.open(logo_p).convert("RGBA"), a.logo_op)
    tw = int(W * a.logo_w)
    th = int(logo.height * tw / logo.width)
    logo_p2 = "/tmp/_logo_skill.png"
    logo.save(logo_p2)

    fc = (f"[0:v][1:v]overlay=0:0[f];"
          f"[2:v]scale={tw}:{th}[l];"
          f"[f][l]overlay=x=(W-w)/2:y=H*{a.logo_y}-h/2[out]")
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-i", a.video, "-i", mold_p, "-i", logo_p2,
           "-filter_complex", fc, "-map", "[out]", "-map", "0:a?",
           "-c:v", "libx264", "-crf", "19", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-c:a", "copy", a.out]
    subprocess.run(cmd, check=True)
    print("OK:", a.out)

if __name__ == "__main__":
    main()
