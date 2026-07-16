STYLE = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500&display=swap');

:root {
  --wilos-green: #00754A;
  --wilos-ink: #1A1712;
  --wilos-muted: #6B665F;
  --wilos-paper: #F2F0EB;
  --wilos-panel: #FFFFFF;
  --wilos-border: #D8D3CA;
}

html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: -0.01em; color: var(--wilos-ink); background: var(--wilos-paper); }
[data-testid="stHeader"] { height: 2.5rem; background: transparent; }

/* Hide Streamlit's hosting chrome. The top-right toolbar/menu and Deploy
   button are already trimmed by toolbarMode="minimal" in config.toml; these
   rules hide the bottom-right Community Cloud viewer badge ("Hosted with
   Streamlit" + the creator's GitHub avatar), the transient status widget, and
   the legacy footer. The viewer badge is injected by Community Cloud and only
   appears on the deployed app, not in local runs. */
#MainMenu { visibility: hidden !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stAppDeployButton"] { display: none !important; }
[class*="viewerBadge"] { display: none !important; }
[data-testid="stSidebar"] { background: var(--wilos-panel); border-right: 1px solid var(--wilos-border); }
[data-testid="stSidebarNavLink"] { border-radius: 8px; color: var(--wilos-muted); }
[data-testid="stSidebarNavLink"]:hover { background: #E8F1EC; color: var(--wilos-green); }
[data-testid="stSidebarNavLink"][aria-current="page"] { background: #E8F1EC; color: var(--wilos-green); font-weight: 600; }

.block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 7rem; }
[data-testid="stHeading"] h1, [data-testid="stHeading"] h2 { font-family: 'Fraunces', Georgia, serif !important; font-weight: 500 !important; color: var(--wilos-green) !important; }
[data-testid="stHeading"] h1 { margin: 0 0 1rem; }
.stMarkdown p { color: var(--wilos-muted); line-height: 1.65; }
.wilos-title { font-family: 'Fraunces', Georgia, serif; font-size: clamp(2.8rem, 9vw, 5rem); font-weight: 750; letter-spacing: -0.06em; text-align: center; color: var(--wilos-ink); margin-top: 8vh; }
.wilos-title span { color: var(--wilos-green); }
.wilos-title--chat { font-size: 2rem; text-align: left; margin: 0 0 1rem; }
.wilos-title--chat span { font-size: 1.2em; }
.wilos-subtitle { text-align: center; color: var(--wilos-muted); font-size: 1.05rem; margin: .2rem 0 1.5rem; }
.wilos-subtitle--chat { font-size: .85rem; margin: .1rem 0 .4rem; padding-left: 1rem; text-align: left; }
.askwil-label { color: var(--wilos-green); font-size: .72rem; font-weight: 700; letter-spacing: .08em; margin-bottom: .25rem; }
.askwil-marker { display: inline-block; margin-top: .55rem; padding: .2rem .55rem; border-radius: 999px; font-size: .72rem; line-height: 1.3; }
.askwil-marker--source { color: #365A49; background: #E8F1EC; }
.askwil-marker--refusal { color: #72543D; background: #F5ECE3; }
.askwil-sources { margin-top: .55rem; color: #365A49; font-size: .72rem; }
.askwil-sources summary { display: inline-block; padding: .2rem .55rem; border-radius: 999px; background: #E8F1EC; cursor: pointer; list-style: none; }
.askwil-sources summary::-webkit-details-marker { display: none; }
.askwil-sources ul { margin: .45rem 0 0 .7rem; padding-left: 1rem; color: var(--wilos-muted); }
.askwil-sources li { margin: .15rem 0; }
[data-testid="stChatMessage"] { background: var(--wilos-panel); border: 1px solid var(--wilos-border); border-radius: 14px; padding: .35rem .6rem; margin-bottom: .7rem; }
[data-testid="stBottom"] { background: color-mix(in srgb, var(--wilos-paper) 92%, transparent); border-top: 1px solid var(--wilos-border); }
.stButton > button { border-radius: 999px; border: 1px solid transparent; background: #E8F1EC; color: var(--wilos-green); font-weight: 600; padding: 0.55rem 1.15rem; box-shadow: 0 1px 2px rgba(26,23,18,.06); transition: background .15s ease, color .15s ease, box-shadow .15s ease, transform .1s ease; }
.stButton > button:hover { background: var(--wilos-green); color: #FFFFFF; box-shadow: 0 4px 10px rgba(0,117,74,.25); }
.stButton > button:focus-visible { outline: 2px solid var(--wilos-green); outline-offset: 2px; }
.stButton > button:active { transform: scale(0.95); box-shadow: 0 1px 2px rgba(26,23,18,.08); }
.wilos-demo { border: 1px solid var(--wilos-border); background: var(--wilos-panel); border-radius: 14px; padding: 1rem 1.15rem; margin: 1rem 0 1.4rem; }
.wilos-demo-q { color: var(--wilos-ink); font-weight: 600; margin-bottom: .7rem; }
.wilos-demo-q span { color: var(--wilos-muted); font-weight: 400; }
.wilos-demo-a { color: var(--wilos-ink); line-height: 1.6; }
.wilos-demo .askwil-label { margin-top: .2rem; }
.wilos-try { display: grid; gap: .5rem; margin: .8rem 0 1.2rem; }
.wilos-try-item { border: 1px solid var(--wilos-border); background: var(--wilos-panel); border-radius: 10px; padding: .6rem .9rem; color: var(--wilos-ink); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .85rem; }
.wilos-flow { display: grid; justify-items: center; gap: .4rem; margin: 1rem 0; }
.wilos-flow-step { width: min(100%, 680px); padding: .8rem 1rem; border: 1px solid var(--wilos-border); background: var(--wilos-panel); border-radius: 12px; }
.wilos-flow-arrow { color: var(--wilos-green); font-weight: 700; }
/* Pinned bottom-right to stay clear of the full-height left sidebar. High
   z-index keeps it above the bottom input bar; pointer-events: none means it
   never intercepts clicks. */
.wilos-cup { position: fixed; right: 16px; bottom: 16px; z-index: 999999; pointer-events: none; opacity: .85; filter: drop-shadow(0 2px 3px rgba(26,23,18,.28)); animation: wilos-cup-float 4.5s ease-in-out infinite; }
.wilos-cup svg { display: block; }
@keyframes wilos-cup-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }

.st-key-wilos_chat_panel { background: var(--wilos-panel); border: 1px solid var(--wilos-border); border-radius: 12px; padding: 1.25rem 1.25rem 0.25rem; box-shadow: 0 0 0.5px rgba(0,0,0,0.14), 0 1px 1px rgba(0,0,0,0.24); }
.st-key-wilos_chat_panel [data-testid="stChatMessage"]:last-child { margin-bottom: 0; }

.st-key-wilos_hero { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 35vh; text-align: center; }
.st-key-wilos_hero [data-testid="stHorizontalBlock"], .st-key-wilos_bottom [data-testid="stHorizontalBlock"] { justify-content: center; gap: .5rem; }
.st-key-wilos_hero [data-testid="stColumn"], .st-key-wilos_bottom [data-testid="stColumn"] { width: auto !important; flex: 0 0 auto !important; }
.st-key-wilos_hero .stButton > button, .st-key-wilos_bottom .stButton > button { min-width: 6.5rem; }

@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; gap: .3rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
  [data-testid="stColumn"] .stButton > button { min-width: 0; padding-left: .25rem; padding-right: .25rem; font-size: .78rem; white-space: nowrap; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
'''

# A small pixel-art Stanley Cup easter egg pinned to the bottom-left corner — a
# nod to the hockey interest in facts.json. Inline SVG so it needs no external
# asset and inherits the app's self-contained, CSP-friendly approach.
STANLEY_CUP = (
    '<div class="wilos-cup">'
    '<svg viewBox="0 0 16 21" width="32" height="42" shape-rendering="crispEdges" '
    'aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="4" y="0" width="8" height="1" fill="#4d515b"/><rect x="4" y="1" width="1" height="1" fill="#4d515b"/><rect x="5" y="1" width="3" height="1" fill="#ccd1db"/><rect x="8" y="1" width="2" height="1" fill="#b4bac6"/><rect x="10" y="1" width="1" height="1" fill="#99a0af"/><rect x="11" y="1" width="1" height="1" fill="#4d515b"/><rect x="4" y="2" width="1" height="1" fill="#4d515b"/><rect x="5" y="2" width="3" height="1" fill="#ccd1db"/><rect x="8" y="2" width="2" height="1" fill="#b4bac6"/><rect x="10" y="2" width="1" height="1" fill="#99a0af"/><rect x="11" y="2" width="1" height="1" fill="#4d515b"/><rect x="5" y="3" width="1" height="1" fill="#4d515b"/><rect x="6" y="3" width="2" height="1" fill="#ccd1db"/><rect x="8" y="3" width="2" height="1" fill="#b4bac6"/><rect x="10" y="3" width="1" height="1" fill="#4d515b"/><rect x="6" y="4" width="1" height="1" fill="#4d515b"/><rect x="7" y="4" width="1" height="1" fill="#ccd1db"/><rect x="8" y="4" width="1" height="1" fill="#b4bac6"/><rect x="9" y="4" width="1" height="1" fill="#4d515b"/><rect x="6" y="5" width="1" height="1" fill="#4d515b"/><rect x="7" y="5" width="1" height="1" fill="#ccd1db"/><rect x="8" y="5" width="1" height="1" fill="#b4bac6"/><rect x="9" y="5" width="1" height="1" fill="#4d515b"/><rect x="5" y="6" width="1" height="1" fill="#4d515b"/><rect x="6" y="6" width="2" height="1" fill="#ccd1db"/><rect x="8" y="6" width="2" height="1" fill="#b4bac6"/><rect x="10" y="6" width="1" height="1" fill="#4d515b"/><rect x="5" y="7" width="1" height="1" fill="#4d515b"/><rect x="6" y="7" width="2" height="1" fill="#ccd1db"/><rect x="8" y="7" width="2" height="1" fill="#b4bac6"/><rect x="10" y="7" width="1" height="1" fill="#4d515b"/><rect x="4" y="8" width="1" height="1" fill="#4d515b"/><rect x="5" y="8" width="3" height="1" fill="#ccd1db"/><rect x="8" y="8" width="2" height="1" fill="#b4bac6"/><rect x="10" y="8" width="1" height="1" fill="#99a0af"/><rect x="11" y="8" width="1" height="1" fill="#4d515b"/><rect x="4" y="9" width="1" height="1" fill="#4d515b"/><rect x="5" y="9" width="3" height="1" fill="#ccd1db"/><rect x="8" y="9" width="2" height="1" fill="#b4bac6"/><rect x="10" y="9" width="1" height="1" fill="#99a0af"/><rect x="11" y="9" width="1" height="1" fill="#4d515b"/><rect x="3" y="10" width="1" height="1" fill="#4d515b"/><rect x="4" y="10" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="10" width="3" height="1" fill="#ccd1db"/><rect x="8" y="10" width="2" height="1" fill="#b4bac6"/><rect x="10" y="10" width="2" height="1" fill="#99a0af"/><rect x="12" y="10" width="1" height="1" fill="#4d515b"/><rect x="3" y="11" width="1" height="1" fill="#4d515b"/><rect x="4" y="11" width="8" height="1" fill="#7c8290"/><rect x="12" y="11" width="1" height="1" fill="#4d515b"/><rect x="3" y="12" width="1" height="1" fill="#4d515b"/><rect x="4" y="12" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="12" width="3" height="1" fill="#ccd1db"/><rect x="8" y="12" width="2" height="1" fill="#b4bac6"/><rect x="10" y="12" width="2" height="1" fill="#99a0af"/><rect x="12" y="12" width="1" height="1" fill="#4d515b"/><rect x="3" y="13" width="1" height="1" fill="#4d515b"/><rect x="4" y="13" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="13" width="3" height="1" fill="#ccd1db"/><rect x="8" y="13" width="2" height="1" fill="#b4bac6"/><rect x="10" y="13" width="2" height="1" fill="#99a0af"/><rect x="12" y="13" width="1" height="1" fill="#4d515b"/><rect x="3" y="14" width="1" height="1" fill="#4d515b"/><rect x="4" y="14" width="8" height="1" fill="#7c8290"/><rect x="12" y="14" width="1" height="1" fill="#4d515b"/><rect x="3" y="15" width="1" height="1" fill="#4d515b"/><rect x="4" y="15" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="15" width="3" height="1" fill="#ccd1db"/><rect x="8" y="15" width="2" height="1" fill="#b4bac6"/><rect x="10" y="15" width="2" height="1" fill="#99a0af"/><rect x="12" y="15" width="1" height="1" fill="#4d515b"/><rect x="3" y="16" width="1" height="1" fill="#4d515b"/><rect x="4" y="16" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="16" width="3" height="1" fill="#ccd1db"/><rect x="8" y="16" width="2" height="1" fill="#b4bac6"/><rect x="10" y="16" width="2" height="1" fill="#99a0af"/><rect x="12" y="16" width="1" height="1" fill="#4d515b"/><rect x="3" y="17" width="1" height="1" fill="#4d515b"/><rect x="4" y="17" width="8" height="1" fill="#7c8290"/><rect x="12" y="17" width="1" height="1" fill="#4d515b"/><rect x="3" y="18" width="1" height="1" fill="#4d515b"/><rect x="4" y="18" width="1" height="1" fill="#e4e8ef"/><rect x="5" y="18" width="3" height="1" fill="#ccd1db"/><rect x="8" y="18" width="2" height="1" fill="#b4bac6"/><rect x="10" y="18" width="2" height="1" fill="#99a0af"/><rect x="12" y="18" width="1" height="1" fill="#4d515b"/><rect x="2" y="19" width="1" height="1" fill="#4d515b"/><rect x="3" y="19" width="2" height="1" fill="#e4e8ef"/><rect x="5" y="19" width="3" height="1" fill="#ccd1db"/><rect x="8" y="19" width="2" height="1" fill="#b4bac6"/><rect x="10" y="19" width="3" height="1" fill="#99a0af"/><rect x="13" y="19" width="1" height="1" fill="#4d515b"/><rect x="2" y="20" width="12" height="1" fill="#4d515b"/>'
    "</svg></div>"
)
