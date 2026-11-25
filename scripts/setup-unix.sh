#!/bin/sh
set -eu

project=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"
model_dir="$HOME/.cache/whisper.cpp"
model_name=ggml-large-v3-turbo-q5_0.bin
model="$model_dir/$model_name"
expected=394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2

valid_model() {
    [ -f "$1" ] || return 1
    if command -v sha256sum >/dev/null 2>&1; then
        digest=$(sha256sum "$1" | cut -d ' ' -f 1)
    else
        digest=$(shasum -a 256 "$1" | cut -d ' ' -f 1)
    fi
    [ "$digest" = "$expected" ]
}

run_as_root() {
    if [ "$(id -u)" -eq 0 ]; then "$@"; else sudo "$@"; fi
}

if [ "${1:-}" != '--check-only' ]; then
    if command -v brew >/dev/null 2>&1; then
        for formula in python ffmpeg-full whisper.cpp; do
            brew list --versions "$formula" >/dev/null 2>&1 || brew install "$formula"
        done
    elif [ "$(uname -s)" = Linux ] && command -v apt-get >/dev/null 2>&1; then
        if ! command -v python3 >/dev/null 2>&1 || ! command -v ffmpeg >/dev/null 2>&1 ||
           ! command -v ffprobe >/dev/null 2>&1 || ! command -v curl >/dev/null 2>&1 ||
           ! command -v whisper-cli >/dev/null 2>&1; then
            run_as_root apt-get update
            run_as_root apt-get install -y python3 ffmpeg curl ca-certificates git cmake build-essential
        fi
        if ! command -v whisper-cli >/dev/null 2>&1; then
            source_dir="$HOME/.local/share/affiliate-video/whisper-cpp-v1.8.2"
            mkdir -p "$(dirname -- "$source_dir")" "$HOME/.local/bin"
            if [ ! -d "$source_dir/.git" ]; then
                git clone --depth 1 --branch v1.8.2 https://github.com/ggml-org/whisper.cpp.git "$source_dir"
            fi
            cmake -S "$source_dir" -B "$source_dir/build" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF
            cmake --build "$source_dir/build" --config Release --target whisper-cli --parallel 2
            install -m 755 "$source_dir/build/bin/whisper-cli" "$HOME/.local/bin/whisper-cli"
        fi
    elif ! command -v python3 >/dev/null 2>&1 || ! command -v ffmpeg >/dev/null 2>&1 ||
         ! command -v ffprobe >/dev/null 2>&1 || ! command -v whisper-cli >/dev/null 2>&1; then
        echo 'Install Homebrew or provide Python 3.10+, FFmpeg 6.1+, FFprobe, and whisper-cli on PATH.' >&2
        exit 1
    fi

    if ! valid_model "$model"; then
        mkdir -p "$model_dir"
        part="$model.part"
        url="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$model_name"
        attempt=1
        while [ "$attempt" -le 4 ] && ! valid_model "$part"; do
            if [ -f "$part" ] && [ "$(wc -c < "$part" | tr -d ' ')" -ge 574041195 ]; then
                echo "Model checksum mismatch: $part" >&2
                exit 1
            fi
            curl --fail --location --connect-timeout 30 --max-time 600 --continue-at - \
                --output "$part" "$url?download=true&setup=$(date +%s)-$attempt" || true
            attempt=$((attempt + 1))
        done
        valid_model "$part" || { echo "Model download incomplete or invalid: $part" >&2; exit 1; }
        mv -f -- "$part" "$model"
    fi
    mkdir -p "$project/Brief" "$project/Video" "$project/Insert" "$project/Output" "$project/.work/tiktok_pro"
fi

valid_model "$model" || { echo 'The verified local Thai ASR model is missing.' >&2; exit 1; }
status=$(sh "$project/scripts/ffmpeg-tool.sh" doctor --json)
printf '%s\n' "$status" | python3 -c '
import json, sys
d = json.load(sys.stdin)
if not d["ok"] or "external:whisper" not in d["available"]:
    sys.exit("Required tools are missing. Run scripts/ffmpeg-tool.sh doctor for details.")
print("Ready: ffmpeg-skill {}, FFmpeg {}, FFprobe {}, local Whisper.".format(d["version"], d["ffmpeg"], d["ffprobe"]))
'
