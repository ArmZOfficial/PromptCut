# Affiliate video workspace

When the user asks to install or verify this kit on a computer, read [START-HERE.md](START-HERE.md) and run the setup or check command for the detected OS. Run it from the extracted project. Continue after recoverable errors. Report the exact missing package, permission, or network dependency if setup remains incomplete. Use the bundled `ffmpeg-skill` and the platform launcher under `scripts/`. The media-tool installation is local. ElevenLabs and other cloud providers use credentials configured by the person who owns that account.

When the user asks to create videos, use [affiliate-video-factory](.agents/skills/affiliate-video-factory/SKILL.md) and the stage skills it links. Use [WORKFLOW.md](WORKFLOW.md) for file contracts, [PROMPTS.md](PROMPTS.md) for copyable prompts, and [VOICE-CLONING.md](VOICE-CLONING.md) when the user selects cloned narration. Use the attached or supplied materials as evidence for the product, footage, or reference workflow.

Before cutting, revising, or reviewing any TikTok clip, read [arm-tiktok-taste](.agents/skills/arm-tiktok-taste/SKILL.md): Arm's editing taste, brand (Space Connex), audio mix rules, and QA bar.

Planning today's clip (ideas, topic, hook, script, prompts): [content-planner](.agents/skills/content-planner/SKILL.md). Missing footage or a non-commercial image: [free-broll-finder](.agents/skills/free-broll-finder/SKILL.md). Choosing sound effects: [sfx.md](.agents/skills/tiktok-pro-showcase/references/sfx.md).

For installation verification, use the launcher’s `doctor` and confirm local Whisper is available alongside FFmpeg and FFprobe. For a media job, verify the actual output with the delivery spec before declaring it ready.
