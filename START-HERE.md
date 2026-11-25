# เริ่มใช้ชุดทำคลิปสินค้าในเครื่องใหม่

[เปิดคู่มือภาพการติดตั้ง](docs/images/01-install-th.png)

แตก ZIP ลงโฟลเดอร์ของคุณ ตรวจว่ามี `AGENTS.md`, `scripts/` และ `.agents/skills/` อยู่ระดับเดียวกัน จากนั้นเปิด **โฟลเดอร์ที่แตกแล้ว** เป็น workspace ใน Codex หรือ AI ที่เปิด terminal และรันคำสั่งบนเครื่องได้ แล้วส่งข้อความนี้ให้ AI

```text
อ่าน AGENTS.md และ START-HERE.md ในโฟลเดอร์นี้ แล้วติดตั้งเครื่องมือสำหรับชุดทำคลิปสินค้าให้พร้อมใช้
ตรวจระบบปฏิบัติการ ใช้สคริปต์ของเครื่องนี้ ติดตั้งเฉพาะที่ยังขาด และรัน doctor หลังติดตั้ง
ฉันต้องการให้ FFmpeg, FFprobe, Python และ Whisper ภาษาไทยในเครื่องพร้อมใช้กับ ffmpeg-skill
บอกผลตรวจและตำแหน่งไฟล์ที่จะวางบรีฟ สินค้า และเสียง ถ้าเจอปัญหาเครือข่ายหรือการติดตั้งให้ลองแก้ตามเอกสารก่อนสรุป
```

ZIP มีคู่มือ พรอมป์ สกิลหลัก 11 ตัว (รวม `arm-tiktok-taste`, `content-planner`, `free-broll-finder`) พร้อม `ffmpeg-skill` ของ `kajisho5` ในตัว ตัวเรียกคำสั่ง สคริปต์ติดตั้ง ฟอนต์ไทยพร้อม OFL คลัง SFX (`assets/sfx_muaaz/`) เพลง Mixkit (`assets/audio_mixkit/`) และแบรนด์ Space Connex (`assets/brand/`) สำหรับใช้ในทีมเท่านั้น ห้ามแจกไฟล์เสียงหรือโลโก้ออกนอกทีม สคริปต์ดาวน์โหลด Whisper โมเดลไทยขนาดประมาณ **574 MB** และติดตั้งแพ็กเกจที่ขาด จึงต้องต่ออินเทอร์เน็ตในรอบติดตั้ง บัญชีและคีย์ API ของบริการเสียงเป็นของผู้รับชุด [แหล่งฟอนต์และใบอนุญาต](https://github.com/google/fonts/tree/main/ofl/notosansthai)

## Windows 10/11 x64

รันใน PowerShell จากโฟลเดอร์ที่แตกแล้ว สคริปต์ใช้ WinGet ของ Microsoft App Installer ติดตั้ง Python หรือ FFmpeg เฉพาะเมื่อเวอร์ชันที่ต้องใช้ยังไม่พร้อม และตรวจ SHA-256 ของ Whisper กับโมเดลก่อนติดตั้ง [Microsoft App Installer](https://learn.microsoft.com/en-us/windows/package-manager/winget/) · [Whisper.cpp Windows release](https://github.com/ggml-org/whisper.cpp/releases/tag/v1.8.2)

```powershell
.\scripts\setup-windows.ps1
.\scripts\ffmpeg-tool.ps1 doctor
```

ใช้ `./scripts/setup-windows.ps1 -CheckOnly` เพื่อเช็กของที่ติดตั้งแล้ว ข้อมูล runtime ของ Whisper เก็บใน `%LOCALAPPDATA%\AffiliateVideo\whisper` สคริปต์สามารถดาวน์โหลดต่อเมื่อการเชื่อมต่อหลุด ถ้านโยบายเปิดสคริปต์จาก ZIP บล็อก ให้ตรวจแหล่งที่มาของ ZIP ตามขั้นตอนขององค์กร แล้วใช้วิธีปลดบล็อกไฟล์ที่อนุญาตสำหรับชุดนี้

## macOS หรือ Linux

บน macOS ใช้ Homebrew สำหรับ FFmpeg แบบ `ffmpeg-full`, Whisper.cpp และ Python หากมี Homebrew อยู่แล้วให้รันคำสั่งด้านล่าง บน Ubuntu 24.04 ขึ้นไปหรือ Debian ที่แพ็กเกจ FFmpeg เป็น 6.1 ขึ้นไป สคริปต์รองรับ apt และคอมไพล์ Whisper.cpp เมื่อเครื่องยังไม่มี `whisper-cli` ทาง apt อาจขอสิทธิ์ผู้ดูแลจากผู้ใช้เครื่อง ดิสโทรอื่นใช้ Homebrew หรือจัดให้มีคำสั่งที่ `doctor` ต้องใช้ใน `PATH` [Homebrew FFmpeg Full](https://formulae.brew.sh/formula/ffmpeg-full) · [Homebrew Whisper.cpp](https://formulae.brew.sh/formula/whisper.cpp)

```sh
sh scripts/setup-unix.sh
sh scripts/ffmpeg-tool.sh doctor
```

ใช้ `sh scripts/setup-unix.sh --check-only` เพื่อตรวจอย่างเดียว โมเดลอยู่ใน `~/.cache/whisper.cpp/` เมื่อใช้คำสั่งในคู่มือ ให้แทน `./scripts/ffmpeg-tool.ps1` ด้วย `sh scripts/ffmpeg-tool.sh` และเปลี่ยน backtick ต่อบรรทัดของ PowerShell เป็น `\` หรือต่อให้เป็นบรรทัดเดียว ขั้นตอนติดตั้งและเรนเดอร์ผ่านการทดสอบบน Windows ส่วนคำสั่ง macOS/Linux จัดให้ตามแพ็กเกจสำหรับเครื่องปลายทาง

## เริ่มงานหลังขึ้น Ready

เปิด [คู่มือใช้งานสำหรับคนทำคลิป](USER-GUIDE.md) แล้วไล่ตั้งแต่ใส่บรีฟไปจนถึงตรวจไฟล์ส่งออก

1. ใส่บรีฟสินค้าใน `Brief/product.md` จาก [พรอมป์ 01](PROMPTS.md#01-บรีฟสินค้าและหลักฐาน) ถ่ายหรือวาง A-roll ใน `Video/` และวาง B-roll ใน `Insert/` ตาม [คู่มือหลัก](WORKFLOW.md)
2. ถ้าจะใช้เสียงจริง เริ่มทำ pilot ได้เลย ถ้าจะใช้เสียงโคลน ให้ผู้รับบันทึกเสียงของตัวเอง เปิดบัญชีที่ใช้งานได้ สร้างโปรไฟล์ แล้วตั้ง Voice ID และ API key ตาม [คู่มือ ElevenLabs](VOICE-CLONING.md)
3. เปิดแชตในโปรเจกต์แล้วเรียก `$affiliate-video-factory` พร้อมระบุโหมดเสียงและสั่งทำคลิปนำร่อง 1–3 คลิป ตรวจพรีวิวและปรับพรีเซ็ตก่อนสั่งทำจนครบ 30 คลิป

ตัวอย่างสั่งหลังติดตั้ง

```text
ใช้ $affiliate-video-factory อ่าน Brief/product.md และสำรวจ Video/ กับ Insert/
ทำแผน 6 หมวด หมวดละ 5 คลิป แล้วเลือก 3 มุมสำหรับ pilot
ใช้เสียง A-roll ของฉัน ทำพรีวิวคลิปแรกและตรวจซับไทยกับ Safe Zone ก่อนส่งออก
```
