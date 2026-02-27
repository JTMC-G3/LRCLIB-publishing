import httpx

# Configuration - Fill these out
TRACK_NAME = "Fuck"
ARTIST_NAME = "glaive"
ALBUM_NAME = "Y'all"  # Optional
LRCLIB_INSTANCE = "https://lrclib.net"

def search_lyrics():
    # Build query parameters
    params = {}
    
    if TRACK_NAME:
        params["track_name"] = TRACK_NAME
    if ARTIST_NAME:
        params["artist_name"] = ARTIST_NAME
    if ALBUM_NAME:
        params["album_name"] = ALBUM_NAME
    
    # Validate at least one required parameter is present
    if "track_name" not in params and "q" not in params:
        print("Error: At least one of 'TRACK_NAME' or a search query is required")
        return
    
    print(f"Searching with parameters: {params}")
    
    # Make request
    api_endpoint = f"{LRCLIB_INSTANCE.rstrip('/')}/api/search"
    timeout = httpx.Timeout(30.0)
    
    with httpx.Client(timeout=timeout, verify=False) as client:
        res = client.get(api_endpoint, params=params)
        
        print(f"[search] Response Status: {res.status_code}")
        
        if res.status_code == 200:
            results = res.json()
            print(f"\nFound {len(results)} result(s):\n")
            
            for i, record in enumerate(results, 1):
                print(f"--- Result {i} ---")
                print(f"ID: {record.get('id')}")
                print(f"Track: {record.get('trackName')}")
                print(f"Artist: {record.get('artistName')}")
                print(f"Album: {record.get('albumName')}")
                print(f"Duration: {record.get('duration')} seconds")
                print(f"Instrumental: {record.get('instrumental')}")
                print(f"Has Plain Lyrics: {bool(record.get('plainLyrics'))}")
                print(f"Has Synced Lyrics: {bool(record.get('syncedLyrics'))}")
                print()
                # dump the synced and plain lyrics into the searchresults.txt file
                with open("searchresults.txt", "a", encoding="utf-8") as f:
                    f.write(f"--- Result {i} ---\n")
                    f.write(f"ID: {record.get('id')}\n")
                    f.write(f"Track: {record.get('trackName')}\n")
                    f.write(f"Artist: {record.get('artistName')}\n")
                    f.write(f"Album: {record.get('albumName')}\n")
                    f.write(f"Duration: {record.get('duration')} seconds\n")
                    f.write(f"Instrumental: {record.get('instrumental')}\n")
                    f.write(f"Has Plain Lyrics: {bool(record.get('plainLyrics'))}\n")
                    f.write(f"Has Synced Lyrics: {bool(record.get('syncedLyrics'))}\n\n")
                    if record.get("plainLyrics"):
                        f.write("Plain Lyrics:\n")
                        f.write(record["plainLyrics"] + "\n\n")
                    if record.get("syncedLyrics"):
                        f.write("Synced Lyrics (LRC format):\n")
                        # Convert synced lyrics JSON to LRC format
                        synced_lyrics = ""
                        for entry in record["syncedLyrics"]:
                            time = entry["time"]
                            minutes = int(time // 60)
                            seconds = int(time % 60)
                            milliseconds = int((time - int(time)) * 1000)
                            timestamp = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                            synced_lyrics += f"[{timestamp}] {entry['line']}\n"
                        f.write(synced_lyrics + "\n")
        else:
            print(f"Error: {res.status_code}")
            print(f"Response: {res.json()}")

if __name__ == "__main__":
    search_lyrics()
