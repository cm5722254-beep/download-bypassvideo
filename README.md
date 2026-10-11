# TDL Media Downloader Pro - Global Senior Edition (`download-bypassvideo`)

⚡ **High-Performance Multi-Host Media Scraper, Stream Resolver & Batch Downloader Web Application**

A full-stack media extraction and downloading suite equipped with live scraper feeds, direct video stream resolver pipelines (ByteDance/Hongguo VOD, DramaBox CDN, iQIYI APIs, and Lucifer Donghua), concurrent multi-threaded downloads, and an ultra-modern cyber-glass UI dashboard.

---

## 🌟 Key Features

- **Multi-Host Stream Resolver Engine**:
  - **Hongguo ByteDance VOD** (`qznovelvod.com`): Live drama (`真人剧`), comic drama (`漫剧`), AI drama (`AI剧`), and comics (`漫画`).
  - **DramaBox Official Streams** (`hwvideoseo.dramaboxdb.com`): Direct episode resolution, metadata extraction, and CDN media streaming.
  - **iQIYI Server APIs & Lucifer Donghua**: Fast direct episode parsing and media extraction.
- **Batch & Parallel Downloader**:
  - Multi-threaded worker pool with configurable concurrency.
  - Live progress tracking, speed calculation (MB/s), file size auditing, and automatic retry mechanisms.
  - Simultaneous media file download + HD poster art caching.
- **Senior Cyber-Glass Web Dashboard**:
  - Live Host Catalog Browser with multi-platform tabs & filter chips.
  - Real-time download manager with interactive cancel, retry, and open-folder actions.
  - Direct URL stream resolution sandbox for ad-hoc video links.
  - Responsive dark cyberpunk / neon glassmorphism UI.

---

## 🚀 Quick Setup & Run

### Prerequisites
- Python 3.9+
- pip (Python Package Installer)
- Git

### 1. Install Dependencies
```bash
pip install fastapi uvicorn beautifulsoup4 requests pydantic
```

### 2. Launch the Application
You can launch directly with Python or using the batch script:
```powershell
python server.py
```
or double-click:
```powershell
START_TOOL.bat
```

### 3. Open the Web Interface
Navigate to your browser:
```
http://localhost:8000
```

---

## 📁 Repository Structure

```
├── static/
│   ├── index.html         # Cyber-glass reactive UI layout
│   ├── style.css          # Modern dark glassmorphic design system
│   └── app.js             # Client-side state manager, catalog & download controller
├── server.py              # FastAPI server, live scrapers, resolvers & download executor
├── START_TOOL.bat         # Windows one-click launcher
├── run_tool.py            # Headless runner & utility runner
├── .gitignore             # Git ignore file excluding APKs and large binary dumps
├── LICENSE                # MIT License
└── README.md              # Project documentation
```

---

## ⚙️ Configuration & API Endpoints

- `GET /api/catalog`: Returns live catalog scraped from official servers.
- `GET /api/status`: Downloads queue, worker health, and system directory status.
- `POST /api/download`: Enqueue one or multiple media items for background processing.
- `POST /api/resolve`: Real-time stream bypass and direct CDN resolution for single URLs.
- `POST /api/config`: Update download destination directory and worker concurrency.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
