const $ = (id) => document.getElementById(id);

const expectedEl = $("expected");
const recordBtn = $("recordBtn");
const refreshBtn = $("refreshBtn");

const statusText = $("statusText");
const progressBar = $("progressBar");
const lastResult = $("lastResult");
const lastClip = $("lastClip");

const clipList = $("clipList");
const player = $("player");
const selectedName = $("selectedName");
const serverPill = $("serverPill");

const overlay = $("overlay");
const countdownEl = $("countdown");

// Fixed behavior (not user editable)
const FIXED_SECONDS = 5;           // server will record this many seconds
const PREP_COUNTDOWN = 3;          // 3..2..1
const POLL_INTERVAL_MS = 700;
const TIMEOUT_MS = 90_000;

let pollTimer = null;

function setStatus(text, pct = null) {
  statusText.textContent = text;
  if (pct === null) return;
  progressBar.style.width = `${Math.max(0, Math.min(100, pct))}%`;
}

async function api(path) {
  const r = await fetch(path, { cache: "no-store" });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return await r.json();
}

function fmtBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(1)} MB`;
  const gb = mb / 1024;
  return `${gb.toFixed(2)} GB`;
}

function showOverlayCountdown(n) {
  overlay.classList.remove("hidden");
  overlay.setAttribute("aria-hidden", "false");
  countdownEl.textContent = String(n);
}

function hideOverlay() {
  overlay.classList.add("hidden");
  overlay.setAttribute("aria-hidden", "true");
}

function sleep(ms) {
  return new Promise((res) => setTimeout(res, ms));
}

function renderClips(clips) {
  clipList.innerHTML = "";
  if (!clips.length) {
    clipList.innerHTML = `<div class="mono">No clips yet.</div>`;
    return;
  }

  for (const c of clips) {
    const el = document.createElement("div");
    el.className = "clipItem";
    el.innerHTML = `
      <div class="clipLeft">
        <div class="clipTitle">${c.name}</div>
        <div class="clipSub">${new Date(c.mtime_ms).toLocaleString()} • ${fmtBytes(c.size_bytes)}</div>
      </div>
      <div class="badge">Play</div>
    `;
    el.onclick = () => {
      const url = `/incoming/${encodeURIComponent(c.name)}`;
      player.src = url;
      selectedName.textContent = c.name;
      player.play().catch(() => {});
    };
    clipList.appendChild(el);
  }
}

async function refresh() {
  try {
    const info = await api("/api/info");
    serverPill.textContent = `Server: ${info.server}`;
  } catch {
    serverPill.textContent = "Server: offline?";
  }

  try {
    const clips = await api("/api/clips");
    renderClips(clips);
  } catch (e) {
    clipList.innerHTML = `<div class="mono">Failed to load clips: ${e.message}</div>`;
  }
}

async function recordFlow() {
  const expected = Number(expectedEl.value ?? 0);
  const expectedClamped = Number.isFinite(expected) ? Math.max(0, Math.min(5, expected)) : 0;
  expectedEl.value = String(expectedClamped);

  // Snapshot current server state so we can detect the "next" result
  let beforeStatus = null;
  try {
    beforeStatus = await api("/api/status");
  } catch {
    beforeStatus = { last_upload_ts: null, last_upload_name: null, last_result: null };
  }
  const beforeTs = beforeStatus.last_upload_ts ?? 0;

  // Countdown
  recordBtn.disabled = true;
  expectedEl.disabled = true;
  refreshBtn.disabled = true;

  setStatus("Get ready…", 5);
  showOverlayCountdown(PREP_COUNTDOWN);
  for (let i = PREP_COUNTDOWN; i >= 1; i--) {
    countdownEl.textContent = String(i);
    await sleep(1000);
  }
  hideOverlay();

  // Trigger recording (seconds not user-set; we send fixed seconds)
  try {
    setStatus("Recording…", 15);
    await api(`/trigger?seconds=${encodeURIComponent(FIXED_SECONDS)}&expected=${encodeURIComponent(expectedClamped)}&json=1`);
  } catch (e) {
    setStatus(`Trigger error: ${e.message}`, 0);
    recordBtn.disabled = false;
    expectedEl.disabled = false;
    refreshBtn.disabled = false;
    return;
  }

  // Poll for new upload/result
  setStatus("Waiting for upload & classification…", 25);

  const start = Date.now();
  if (pollTimer) clearInterval(pollTimer);

  pollTimer = setInterval(async () => {
    try {
      const st = await api("/api/status");

      // update last clip text as soon as we see a new upload
      if (st.last_upload_name) lastClip.textContent = st.last_upload_name;

      const elapsed = Date.now() - start;
      const pct = 25 + Math.min(70, (elapsed / TIMEOUT_MS) * 70);
      progressBar.style.width = `${pct}%`;

      const isNewUpload = (st.last_upload_ts ?? 0) > beforeTs;

      // When new upload arrives and server has a result, we finish
      if (isNewUpload && st.last_result !== null && st.last_upload_name) {
        clearInterval(pollTimer);
        pollTimer = null;

        lastResult.textContent = String(st.last_result);
        lastClip.textContent = st.last_upload_name;
        setStatus("Done ✔", 100);

        await refresh();

        // auto load video
        player.src = `/incoming/${encodeURIComponent(st.last_upload_name)}`;
        selectedName.textContent = st.last_upload_name;
        player.play().catch(() => {});

        recordBtn.disabled = false;
        expectedEl.disabled = false;
        refreshBtn.disabled = false;
        return;
      }

      if (elapsed > TIMEOUT_MS) {
        clearInterval(pollTimer);
        pollTimer = null;
        setStatus("Timed out waiting for result.", 0);
        recordBtn.disabled = false;
        expectedEl.disabled = false;
        refreshBtn.disabled = false;
      }
    } catch {
      // ignore transient errors, keep polling
    }
  }, POLL_INTERVAL_MS);
}

recordBtn.addEventListener("click", recordFlow);
refreshBtn.addEventListener("click", refresh);

refresh();
