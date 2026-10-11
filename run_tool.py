import os
import sys
import time
import webbrowser
import threading
import uvicorn

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8989"
    print(f"\n=======================================================")
    print(f"🚀 TDL Media Downloader Pro is running!")
    print(f"🌐 Opening URL: {url}")
    print(f"=======================================================\n")
    webbrowser.open(url)

if __name__ == "__main__":
    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run uvicorn server
    uvicorn.run("server:app", host="127.0.0.1", port=8989, reload=False, log_level="info")
