"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import Image from "next/image";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://kbsss-equation-solver.hf.space/predict";

interface BoundingBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

interface Result {
  equation: string;
  result: number | null;
  symbols_count: number;
  error: string | null;
  boxes?: BoundingBox[];
}

const SAMPLE_EQUATIONS = [
  { file: "/test_simple_add.png" },
  { file: "/test_simple_sub.png" },
  { file: "/test_simple_mul.png" },
  { file: "/test_simple_div.png" },
];

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [imageDimensions, setImageDimensions] = useState<{ width: number; height: number } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageContainerRef = useRef<HTMLDivElement>(null);

  const handleFile = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("Please select an image file");
      return;
    }
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setSelectedImage(url);
    setResult(null);
    setError(null);

    const img = new window.Image();
    img.onload = () => {
      setImageDimensions({ width: img.width, height: img.height });
    };
    img.src = url;
  }, []);

  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.startsWith("image/")) {
          const file = items[i].getAsFile();
          if (file) {
            handleFile(file);
            e.preventDefault();
            break;
          }
        }
      }
    };

    document.addEventListener("paste", handlePaste);
    return () => document.removeEventListener("paste", handlePaste);
  }, [handleFile]);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleSampleClick = async (sampleFile: string) => {
    setError(null);
    setResult(null);
    setSelectedImage(sampleFile);

    const response = await fetch(sampleFile);
    const blob = await response.blob();
    const file = new File([blob], sampleFile.split("/").pop() || "sample.png", {
      type: "image/png",
    });
    setSelectedFile(file);

    const img = new window.Image();
    img.onload = () => {
      setImageDimensions({ width: img.width, height: img.height });
    };
    img.src = sampleFile;
  };

  useEffect(() => {
    if (!result?.boxes || !canvasRef.current || !imageContainerRef.current || !imageDimensions) {
      return;
    }

    const canvas = canvasRef.current;
    const container = imageContainerRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = container.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    const scaleX = rect.width / imageDimensions.width;
    const scaleY = rect.height / imageDimensions.height;
    const scale = Math.min(scaleX, scaleY);

    const offsetX = (rect.width - imageDimensions.width * scale) / 2;
    const offsetY = (rect.height - imageDimensions.height * scale) / 2;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#22c55e";
    ctx.lineWidth = 2;
    ctx.font = "600 12px system-ui, sans-serif";
    ctx.fillStyle = "#22c55e";

    result.boxes.forEach((box, index) => {
      const x = offsetX + box.x * scale;
      const y = offsetY + box.y * scale;
      const w = box.w * scale;
      const h = box.h * scale;

      ctx.strokeRect(x, y, w, h);
      ctx.fillText(String(index + 1), x + 2, y - 4);
    });
  }, [result, imageDimensions]);

  const handleSolve = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const reader = new FileReader();
      const base64Promise = new Promise<string>((resolve) => {
        reader.onload = () => resolve(reader.result as string);
        reader.readAsDataURL(selectedFile);
      });
      const base64 = await base64Promise;

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: [base64],
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      if (data.data && data.data[0]) {
        setResult(data.data[0]);
      } else if (data.error) {
        setError(data.error);
      } else {
        setError("Unexpected response format");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to process image");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setImageDimensions(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <main className="min-h-screen py-16 px-4 sm:px-6">
      <div className="max-w-xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-3xl font-semibold tracking-tight mb-2">
            Equation Solver
          </h1>
          <p className="text-[var(--color-text-secondary)]">
            Handwritten math recognition powered by CNN
          </p>
        </header>

        <section className="mb-8">
          <div
            className={`upload-zone p-8 text-center cursor-pointer min-h-[280px] flex flex-col justify-center ${
              dragOver ? "drag-over" : ""
            } ${selectedImage ? "has-image" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => !selectedImage && fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFile(file);
              }}
            />

            {selectedImage ? (
              <div className="space-y-4">
                <div 
                  ref={imageContainerRef}
                  className="relative w-full max-w-md mx-auto h-40 bg-white/50 rounded-lg overflow-hidden"
                >
                  <Image
                    src={selectedImage}
                    alt="Selected equation"
                    fill
                    className="object-contain p-2"
                    sizes="(max-width: 448px) 100vw, 448px"
                  />
                  <canvas ref={canvasRef} className="bbox-canvas" />
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text)] transition-colors"
                >
                  Change image
                </button>
              </div>
            ) : (
              <div>
                <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-black/5 flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-[var(--color-text-secondary)]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </div>
                <p className="text-[var(--color-text)] font-medium mb-1">
                  Drop image here or click to browse
                </p>
                <p className="text-sm text-[var(--color-text-secondary)]">
                  PNG, JPG supported · Ctrl+V to paste
                </p>
              </div>
            )}
          </div>

          {selectedImage && (
            <div className="flex gap-3 mt-5 justify-center">
              <button
                onClick={handleSolve}
                disabled={loading}
                className="px-6 py-2.5 bg-[var(--color-accent)] text-white rounded-lg font-medium text-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
              >
                {loading && <span className="spinner" />}
                {loading ? "Processing..." : "Solve"}
              </button>
              <button
                onClick={handleClear}
                className="px-5 py-2.5 bg-white border border-black/10 rounded-lg font-medium text-sm hover:bg-gray-50 text-[var(--color-text-secondary)] transition-colors"
              >
                Clear
              </button>
            </div>
          )}
        </section>

        {(result || error) && (
          <section className="mb-8 animate-fade-in">
            <div className="card p-6">
              {error ? (
                <p className="text-red-600 text-center">{error}</p>
              ) : result ? (
                <div className="text-center">
                  <div className="mb-4">
                    <span className="text-xs uppercase tracking-wider text-[var(--color-text-secondary)] block mb-2">
                      Detected
                    </span>
                    <span className="text-2xl font-medium tracking-wide">{result.equation}</span>
                  </div>
                  {result.result !== null && (
                    <div className="pt-4 border-t border-black/10">
                      <span className="text-xs uppercase tracking-wider text-[var(--color-text-secondary)] block mb-2">
                        Result
                      </span>
                      <span className="text-4xl font-semibold text-[var(--color-accent)]">
                        {result.result}
                      </span>
                    </div>
                  )}
                  {result.error && (
                    <p className="text-sm text-[var(--color-text-secondary)] mt-4">
                      {result.error}
                    </p>
                  )}
                </div>
              ) : null}
            </div>
          </section>
        )}

        <section>
          <p className="text-sm text-[var(--color-text-secondary)] mb-4 text-center">
            Try a sample
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {SAMPLE_EQUATIONS.map((sample, index) => (
              <button
                key={index}
                onClick={() => handleSampleClick(sample.file)}
                className="sample-thumb bg-white/90 backdrop-blur rounded-xl overflow-hidden aspect-[4/3]"
              >
                <div className="relative w-full h-full">
                  <Image
                    src={sample.file}
                    alt={`Sample ${index + 1}`}
                    fill
                    className="object-contain p-2"
                  />
                </div>
              </button>
            ))}
          </div>
        </section>

        <footer className="mt-16 text-center text-xs text-[var(--color-text-secondary)]">
          Built with TensorFlow & Next.js
        </footer>
      </div>
    </main>
  );
}
