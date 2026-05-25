<div align="center">

# 🎬 EPIC-STUDIO'S
**The Elite AI Automation Layer for FL Studio**

[![CI Pipeline](https://img.shields.io/github/actions/workflow/status/credkellar-boop/EPIK-STUDIOS/main.yml?branch=main&label=Build&style=flat-square)](https://github.com/credkellar-boop/EPIK-STUDIOS/actions)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FL Studio](https://img.shields.io/badge/FL%20Studio-21%2B-orange?style=flat-square)](https://www.image-line.com/)
[![Gemini API](https://img.shields.io/badge/Powered%20By-Gemini%202.5%20Pro-8E75B2?style=flat-square)](https://aistudio.google.com/)
[![Code Style: Flake8](https://img.shields.io/badge/Linting-Flake8-black?style=flat-square)](https://flake8.pycqa.org/)

</div>

---

## 🚀 Overview

**EPIC-STUDIO'S** is a high-fidelity, AI-driven automation engine built directly for FL Studio. Powered by the Gemini 2.5 Pro model, it bridges the gap between software development and top-tier music industry production. 

Designed specifically for blockbuster film scoring, 8K cinematic rendering, and streaming-ready audio quality, this system translates natural language into native Python DAW scripts, generative MIDI piano roll macros, and real-time hardware routing matrices.

## ✨ Core Industry Features

* **🎬 8K Cinematic Orchestration:** Generates visualizer configurations tailored for `7680x4320` resolution at a strict `23.976 FPS` Hollywood standard.
* **💎 32-Bit Float Mastering:** Native configuration enforces `96,000 Hz` sampling rates and zero-clipping audio pipelines for commercial releases.
* **🎻 Generative Symphonic Macros:** Injects mathematical timing variations, exponential crescendo curves, and humanization into the FL Studio Piano Roll.
* **👁️ Live A/V Vision Bridge:** Utilizes multi-threaded OpenCV to track real-time camera feeds, converting physical movement into MIDI CC data to control 8K visuals and audio filters simultaneously.
* **⚡ Automated Workflow Engine:** FastAPI backend with an embedded web console that generates, compiles, and directly injects Python logic into FL Studio's secure directories.

---

## 📂 Perfect Project Structure

```text
EPIK-STUDIOS/
├── .github/
│   └── workflows/
│       └── main.yml                  # Flake8 Linting & CI Automation Pipeline
├── brain/
│   ├── cv_midi_bridge.py             # Multi-threaded OpenCV to MIDI CC router
│   ├── engine.py                     # Gemini API orchestration & DAW macro compiler
│   ├── exporter.py                   # Script injection to local FL Studio directories
│   └── scraper.py                    # GitHub API context retrieval
├── Documents/Image-Line/FL Studio/Settings/
│   └── Hardware/Epic_Controller/
│       └── device_EpicVision.py      # ZGameEditor 8K Visualizer routing script
├── piano_roll/
│   └── Epic_Symphonic_Engine.py      # Humanized velocity & micro-timing macros
├── templates/
│   ├── fl_panel.html                 # Embedded DAW borderless UI
│   └── index.html                    # Main web dashboard interface
├── .gitignore
├── cinematic_core.py                 # Core constraint enforcer for industry specs
├── config.json                       # 96kHz / 8K Video global configurations
├── epic_studios_brain.py             # Auto-tone & specialized pitch tracking
├── main.py                           # FastAPI web server and routing handler
└── requirements.txt                  # System dependencies (Headless OpenCV, GenAI)
