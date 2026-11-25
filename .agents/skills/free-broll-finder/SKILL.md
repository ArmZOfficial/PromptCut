---
name: free-broll-finder
description: Find free, commercially usable B-roll videos and photos on the web that match each beat of a clip, download them, and log licenses. Use when a clip needs inserts, a shot is missing from the footage, or an AI/non-commercial image must be replaced.
---

# หา B-roll และภาพฟรีให้ตรงคลิป

1. **ทำรายการช็อตที่ต้องหา** — อ่านบทหรือ edit plan แล้วเขียนหนึ่งแถวต่อช่วง: เวลา, คำที่พูด, ภาพที่ต้องเห็น, คำค้นอังกฤษ 2–3 แบบ (เช่น "ของสดไม่มีตู้แช่" → `raw fish on table market`, `fresh fish market thailand`) เสร็จเมื่อทุกช่วงที่ต้องใช้ B-roll มีคำค้น
2. **ค้นตามลำดับแหล่ง** เลือกภาพแนวตั้งที่วัตถุหลักอยู่กลางเฟรม (การ์ด 700×1244 ครอปตรงกลาง)
   - **Pexels** (วิดีโอ + ภาพ) — เปิด `https://www.pexels.com/search/<คำค้น>/?orientation=portrait` ใน browser (ใช้ `/search/videos/<คำค้น>/` สำหรับวิดีโอ) ดึง id จากลิงก์ `/photo/...-<id>/` แล้วดาวน์โหลดภาพที่ `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&w=1200` ถ้ามี `PEXELS_API_KEY` ใช้ API `https://api.pexels.com/v1/search` และ `/videos/search` แทน
   - **Pixabay** (ต้องมี `PIXABAY_API_KEY`), **Unsplash** (ภาพนิ่ง), **Wikimedia Commons** (เช็กไลเซนส์ทีละไฟล์ เลือก CC0/CC BY)
   - ภาพจาก AI ฟรี (ElevenLabs, Flow รุ่นฟรี) ใช้เชิงพาณิชย์ไม่ได้ ใช้เป็นตัวเลือกสุดท้ายพร้อมแจ้ง
3. **ดาวน์โหลดลงโฟลเดอร์แยก** `B-roll/pexels/` (วิดีโอ) หรือ `B-roll/pexels_photos/` (ภาพ) ชื่อไฟล์ `<ลำดับ>_<คำสั้น>_<id>.<ext>` แล้วทำ contact sheet ของผู้สมัครทุกตัวด้วย ffmpeg (`xstack` พร้อมชื่อไฟล์) ดูด้วยตา เลือกตัวที่ตรงคำพูดที่สุด และตรวจว่าวัตถุหลักไม่หลุดเฟรมเมื่อครอปเป็นการ์ด
4. **ลงทะเบียน** ใน `credits.csv` ของโฟลเดอร์: `asset_id,path,source,source_url,license,used_in` เสร็จเมื่อทุกไฟล์ที่ใช้ในคลิปมีแถวพร้อมไลเซนส์

แหล่งที่ใช้แล้วผ่าน: Pexels License ใช้เชิงพาณิชย์ได้ ไม่ต้องให้เครดิต (ห้ามขายไฟล์ต่อแบบไม่ดัดแปลง) โฟลเดอร์ `B-roll/` อยู่ใน `.gitignore` เพราะ repo เป็น public
