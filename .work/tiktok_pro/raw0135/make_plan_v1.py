"""Build plan_v1.json (source-time edit plan) for Raw_v1_original-voice."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = "Space Connex"   # confirmed by user 2026-11-24 (ASR hears "สเปสคอนเนค")
ITEM2 = "กระทะร้อน"     # «ต้องตรวจ» ASR hears "กระทาละร้อน"
WRONG = "ผิดจุด"         # confirmed by user 2026-11-24

# speech pieces: (in, out, [subtitle phrases])  — times from silencedetect on the raw take
pieces = [
    (52.62, 55.25, ["เคยเห็นการวางสินค้าแปลก ๆ"]),
    (55.30, 56.48, ["ที่เห็นแล้วเราต้องเกาหัวบ้างไหมคะ"]),
    (100.55, 101.18, ["อย่างเช่น"]),
    (101.38, 102.50, ["เอาครีมทาผิว"]),
    (102.57, 104.30, [f"มาวางคู่กับ{ITEM2}"]),
    (112.50, 113.37, ["หรือเอาของสด"]),
    (113.70, 116.50, ["มาวางไว้อยู่บนเคาน์เตอร์", "โดยที่ไม่มีตู้แช่"]),
    (129.30, 134.90, [f"การวาง{WRONG}", "หรือการวางผิดที่แบบนี้นะคะ", "ก็อาจจะทำให้เกิดปัญหา", "กับสินค้ากับทางร้านค้าได้"]),
    (136.42, 139.05, ["แล้วก็ทำให้สินค้าของท่าน", "ขายไม่ได้เหมือนกันนะคะ"]),
    (147.45, 149.10, ["อย่าให้เกิดกับร้านคุณนะ"]),
    (209.15, 211.95, ["ถ้าไม่รู้ว่าจะเอาสินค้าอะไร", "วางคู่กับอะไรเนี่ย"]),
    (214.83, 217.30, [f"ทักมาให้ {BRAND}", "เช็คให้ก่อนได้นะคะ"]),
]
END_HOLD = 218.55  # extend last piece for logo end card

subs = []
for a, b, phrases in pieces:
    tot = sum(len(p) for p in phrases)
    t = a + 0.04
    span = (b - 0.04) - t
    if a == 129.30:  # known pause after first phrase
        subs.append({"s": 129.32, "e": 129.98, "text": phrases[0]})
        t, span, phrases2 = 130.10, 134.86 - 130.10, phrases[1:]
        tot = sum(len(p) for p in phrases2)
    else:
        phrases2 = phrases
    for p in phrases2:
        d = span * len(p) / tot
        subs.append({"s": round(t, 3), "e": round(t + d, 3), "text": p}); t += d

# picture segments: split pieces into ~1.2–2.4 s shots with alternating punch-in
Z = {"wide": (1.0, 0.42), "med": (1.22, 0.40), "close": (1.45, 0.37)}
cuts = {  # extra video cut points inside a piece (audio continuous)
    52.62: [(52.62, "close"), (53.95, "med")],
    55.30: [(55.30, "close")],
    100.55: [(100.55, "wide")],
    101.38: [(101.38, "close")],
    102.57: [(102.57, "med")],
    112.50: [(112.50, "close")],
    113.70: [(113.70, "wide"), (115.05, "close")],
    129.30: [(129.30, "med"), (130.10, "close"), (131.82, "wide"), (133.20, "med")],
    136.42: [(136.42, "close"), (137.75, "med")],
    147.45: [(147.45, "close")],
    209.15: [(209.15, "med"), (210.55, "close")],
    214.83: [(214.83, "close"), (216.05, "med")],
}
segments = []
for idx, (a, b, _) in enumerate(pieces):
    if idx == len(pieces) - 1:
        b = END_HOLD
    pts = cuts[a]
    for k, (s, z) in enumerate(pts):
        e = pts[k + 1][0] if k + 1 < len(pts) else b
        zoom, cy = Z[z]
        sg = {"in": s, "out": e, "zoom": zoom, "cy": cy}
        if z == "wide" and e - s > 1.0:
            sg["push"] = 0.06
        if idx == len(pieces) - 1 and k == len(pts) - 1:
            sg["push"] = 0.05
        segments.append(sg)

W, C = "w", "c"
superx = [
    {"s": 52.62, "e": 55.25, "lines": [["เคยเห็นการวาง", W], ["สินค้าแปลก ๆ ?", C]]},
    {"s": 55.30, "e": 56.48, "lines": [[["เห็นแล้ว", W], ["เกาหัว!", C]]]},
    {"s": 100.55, "e": 102.50, "lines": [[["เช่น ", W], ["ครีมทาผิว", C]]]},
    {"s": 102.57, "e": 104.30, "lines": [["วางผิดคู่!", C]]},
    {"s": 112.50, "e": 113.70, "lines": [[["หรือ ", W], ["ของสด", C]]]},
    {"s": 113.70, "e": 115.05, "lines": [["วางบนเคาน์เตอร์", W]]},
    {"s": 115.05, "e": 116.50, "lines": [["ไม่มีตู้แช่!", C]]},
    {"s": 129.30, "e": 131.82, "lines": [["วางผิดที่", W], ["= ปัญหา!", C]]},
    {"s": 131.82, "e": 134.90, "lines": [[["ร้านค้า", W], ["เจอปัญหา!", C]]]},
    {"s": 136.42, "e": 139.05, "lines": [["สินค้า", W], ["ขายไม่ออก!", C]]},
    {"s": 147.45, "e": 149.10, "lines": [["อย่าให้เกิดกับ", W], ["ร้านคุณ!", C]]},
    {"s": 209.15, "e": 211.95, "lines": [["ไม่รู้จะวาง", W], ["อะไรคู่อะไร?", C]]},
    {"s": 214.83, "e": END_HOLD, "lines": [["ทักมาเลย!", C], ["ให้เราเช็คให้ก่อน", W]]},
]

plan = {
    "build": "v1",
    "segments": segments,
    "super": superx,
    "subs": subs,
    "flash": [129.30, 209.15],
    "logo": {"s": 214.83, "e": END_HOLD, "path": "assets/brand/endcard_card.png", "size": 1000, "y": 250},
    "crf": 18,
    "super_y": 1265,
}
json.dump(plan, open(os.path.join(HERE, "plan_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(segments), "segments,", len(subs), "subs")
