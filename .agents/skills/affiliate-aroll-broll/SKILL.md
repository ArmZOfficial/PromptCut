---
name: affiliate-aroll-broll
description: Plan a single A-roll recording session and a reusable B-roll library for Thai product scripts, or index recorded takes and proof shots. Use for shoot orders, take maps, and footage handoff.
---

# วางคิวถ่าย A-roll และ B-roll

1. อ่าน `Brief/scripts.json` จัดคิวบทตาม `clip_id` ให้พูดรหัสก่อนบทแล้วเว้นจังหวะไว้สำหรับแยกเทค จัดมุมที่เห็นหน้าคนพูดและมุมสินค้าแยกกันตามการใช้งาน ถ้าถ่ายเสร็จแล้ว ให้ทำ `Video/a-roll-map.csv` จากไฟล์จริง โดยเก็บ `clip_id,source,start_s,end_s,take,selected` และเริ่มช่วงบทหลังคำประกาศรหัส
2. รวมความต้องการภาพที่ใช้ด้วยกันได้ แล้ววางแผนถ่าย 20–30 ช็อตตามมุมกล้อง พร็อพ และสถานที่ คงภาพหลักฐานเฉพาะรุ่นตามข้อเท็จจริง เช่น ฉลาก อุปกรณ์ในกล่อง และวิธีใช้ เก็บช่วงเผื่อหัวท้ายให้ทันการเคลื่อนไหว
3. ส่ง `Brief/shot-list.md` กับ `Insert/assets.csv` ใช้ `asset_id,path,kind,tags,framing,source,rights,proof_for,disclosure` สำหรับไฟล์ที่มีจริง แยกช็อตที่ต้องถ่ายกับช็อตบรรยากาศที่สร้างทดแทนได้ ตรวจให้ครบว่าทุกคลิปมีแหล่งเสียงและภาพหลัก หรือมีเหตุผลที่ยังขาด

อ่าน [พรอมป์จัดคิวถ่าย](../../../PROMPTS.md#04-ช็อตลิสต์ให้ถ่ายรวดเดียว) เมื่อต้องทำช็อตลิสต์จากบทใหม่
