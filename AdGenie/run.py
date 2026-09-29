import sys
import webbrowser
import threading
import time
from pathlib import Path

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

def open_browser_tab():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000/demo")

def main():
    print("""
    ===================================================================
      ADGENIE API: AI RECOMMENDATIONS & REGIONAL AD GENERATION
      Authors: Mohit Sharma (24020003019) & Rohit Gupta (24020003028)
      College: Satyug Darshan Institute of Engineering & Technology
    ===================================================================
    -> Interactive E-Commerce Demo Store: http://localhost:8000/demo
    -> Interactive Presentation Slides:   http://localhost:8000/presentation/presentation.html
    -> Interactive Swagger API Docs:      http://localhost:8000/docs
    -> PowerPoint PPT Deck File:         presentation/AdGenie_College_Presentation.pptx
    ===================================================================
    Starting FastAPI server on http://localhost:8000...
    """)
    
    # Launch browser automatically
    threading.Thread(target=open_browser_tab, daemon=True).start()

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
