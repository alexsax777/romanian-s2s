/* romanian-s2s — film 43.6s @30fps. VO Supertonic: L1@0.0 L2@3.45 L3@9.7 L4@17.0 L5@23.4 L6@29.5 L7@37.0 */
const M = Motion.film({ fps: 30, duration: 43.6, width: 1920, height: 1080, clock: 'smooth' });
const ACCENT = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();

/* ===== B1 HOOK (f0-102): waveform = vocea. Buys: vocea e sintetică. ===== */
const wv1 = document.querySelector('#wv1');
for (let i = 0; i < 56; i++) {
  const b = document.createElement('div');
  b.className = 'wb';
  b.style.left = (240 + i * 26) + 'px';
  b.style.height = (24 + 150 * Math.abs(Math.sin(i * 0.53))) + 'px';
  wv1.appendChild(b);
}
wv1.querySelectorAll('.wb').forEach((b, i) => {
  M.kf(b, 'scaleY', [
    [0, 0.3],
    [14, 0.55 + 0.45 * Math.abs(Math.sin(i * 0.55)), 'glide'],
    [34, 0.35 + 0.5 * Math.abs(Math.sin(i * 0.9)), 'glide'],
    [72, 0.3, 'gentleIn'],
    [102, 0.1, 'gentleIn'],
  ], { fmt: v => v.toFixed(3) });
});
M.words('#h1a', { at: 8, mech: 'rise', dist: 74, gaps: 6, ease: 'softLand', smear: true, accent: { color: ACCENT, frames: 20 } });
M.words('#h1b', { at: 26, mech: 'rise', dist: 46, gaps: [5, 4, 5], ease: 'softLand' });
M.drift('#h1a', { prop: 'scale', from: 1, to: 1.04, start: 8, end: 100 });

/* ===== B2 TURN (f102-288): pipeline real. Carrier: banda de waveform. ===== */
M.cut(102, { hide: ['#s1'], show: ['#s2'] });
M.kf('#wv2', 'scaleX', [[102, 0.06], [126, 1, 'softLand']], { fmt: v => v.toFixed(3) });
M.kf('#wv2', 'transform-origin', [[102, '0% 50%']], { fmt: v => v });
M.enter('#p_stt', { at: 104, frames: 12, from: { y: 44, scale: 0.94 }, smear: { axis: 'y', px: 26 } });
M.enter('#p_stt_d', { at: 116, frames: 10, from: { y: 26 }, ease: 'softLand' });
M.enter('#p_llm', { at: 132, frames: 10, from: { y: 40, scale: 0.94 }, smear: { axis: 'y', px: 24 } });
M.enter('#p_llm_s', { at: 130, frames: 12, from: { y: 36 }, ease: 'softLand' });
M.enter('#p_tts', { at: 160, frames: 10, from: { y: 40, scale: 0.94 } });
M.enter('#p_tts_s', { at: 128, frames: 10, from: { y: 30 }, ease: 'softLand' });
M.kf('#arrow1', 'scaleX', [[112, 0], [128, 1, 'softLand']], { fmt: v => v.toFixed(3) });
M.kf('#arrow2', 'scaleX', [[132, 0], [146, 1, 'softLand']], { fmt: v => v.toFixed(3) });
M.words('#t2', { at: 150, mech: 'rise', dist: 40, gaps: [4, 3], ease: 'softLand' });

/* ===== B3 PROOF STT (f288-508): screenshot real mărit + linia reală de benchmark ===== */
M.cut(288, { hide: ['#s2'], show: ['#s3'] });
M.kf('#sh_whisper', 'scale', [[288, 1.35], [330, 1.0, 'snapSettle']], { fmt: v => v.toFixed(3) });
M.drift('#sh_whisper', { prop: 'scale', from: 1, to: 1.045, start: 332, end: 505 });
M.type('#term3', { at: 300, style: 'fast', seed: 7, cps: 30 });

/* ===== B4 PROOF LLM (f510-699): config real + fallback accent ===== */
M.cut(510, { hide: ['#s3'], show: ['#s4'] });
M.type('#cfg4', { at: 509, style: 'fast', seed: 3, cps: 26, accentNewest: { color: ACCENT, frames: 2 } });
M.words('#tok4', { at: 560, mech: 'rise', dist: 44, gaps: [4, 3], ease: 'softLand' });
M.enter('#fb4', { at: 640, frames: 12, from: { y: 30, scale: 0.95 }, ease: 'softLand', smear: { axis: 'y', px: 22 } });

/* ===== B5 PROOF TTS (f702-873): counter real 1.68s ===== */
M.cut(699, { hide: ['#s4'], show: ['#s5'] });
M.count('#c5', { at: 710, from: 0, to: 1.68, frames: 26, skip: 0.08, seed: 4 });
M.drift('#sh_sup', { prop: 'scale', from: 1, to: 1.05, start: 702, end: 870 });
M.kf('#sh_sup', 'transform-origin', [[702, '50% 10%']], { fmt: v => v });
M.words('#lbl5', { at: 780, mech: 'rise', dist: 30, gaps: [4, 3], ease: 'softLand' });

/* ===== B6 ONESTITATE (f876-1107): counter TTFT real ===== */
M.cut(876, { hide: ['#s5'], show: ['#s6'] });
M.words('#h6', { at: 882, mech: 'rise', dist: 60, gaps: [5, 4], ease: 'softLand', smear: true, accent: { color: ACCENT, frames: 18, word: -1 } });
M.count('#ttft6', { at: 900, from: 0, to: 3.76, frames: 24, round: false });
M.words('#h6c', { at: 940, mech: 'rise', dist: 34, gaps: [5, 4], ease: 'softLand' });
M.drift('#h6', { prop: 'scale', from: 1, to: 1.05, start: 878, end: 1100 });

/* ===== B7 CTA (f1110-1308): repo real + meta reveal. End hold ≤1.4s. ===== */
M.cut(1110, { hide: ['#s6'], show: ['#s7'] });
M.enter('#sh_repo', { at: 1112, frames: 18, ease: 'snapSettle', from: { scale: 1.08, y: 40, blur: 10 } });
M.enter('#url7', { at: 1150, frames: 12, from: { y: 34 }, ease: 'softLand' });
M.kf('#und7', 'scaleX', [[1180, 0], [1240, 1, 'softLand']], { fmt: v => v.toFixed(3) });
M.words('#meta7', { at: 1215, mech: 'rise', dist: 30, gaps: [5, 4], ease: 'softLand', accent: { color: ACCENT, frames: 30, word: -1 } });
M.drift('#cam7', { prop: 'scale', from: 1, to: 0.94, start: 1140, end: 1298 });
M.drift('#cam7', { prop: 'y', from: 0, to: 16, start: 1140, end: 1296 });

window.__ready = Motion.loaded().then(() => {
  if (/selftest/.test(location.search)) Motion.selfTest(M, { samples: 24 });
});

/* șablonuri de origini fixate static (nu pe timeline) */
document.querySelector('#sh_sup').style.transformOrigin = '50% 10%';
document.querySelector('#sh_whisper').style.transformOrigin = '72% 30%';
