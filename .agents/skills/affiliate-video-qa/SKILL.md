---
name: affiliate-video-qa
description: Review Thai product video previews, caption and audio alignment, truthful visuals, and final MP4 specifications. Use before marking a clip or batch ready for handoff.
---

# ตรวจพรีวิวและไฟล์คลิป

1. เปิด contact sheet และพรีวิว ตรวจ Hook, การเปลี่ยนเลย์เอาต์, ภาพสาธิต และ CTA เทียบ `claim_id` กับหลักฐานและ SKU ตรวจพื้นที่ UI ด้วยพรีวิวแนวตั้งจริง อ่านซับไทยและตำแหน่งวรรณยุกต์
2. ตรวจรอยต่อเสียงและภาพ ซิงก์ปาก ชื่อสินค้า ตัวเลข และการกลบเสียงพูดจาก BGM ผลวัด peak ช่วยคัดปัญหา ให้ระบุแยกเมื่อยังฟังทวนไม่ได้ ตรวจสิทธิ์สื่อและข้อมูลเปิดเผยภาพหรือเสียงจำลองตามช่องทางที่ระบุ
3. ใช้ [สเปกส่งออก](../tiktok-pro-showcase/references/editing.md#พรีวิวและส่งออก) ตรวจไฟล์ด้วย `ffprobe` และลอง decode เมื่อเรนเดอร์คลิปเสร็จ อ่าน [ffmpeg-skill](../ffmpeg-skill/SKILL.md) หากใช้คำสั่งตรวจของแพ็กเกจ ให้ค่าพรีเซ็ตของโปรเจกต์เป็นสเปกที่ใช้ตัดสิน
4. ส่ง `qa.json` ต่อคลิปด้วย `clip_id,status,checks,issues` และใช้ `pass` เมื่อมีไฟล์จริงผ่านรายการตรวจตามขอบเขต ระบุ timestamp สาเหตุ และสิ่งที่ต้องแก้เมื่อเป็น `needs_fix` อัปเดต `Output/batch-report.csv` สำหรับล็อต
