# Handwritten Equation Solver

A full-stack application that recognizes and solves handwritten mathematical equations using Deep Learning.

## Live Demo

- **Frontend**: [https://simple-math-solver.vercel.app/](https://simple-math-solver.vercel.app/)
- **Backend API**: [https://huggingface.co/spaces/kbsss/equation-solver](https://huggingface.co/spaces/kbsss/equation-solver)

## Screenshots

### Before Solving
![Before - Upload Interface](docs/screenshots/before.png)

### After Solving
![After - Result Display](docs/screenshots/after.png)

## About The Project

Upload an image of a handwritten mathematical equation, and the system will:
1. Segment the image into individual symbols
2. Recognize each symbol using a CNN (digits 0-9, operators +, -, ×, ÷)
3. Compute and display the result

### Supported Operations
- Addition (+)
- Subtraction (-)
- Multiplication (×)
- Division (÷)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js, Tailwind CSS, TypeScript |
| Backend | Python, FastAPI |
| ML Model | TensorFlow/Keras, OpenCV |
| Deployment | Vercel (Frontend), Hugging Face Spaces (Backend) |

## Project Structure

```
├── frontend/                  # Next.js web application
│   ├── app/                  # App router pages
│   └── public/               # Static assets & sample images
├── backend/
│   └── huggingface/          # HuggingFace Spaces deployment
│       ├── app.py            # FastAPI backend
│       ├── Dockerfile        # Docker configuration
│       ├── model.h5          # Trained CNN model
│       └── requirements.txt  # Backend dependencies
├── data/
│   ├── models/               # Model files
│   └── samples/              # Sample test images
├── docs/                     # Documentation & screenshots
├── notebooks/                # Jupyter notebooks
└── requirements.txt          # Python dependencies (for training)
```

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- Docker (optional, for backend)

### Running Locally

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

#### Backend (Docker)

```bash
cd backend/huggingface
docker build -t equation-solver-backend .
docker run -p 7860:7860 equation-solver-backend
```

The API will be available at `http://localhost:7860`

### Training the Model

If you need to retrain the model:

```bash
python train_model.py
```

This requires the dataset in `data/data/dataset/` directory.

## Model Architecture

- **Input**: 32×32 grayscale images
- **Architecture**: 3 Conv2D layers → MaxPooling → Dense layers → Softmax
- **Output**: 14 classes (0-9, +, -, ×, ÷)
- **Accuracy**: ~95% on test set

## Features

- Drag & drop image upload
- Paste from clipboard (Ctrl+V)
- Sample equations for quick testing
- Bounding box visualization
- Mobile responsive design

## License

MIT License
