# 🧠 Synthetic Image (Face) Detection — Web Integrated

A web application that detects **synthetic / AI-generated face images** using a **Vision Transformer (ViT)** model, a **Flask backend**, and a **React + TypeScript frontend**.  
It provides an end-to-end workflow — from model inference to visualization in a modern, responsive interface.

---

## 🚀 Overview

This project integrates three major components:

- 🧠 **Vision Transformer Model (DeepfakeViT):** trained to classify images as *Real* or *Fake*.
- ⚙️ **Flask Backend API:** serves the model for inference via REST endpoints.
- 💻 **React Frontend:** provides an interactive UI for image upload, analysis, and visualization of detection results.

---

## ⚙️ Features

- ✅ Detect synthetic vs real faces using **Vision Transformer (ViT-Tiny)**
- ⚡ REST API for **single**, **batch**, and **Base64** image detection
- 🌓 Dark/Light mode toggle
- 📂 Drag & drop upload and **batch analysis**
- 🧾 Export results as **JSON** or **TXT**
- 💾 History of all analyses
- 📊 Confidence and risk-level visualization

---

## 🧠 Technology Stack

| Layer | Technology |
|-------|-------------|
| **Model** | PyTorch, timm (Vision Transformer) |
| **Backend** | Flask, Flask-CORS, Torch, Torchvision, Pillow |
| **Frontend** | React + TypeScript, TailwindCSS, Lucide Icons, Vite |

---

## 🧩 Project Architecture

```
frontend/
│
├── node_modules/                 # Dependencies (auto-generated)
│
├── src/
│   ├── App.tsx                   # Main React component (UI + logic)
│   ├── index.css                 # Global CSS styles
│   ├── main.tsx                  # React entry point
│   └── vite-env.d.ts             # Vite + TypeScript environment declarations
│
├── .gitignore                    # Ignored files
├── eslint.config.js              # ESLint configuration
├── index.html                    # Root HTML file
├── package.json                  # Project dependencies & scripts
├── package-lock.json             # Dependency lock file
├── postcss.config.js             # PostCSS configuration
├── tailwind.config.js            # TailwindCSS setup
├── tsconfig.json                 # TypeScript base config
├── tsconfig.app.json             # TS configuration for frontend app
├── tsconfig.node.json            # TS configuration for node environment
└── vite.config.ts                # Vite dev server & build configuration
│
backend/
│
├── app.py                        # Flask backend API
├── deepfake_vit_final.pth        # Trained Vision Transformer model weights
├── model.ipynb                   # Model training & evaluation notebook
├── requirements.txt              # Python dependencies
└── README.md                     # Backend documentation (optional)
│
root/
│
├── .gitignore
└── README.md                     # This file (project-level)
```

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/synthetic-image-detection.git
cd synthetic-image-detection
```

---

### 2️⃣ Backend Setup (Flask)

#### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

#### Install Dependencies
Create a `requirements.txt` file with:
```text
flask
flask-cors
torch
torchvision
timm
pillow
```

Install:
```bash
pip install -r requirements.txt
```

#### Run Backend
Make sure `deepfake_vit_final.pth` is in the same directory as `app.py`.
```bash
python app.py
```

Backend runs by default at:
```
http://127.0.0.1:5000
```

---

### 3️⃣ Frontend Setup (React + TypeScript)

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Run the Frontend
```bash
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

If backend runs on another host/port, update:
```ts
fetch('http://127.0.0.1:5000/api/detect', ...)
```

---

## 🖥️ Application Features & UI Previews

Below are the main UI modules of the system.  
You can upload screenshots into a folder like `frontend/src/assets/` and reference them here.

---

### 🖼️ 1. Image Upload Interface
- Drag & drop or select an image file (JPG, PNG, GIF).
- Validates file size (max 10MB) and format.
- Smooth animations and progress feedback.

**Preview:**
<img width="1882" height="877" alt="image" src="https://github.com/user-attachments/assets/d0d634dc-68cf-4133-884f-666862049f63" />


---

### 🔍 2. Detection Results
- Displays whether the uploaded image is **Real** or **Synthetic**.
- Shows **confidence percentage**, **risk level**, and **probabilities**.
- Allows export of the report as **JSON** or **TXT**.

**Preview:**
<img width="1442" height="881" alt="image" src="https://github.com/user-attachments/assets/e0e8848c-35b0-4658-af91-4825a603ccf9" />



---

### 🌓 3. Dark / Light Mode
- Instant toggle between **Dark** and **Light** UI themes.
- Maintains contrast and visual balance across all panels.

**Preview:**
<img width="1873" height="857" alt="image" src="https://github.com/user-attachments/assets/4f0b6fa8-304c-4368-9417-a652820f9cb0" />


---

### 🧺 4. Batch Processing
- Upload and analyze **multiple images** in one go.
- Displays progress, individual confidence, and export options.
- Supports JSON export of all batch results.

**Preview:**
<img width="1522" height="450" alt="image" src="https://github.com/user-attachments/assets/3986de47-4758-442f-a82f-bfb3e2cc98d5" />


---

### 🕒 5. Analysis History
- Automatically logs all previous analyses.
- Allows reloading old results.
- Clear history or export previous reports anytime.

**Preview:**
<img width="1416" height="550" alt="image" src="https://github.com/user-attachments/assets/bd7260ca-d5fc-4a3f-a08a-02acbdfba365" />


---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Health check |
| `/api/detect` | POST | Detect a single uploaded image |
| `/predict_base64` | POST | Detect via base64-encoded image |
| `/batch_predict` | POST | Detect multiple images at once |

---

### 🧾 Example: Detect a Single Image
```bash
curl -X POST -F "image=@sample.jpg" http://127.0.0.1:5000/api/detect
```

**Response Example**
```json
{
  "prediction": "Fake",
  "confidence": 0.93,
  "probabilities": {
    "fake": 0.93,
    "real": 0.07
  },
  "class_id": 0
}
```

---

## 🧠 Model Overview

- Architecture: **Vision Transformer (Tiny)**
- Input size: **224×224**
- Preprocessing: Resize → Normalize (ImageNet mean/std)
- Core Techniques:
  - Self-Attention Mechanism  
  - Patch Embedding  
  - Multi-Head Attention  
  - Position Encoding  
  - Layer Normalization  
  - Feed-Forward Layers

---

## 🧪 Model Training (Notebook)

Notebook `model.ipynb` includes:
- Dataset preparation (e.g., CIFAKE / Deepfake faces)
- Fine-tuning ViT for binary classification
- Evaluation (accuracy, confusion matrix)
- Model export to `deepfake_vit_final.pth`

---

## ⚠️ Troubleshooting

| Issue | Cause | Solution |
|-------|--------|-----------|
| ❌ Model not loaded | Missing `deepfake_vit_final.pth` | Place model in backend folder |
| ⚠️ CORS error | Frontend–backend domain mismatch | CORS enabled by default (`flask_cors.CORS(app)`) |
| 🔥 CUDA unavailable | GPU not detected | Runs on CPU automatically |
| 📦 Image too large | Frontend limit = 10MB | Resize before uploading |
| 🚫 Wrong URL | API not on `127.0.0.1:5000` | Update fetch URL in `App.tsx` |

---

## 🧰 Optional: Docker Support

**Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

**Build & Run**
```bash
docker build -t deepfake-detector .
docker run -p 5000:5000 deepfake-detector
```

---


## 🪪 License

This project is released under the **MIT License** —  
free to use, modify, and distribute for research and educational purposes.

---

## 💡 Acknowledgements

- [PyTorch](https://pytorch.org)  
- [timm Vision Transformer Models](https://rwightman.github.io/pytorch-image-models/)  
- [React](https://react.dev)  
- [TailwindCSS](https://tailwindcss.com)  
- [Lucide Icons](https://lucide.dev)  
- [CIFAKE / Deepfake Datasets](https://www.kaggle.com/)

---

⭐ **If you found this project helpful, please give it a star on GitHub!**
