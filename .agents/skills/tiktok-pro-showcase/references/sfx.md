# เลือก SFX ตามบริบทคลิป

คลังหลัก: `assets/sfx_muaaz/` (43 ไฟล์จาก [Sound Effects Creators Actually Use](https://muaazws.notion.site/Sound-Effects-Creators-Actually-Use-3fe84fe99b3181ad9cbed1be16bfa69b) ผู้ทำแจกให้ใช้ใน YouTube/TikTok/Reels) ชื่อไฟล์ขึ้นต้นด้วยหมวด `whoosh_`, `pop_`, `click_`, `ding_`, `foley_` และ `index.csv` เก็บ `duration_s,onset_s,peak_dbfs` ต่อไฟล์ ถ้าเครื่องยังไม่มีโฟลเดอร์นี้ ให้เปิดหน้า Notion ด้วย browser แล้วดึงลิงก์ไฟล์จากแท็ก `<audio>` (หน้าเรนเดอร์ด้วย JavaScript ตัว fetch ธรรมดาอ่านไม่ได้)

## กติกา

1. **หนึ่งเสียงต่อหนึ่งจังหวะ และอยู่ใต้เสียงพูดเสมอ** — คลิป 25–30 วินาทีใช้ราว 5–7 เสียง คำบนจอส่วนใหญ่ปล่อยเงียบ
2. **เสียงต้องเล่าเรื่องเดียวกับภาพ** — อ่านบทและ edit plan ก่อน แล้วเลือกจากตารางด้านล่างทีละจังหวะ จดเหตุผลสั้น ๆ ข้างแต่ละเสียงใน plan
3. **ตรงจังหวะ** — วางที่ `t − onset_s` เพื่อให้หัวเสียงตรงรอยตัดหรือคำเด้ง whoosh นำรอยตัด 0.02–0.05 วินาที
4. **ระดับเท่ากันทุกไฟล์** — normalize เป็น peak −3 dBFS จาก `peak_dbfs` แล้วคูณ gain 0.10–0.16 ตัดหาง 1.8 วินาทีพร้อม fade 0.4 วินาที
5. **ใช้เฉพาะเสียงทั่วไป** — เสียงที่เลียนแบรนด์หรือการ์ตูน (Discord, iPhone, Pokemon, SpongeBob) ไม่ได้ดาวน์โหลดมา

## จังหวะ → เสียง

| จังหวะในคลิป | เลือกจาก | ตัวอย่างที่ใช้แล้วผ่าน |
| --- | --- | --- |
| Hook box / ข้อความเปิดเด้งขึ้น | `pop_main_pop`, `pop_bubble_pop`, `whoosh_impact_whoosh_drum` (hook แรง) | `pop_main_pop` 0.16 |
| เข้า B-roll ชุดแรก | `whoosh_swoosh_01`, `whoosh_whoosh_02`, `whoosh_stereo_air_whoosh` | `whoosh_swoosh_01` 0.12 |
| เข้า B-roll ชุดถัดไป | `whoosh_fast_woosh_01/02`, `whoosh_swipe`, `whoosh_cartoon_swipe` (โทนสนุก) | `whoosh_fast_woosh_01` 0.11 |
| พลิกจากปัญหาเป็นทางแก้ | `whoosh_magic_wand_whoosh`, `ding_twinkling_notification` | `whoosh_magic_wand_whoosh` 0.10 |
| ก่อนเฉลย / ตัวเลขผลลัพธ์ | `whoosh_riser_01`, `whoosh_perfect_riser`, `whoosh_breath_riser` แล้วตามด้วย `whoosh_whoosh_hit` | — |
| การ์ดแบรนด์ / ข้อความยืนยัน | `ding_positive_notification`, `ding_ding_01`, `ding_idea` | `ding_positive_notification` 0.10 |
| ปุ่ม CTA / UI บนจอ | `click_mouse_click_01`, `click_button_click`, `click_switch_click_01` | `click_mouse_click_01` 0.16 |
| ข้อความเตือนว่าผิด | `ding_negative_notification_bleep` เบามาก หรือเว้นว่าง | — (อาร์มไม่ชอบเสียงบัซเซอร์) |
| ภาพแชต / ข้อความเข้า | `ding_message_sound`, `click_glitch_click` | — |
| ภาพมีของจริงเคลื่อน | foley ตรงภาพ: พิมพ์ = `foley_keyboard_typing`, ถ่ายรูป = `foley_camera_shutter_01`, เขียน = `foley_pencil`, ของแตก = `foley_plate_breaking` | — |

ผลที่ต้องได้: ทุกเสียงใน plan มีเวลา ไฟล์ gain และเหตุผลจากบริบท แล้วตรวจ peak ช่วง SFX ใน `final.wav` ไม่ดังกว่าช่วงเสียงพูดรอบข้าง
