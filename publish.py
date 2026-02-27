import json
import httpx
from getchallenge import request
from getpublishtoken import solve_challenge

# Configuration - Fill these out
TRACK_NAME = "It Is What It Is"
ARTIST_NAME = "glaive"
ALBUM_NAME = "Y'all"
DURATION = 142  # Duration in seconds
PLAIN_LYRICS_FILE = "lyrics.txt"
SYNCED_LYRICS_FILE = "synced.json"  # Output from your lyrics syncer app
LRCLIB_INSTANCE = "https://lrclib.net"


def ms_to_lrc_timestamp(ms: int) -> str:
    """Convert milliseconds to LRC timestamp format [mm:ss.xx]"""
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    # LRC uses centiseconds (2 decimal places)
    return f"[{minutes:02d}:{seconds:05.2f}]"


def synced_json_to_lrc(synced_path: str) -> str:
    """Load a synced.json file and convert it to an LRC string."""
    with open(synced_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = data.get("lines", [])
    if not lines:
        raise ValueError("No lines found in synced JSON file.")

    lrc_lines = []
    for line in lines:
        timestamp = ms_to_lrc_timestamp(line["time_ms"])
        lrc_lines.append(f"{timestamp} {line['text']}")

    return "\n".join(lrc_lines)


def publish_lyrics():
    # ── Plain lyrics ──────────────────────────────────────────────────────────
    try:
        with open(PLAIN_LYRICS_FILE, "r", encoding="utf-8") as f:
            plain_lyrics = f.read().strip()
        print(f"[DEBUG] Plain lyrics loaded: {len(plain_lyrics)} characters")
    except FileNotFoundError:
        print(f"Error: {PLAIN_LYRICS_FILE} not found")
        return

    # ── Synced lyrics (LRC) ───────────────────────────────────────────────────
    synced_lyrics = ""
    try:
        synced_lyrics = synced_json_to_lrc(SYNCED_LYRICS_FILE)
        print(f"[DEBUG] Synced lyrics converted: {len(synced_lyrics.splitlines())} lines")
        print("[DEBUG] First 3 LRC lines:")
        for line in synced_lyrics.splitlines()[:3]:
            print(f"  {line}")
    except FileNotFoundError:
        print(f"Warning: {SYNCED_LYRICS_FILE} not found — publishing without synced lyrics.")
    except ValueError as e:
        print(f"Warning: {e} — publishing without synced lyrics.")

    # ── Challenge + token ─────────────────────────────────────────────────────
    print("Requesting challenge...")
    challenge_response = request(LRCLIB_INSTANCE)
    prefix = challenge_response["prefix"]
    target = challenge_response["target"]

    print("Solving challenge...")
    nonce = solve_challenge(prefix, target)
    publish_token = f"{prefix}:{nonce}"
    print(f"Token obtained: {publish_token}")

    # ── Publish ───────────────────────────────────────────────────────────────
    headers = {"X-Publish-Token": publish_token}
    data = {
        "trackName": TRACK_NAME,
        "artistName": ARTIST_NAME,
        "albumName": ALBUM_NAME,
        "duration": DURATION,
        "plainLyrics": plain_lyrics,
        "syncedLyrics": synced_lyrics,
    }

    print("Publishing lyrics...")
    api_endpoint = f"{LRCLIB_INSTANCE.rstrip('/')}/api/publish"

    timeout = httpx.Timeout(30.0)
    with httpx.Client(timeout=timeout, verify=False) as client:
        res = client.post(api_endpoint, json=data, headers=headers)

        print(f"[publish] Response Status: {res.status_code}")
        if res.status_code == 201:
            print("Success! Lyrics published.")
            if res.content:
                print(f"[publish] Response Body: {res.json()}")
        else:
            print(f"Error: {res.status_code}")
            if res.content:
                print(f"[publish] Response Body: {res.json()}")


if __name__ == "__main__":
    publish_lyrics()