"""Render a TikTok cut from an edit plan (source-time) of DJI_..._0135_D.MP4.

Usage: python -I render.py PLAN.json OUT.mp4 [--voice VOICE.wav] [--preview]

Plan keys (all times in SOURCE seconds unless noted):
  segments: [{in, out, zoom, cy, push}]   picture+audio pieces, in order
  super:    [{s, e, lines: [[text, color], ...] or [[[text,color],[text,color]], ...]}]
  subs:     [{s, e, text}]
  flash:    [src_t]                         white flash + whoosh
  logo:     {s, e, path}                    end card logo
  voice:    optional, replaces the source audio with an external VO whose clock is the OUTPUT clock;
            then segments carry 'vo_s' (output time) and super/subs use output time via key 'clock':'out'.
"""
import json, os, subprocess, sys, math, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RAW = os.path.join(ROOT, "Raw File", "DJI_20260814181807_0135_D.MP4")
W, H, FPS = 1080, 1920, 60
SRC_W, SRC_H = 1728, 3072
FONT_SUPER = "Leelawadee UI"
COLORS = {"w": "&H00FFFFFF&", "c": "&H00FFE500&", "y": "&H0000E1FF&"}  # ASS BGR: cyan #00E5FF, yellow #FFE100


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r


def ts(t):
    t = max(0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_map(segs):
    out = 0.0; m = []
    for sg in segs:
        d = sg["out"] - sg["in"]
        m.append((sg["in"], sg["out"], out)); out += d
    return m, out


def to_out(m, t, prefer_end=False):
    best = None
    for a, b, o in m:
        if a - 1e-6 <= t <= b + 1e-6:
            v = o + (t - a)
            if best is None or (prefer_end and v > best) or (not prefer_end and v < best):
                best = v if best is None else (max(best, v) if prefer_end else min(best, v))
    if best is None:  # snap to nearest boundary
        cand = []
        for a, b, o in m:
            cand.append((abs(t - a), o)); cand.append((abs(t - b), o + b - a))
        best = min(cand)[1]
    return best


def esc(s):
    return s.replace("{", "(").replace("}", ")")


def ass_doc(plan, m, dur):
    clock_out = plan.get("clock") == "out"
    T = (lambda t, e=False: t) if clock_out else (lambda t, e=False: to_out(m, t, e))
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Super,{FONT_SUPER},118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,11,7,5,70,70,0,222
Style: Sub,{FONT_SUPER},52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,5,2,2,110,110,0,222
Style: Flash,Arial,10,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    pops = []
    sy = plan.get("super_y", 1130)
    for c in plan.get("super", []):
        s, e = T(c["s"]), T(c["e"], True)
        if e - s < 0.3: e = s + 0.3
        lines = c["lines"]
        n = len(lines); lh = 128
        for k, ln in enumerate(lines):
            parts = ln if isinstance(ln[0], list) else [ln]
            txt = "".join(f"{{\\c{COLORS[col]}}}{esc(t)}" for t, col in parts)
            y = int(sy - (n - 1) * lh / 2 + k * lh)
            delay = int(k * 90)
            anim = (f"{{\\pos(540,{y})\\fscx0\\fscy0\\t({delay},{delay+90},\\fscx118\\fscy118)"
                    f"\\t({delay+90},{delay+170},\\fscx100\\fscy100)}}")
            ev.append(f"Dialogue: 2,{ts(s)},{ts(e)},Super,,0,0,0,,{anim}{txt}")
        pops.append(s)
    for c in plan.get("subs", []):
        s, e = T(c["s"]), T(c["e"], True)
        ev.append(f"Dialogue: 1,{ts(s)},{ts(e)},Sub,,0,0,0,,{{\\pos(540,{plan.get('sub_y', 1545)})}}{esc(c['text'])}")
    whoosh = []
    for f in plan.get("flash", []):
        s = T(f)
        ev.append(f"Dialogue: 5,{ts(max(0, s - 0.02))},{ts(s + 0.22)},Flash,,0,0,0,,"
                  f"{{\\pos(0,0)\\alpha&H40&\\t(0,220,\\alpha&HFF&)\\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
        whoosh.append(max(0, s - 0.15))
    return hdr + "\n".join(ev) + "\n", pops, whoosh


def render_segments(plan, work):
    parts = []
    os.makedirs(os.path.join(work, "seg"), exist_ok=True)
    for i, sg in enumerate(plan["segments"]):
        z = sg.get("zoom", 1.0); cy = sg.get("cy", 0.42); push = sg.get("push", 0.0)
        d = sg["out"] - sg["in"]
        cw = int(SRC_W / z) // 2 * 2; chh = int(SRC_H / z) // 2 * 2
        y0 = int(min(max(cy * SRC_H - chh / 2, 0), SRC_H - chh))
        x0 = (SRC_W - cw) // 2
        vf = f"crop={cw}:{chh}:{x0}:{y0},scale={W}:{H}:flags=lanczos"
        if push:
            vf += (f",scale=w='trunc({W}*(1+{push}*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,"
                   f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.45")
        vf += f",fps={FPS},format=yuv420p"
        key = json.dumps(sg, sort_keys=True)
        p = os.path.join(work, "seg", f"s{i:03d}.mkv")
        kp = p + ".key"
        src = sg.get("src")
        if src and not (os.path.exists(p) and os.path.exists(kp) and open(kp).read() == key):
            # B-roll clip or still: cover-scale to 9:16, silent audio
            path = os.path.join(ROOT, src)
            is_img = src.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            fx = sg.get("fx", 0.5)
            bvf = (f"scale={W}*{z}:{H}*{z}:force_original_aspect_ratio=increase:flags=lanczos,"
                   f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})*{cy}")
            if push:
                bvf += (f",scale=w='trunc({W}*(1+{push}*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,"
                        f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2")
            bvf += f",fps={FPS},format=yuv420p,setsar=1"
            vin = (["-loop", "1", "-framerate", str(FPS), "-i", path] if is_img
                   else ["-ss", f"{sg.get('ss', 0):.3f}", "-i", path])
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *vin,
                 "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{d:.3f}",
                 "-map", "0:v:0", "-map", "1:a:0", "-vf", bvf,
                 "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "pcm_s24le", "-ar", "48000", "-ac", "2", p])
            open(kp, "w").write(key)
        if not (os.path.exists(p) and os.path.exists(kp) and open(kp).read() == key):
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{sg['in']:.3f}", "-i", RAW,
                 "-t", f"{d:.3f}", "-map", "0:v:0", "-map", "0:a:0", "-vf", vf,
                 "-af", f"afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.3f}:d=0.012",
                 "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "pcm_s24le", "-ar", "48000", "-ac", "2", p])
            open(kp, "w").write(key)
        parts.append(p)
    lst = os.path.join(work, "seg", "list.txt")
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{os.path.basename(p)}'\n")
    joined = os.path.join(work, "joined.mkv")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", joined])
    return joined


def make_sfx(work):
    pop = os.path.join(work, "sfx_pop.wav"); wh = os.path.join(work, "sfx_whoosh.wav")
    if not os.path.exists(pop):
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
             "aevalsrc='0.6*sin(2*PI*(500+1400*exp(-t*40))*t)*exp(-t*28)':s=48000:d=0.16", "-ac", "2", pop])
    if not os.path.exists(wh):
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
             "anoisesrc=d=0.45:c=pink:r=48000:a=0.8", "-af",
             "bandpass=f=1800:width_type=o:w=2.5,afade=t=in:d=0.25:curve=exp,afade=t=out:st=0.25:d=0.2,volume=1.6",
             "-ac", "2", wh])
    return pop, wh


def main():
    plan_path, out = sys.argv[1], sys.argv[2]
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else None
    plan = json.load(open(plan_path, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(out))[0]
    work = os.path.join(HERE, "build_" + plan.get("build", name))
    os.makedirs(work, exist_ok=True)
    m, dur = build_map(plan["segments"])
    joined = render_segments(plan, work)
    ass, pops, whoosh = ass_doc(plan, m, dur)
    ass_path = os.path.join(work, "text.ass")
    open(ass_path, "w", encoding="utf-8").write(ass)
    pop, wh = make_sfx(work)

    # audio chain
    inputs = ["-i", joined]
    voice_idx = 0
    if voice:
        inputs += ["-i", voice]; voice_idx = 1
    base_idx = len(inputs) // 2
    inputs += ["-i", pop, "-i", wh]
    room = plan.get("room_tone")
    fc = []
    if voice:
        vchain = plan.get("vo_chain", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
                                       "equalizer=f=250:t=q:w=1.2:g=1.5,equalizer=f=6500:t=q:w=1.5:g=-1.5,aecho=0.8:0.25:18:0.08")
        fc.append(f"[{voice_idx}:a]aresample=48000,aformat=channel_layouts=stereo,{vchain},apad=whole_dur={dur:.3f}[v]")
        if room:
            fc.append(f"[0:a]highpass=f=60,lowpass=f=3000,volume={room}[rt]")
            fc.append("[v][rt]amix=inputs=2:normalize=0:duration=first[vm]")
            vlabel = "vm"
        else:
            vlabel = "v"
    else:
        fc.append("[0:a]highpass=f=80,afftdn=nf=-28,acompressor=threshold=-22dB:ratio=3:attack=5:release=90,"
                  "equalizer=f=3500:t=q:w=1.5:g=2[v]")
        vlabel = "v"
    mix = [f"[{vlabel}]"]
    n = 1
    for k, t in enumerate(pops):
        fc.append(f"[{base_idx}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.22[p{k}]"); mix.append(f"[p{k}]"); n += 1
    for k, t in enumerate(whoosh):
        fc.append(f"[{base_idx+1}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.30[w{k}]"); mix.append(f"[w{k}]"); n += 1
    fc.append("".join(mix) + f"amix=inputs={n}:normalize=0:duration=first,atrim=0:{dur:.3f}[mx]")
    mix_wav = os.path.join(work, "mix.wav")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[mx]", "-c:a", "pcm_s24le", "-ar", "48000", mix_wav])
    # two-pass loudnorm to -14 LUFS / -1.5 dBTP
    r = run(["ffmpeg", "-hide_banner", "-i", mix_wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"])
    js = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    L = json.loads(js)
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={L['input_i']}:measured_TP={L['input_tp']}:"
          f"measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true")
    final_wav = os.path.join(work, "final.wav")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mix_wav, "-af", ln + ",aresample=48000",
         "-c:a", "pcm_s24le", final_wav])

    # picture + text + logo
    vf_in = []
    rel_ass = os.path.relpath(ass_path, HERE).replace("\\", "/")
    logo = plan.get("logo")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", joined, "-i", final_wav]
    if logo:
        cmd += ["-loop", "1", "-i", os.path.join(ROOT, logo["path"])]
        T = (lambda t: t) if plan.get("clock") == "out" else (lambda t: to_out(m, t))
        ls_, le_ = T(logo["s"]), T(logo["e"])
        sz = logo.get("size", 420)
        fcv = (f"[2:v]scale={sz}:-1,format=rgba,fade=t=in:st={ls_:.2f}:d=0.25:alpha=1[lg];"
               f"[0:v][lg]overlay=(W-w)/2:{logo.get('y', 300)}:enable='between(t,{ls_:.2f},{le_:.2f})':shortest=1[v1];"
               f"[v1]subtitles='{rel_ass}':fontsdir='C\\:/Windows/Fonts'[vo]")
    else:
        fcv = f"[0:v]subtitles='{rel_ass}':fontsdir='C\\:/Windows/Fonts'[vo]"
    crf = str(plan.get("crf", 18))
    tmp = out + ".part.mp4"
    cmd += ["-filter_complex", fcv, "-map", "[vo]", "-map", "1:a", "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "slow" if "--preview" not in sys.argv else "veryfast", "-crf", crf,
            "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp]
    old = os.getcwd(); os.chdir(HERE)
    try:
        run(cmd)
    finally:
        os.chdir(old)
    os.replace(tmp, out)
    # SRT on output clock
    srt = os.path.splitext(out)[0] + ".srt"
    T = (lambda t, e=False: t) if plan.get("clock") == "out" else (lambda t, e=False: to_out(m, t, e))
    def st(t):
        ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
    with open(srt, "w", encoding="utf-8") as f:
        for k, c in enumerate(plan.get("subs", []), 1):
            f.write(f"{k}\n{st(T(c['s']))} --> {st(T(c['e'], True))}\n{c['text']}\n\n")
    print(json.dumps({"out": out, "srt": srt, "duration": round(dur, 3), "segments": len(plan["segments"])}))


if __name__ == "__main__":
    main()
