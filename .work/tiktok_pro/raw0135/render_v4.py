"""v4 (= v3 cut/audio/B-roll) + new minimal font, blue-white brand palette, cool clean grade.
v3: original voice (v1 A-roll) + B-roll cards over blurred A-roll, example-style text, Mixkit music + SFX.
Usage: python -X utf8 -I render_v4.py OUT.mp4   env: FONT_NAME, FONT_DIR (under assets/fonts), GRADE=1/0, CARD_DIR
All times are OUTPUT clock of build_v1/joined.mkv (27.41 s).
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
AROLL = os.path.join(HERE, "build_v3a", "joined.mkv")   # v1 cut, reframed higher
WORK = os.path.join(HERE, os.environ.get("WORK_NAME", "build_v4"))
AUD = os.path.join(ROOT, "assets", "audio_mixkit")
SFXD = os.path.join(ROOT, "assets", "sfx_muaaz")   # Muaaz "Sound Effects Creators Actually Use" (index.csv: onset/peak)
W, H, FPS = 1080, 1920, 60
DUR_SRC = 26.65   # end on her smile, before she reaches for the mic
# tighten: drop the redundant line "ก็อาจจะทำให้เกิดปัญหา กับสินค้ากับทางร้านค้าได้" then speed up 1.1x
CUT_A = CUT_B = None   # no line removed (user: content must stay complete)
GAP = 0 if CUT_A is None else CUT_B - CUT_A
SPEED = 1.0   # no time-stretch: keeps the voice natural
def M(t):
    return t if CUT_A is None or t <= CUT_A else (CUT_A if t < CUT_B else t - GAP)
def gone(s, e):
    return CUT_A is not None and s >= CUT_A - 1e-6 and e <= CUT_B + 1e-6
DUR = M(DUR_SRC)
CW, CH, BR = 700, 1244, 8          # card size, border
FONT = os.environ.get("FONT_NAME", "LINE Seed Sans TH ExtraBold")
FONTDIR = "../../../assets/fonts/" + os.environ.get("FONT_DIR", "lineseed")
GRADE = os.environ.get("GRADE", "1") == "1"
# cool, clean, airy: tame the garden greens/yellows, lift and cool the whites (Space Connex blue-white)
GRADE_VF = ("huesaturation=colors=g+y:saturation=-0.32:strength=1.4,"
            "colorbalance=rs=-0.03:gs=-0.01:bs=0.05:rm=-0.03:gm=-0.01:bm=0.05:rh=-0.02:bh=0.04,"
            "eq=contrast=1.04:brightness=0.025:saturation=0.92:gamma=1.02")   # relative to HERE (render runs with cwd=HERE)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(" ".join(cmd)[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
P = "B-roll/pexels/"
# cutaway windows: (start, end, src, ss)
CUTS = [
    (3.81, 5.56, P + "02_cream_5468796.mp4", 0.0),
    (5.56, 7.29, P + "03b_pan_6216462.mp4", 2.6),
    (7.29, 9.51, P + "04_meat_39327769.mp4", 0.5),
    (9.51, 10.96, "B-roll/pexels_photos/p_40101227.jpg", 0),
    (13.54, 14.86, P + "05_cluttered_26747688.mp4", 0.0),
    (16.56, 17.89, "B-roll/pexels_photos/p_18121624.jpg", 0),
    (17.89, 19.40, P + "04_meat_39327769.mp4", 3.0),   # covers take jump at 19.19
    (20.84, 22.24, P + "08_arranging_6963727.mp4", 1.0),
    (22.24, 23.64, P + "07_neat_store_31858797.mp4", 0.0),
]
CUTS = [(M(s), M(e), src, ss) for s, e, src, ss in CUTS if not gone(s, e)]

# ---------- ASS text ----------
def ts(t):
    t = max(0, t); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

WHT, NAVY, BLUE, KEY = "&H00FFFFFF&", "&H00321B0B&", "&H00C86604&", "&H00FF9A3C&"   # #0B1B32 #0466C8 #3C9AFF
YEL = RED = WHT; CYA = KEY
HDR = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BoxBig,{FONT},84,&H00FFFFFF,&H00FFFFFF,&H00C86604,&H00000000,0,0,0,0,100,100,0,0,3,20,0,5,40,40,0,222
Style: BoxSmall,{FONT},48,&H00321B0B,&H00321B0B,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,3,13,0,5,40,40,0,222
Style: Top,{FONT},76,&H00FFFFFF,&H00FFFFFF,&H00321B0B,&H70321B0B,0,0,0,0,100,100,0,0,1,6,4,5,40,40,0,222
Style: TopBig,{FONT},92,&H00FFFFFF,&H00FFFFFF,&H00C86604,&H00000000,0,0,0,0,100,100,0,0,3,20,0,5,40,40,0,222
Style: Warn,{FONT},88,&H00FFFFFF,&H00FFFFFF,&H00321B0B,&H00000000,0,0,0,0,100,100,0,0,3,18,0,5,40,40,0,222
"""
# spec: pop-up bounce 0% -> 115% -> 100%
POP = "\\fscx0\\fscy0\\t(0,120,\\fscx115\\fscy115)\\t(120,210,\\fscx100\\fscy100)"
C = lambda col, s: f"{{\\c{col}}}{s}{{\\c{WHT}}}"
ev, pops, wrongs = [], [], []


def text(s, e, style, txt, y, x=540, pop=True, color=None, sfx=True):
    if gone(s, e): return
    s, e = M(s), M(e)
    c = f"\\c{color}" if color else ""
    ev.append(f"Dialogue: 3,{ts(s)},{ts(e)},{style},,0,0,0,,{{\\pos({x},{y}){c}{POP if pop else ''}}}{txt}")
    if sfx: pops.append(s)


TY = 262  # top text line (above card)
# hook box (example: yellow headline on black box + white line)
text(0.05, 3.81, "BoxBig", "วางสินค้าผิดที่ = ขายไม่ออก", 1330)
text(0.25, 3.81, "BoxSmall", "เคยเห็นร้านแบบนี้ไหม?", 1440, sfx=False)
text(3.81, 5.56, "Top", C(CYA, "ครีมทาผิว"), TY)
text(5.56, 7.29, "Top", "ครีมทาผิว + " + C(CYA, "กระทะร้อน"), TY, pop=False, sfx=False)
text(5.66, 7.29, "Warn", "วางผิดคู่!", 1490, sfx=False); wrongs.append(5.66)
text(7.29, 9.51, "Top", C(CYA, "ของสด") + " บนเคาน์เตอร์", TY)
text(9.51, 10.96, "Top", C(CYA, "ของสด") + " บนเคาน์เตอร์", TY, pop=False, sfx=False)
text(9.60, 10.96, "Warn", "ไม่มีตู้แช่!", 1490, sfx=False); wrongs.append(9.60)
text(10.98, 13.54, "Top", "\"วาง" + C(CYA, "ผิดจุด") + "\"", 250)
# build-up keywords like the example; newest word in cyan
text(13.54, 14.87, "Top", C(CYA, "ปัญหา"), TY)
text(14.87, 15.60, "Top", "ปัญหา  " + C(CYA, "สินค้า"), 250, pop=False)
text(15.60, 16.56, "Top", "ปัญหา  สินค้า  " + C(CYA, "ร้านค้า"), 250, pop=False)
text(16.56, 17.89, "TopBig", "ขายไม่ออก!", 262)
text(17.89, 19.19, "TopBig", "ขายไม่ออก!", 262, pop=False, sfx=False)
text(19.23, 20.84, "Top", "\"อย่าให้เกิดกับ" + C(CYA, "ร้านคุณ") + "\"", 250)
text(20.88, 23.64, "Top", "วางอะไร " + C(CYA, "คู่กับอะไร?"), TY)
# CTA = designed brand card + button (assets/brand/*.png, overlaid in main)
ASS = HDR + "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ev) + "\n"


def main(final_out):
    os.makedirs(WORK, exist_ok=True)
    global AROLL
    src_aroll = AROLL
    AROLL = os.path.join(WORK, "aroll_tight.mkv")
    if CUT_A is None:
        run(FF + ["-i", src_aroll, "-t", f"{DUR_SRC}", "-c", "copy", AROLL])
    else:
      run(FF + ["-i", src_aroll, "-filter_complex",
              f"[0:v]trim=0:{CUT_A},setpts=PTS-STARTPTS[v0];[0:v]trim={CUT_B}:{DUR_SRC},setpts=PTS-STARTPTS[v1];"
              f"[0:a]atrim=0:{CUT_A},asetpts=PTS-STARTPTS,afade=t=out:st={CUT_A-0.02}:d=0.02[a0];"
              f"[0:a]atrim={CUT_B}:{DUR_SRC},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[a1];"
              f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
              "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
              "-c:a", "pcm_s24le", AROLL])
    out = os.path.join(WORK, "normal_speed.mp4")
    mask = os.path.join(WORK, "mask.png"); border = os.path.join(WORK, "border.png")
    r = 46
    expr = lambda w, h, rr: (f"255*lte(hypot(max(0\\,abs(X-{w}/2)-({w}/2-{rr}))\\,"
                             f"max(0\\,abs(Y-{h}/2)-({h}/2-{rr})))\\,{rr})")
    run(FF + ["-f", "lavfi", "-i", f"color=c=black:s={CW}x{CH}:d=1", "-vf", f"format=gray,geq=lum='{expr(CW, CH, r)}'",
              "-frames:v", "1", mask])
    bw, bh = CW + 2 * BR, CH + 2 * BR
    run(FF + ["-f", "lavfi", "-i", f"color=c=white:s={bw}x{bh}:d=1", "-vf",
              f"format=rgba,geq=r=255:g=255:b=255:a='{expr(bw, bh, r + BR)}'", "-frames:v", "1", border])

    # windows over the full timeline
    wins, t = [], 0.0
    for s, e, src, ss in CUTS:
        if s > t + 1e-3: wins.append((t, s, None, 0))
        wins.append((s, e, src, ss)); t = e
    if t < DUR: wins.append((t, DUR, None, 0))

    parts = []
    for i, (s, e, src, ss) in enumerate(wins):
        d = e - s; p = os.path.join(WORK, f"w{i:02d}.mp4"); parts.append(p)
        key = json.dumps([s, e, src, ss, CW, CH]); kp = p + ".key"
        if os.path.exists(p) and os.path.exists(kp) and open(kp).read() == key:
            continue
        if src is None:
            run(FF + ["-ss", f"{s:.3f}", "-i", AROLL, "-t", f"{d:.3f}", "-an", "-vf", f"fps={FPS},format=yuv420p",
                      "-c:v", "libx264", "-preset", "fast", "-crf", "14", p])
        else:
            path = os.path.join(ROOT, src)
            img = src.lower().endswith((".png", ".jpg", ".jpeg"))
            bin_ = (["-loop", "1", "-framerate", str(FPS), "-i", path] if img else ["-ss", f"{ss:.3f}", "-i", path])
            fc = (f"[0:v]boxblur=28:2,eq=brightness=-0.12:saturation=0.85,fps={FPS}[bg];"
                  f"[1:v]scale=w='trunc({CW}*(1+0.07*t/{d:.3f})/2)*2':h=-2:eval=frame,"
                  f"scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH},fps={FPS},format=rgba[b];"
                  f"[2:v]format=gray,fps={FPS}[m];[b][m]alphamerge[bc];"
                  f"[3:v]format=rgba,fps={FPS}[bd];[bd][bc]overlay={BR}:{BR}:shortest=1[card];"
                  f"[card]scale=w='trunc({bw}*min(1,0.9+0.1*t/0.14)/2)*2':h=-2:eval=frame[cs];"
                  f"[bg][cs]overlay=x=(W-w)/2:y=330+({bh}-h)/2:shortest=1,format=yuv420p[v]")
            run(FF + ["-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", AROLL, *bin_,
                      "-loop", "1", "-framerate", str(FPS), "-i", mask, "-loop", "1", "-framerate", str(FPS), "-i", border,
                      "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}", "-an",
                      "-c:v", "libx264", "-preset", "fast", "-crf", "14", p])
        open(kp, "w").write(key)
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    joined = os.path.join(WORK, "pic.mp4")
    run(FF + ["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    # ---------- audio ----------
    # whoosh only when a B-roll run starts (not on every cut)
    whoosh = [c[0] - 0.10 for k, c in enumerate(CUTS) if k == 0 or abs(CUTS[k - 1][1] - c[0]) > 1e-3]
    key_pops = [0.05, M(23.68)]   # pop only on hook + CTA boxes
    soft_whoosh = [c[0] - 0.08 for k, c in enumerate(CUTS) if k > 0 and abs(CUTS[k - 1][1] - c[0]) <= 1e-3]
    kw_pops = [t for t in pops if t not in key_pops]
    # voice rebuilt from the raw take: continuous inside each v1 piece (no dips at punch-in cuts),
    # 25 ms fades only where takes join, plus real location room tone underneath the whole clip
    p1 = json.load(open(os.path.join(HERE, "plan_v1.json"), encoding="utf-8"))
    pieces = []
    for sg in p1["segments"]:
        if pieces and abs(pieces[-1][1] - sg["in"]) < 1e-3: pieces[-1][1] = sg["out"]
        else: pieces.append([sg["in"], sg["out"]])
    rawa = os.path.join(HERE, "audio48k.wav")
    vf = []
    for k, (a, b) in enumerate(pieces):
        vf.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,pan=mono|c0=c0,"
                  f"afade=t=in:d=0.025,afade=t=out:st={b-a-0.025:.3f}:d=0.025[p{k}]")
    vf.append("".join(f"[p{k}]" for k in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[vx]")
    vf.append("[0:a]atrim=26.85:31.35,asetpts=PTS-STARTPTS,pan=mono|c0=c0,aloop=loop=-1:size=216000,"
              f"atrim=0:{DUR_SRC},afade=t=in:d=0.3[rt]")
    vf.append(f"[vx][rt]amix=inputs=2:normalize=0:duration=first,atrim=0:{DUR_SRC}[vm]")
    voice_raw = os.path.join(WORK, "voice_raw.wav")
    run(FF + ["-i", rawa, "-filter_complex", ";".join(vf), "-map", "[vm]", "-ar", "48000", "-c:a", "pcm_s24le", voice_raw])
    if CUT_A is not None:
        tmpv = voice_raw + ".tight.wav"
        run(FF + ["-i", voice_raw, "-filter_complex",
                  f"[0:a]atrim=0:{CUT_A},asetpts=PTS-STARTPTS[a0];[0:a]atrim={CUT_B}:{DUR_SRC},asetpts=PTS-STARTPTS[a1];"
                  f"[a0][a1]acrossfade=d=0.03", "-c:a", "pcm_s24le", tmpv]); voice_raw = tmpv
    ins = ["-i", voice_raw, "-i", os.path.join(AUD, "music_pop_track_03.mp3")]
    # minimal SFX (user: busy SFX is annoying): one whoosh per B-roll run, one pop on the hook, one ding on the brand card
    # context-picked SFX (one sound per moment, under the voice). (file, [times], gain); gain is applied after
    # normalising each file to -3 dBFS peak, and each hit is shifted back by the file's measured onset.
    runs = [c[0] for k, c in enumerate(CUTS) if k == 0 or abs(CUTS[k - 1][1] - c[0]) > 1e-3]
    SFX_PLAN = [
        ("pop_main_pop.mp3", [0.05], 0.16),                      # hook box pops in
        ("whoosh_swoosh_01.wav", [runs[0] - 0.05], 0.12),        # into problem B-roll (cream / pan)
        ("whoosh_fast_woosh_01.mp3", [runs[1] - 0.03], 0.11),    # into second problem run (cluttered)
        ("whoosh_magic_wand_whoosh.wav", [runs[3] - 0.02], 0.10),  # turn to the fix: arranging -> neat store
        ("ding_positive_notification.mp3", [M(23.66)], 0.10),   # Space Connex card
        ("click_mouse_click_01.mp3", [M(24.02) + 0.18], 0.16),  # chat button lands (UI click)
    ]
    idx_csv = {r.split(",")[0]: r.split(",") for r in open(os.path.join(SFXD, "index.csv"), encoding="utf-8").read().splitlines()[1:]}
    sfx = []
    for f, times, g in SFX_PLAN:
        onset, peak = float(idx_csv[f][3]), float(idx_csv[f][4])
        sfx.append((f, [t - onset for t in times], g * 10 ** ((-3.0 - peak) / 20)))
    # mic is on the LEFT channel only -> take it as mono and centre it; no denoise (keeps voice full)
    fc = ["[0:a]pan=stereo|c0=c0|c1=c0,highpass=f=75,equalizer=f=250:t=q:w=1.2:g=-2,"
          "equalizer=f=4000:t=q:w=1.4:g=2.5,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120:makeup=2,"
          f"afade=t=out:st={DUR-0.2:.2f}:d=0.2,asplit=2[voice][sc]",
          f"[1:a]atrim=0:{DUR},volume=0.07,afade=t=in:d=0.4,afade=t=out:st={DUR-1.6:.2f}:d=1.6,aformat=channel_layouts=stereo[mu]",
          "[mu][sc]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[duck]"]
    mix = ["[voice]", "[duck]"]; n = 2; idx = 2
    for f, times, vol in sfx:
        ins += ["-i", os.path.join(SFXD, f)]
        if times:
            tag = f"s{idx}"
            fc.append(f"[{idx}:a]aformat=channel_layouts=stereo,atrim=0:1.8,afade=t=out:st=1.4:d=0.4,asplit={len(times)}" + "".join(f"[{tag}_{k}]" for k in range(len(times))))
            for k, tt in enumerate(times):
                ms = int(max(0, tt) * 1000)
                fc.append(f"[{tag}_{k}]adelay={ms}|{ms},volume={vol}[{tag}d{k}]"); mix.append(f"[{tag}d{k}]"); n += 1
        idx += 1
    fc.append("".join(mix) + f"amix=inputs={n}:normalize=0:duration=first,atrim=0:{DUR}[mx]")
    mixw = os.path.join(WORK, "mix.wav")
    run(FF + [*ins, "-filter_complex", ";".join(fc), "-map", "[mx]", "-ar", "48000", "-c:a", "pcm_s24le", mixw])
    r = run(["ffmpeg", "-hide_banner", "-i", mixw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"])
    L = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={L['input_i']}:measured_TP={L['input_tp']}:"
          f"measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true")
    finw = os.path.join(WORK, "final.wav")
    run(FF + ["-i", mixw, "-af", ln + ",aresample=48000", "-c:a", "pcm_s24le", finw])

    # ---------- picture + text + logo ----------
    open(os.path.join(WORK, "text.ass"), "w", encoding="utf-8").write(ASS)
    # logo badge: white rounded card + soft shadow, bounce in (0 -> 115% -> 100%) then gentle float
    # brand card (HTML -> PNG, see .work/brand/card.html) slides up + fades; button pops then pulses
    CARD_DIR = os.environ.get("CARD_DIR", os.path.join(ROOT, "assets", "brand"))
    card = os.path.join(CARD_DIR, "endcard_card.png")   # 1080x420 rgba
    pill = os.path.join(CARD_DIR, "endcard_button.png")  # 1080x200 rgba
    T0, CY, T1, PY = M(23.70), 940, M(24.02), 1300
    ease = f"(1-pow(1-min(1,max(0,(t-{T0})/0.38)),3))"
    f = (f"if(lt(t,{T1}),0.02,if(lt(t,{T1}+0.18),0.02+1.13*(t-{T1})/0.18,"
         f"if(lt(t,{T1}+0.30),1.15-0.15*(t-{T1}-0.18)/0.12,1+0.03*sin(2*PI*(t-{T1}-0.30)/1.2))))")
    fcv = ((f"[0:v]{GRADE_VF}[g0];" if GRADE else "[0:v]null[g0];") + f"[2:v]format=rgba,fade=t=in:st={T0}:d=0.30:alpha=1[cd];"
           f"[g0][cd]overlay=x=0:y='{CY}+110*(1-{ease})':eval=frame:enable='between(t,{T0},{DUR})':shortest=1[v1];"
           f"[3:v]format=rgba,scale=w='trunc(1080*({f})/2)*2':h=-2:eval=frame[pl];"
           f"[v1][pl]overlay=x=(W-w)/2:y='{PY}+(200-h)/2':eval=frame:enable='between(t,{T1},{DUR})':shortest=1[v2];"
           f"[v2]subtitles='{os.path.basename(WORK)}/text.ass':fontsdir='{FONTDIR}'[vo]")
    tmp = out + ".part.mp4"
    old = os.getcwd(); os.chdir(HERE)
    try:
        run(FF + ["-i", joined, "-i", finw, "-loop", "1", "-i", card, "-loop", "1", "-i", pill, "-filter_complex", fcv,
                  "-map", "[vo]", "-map", "1:a", "-t", f"{DUR}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                  "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
                  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp])
    finally:
        os.chdir(old)
    os.replace(tmp, out)
    # speed-up pass only when SPEED != 1 (pitch kept by atempo)
    tmp2 = final_out + ".part.mp4"
    if SPEED == 1.0:
        import shutil; shutil.copy(out, tmp2)
    else:
      run(FF + ["-i", out, "-filter_complex",
              f"[0:v]setpts=PTS/{SPEED},fps={FPS}[v];[0:a]atempo={SPEED},loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]",
              "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
              "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
              "-movflags", "+faststart", tmp2])
    os.replace(tmp2, final_out)
    # SRT from v1 subtitle timing, remapped to the tight + sped-up clock
    p1 = json.load(open(os.path.join(HERE, "plan_v1.json"), encoding="utf-8"))
    mp, o = [], 0.0
    for sg in p1["segments"]:
        mp.append((sg["in"], sg["out"], o)); o += sg["out"] - sg["in"]
    def v1out(t):
        for a, b, oo in mp:
            if a - 1e-6 <= t <= b + 1e-6: return oo + t - a
        return min(((abs(t - a), oo) for a, b, oo in mp))[1]
    def st(t):
        ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
    k, lines = 0, []
    for c in p1["subs"]:
        s0, e0 = v1out(c["s"]), v1out(c["e"])
        if gone(s0, e0) or s0 >= DUR_SRC: continue
        k += 1
        lines.append(f"{k}\n{st(M(s0)/SPEED)} --> {st(min(M(e0), DUR)/SPEED)}\n{c['text']}\n")
    open(os.path.splitext(final_out)[0] + ".srt", "w", encoding="utf-8").write("\n".join(lines))
    print(json.dumps({"out": final_out, "dur": round(DUR / SPEED, 2), "windows": len(wins), "pops": len(pops), "whoosh": len(whoosh)}))


if __name__ == "__main__":
    main(sys.argv[1])
