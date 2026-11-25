import wave, array, math, json
w = wave.open("audio48k.wav"); sr = w.getframerate(); sw = w.getsampwidth(); ch = w.getnchannels()
raw = w.readframes(w.getnframes()); assert sw == 2
a = array.array("h", raw)[0::ch]          # left channel (mic)
HOP = sr // 100                            # 10 ms
env = []
for i in range(0, len(a) - HOP, HOP):
    s = sum(x * x for x in a[i:i + HOP]) / HOP
    env.append(20 * math.log10(math.sqrt(s) / 32768 + 1e-9))
def db(t): return env[min(len(env) - 1, max(0, int(t * 100)))]
p = json.load(open("plan_v1.json", encoding="utf-8"))
# piece boundaries = where consecutive segments are not contiguous in source
segs = p["segments"]; edges = []
for k, sg in enumerate(segs):
    if k == 0 or abs(segs[k-1]["out"] - sg["in"]) > 1e-3: edges.append(("IN ", sg["in"]))
    if k == len(segs)-1 or abs(segs[k+1]["in"] - sg["out"]) > 1e-3: edges.append(("OUT", sg["out"]))
for kind, t in edges:
    prof = " ".join(f"{db(t + d/100):5.0f}" for d in range(-15, 16, 5))
    print(kind, f"{t:7.2f}", "| -150ms..+150ms:", prof)
