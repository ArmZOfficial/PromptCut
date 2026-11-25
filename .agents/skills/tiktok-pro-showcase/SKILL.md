---
name: tiktok-pro-showcase
description: Cut one Single High-Production Voiceover Video (9:16) from a Thai voice track plus inserts — multi-layout B-roll, Super Text popping the whole clip, context-picked SFX, QA'd H.264/AAC export. Use to cut, re-cut, or restyle one TikTok clip.
---

# ตัดคลิปเดียวแบบ High-Production

สูตรของคลิปอ้างอิง: **เสียงพูดเป็นแกน → ภาพเปลี่ยนตลอด (Multi-Layout) → Super Text เด้งทั้งคลิป → SFX มืออาชีพแค่จังหวะสำคัญ** อ่าน [arm-tiktok-taste](../arm-tiktok-taste/SKILL.md) ก่อนเริ่ม เพราะรสนิยมของอาร์มชนะสเปกนี้เมื่อขัดกัน

1. **เก็บวัตถุดิบ** — เสียงหลักจาก `Video/` (หรือ A-roll ในไฟล์ดิบ), ฟุตเทจจาก `Insert/` / `B-roll/`, บทจาก `Brief/scripts.json` ถอดเสียงไทยด้วย Whisper ในเครื่อง (`-mc 0`, ถอดทีละช่วงเมื่อไฟล์ยาว) เสร็จเมื่อทุกประโยคที่จะใช้มีเวลาเริ่ม–จบจากช่วงเงียบจริง และคำที่ ASR ไม่แน่ใจถูกถามผู้ใช้ครั้งเดียวรวมกัน
2. **วาง edit plan บน output clock** — ทุกช่วงมี: source in–out, layout, ข้อความบนจอ, B-roll, SFX
   - Layout: **A** Hook 0–3 วิ ตัดเร็ว · **B** Split เมื่อมีภาพก่อน/หลังจริง · **D** การ์ด B-roll บนพื้นเบลอ หรือ punch-in คนพูด (1.15 / 1.32 / 1.55) — เปลี่ยนภาพทุก 1.2–2.5 วินาที ไม่ค้างเกิน 3 วินาที
   - ทุกรอยต่อข้ามเทคที่เป็นคนพูด→คนพูด ปิดด้วย B-roll
   - ช่วงที่ไม่มีฟุตเทจตรงคำพูด → หาด้วย [free-broll-finder](../free-broll-finder/SKILL.md)
   - SFX เลือกตามบริบทจาก [sfx.md](references/sfx.md)

   เสร็จเมื่อทุกวินาทีของคลิปอยู่ในตาราง
3. **เรนเดอร์** ด้วย `.work/tiktok_pro/raw0135/render_v4.py` เป็นแพตเทิร์น (การ์ด B-roll, Super Text ASS, end card จาก HTML, เสียงต่อเนื่อง + room tone, SFX ตาม onset, loudnorm 2 รอบ) สเปกเลย์เอาต์ ฟอนต์ safe zone และการส่งออกอยู่ใน [editing.md](references/editing.md)
4. **QA** ตามรายการใน [arm-tiktok-taste](../arm-tiktok-taste/SKILL.md#qa-ก่อนส่ง-ทุกข้อพร้อมตัวเลข) แก้จนผ่านทุกข้อ แล้วส่งไฟล์พร้อมตัวเลข QA และสิ่งที่ยังตรวจไม่ได้ (เช่น ยังไม่ได้ฟังด้วยหู)
