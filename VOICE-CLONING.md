# ทำเสียงโคลนของตัวเองสำหรับคลิปขายสินค้า

สำหรับงานนี้ให้เริ่มจาก **ElevenLabs Instant Voice Cloning + Eleven v4** ด้วยเสียงไทยของคุณเอง แล้ววัดความเหมือนและความชัดจากบททดสอบสามแบบก่อนสร้างทั้งล็อต โปรไฟล์อยู่ในบัญชีและนำกลับมาใช้กับบทใหม่ผ่าน `voice_id` ได้ ในระบบวิดีโอควรบันทึกหนึ่งไฟล์เสียงต่อ `clip_id` เพื่อแก้คำอ่านหรือเปลี่ยนบทเป็นรายคลิป [ElevenLabs Instant Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning) · [รายการโมเดล ElevenLabs](https://elevenlabs.io/docs/overview/models/)

## เลือกเครื่องมือ

ตรวจข้อมูลฟีเจอร์จากเอกสารผู้ให้บริการวันที่ 24 พฤศจิกายน 2569 ความเหมือนของเสียงและความชัดภาษาไทยต้องทดสอบจากตัวอย่างเสียงและบทของคุณ

| เครื่องมือ | ใช้ซ้ำอย่างไร | เหมาะกับงานแบบไหน |
| --- | --- | --- |
| **ElevenLabs Instant Voice Cloning** | อัดเสียงชัดประมาณ 1–2 นาที สร้างโปรไฟล์แล้วเก็บ `voice_id` ใช้ v4 หรือ v3 ที่รองรับไทย | เริ่มเร็วผ่านหน้าเว็บ และต่อ API เมื่อผ่านการฟังตัวอย่าง หน้าแพ็กเกจระบุ Instant Voice Cloning และสิทธิ์เชิงพาณิชย์ใน Starter ตรวจเงื่อนไขแผนของบัญชีที่ใช้ [วิธีสร้าง IVC](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning) · [แพ็กเกจ](https://elevenlabs.io/pricing) |
| **ElevenLabs Professional Voice Cloning** | ใช้เสียงเจ้าของบัญชีพร้อมยืนยันตัวตนเสียง เตรียมเสียงประมาณ 30–180 นาทีตามคำแนะนำ และใช้ voice ID เมื่อฝึกสำเร็จ | ทำเสียงประจำช่องเมื่อ IVC ยังจับสำเนียงหรือโทนได้ไม่ตรงใจ เอกสารปัจจุบันระบุไทยผ่านตระกูล v4 และต้องใช้ Creator ขึ้นไป [Voice Cloning รุ่น Professional](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning) · [ภาษาของ PVC](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/) |
| **Fish Audio** | สร้างโปรไฟล์แบบ persistent แล้วส่ง ID ใน `reference_id` หรือทดลอง one-shot จากตัวอย่างเสียงและคำถอดตรงกับตัวอย่าง | ทางเลือกสำหรับเทียบเสียงและต่อ API รุ่น `s2.1-pro` เป็นตัวเลือก production ในเอกสาร Fish ส่วน `s2.1-pro-free` ใช้ทดสอบตามเงื่อนไขของบัญชี ตระกูล S2 มีภาษาไทย [ความสามารถด้านภาษา](https://fish.audio/s2/) · [ระบบโคลนเสียง](https://docs.fish.audio/features/voice-cloning) · [ราคาและขีดจำกัด](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits) |
| **Microsoft Azure Personal Voice / MAI-Voice** | ใช้ข้อความยินยอมด้วยเสียงและตัวอย่างสะอาด เรียกใช้ profile ผ่าน API หรือ SSML ตามรุ่นที่เปิดให้บัญชี | เหมาะกับงานบน Azure ที่มีการจัดการสิทธิ์และยื่นขอใช้ฟีเจอร์ได้ Personal Voice แบบ Foundry ระบุตัวอย่าง 5–90 วินาที และ MAI-Voice ระบุภาษาไทยและการโคลนแบบขอสิทธิ์ [Personal Voice](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview) · [MAI-Voice](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-voices) |
| **Thonburian TTS** | รันในเครื่องโดยให้เสียงอ้างอิงสั้น ๆ กับโมเดลภาษาไทย | เหมาะกับการทดลองในเครื่องแบบไม่ใช้เชิงพาณิชย์ โมเดลที่เผยแพร่ใช้ CC BY-NC-SA 4.0 จึงควรใช้ทางเลือกเชิงพาณิชย์สำหรับคลิปขายสินค้าหากไม่มีใบอนุญาตเพิ่มเติม [โค้ดและสิทธิ์โมเดล](https://github.com/biodatlab/thonburian-tts#license) |

**เลือกโมเดลภาษาไทยให้ถูกตัว** Eleven v4 (`eleven_v4`) และ Eleven v3 (`eleven_v3`) ระบุ `th` ในเอกสาร ส่วน Multilingual v2 และ Flash v2.5 ใช้รายการภาษาอีกชุดที่ไม่มีภาษาไทย ตัวอย่าง API ทั่วไปของ ElevenLabs บางหน้าตั้ง Multilingual v2 ไว้ จึงต้องกำหนด `model_id` ในคำขอและตรวจโมเดลที่บัญชีใช้งานได้ [รายการโมเดลและภาษา](https://elevenlabs.io/docs/overview/models/) · [API รายการโมเดล](https://elevenlabs.io/docs/api-reference/models/list)

## ทำ ElevenLabs ผ่านหน้าเว็บ

1. อัดเสียงตัวเองในห้องเงียบด้วยไมค์เดียว ระยะปากคงที่ ใช้เสียงพูดตามธรรมชาติในโทนเดียวกับช่อง เก็บเสียงคนเดียว ไม่มีเพลงหรือเสียงคนอื่น สำหรับ IVC เริ่มที่ 60–120 วินาทีสะอาด แยกบททดสอบออกจากไฟล์ตัวอย่าง [แนวทางอัดเสียง IVC](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning)
2. เข้า **Voices → Add a new voice → Instant Voice Clone** ตั้งชื่อ เช่น `Own Thai product narration` อัปโหลดไฟล์และยืนยันสิทธิ์เสียง เมื่อต้องการ PVC ให้สร้างและยืนยันเสียงของตนเองตามขั้นตอนในบัญชี [Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/)
3. เปิดเสียงจาก **My Voices** ไปหน้า Text to Speech เลือก Eleven v4 หรือ Eleven v3 วางบทไทยหนึ่งคลิป ฟังตั้งแต่คำเปิดถึง CTA ดาวน์โหลด MP3 เป็น `Video/P01-01_voice.mp3` และคัดลอก Voice ID ไว้สำหรับ API [ElevenLabs IVC Quickstart](https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/instant-voice-cloning)
4. ทดสอบ 3 แบบด้วยข้อความเดียวกันข้ามโมเดลหรือผู้ให้บริการ ประกอบด้วย Hook สั้น ขั้นตอนที่มีชื่อสินค้าและหน่วย และ CTA ที่มีชื่อรุ่น ให้เจ้าของเสียงตรวจความเหมือน ความชัด วรรณยุกต์ ความเป็นธรรมชาติ และเวลาที่อ่าน ถ้าชื่อหลุดให้แก้คำอ่านใน `voice_text` แล้วคงตัวสะกดบนจอตามฉลาก

### บทซ้อมอัดเสียงอ้างอิง

> วันนี้จะลองจัดโต๊ะทำงานให้หยิบของง่ายขึ้น เริ่มจากวางของที่ใช้ทุกวันไว้ใกล้มือ แล้วเก็บของที่ไม่ค่อยได้ใช้ไว้ด้านข้าง ถ้าคุณมีพื้นที่น้อย ลองวัดจากขอบโต๊ะถึงหน้าจอก่อน จะได้รู้ว่าชิ้นไหนวางได้พอดี เวลาจะเลือกซื้อ ลองดูขนาดจากฉลากและเทียบกับของที่มีอยู่แล้ว ผมจะเปิดกล่องให้ดูทีละชิ้นและลองใช้งานให้เห็นในมุมใกล้ ๆ จากนั้นค่อยดูว่ารุ่นนี้เหมาะกับการใช้งานของคุณหรือเปล่า

พูดต่อด้วยคำอธิบายวิธีใช้สินค้าจริงของคุณให้ครบเวลาที่ต้องการ ใช้จังหวะเดียวกับงานขายจริง และเว้นช่องว่างสั้นตามธรรมชาติ

## เรียก ElevenLabs จาก PowerShell สำหรับคลิปนำร่อง

ตัวอย่างอ่าน `voice_text` จาก `Brief/scripts.json` เรียกโมเดลที่บัญชีรองรับภาษาไทยและบันทึกเฉพาะคลิปที่เลือก ต้องมี FFprobe บน `PATH` เพื่อทดสอบไฟล์ก่อนย้ายไปโฟลเดอร์งาน คีย์อยู่ใน environment ของ session ปัจจุบัน คำขอสร้างเสียงอาจใช้เครดิต [Create speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert/) · [List models](https://elevenlabs.io/docs/api-reference/models/list)

```powershell
if (-not $env:ELEVENLABS_API_KEY) {
    $secureKey = Read-Host 'ElevenLabs API key' -AsSecureString
    $env:ELEVENLABS_API_KEY = [Net.NetworkCredential]::new('', $secureKey).Password
}

$clipId = 'P01-01'
$voiceId = Read-Host 'Voice ID จาก My Voices'
$modelId = 'eleven_v4'
if ($voiceId -notmatch '^[A-Za-z0-9_-]+$') { throw 'กรุณาตรวจ Voice ID' }
Get-Command ffprobe -ErrorAction Stop | Out-Null

$scripts = Get-Content -LiteralPath 'Brief/scripts.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$entries = @($scripts | Where-Object clip_id -eq $clipId)
if ($entries.Count -ne 1 -or -not $entries[0].voice_text) { throw "ตรวจสคริปต์ $clipId" }

$headers = @{ 'xi-api-key' = $env:ELEVENLABS_API_KEY }
$available = Invoke-RestMethod -Method Get -Uri 'https://api.elevenlabs.io/v1/models' -Headers $headers
$thaiModel = $available | Where-Object {
    $_.model_id -eq $modelId -and $_.can_do_text_to_speech -and
    $_.languages.language_id -contains 'th'
}
if (-not $thaiModel) { throw "บัญชีนี้ยังใช้ $modelId กับภาษาไทยไม่ได้ ให้ตรวจรายการโมเดลก่อน" }

$outputPath = Join-Path 'Video' "${clipId}_voice.mp3"
if (Test-Path -LiteralPath $outputPath) { throw "มีไฟล์ $outputPath แล้ว เปลี่ยนชื่อเทคเดิมก่อนสร้างใหม่" }
New-Item -ItemType Directory -Force -Path 'Video' | Out-Null
$tempPath = Join-Path 'Video' "${clipId}_$([guid]::NewGuid().ToString('N')).part.mp3"
$payload = @{ text = $entries[0].voice_text; model_id = $modelId; language_code = 'th' } |
    ConvertTo-Json -Compress
$uri = "https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128"

try {
    Invoke-WebRequest -UseBasicParsing -Method Post -Uri $uri -Headers $headers `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([Text.Encoding]::UTF8.GetBytes($payload)) -OutFile $tempPath -TimeoutSec 90 -ErrorAction Stop
    $codec = ffprobe -v error -select_streams a:0 -show_entries 'stream=codec_name' `
        -of 'default=noprint_wrappers=1:nokey=1' $tempPath
    if ($LASTEXITCODE -ne 0 -or $codec -ne 'mp3') { throw 'ไฟล์ที่ตอบกลับไม่ผ่านการตรวจเสียง MP3' }
    Move-Item -LiteralPath $tempPath -Destination $outputPath -ErrorAction Stop
    Get-Item -LiteralPath $outputPath | Select-Object FullName, Length
} finally {
    if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath }
}
```

ถ้าทดสอบ `eleven_v3` ให้เปลี่ยน `$modelId` แล้วรันการตรวจรายการโมเดลเดิม ถ้าโมเดลแสดงภาษาไทยแต่เสียงหรือ endpoint ใช้งานไม่ได้ ให้ตรวจสิทธิ์คีย์ ประเภทเสียง และสิทธิ์แพ็กเกจในบัญชี การอ่าน `ffprobe` ยืนยันชนิดไฟล์ ให้เปิดฟังทั้งคลิปก่อนใช้จริง

## ต่อเข้าคิว 30 คลิป

1. เก็บโปรไฟล์เสียงเป็น alias เช่น `my-thai-voice` แล้ว resolve ไป `voice_id`, `reference_id` หรือ `speakerProfileId` ตอนรัน เก็บ API key ใน environment หรือ secret store ของเครื่องที่ประมวลผล
2. จัดคำพูดให้มี `voice_text` ตามการออกเสียง เก็บ `overlay_text` ตามการสะกดจริง เช่น `500 มล.` บนจอและ `ห้าร้อยมิลลิลิตร` ในบท ระบุโมเดล ผู้ให้บริการ และโหมดเสียงใน manifest ต่อคลิป
3. คำนวณ fingerprint จาก provider, voice ID, model, voice settings, output format และ `voice_text` ที่ส่งจริง จับคู่คลิปกับไฟล์เสียงที่ผ่านตรวจ ถ้าบทเดิมและ fingerprint ตรง ใช้ไฟล์เดิม รันครั้งละน้อยตาม concurrency ของบัญชี
4. ถ้าเจอ `429` ใช้ `Retry-After` เมื่อมีและจำกัดรอบ retry ถ้า `401` หรือ `403` ตรวจคีย์และสิทธิ์ ถ้า timeout หลังส่งคำขอให้บันทึกว่าสถานะผู้ให้บริการยังไม่แน่ชัดและตรวจงานเดิมก่อนส่งซ้ำ เพื่อคุมเครดิต
5. หลังได้ไฟล์เสียง ให้ ASR หรือ alignment วัดเวลาจริง ทำซับ แล้วค่อยเรียง B-roll ด้วยเวลาเดียวกัน หากใช้เสียงโคลนกับภาพที่เห็นปากผู้พูดชัด ให้สลับไปใช้ช็อตมือหรือสินค้าในช่วงนั้น หรือใช้เสียงจริงของเทคนั้นเพื่อรักษาซิงก์

สำหรับ Fish Audio ให้สร้างโปรไฟล์แบบ private รอจนสถานะพร้อม จากนั้นส่ง model ID ของเสียงเป็น `reference_id` ใน body ของ `POST /v1/tts` เลือกรุ่นด้วย HTTP header `model` แล้วตั้ง `format` เป็น `mp3` ระบบส่วนที่อ่านไฟล์ตาม `clip_id` ใช้โครงเดียวกับ ElevenLabs ได้ [Fish Audio Clone and Wait](https://docs.fish.audio/developer-guide/sdk-guide/cookbook/clone-and-wait-until-ready) · [Fish Audio TTS endpoint](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech)
