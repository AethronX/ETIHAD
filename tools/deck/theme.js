// Shared design system for the Etihad deck.
// Palette is taken from the client's own assets: the logo navy sampled from
// etihad-logo.png (#051C4A) and the product's own tokens.

const C = {
  navy: '#051C4A',      // logo navy — dominant
  navy2: '#0A2A63',     // lighter navy for depth
  blue: '#0F4C81',      // product primary
  cyan: '#00B8D9',      // product accent (movement / logistics)
  orange: '#F7931E',    // product accent (needs action)
  green: '#16A34A',
  red: '#DC2626',
  ink: '#111827',
  body: '#374151',
  muted: '#6B7280',
  line: '#E5E7EB',
  bg: '#F6F8FB',
  card: '#FFFFFF',
  white: '#FFFFFF',
};

const CSS = `
  @font-face { font-family:'PlexAr'; src:url('fonts/plex-Qw3CZRtWPQCuHme67tEYUIx3Kh0PHR9N6bs6.ttf'); font-weight:400; }
  @font-face { font-family:'PlexAr'; src:url('fonts/plex-Qw3NZRtWPQCuHme67tEYUIx3Kh0PHR9N6YPO_9CT.ttf'); font-weight:500; }
  @font-face { font-family:'PlexAr'; src:url('fonts/plex-Qw3NZRtWPQCuHme67tEYUIx3Kh0PHR9N6YPi-NCT.ttf'); font-weight:600; }
  @font-face { font-family:'PlexAr'; src:url('fonts/plex-Qw3NZRtWPQCuHme67tEYUIx3Kh0PHR9N6YOG-dCT.ttf'); font-weight:700; }
  @font-face { font-family:'InterNum'; src:url('fonts/inter-UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf'); font-weight:400; }
  @font-face { font-family:'InterNum'; src:url('fonts/inter-UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf'); font-weight:600; }
  @font-face { font-family:'InterNum'; src:url('fonts/inter-UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf'); font-weight:700; }

  * { box-sizing:border-box; margin:0; padding:0; }
  html,body { width:1920px; height:1080px; overflow:hidden; }
  body {
    font-family:'PlexAr', sans-serif; direction:rtl; background:${C.bg};
    color:${C.ink}; -webkit-font-smoothing:antialiased;
    font-feature-settings:'kern' 1;
  }
  .slide { position:relative; width:1920px; height:1080px; overflow:hidden; }
  .pad { position:absolute; inset:0; padding:88px 104px; }
  /* Vertically centres a slide whose content is shorter than the canvas,
     so short slides do not leave a dead band along the bottom. */
  .pad.ctr { display:flex; flex-direction:column; justify-content:center; }

  /* ---- type scale (one scale, used everywhere) ---- */
  .kicker { font-size:19px; font-weight:600; letter-spacing:.16em; color:${C.cyan}; }
  .kicker.dk { color:${C.blue}; }
  h1 { font-size:96px; font-weight:700; line-height:1.1; letter-spacing:-.02em; }
  h2 { font-size:56px; font-weight:700; line-height:1.18; letter-spacing:-.015em; }
  h3 { font-size:30px; font-weight:600; line-height:1.3; }
  .lead { font-size:27px; font-weight:400; line-height:1.65; color:${C.body}; }
  .body { font-size:22px; font-weight:400; line-height:1.7; color:${C.body}; }
  .cap  { font-size:18px; font-weight:400; line-height:1.55; color:${C.muted}; }
  .num  { font-family:'InterNum','PlexAr',sans-serif; font-feature-settings:'tnum' 1; direction:ltr; unicode-bidi:plaintext; display:inline-block; }
  .stat { font-family:'InterNum',sans-serif; font-size:76px; font-weight:700; line-height:1; letter-spacing:-.03em; }

  /* ---- surfaces ---- */
  .dark { background:${C.navy}; color:#fff; }
  .dark .lead,.dark .body { color:#C3D0E4; }
  .dark .cap { color:#8A9CBB; }
  .card {
    background:${C.card}; border:1px solid ${C.line}; border-radius:24px;
    box-shadow:0 1px 2px rgba(5,28,74,.04), 0 12px 32px rgba(5,28,74,.06);
  }
  .card.tint { background:#fff; }
  .chip {
    display:inline-flex; align-items:center; gap:10px; padding:9px 20px;
    border-radius:999px; font-size:19px; font-weight:600;
  }
  .dot { width:52px; height:52px; border-radius:16px; display:grid; place-items:center;
         font-size:24px; font-weight:700; color:#fff; flex:0 0 52px; }

  /* ---- device frames ---- */
  .laptop { position:relative; }
  .laptop .screen {
    background:#0B1220; border-radius:18px; padding:14px;
    box-shadow:0 40px 90px rgba(5,28,74,.28), 0 8px 20px rgba(5,28,74,.14);
  }
  .laptop .screen img { display:block; width:100%; border-radius:8px; }
  /* Crops a tall app screenshot to the height the slide can actually give it,
     keeping the top of the screen (header + first cards) rather than squashing. */
  .laptop .screen img.crop { object-fit:cover; object-position:top center; }
  .laptop .base {
    height:16px; margin:0 auto; border-radius:0 0 14px 14px;
    background:linear-gradient(180deg,#2A3444,#151C28);
  }
  .laptop .foot { height:7px; margin:0 auto; border-radius:0 0 20px 20px; background:rgba(5,28,74,.18); }

  .phone { position:relative; }
  .phone .shell {
    background:#0B1220; border-radius:44px; padding:11px;
    box-shadow:0 30px 70px rgba(5,28,74,.30), 0 6px 16px rgba(5,28,74,.16);
  }
  .phone .shell img { display:block; width:100%; border-radius:34px; }

  /* ---- logo lockup ---- */
  .lock { display:flex; align-items:center; gap:20px; }
  .lock img { height:66px; }
  .lock .nm { font-size:34px; font-weight:700; line-height:1.1; }
  .lock .sb { font-size:15px; letter-spacing:.16em; color:#7E8DA6; margin-top:4px; }

  /* ---- page number / footer mark ---- */
  .pg { position:absolute; bottom:44px; left:104px; font-family:'InterNum',sans-serif;
        font-size:17px; font-weight:600; color:${C.muted}; }
  .dark .pg { color:#63799B; }
  .mark { position:absolute; bottom:44px; right:104px; display:flex; align-items:center; gap:12px; }
  .mark span { font-size:16px; color:${C.muted}; letter-spacing:.02em; }
  .dark .mark span { color:#63799B; }

  .flow { display:flex; gap:0; align-items:stretch; }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:28px; }
  .grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:26px; }
  .grid4 { display:grid; grid-template-columns:repeat(4,1fr); gap:22px; }
`;

module.exports = { C, CSS };
