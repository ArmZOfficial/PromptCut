# เลือก SFX ตามบริบทคลิป

คลังหลัก: `assets/sfx_muaaz/` (43 ไฟล์จาก [Sound Effects Creators Actually Use](https://muaazws.notion.site/Sound-Effects-Creators-Actually-Use-3fe84fe99b3181ad9cbed1be16bfa69b) ผู้ทำแจกให้ใช้ใน YouTube/TikTok/Reels) ชื่อไฟล์ขึ้นต้นด้วยหมวด `whoosh_`, `pop_`, `click_`, `ding_`, `foley_` และ `index.csv` เก็บ `duration_s,onset_s,peak_dbfs` ต่อไฟล์ ถ้าเครื่องยังไม่มีโฟลเดอร์นี้ ให้เปิดหน้า Notion ด้วย browser แล้วดึงลิงก์ไฟล์จากแท็ก `<audio>` (หน้าเรนเดอร์ด้วย JavaScript ตัว fetch ธรรมดาอ่านไม่ได้)

## กติกา

0. **เริ่มจากบริบท ไม่ใช่จากคลัง** — ดูเฟรมและคำพูดตรงจุดนั้นก่อน แล้วถามว่า "ภาพ/คำนี้ให้อารมณ์อะไร" (งง, ผิด, ตึงเครียด, ผลเสีย, คลี่คลาย, ยืนยัน) แล้วเลือกเสียงที่ให้อารมณ์เดียวกัน หาเวลาท่าทางจริงจากเฟรม (เช่น มือแตะหัวที่ 2.6 วิ) เสียงที่ไม่มีเหตุผลจากภาพหรือคำ ตัดทิ้ง (boom บนท่าเกาหัวงง ๆ = ผิดอารมณ์)
1. **ฟีลไวรัลไทย ไม่ใช่ whoosh เรียบ ๆ** — Hook และคำแรงใช้ boom, คำเตือนใช้เสียงตลก (แตก / cartoon pop), ภาพนิ่งใช้เสียงแฟลชกล้อง, จุดพลิกเป็นทางแก้ใช้ magic + sparkle (อาร์ม: whoosh ล้วน "น่าเบื่อ ไม่เหมือน TikTok ไวรัลไทย")
2. **ราว 12–13 เสียงต่อคลิป 25–30 วินาที เฉพาะจังหวะที่มีความหมาย** — การเปลี่ยนการ์ดในชุดเดียวกันและคำที่ขึ้นทีละคำปล่อยเงียบ (20 เสียง = "รก", 6 เสียงเบา = "โล่ง")
3. **ตรงจังหวะ และไม่ทับพยางค์แรก** — renderer ตัดไฟล์เริ่มที่ `onset_s − 0.03` แล้ววางที่เวลาเป้าหมาย − 0.03 (riser ใส่ความยาวเป็นค่าที่ 4 ให้จบตรง hit) เว้นเสียงที่คำแรกของคลิป เพราะทำให้ Whisper ได้ยินผิด ("เคยเห็น" → "ช่วยเห็น")
4. **ระดับตาม tier** (ตั้ง peak เป้าหมายของแต่ละ hit จาก `peak_dbfs`): **T1 −15 dBFS** magic/เปลี่ยนฉากใหญ่, **T2 −18** boom, คำเตือน, การ์ด, ปุ่ม, **T3 −21** เสียงประกอบเล็ก — boom เบสหนักฟังดังกว่าตัวเลข จึงอยู่ T2 (ประวัติ: −21 แบน = ไม่ได้ยิน, −9/−12/−15 = ดัง, −13/−16/−19 = เบาลงหน่อย)
5. **ใช้เฉพาะเสียงทั่วไป** — เสียงที่เลียนแบรนด์หรือการ์ตูนดัง (Discord, iPhone, Pokemon, SpongeBob) ไม่ได้ดาวน์โหลดมา

## จังหวะ → เสียง (RAW0135 v9: อารมณ์ → เสียง)

| ภาพ / คำ | อารมณ์ | ใช้ | ทางเลือก |
| --- | --- | --- | --- |
| เกาหัว "เห็นแล้วต้องเกาหัว" | งง ขำ | `pop_cartoon_pop_01` T2 ตรงมือแตะหัว | `pop_cute_pop`, `pop_orb` |
| เข้าตัวอย่างแรก | เปลี่ยนฉาก | `whoosh_swoosh_01` T2 | `whoosh_big_whoosh`, `whoosh_cartoon_swipe` |
| กระทะร้อน + "วางผิดคู่!" | ผิดจนพัง (ในครัว) | `foley_plate_breaking` T2 | `click_glitch_click` (ไม่ใช้บัซเซอร์) |
| ตัดไปภาพนิ่ง | ภาพถ่าย | `foley_camera_flash` T3 | `foley_camera_shutter_01` |
| "ไม่มีตู้แช่!" | เตือน error | `click_glitch_click` T2 | `pop_cartoon_pop_01` |
| คำเรียง "ปัญหา → สินค้า → ร้านค้า" | ตึงขึ้นเรื่อย ๆ | `whoosh_riser_01` T3 ยาว 2.95 วิ จบตรง hit | `whoosh_perfect_riser`, `whoosh_airy_stutter_riser_braam` |
| "ขายไม่ออก!" | ผลเสียมาถึง | `whoosh_cold_suspense_impact` T2 | `whoosh_swish_boom_03`, `whoosh_whoosh_hit` |
| ชี้คนดู "ร้านคุณ" | พูดตรงถึงคนดู | `pop_watery_pop` T3 | `pop_bubble_pop` |
| จัดชั้นวางใหม่ | คลี่คลาย | `whoosh_magic_wand_whoosh` T1 | — |
| ร้านเรียบร้อย | ดีขึ้น | `ding_twinkling_notification` T3 | `ding_positive_notification` |
| การ์ดแบรนด์ | มีทางออก | `ding_idea` T2 | `ding_ding_01` |
| ปุ่ม CTA | กดได้ | `click_mouse_click_01` T2 | `click_button_click` |
| Hook ที่เป็นคำประกาศแรง / ตัวเลข | หยุดนิ้ว | `whoosh_swish_boom_02` T2 (เว้นพยางค์แรก) | `whoosh_kick_reverberant` |
| แชต / พิมพ์ / เขียน | foley ตรงภาพ | `ding_message_sound`, `foley_keyboard_typing`, `foley_pencil` | — |

## เพลง

ใช้เพลงจังหวะเด้ง groovy จาก Mixkit (`assets/audio_mixkit/`) ค่าเริ่มต้น `music_funky_hip_hop.mp3` เริ่มที่ 7.5 วินาที (ช่วงที่บีตเต็ม) renderer วัด LUFS ของช่วงที่ใช้แล้วปรับให้ได้ **−31.5 LUFS** ก่อนผสม (= ระดับที่อาร์มอนุมัติ) และ duck ใต้เสียงพูด เปลี่ยนเพลงด้วย `MUSIC=<ไฟล์> MUSIC_SS=<วินาที>` ตัวเลือกที่มี: `music_like_a_loop_machine`, `music_funky_fit`, `music_comical` (Pop Track 03 อาร์มว่า "น่าเบื่อ")

ผลที่ต้องได้: ทุกเสียงใน plan มีเวลา tier และเหตุผลจากบริบท, peak ใน `mix.wav` ตรงแต่ละ hit ไม่เกินช่วงเสียงพูดรอบข้าง และ Whisper ถอดไฟล์จริงได้ครบทุกประโยค
