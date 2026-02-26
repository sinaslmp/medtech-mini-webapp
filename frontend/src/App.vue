<template>
  <div class="page">
    <h1 class="title">Medical Phase Simulator</h1>

    <div class="card controls">
      <div class="row">
        <input type="file" accept="image/png,image/jpeg" @change="onFile" />

        <label class="radio">
          <input type="radio" name="phase" value="arterial" v-model="phase" />
          Arteriosa
        </label>

        <label class="radio">
          <input type="radio" name="phase" value="venous" v-model="phase" />
          Venosa
        </label>

        <button class="btn" :disabled="!file || loading" @click="process">
          <span v-if="loading" class="btnContent">
            <span class="spinner" aria-hidden="true"></span>
            Processing...
          </span>
          <span v-else>Elabora immagine</span>
        </button>
      </div>

      <p class="hint">
        Upload an image and select a phase. Processing runs on the Python backend.
      </p>
    </div>

    <div class="grid">
      <div class="card">
        <h2 class="subtitle">Originale</h2>
        <div class="imgbox">
          <img v-if="originalUrl" :src="originalUrl" alt="Original" />
          <div v-else class="placeholder">No image uploaded</div>
        </div>
      </div>

      <div class="card">
        <h2 class="subtitle">Elaborata</h2>
        <div class="imgbox">
          <img v-if="processedUrl" :src="processedUrl" alt="Processed" />
          <div v-else class="placeholder">No processed image yet</div>
        </div>
      </div>
    </div>

    <div v-if="done" class="done">✅ Elaborazione completata</div>
    <div v-if="error" class="error">⚠️ {{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL as string;

const file = ref<File | null>(null);
const phase = ref<"arterial" | "venous">("arterial");
const loading = ref(false);

const originalUrl = ref<string>("");
const processedUrl = ref<string>("");
const done = ref(false);
const error = ref<string>("");

function onFile(e: Event) {
  const input = e.target as HTMLInputElement;
  const f = input.files?.[0] || null;
  file.value = f;
  done.value = false;
  error.value = "";
  processedUrl.value = "";

  if (originalUrl.value) URL.revokeObjectURL(originalUrl.value);
  originalUrl.value = f ? URL.createObjectURL(f) : "";
}

async function process() {
  if (!file.value) return;
  if (!BACKEND_URL) {
    error.value = "Missing VITE_BACKEND_URL env var.";
    return;
  }

  loading.value = true;
  done.value = false;
  error.value = "";

  try {
    const form = new FormData();
    form.append("file", file.value);
    form.append("phase", phase.value);

    const res = await fetch(`${BACKEND_URL}/process`, {
      method: "POST",
      body: form,
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `Request failed: ${res.status}`);
    }

    const blob = await res.blob();
    if (processedUrl.value) URL.revokeObjectURL(processedUrl.value);
    processedUrl.value = URL.createObjectURL(blob);
    done.value = true;
  } catch (e) {
    done.value = false;
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}
</script>

<style>
:root {
  --bg1: #0b1220;
  --bg2: #0f172a;
  --card: rgba(255, 255, 255, 0.06);
  --cardBorder: rgba(255, 255, 255, 0.12);
  --text: #e8eefc;
  --muted: rgba(232, 238, 252, 0.7);
  --primary: #3b82f6;
  --primary2: #2563eb;
  --danger: #ff4d6d;
  --success: #22c55e;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: radial-gradient(1200px 600px at 20% 10%, rgba(59,130,246,0.25), transparent 55%),
              radial-gradient(900px 500px at 80% 0%, rgba(34,197,94,0.18), transparent 55%),
              linear-gradient(180deg, var(--bg1), var(--bg2));
  color: var(--text);
}

.page {
  max-width: 980px;
  margin: 36px auto;
  padding: 0 16px 28px;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.title {
  text-align: center;
  font-size: 34px;
  margin: 8px 0 16px;
  letter-spacing: 0.2px;
}

.card {
  background: var(--card);
  border: 1px solid var(--cardBorder);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(8px);
}

.controls .row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

/* File input a bit nicer */
input[type="file"] {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.16);
  background: rgba(0,0,0,0.22);
  color: var(--text);
  max-width: 100%;
}
input[type="file"]::file-selector-button {
  margin-right: 10px;
  border: none;
  border-radius: 10px;
  padding: 8px 12px;
  background: rgba(255,255,255,0.14);
  color: var(--text);
  cursor: pointer;
}
input[type="file"]::file-selector-button:hover {
  background: rgba(255,255,255,0.18);
}

.radio {
  display: inline-flex;
  gap: 8px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.18);
}
.radio input {
  accent-color: var(--primary);
}

.btn {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.12);
  background: linear-gradient(180deg, var(--primary), var(--primary2));
  color: #fff;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
  transition: transform 0.08s ease, filter 0.12s ease;
}
.btn:hover { filter: brightness(1.05); }
.btn:active { transform: translateY(1px); }
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

/* Spinner inside button */
.btnContent {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
.spinner {
  width: 16px;
  height: 16px;
  border-radius: 999px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: rgba(255,255,255,0.95);
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.hint {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 13px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}

.subtitle {
  font-size: 18px;
  margin: 0 0 10px;
}

/* Image container: use a softer dark, with subtle border */
.imgbox {
  background: rgba(0,0,0,0.28);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  min-height: 300px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.imgbox img {
  max-width: 100%;
  height: auto;
  display: block;
  filter: contrast(1.05);
}

.placeholder {
  color: rgba(232, 238, 252, 0.65);
  font-size: 14px;
}

.done {
  margin-top: 14px;
  color: var(--success);
  font-weight: 700;
  text-align: center;
}

.error {
  margin-top: 12px;
  color: var(--danger);
  white-space: pre-wrap;
  text-align: center;
}

@media (max-width: 820px) {
  .grid { grid-template-columns: 1fr; }
  .title { font-size: 28px; }
}
</style>