"""Обрезка концовки «старт первого ноября» у роликов для YouTube (решение Мансура 18.11.2026).

Shorts: убирается сцена outro, длинные: сцена cta. Длительность сцены считается как в video/src/plan.js:
lead 4 кадра + голос (speechEndMs) + хвост (outro 36, cta 60), 30 кадров/с. В конце — затухание 0,4 с.
Shorts пережимаются до < 9,5 МБ (одна загрузка через Chrome), длинные — CRF 23.

Запуск: .venv/Scripts/python.exe tools/social/trim_outro.py  →  u/yt/<ID>.mp4 (вне Git)
"""
import json
import math
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'deliverables'
OUT = ROOT / 'u' / 'yt'
FPS = 30
TAIL = {'outro': 36, 'cta': 60}
SHORTS = [f'R{i:03d}' for i in range(1, 20)] + [f'B{i:03d}' for i in range(1, 20)] + [f'S{i:03d}' for i in range(1, 5)]
LONG = ['Y009', 'Y010', 'Y011', 'Y012']


def duration(p: Path) -> float:
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def cut_point(vid: str, total: float) -> float:
    t = json.loads((ROOT / 'video/src/reels' / f'{vid.lower()}.timing.json').read_text(encoding='utf-8'))
    last = t['scenes'][-1]
    assert last['id'] in TAIL, (vid, last['id'])
    frames = 4 + math.ceil(last['speechEndMs'] / 1000 * FPS) + TAIL[last['id']]
    return total - frames / FPS


def encode(src: Path, dst: Path, end: float, vbit: str | None):
    fade = max(end - 0.4, 0)
    v = ['-c:v', 'libx264', '-preset', 'slow', '-pix_fmt', 'yuv420p']
    v += ['-b:v', vbit, '-maxrate', vbit, '-bufsize', vbit] if vbit else ['-crf', '23']
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src), '-t', f'{end:.3f}',
                    '-vf', f'fade=t=out:st={fade:.3f}:d=0.4', '-af', f'afade=t=out:st={fade:.3f}:d=0.4',
                    *v, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(dst)], check=True)


def main(ids):
    OUT.mkdir(parents=True, exist_ok=True)
    for vid in ids:
        src = SRC / ('youtube' if vid.startswith('Y') else 'reels') / f'{vid}.mp4'
        total = duration(src)
        end = cut_point(vid, total)
        dst = OUT / f'{vid}.mp4'
        if vid.startswith('Y'):
            encode(src, dst, end, None)
        else:
            kbps = int((9.3 * 8 * 1024) / end - 140)  # уложиться в ~9,3 МБ вместе со звуком
            encode(src, dst, end, f'{min(kbps, 4000)}k')
        print(f'{vid}: {total:.1f} → {end:.1f} с, {dst.stat().st_size / 1e6:.1f} МБ')


if __name__ == '__main__':
    main(sys.argv[1:] or SHORTS + LONG)
