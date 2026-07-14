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
.stButton > button { border-radius: 999px; border: 1px solid var(--wilos-border); background: var(--wilos-panel); color: var(--wilos-green); font-weight: 600; transition: background .15s ease, border-color .15s ease; }
.stButton > button:hover { background: #E8F1EC; border-color: var(--wilos-green); }
.stButton > button:focus-visible { outline: 2px solid var(--wilos-green); outline-offset: 2px; }
.stButton > button:active { transform: scale(0.95); }
.wilos-flow { display: grid; justify-items: center; gap: .4rem; margin: 1rem 0; }
.wilos-flow-step { width: min(100%, 680px); padding: .8rem 1rem; border: 1px solid var(--wilos-border); background: var(--wilos-panel); border-radius: 12px; }
.wilos-flow-arrow { color: var(--wilos-green); font-weight: 700; }

.st-key-wilos_chat_panel { background: var(--wilos-panel); border: 1px solid var(--wilos-border); border-radius: 12px; padding: 1.25rem 1.25rem 0.25rem; box-shadow: 0 0 0.5px rgba(0,0,0,0.14), 0 1px 1px rgba(0,0,0,0.24); }
.st-key-wilos_chat_panel [data-testid="stChatMessage"]:last-child { margin-bottom: 0; }

.st-key-wilos_hero { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 35vh; text-align: center; }
.st-key-wilos_hero [data-testid="stHorizontalBlock"], .st-key-wilos_bottom [data-testid="stHorizontalBlock"] { justify-content: center; gap: .5rem; }
.st-key-wilos_hero [data-testid="stColumn"], .st-key-wilos_bottom [data-testid="stColumn"] { width: auto !important; flex: 0 0 auto !important; }
.st-key-wilos_hero .stButton > button, .st-key-wilos_bottom .stButton > button { padding-left: 1rem; padding-right: 1rem; }

@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; gap: .3rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
  [data-testid="stColumn"] .stButton > button { padding-left: .25rem; padding-right: .25rem; font-size: .78rem; white-space: nowrap; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
'''
