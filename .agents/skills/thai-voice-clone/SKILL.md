---
name: thai-voice-clone
description: Set up or reuse an authorized Thai voice clone, choose a Thai-capable TTS model, and synthesize one narration file per clip. Use for ElevenLabs voice IDs or compatible provider profiles.
---

# โคลนเสียงไทยของเจ้าของเสียง

1. อ่าน [คู่มือผู้ให้บริการและตัวอย่าง API](../../../VOICE-CLONING.md) เมื่อสร้างเสียงใหม่หรือเปลี่ยนโมเดล ใช้ตัวอย่างเสียงของผู้ใช้เองหรือแหล่งที่ได้รับสิทธิ์ตามเงื่อนไขของผู้ให้บริการ โปรไฟล์ ElevenLabs Professional ให้เจ้าของเสียงสร้างและยืนยันบนบัญชีของตน
2. จับคู่ `clip_id` กับ `voice_text` และ alias ของโปรไฟล์ ตรวจรายชื่อโมเดลที่รองรับ `th` จากบัญชีที่รัน ใช้คีย์จาก environment หรือ secret store เมื่อมีการตั้งไว้ ทำคำอ่านชื่อ ราคา รุ่น และหน่วยให้ชัด ทดลองคลิปเดียวก่อนเริ่มล็อต
3. สร้าง `Video/<clip_id>_voice.mp3` หรือไฟล์ WAV ตามรูปแบบของผู้ให้บริการ ตรวจว่าเปิดอ่านได้และมีระยะเวลาที่วัดได้ ให้เจ้าของเสียงหรือผู้ตรวจงานฟังความเหมือนและคำสำคัญ เก็บรุ่นและ fingerprint สำหรับใช้ซ้ำโดยไม่เรียกสร้างเสียงใหม่ซ้ำ
4. ส่งต่อเสียงและสคริปต์ให้ [tight-thai-voiceover](../tight-thai-voiceover/SKILL.md) สำหรับเวลาจริงและซับ ถ้าขาดโปรไฟล์หรือคีย์ ให้ส่งบทที่เตรียมแล้วและตำแหน่งไฟล์เสียงที่ต้องการ
