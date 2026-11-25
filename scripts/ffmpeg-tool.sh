#!/bin/sh
set -eu

project=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
tools="$project/.agents/skills/ffmpeg-skill/scripts"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"
if command -v brew >/dev/null 2>&1; then
    full_ffmpeg=$(brew --prefix ffmpeg-full 2>/dev/null || true)
    if [ -n "$full_ffmpeg" ] && [ -x "$full_ffmpeg/bin/ffmpeg" ]; then
        export PATH="$full_ffmpeg/bin:$PATH"
    fi
fi
model="$HOME/.cache/whisper.cpp/ggml-large-v3-turbo-q5_0.bin"
if [ -z "${FFMPEG_SKILL_ASR_MODEL:-}" ] && [ -f "$model" ]; then
    export FFMPEG_SKILL_ASR_MODEL="$model"
fi

if [ "$#" -eq 0 ]; then set -- doctor; fi
tool=$1
shift
case "$tool" in
    doctor|contract) exec python3 -B "$tools/_contract.py" "$tool" "$@" ;;
    -*|*/*|*\\*|.*|*[!a-zA-Z0-9_.-]*) echo "Invalid tool name: $tool" >&2; exit 2 ;;
    *) exec python3 -B "$tools/${tool%.py}.py" "$@" ;;
esac
