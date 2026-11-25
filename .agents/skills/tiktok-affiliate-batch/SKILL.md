---
name: tiktok-affiliate-batch
description: Turn one product brief into a six-category, five-ideas-per-category matrix and Thai short-video scripts. Use for ideation, hooks, storyboard beats, or affiliate copy backed by product evidence.
---

# แตกไอเดียและสคริปต์ 30 คลิป

1. ทำ `Brief/product.md` จาก SKU วิธีใช้ ผู้ชม ข้อจำกัด และหลักฐานที่ผู้ใช้ให้ ผูกข้อเท็จจริงกับ `claim_id` และที่มา เก็บข้อมูลยังไม่ยืนยันไว้เป็นประเด็นรอตรวจ
2. ทำ `Brief/ideas.md` ด้วย `P01` ปัญหาก่อนใช้, `P02` สาธิต, `P03` รายละเอียดและหลักฐาน, `P04` ตอบข้อสงสัย, `P05` สถานการณ์ใช้จริง และ `P06` ช่วยตัดสินใจ หรือใช้หมวดที่ผู้ใช้ระบุ แต่ละหมวดมี 5 มุม ตรวจว่าคำเปิด ภาพเปิด และคำถามของผู้ชมต่างกันจริง
3. ทำ `Brief/scripts.json` หนึ่งรายการต่อ `clip_id` ตาม [ตัวอย่าง JSON และพรอมป์](../../../PROMPTS.md#03-สคริปต์และสตอรีบอร์ด-30-คลิป) แยกคำอ่านใน `voice_text` จากตัวสะกดใน `overlay_text` อ้างหลักฐานสำหรับข้อมูลสินค้า และระบุ `visual_need` ต่อ beat เวลา `target_s` เป็นเวลาเป้าหมายสำหรับวางแผน
4. เช็กจำนวน รหัสซ้ำ ความสอดคล้องของ `claim_ids` กับบรีฟ และว่าคลิปหนึ่งจบด้วย CTA ที่ใช้ได้จริง เลือกสามคลิปนำร่องที่ใช้ภาพและการเล่าต่างกัน ส่งต่อ `clip_id` กับความต้องการฟุตเทจให้ขั้นถ่าย
