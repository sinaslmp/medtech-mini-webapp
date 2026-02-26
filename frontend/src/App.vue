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
          {{ loading ? "Processing..." : "Elabora immagine" }}
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
.page {
  max-width: 980px;
  margin: 40px auto;
  padding: 0 16px;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: #111;
}
.title {
  text-align: center;
  font-size: 34px;
  margin-bottom: 18px;
}
.card {
  background: #fff;
  border: 1px solid #e6e6e6;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.controls .row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
.radio {
  display: inline-flex;
  gap: 8px;
  align-items: center;
}
.btn {
  padding: 10px 14px;
  border-radius: 10px;
  border: none;
  background: #111;
  color: #fff;
  cursor: pointer;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.hint {
  margin: 10px 0 0;
  color: #555;
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
.imgbox {
  background: #0b0b0b;
  border-radius: 10px;
  min-height: 280px;
  display: grid;
  place-items: center;
  overflow: hidden;
}
.imgbox img {
  max-width: 100%;
  height: auto;
  display: block;
}
.placeholder {
  color: #bdbdbd;
  font-size: 14px;
}
.done {
  margin-top: 14px;
  color: #0b7a2a;
  font-weight: 600;
  text-align: center;
}
.error {
  margin-top: 12px;
  color: #b00020;
  white-space: pre-wrap;
  text-align: center;
}
@media (max-width: 820px) {
  .grid { grid-template-columns: 1fr; }
}
</style>