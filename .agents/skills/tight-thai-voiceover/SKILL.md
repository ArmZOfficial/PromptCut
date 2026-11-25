---
name: tight-thai-voiceover
description: Clean and align Thai narration for a short product video. Use for silence trimming, A-roll and voiceover synchronization, final-clock captions, and word-level timing.
---

# ตัดช่วงเงียบและซิงก์ซับไทย

1. เลือกแหล่งเสียงโดย `clip_id` ถ้าเป็นเสียง A-roll ให้แยกช่วงด้วย `a-roll-map.csv` และใช้ช่วงตัดเดียวกันกับภาพ ถ้าเป็น VO ให้ใช้ไฟล์เสียงที่กำหนดใน manifest
2. อ่าน [ขั้นเสียงและเวลา](../tiktok-pro-showcase/references/editing.md#เสียงและการแมปเวลา) สำหรับเกณฑ์จับความเงียบ crossfade และทำเวลาใหม่ ใช้ ASR ที่ให้เวลาได้จริง ตรวจคำสำคัญจากบรีฟ แล้วถอดเสียงสะอาดใหม่หลังตัดหรือแมปคำด้วย EDL ถ้าเวลาไทยไม่นิ่ง ให้ใช้จังหวะวลีที่ตรวจได้
3. ส่ง `voice-clean.wav`, `kept-ranges.json`, `words.json` และ `captions.srt` ที่อ้างเวลาหลังตัด ใช้หน่วยให้ชัด ตรวจว่าช่วงเวลาเรียงต่อกัน ซับอยู่ในขอบเขตของเสียงจริง และไม่มีเสียงท้ายคำหายที่รอยต่อ ระบุจุดที่ต้องฟังตรวจหากเสียงตรวจได้เพียงด้วยเครื่องมือ
