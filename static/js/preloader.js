(function () {
  const DURATION_MS = 2500; // hard cap: 2.5s
  const preloader = document.getElementById('preloader');
  if (!preloader) return; // safety

  const audio = document.getElementById('pour-sound');

  // Try to play (may be blocked; it's fine either way)
  const tryPlay = () => { if (audio) audio.play().catch(()=>{}); };
  document.addEventListener('DOMContentLoaded', tryPlay, { once:true });

  // Also try on first interaction (browsers often allow this)
  ['click','touchstart','keydown'].forEach(evt => {
    window.addEventListener(evt, () => tryPlay(), { once:true, passive:true });
  });

  // Reveal after 5s no matter what
  const reveal = () => {
    preloader.classList.add('is-hiding');
    // stop sound shortly after hiding
    setTimeout(() => { if (audio) { audio.pause(); audio.currentTime = 0; } }, 300);
    // remove from DOM to avoid stacking issues
    setTimeout(() => preloader.remove(), 450);
  };

  // Start the 5s timer **after** the whole page loads (safer on slow nets)
  window.addEventListener('load', () => {
    setTimeout(reveal, DURATION_MS);
  });
})();