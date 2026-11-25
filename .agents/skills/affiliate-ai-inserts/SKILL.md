---
name: affiliate-ai-inserts
description: Design simulated visual inserts for product videos where the needed B-roll is difficult to film. Use for Google Flow image or video prompts and for registering generated footage with placement and disclosure.
---

# ทำภาพแทรกสำหรับฉากที่ถ่ายยาก

1. เทียบ `visual_need` ในสคริปต์กับ `Insert/assets.csv` เลือกเฉพาะช่องว่างที่เป็นฉากประกอบ เช่น สถานที่หรือสถานการณ์ทั่วไป ระบุรายการต้องถ่ายจริงแยกไว้สำหรับฉลาก ผลทดสอบ ภาพเปรียบเทียบ และการสาธิตที่ใช้ยืนยันข้อมูล
2. เขียนพรอมป์ภาพนิ่งและภาพเคลื่อนไหวแนวตั้ง 9:16 ตาม [พรอมป์ Flow](../../../PROMPTS.md#05-ภาพนิ่งและวิดีโอแทรกใน-flow) ให้แสง ขนาดวัตถุ และทิศทางการเคลื่อนไหวต่อกับฉากข้างเคียง รอบทดลองใช้ช็อตสั้นและพื้นที่เผื่อข้อความ
3. เมื่อมีไฟล์จริง ให้ตรวจภาพแปลก ตัวอักษรในภาพ และความตรงกับบริบท ลงดัชนีเป็น `ai_insert` พร้อม `asset_id`, ตำแหน่งใช้งาน และข้อมูลเปิดเผยว่าเป็นฉากจำลอง กรณีส่งมอบเฉพาะพรอมป์ให้บันทึกสถานะรอไฟล์
