#!/usr/bin/env python3
"""Script de processamento rápido de vídeos usando a Skill NUAKEY.
Varre a pasta videos/ ou arquivos enviados e aplica a moldura automaticamente.
"""
import os
import sys
import glob
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

def get_next_version():
    entregas = list(REPO_ROOT.glob("entregas/NUAKY_edit_v*.mp4"))
    nums = [0]
    for p in entregas:
        m = re.search(r"NUAKY_edit_v(\d+)\.mp4", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1

def process_video(video_path, moldura=None):
    video_path = Path(video_path).resolve()
    v_num = get_next_version()
    out_dir = REPO_ROOT / "entregas"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"NUAKY_edit_v{v_num}.mp4"
    
    cmd = [
        sys.executable,
        str(REPO_ROOT / "molduras" / "apply_moldura.py"),
        str(video_path),
        "-o",
        str(out_file)
    ]
    if moldura:
        cmd.extend(["--moldura", str(moldura)])
        
    print(f"🎬 Processando: {video_path.name} -> {out_file.name}...")
    subprocess.run(cmd, check=True)
    print(f"✅ Vídeo gerado com sucesso: {out_file}")
    print(f"📦 Link GitHub (após push): https://github.com/anonyby777-lgtm/hermes-agent/blob/arena/01a0a872-hermes-agent/entregas/{out_file.name}")
    print(f"🔗 Link Raw Direto: https://raw.githubusercontent.com/anonyby777-lgtm/hermes-agent/arena/01a0a872-hermes-agent/entregas/{out_file.name}")
    return out_file

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vid = sys.argv[1]
        mold = sys.argv[2] if len(sys.argv) > 2 else None
        process_video(vid, mold)
    else:
        # Check videos folder
        vids = list((REPO_ROOT / "videos").glob("*.mp4")) + list((REPO_ROOT / "videos").glob("*.mov"))
        if not vids:
            print("Nenhum vídeo novo encontrado na pasta videos/.")
            print("Envie pelo link: https://github.com/anonyby777-lgtm/hermes-agent/upload/arena/01a0a872-hermes-agent/videos")
        else:
            for v in vids:
                process_video(v)
