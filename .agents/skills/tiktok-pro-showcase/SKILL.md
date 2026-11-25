---
name: tiktok-pro-showcase
description: Cut one high-production vertical product showcase from Thai A-roll or voiceover and indexed inserts. Use for the clip's A/B/D layouts, dynamic Super Text, audio polish, contact sheet, and H.264/AAC export.
---

# ตัดคลิปแนวตั้งแบบ Pro Showcase

1. อ่าน [สเปกภาพ เสียง และไฟล์ส่งออก](references/editing.md) ตรวจ `Video/`, `Insert/` และงานของ `clip_id` ที่ผู้ใช้เลือก ใช้ [ffmpeg-skill](../ffmpeg-skill/SKILL.md) เมื่อต้อง probe สื่อ ตัดเสียงตามช่วง ผสมเสียง ทำซับ ส่งออก หรือตรวจไฟล์ เรียกสคริปต์ที่ตรงงานตามแผนอ้างอิงของเวอร์ชันที่ติดตั้ง
2. ใช้ [tight-thai-voiceover](../tight-thai-voiceover/SKILL.md) สร้างเสียงหลักและเวลาที่ถูกต้อง จัด EDL จาก beat กับไฟล์ที่มีจริง ใช้เลย์เอาต์ A เปิดคลิป ใช้ B เมื่อมีภาพเปรียบเทียบที่เชื่อถือได้ และใช้ D สำหรับช็อตปกติ
3. ใส่ Super Text ตามเสียงและรูปแบบในสเปก จัดตำแหน่งให้หลบ UI และสินค้า มิกซ์เสียงตามพรีเซ็ตและวัด peak หลังมิกซ์ สร้างพรีวิวพร้อม contact sheet ให้ [affiliate-video-qa](../affiliate-video-qa/SKILL.md) ตรวจ
4. เรนเดอร์ MP4 เมื่อพรีวิวผ่านและตามเงื่อนไขส่งมอบที่ผู้ใช้กำหนด ตรวจด้วย `ffprobe` ก่อนรายงานไฟล์ ถ้าเครื่องมือตัดต่อหรือสื่อไม่ครบ ให้ส่ง EDL และระบุรายการที่ต้องเติม
