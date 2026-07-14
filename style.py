STYLE = r'''
<style>
:root {
  --wilos-green: #00754A;
  --wilos-ink: #1A1712;
  --wilos-muted: #6B665F;
  --wilos-paper: #F2F0EB;
  --wilos-panel: #FFFFFF;
  --wilos-border: #D8D3CA;
}

.block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 7rem; }
.wilos-title { font-size: clamp(2.8rem, 9vw, 5rem); font-weight: 750; letter-spacing: -0.06em; text-align: center; color: var(--wilos-ink); margin-top: 8vh; }
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
.wilos-flow { display: grid; justify-items: center; gap: .4rem; margin: 1rem 0; }
.wilos-flow-step { width: min(100%, 680px); padding: .8rem 1rem; border: 1px solid var(--wilos-border); background: var(--wilos-panel); border-radius: 12px; }
.wilos-flow-arrow { color: var(--wilos-green); font-weight: 700; }
@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; gap: .3rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
  [data-testid="stColumn"] .stButton > button { padding-left: .25rem; padding-right: .25rem; font-size: .78rem; white-space: nowrap; }
}
</style>
'''
