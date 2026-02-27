import os
from typing import Optional
import httpx


class ResponseError(Exception):
    def __init__(self, status_code: Optional[int], error: str, message: str):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"{error}: {message}")


def request(lrclib_instance: str) -> dict:
    version = os.getenv("CARGO_PKG_VERSION", "unknown")
    user_agent = f"LRCGET v{version} (https://github.com/tranxuanthang/lrcget)"
    
    timeout = httpx.Timeout(30.0)
    with httpx.Client(timeout=timeout, headers={"User-Agent": user_agent}) as client:
        api_endpoint = f"{lrclib_instance.rstrip('/')}/api/request-challenge"
        res = client.post(api_endpoint)
        
        print(f"[getchallenge] Response Status: {res.status_code}")
        print(f"[getchallenge] Response Body: {res.json()}")
        
        if res.status_code == 200:
            return res.json()
        elif res.status_code in (400, 503, 500):
            error_data = res.json()
            raise ResponseError(
                status_code=error_data.get("statusCode"),
                error=error_data["error"],
                message=error_data["message"]
            )
        else:
            raise ResponseError(
                status_code=None,
                error="UnknownError",
                message="Unknown error happened"
            )


if __name__ == "__main__":
    response = request("https://lrclib.net")
    print(response)

