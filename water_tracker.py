"""
💧 My Water Tracker  –  single-file Streamlit app (works on PC, tablet and phone)

    pip install streamlit
    streamlit run water_tracker.py

Deploying to Streamlit Cloud? Add a requirements.txt containing the single line:  streamlit
"""
from datetime import date

import streamlit as st

DEFAULT_GOAL_ML = 2000
QUICK_ADDS = [("🥛 Glass", 250), ("🍶 Small bottle", 500), ("🧴 Large bottle", 1000)]


# ------------------------------ state helpers ------------------------------
def reset_day():
    st.session_state.drinks = []          # list of ml amounts, newest last
    st.session_state.celebrated = False
    st.session_state.day = date.today()


def init_state():
    if "goal" not in st.session_state:
        st.session_state.goal = DEFAULT_GOAL_ML
    if "drinks" not in st.session_state or st.session_state.get("day") != date.today():
        reset_day()                       # new browser session or a new calendar day


def add_water(ml):
    st.session_state.drinks.append(int(ml))


def add_custom():
    add_water(st.session_state.custom_ml)


def undo_last():
    if st.session_state.drinks:
        st.session_state.drinks.pop()
        st.session_state.celebrated = sum(st.session_state.drinks) >= st.session_state.goal


def set_goal():
    st.session_state.goal = int(st.session_state.goal_input)


def fmt(ml):
    """1250 -> '1.25 L', 800 -> '800 ml'"""
    return f"{ml / 1000:.2f} L".replace(".00 L", " L") if ml >= 1000 else f"{ml:.0f} ml"


def message(pct):
    if pct >= 100:
        return "success", "🎉 Goal reached! Fantastic work – your body says thank you! 💙"
    if pct >= 75:
        return "info", "🌊 Almost there! Just a few more sips to reach your goal."
    if pct >= 50:
        return "info", "💪 Halfway and beyond – keep it flowing!"
    if pct >= 25:
        return "info", "🙂 Nice start! Keep a bottle close and sip regularly."
    return "info", "💧 Let's begin! Have your first glass of water now."


def bottle_svg(pct):
    """Animated glass that fills up with the progress."""
    p = max(0.0, min(pct, 100.0)) / 100
    top, bottom = 22, 186
    y = bottom - (bottom - top) * p
    color = "#2fbf71" if pct >= 100 else "#3d9bff"
    return f"""
<svg viewBox="0 0 120 210" class="glass" role="img" aria-label="Water level {pct:.0f} percent">
  <defs>
    <clipPath id="cut"><polygon points="16,{top} 104,{top} 90,{bottom} 30,{bottom}"/></clipPath>
    <linearGradient id="w" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{color}" stop-opacity=".75"/><stop offset="1" stop-color="{color}"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#cut)">
    <rect x="0" y="{y:.1f}" width="120" height="{210 - y:.1f}" fill="url(#w)" class="level"/>
    <path class="wave" fill="{color}" opacity=".55"
          d="M-60 {y:.1f} q15 -9 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 V{bottom + 10} H-60Z"/>
  </g>
  <polygon points="16,{top} 104,{top} 90,{bottom} 30,{bottom}" fill="none" stroke="#7fb4e8" stroke-width="4" stroke-linejoin="round"/>
  <text x="60" y="112" text-anchor="middle" class="pct">{pct:.0f}%</text>
</svg>"""


CSS = """
<style>
.stApp{background:linear-gradient(170deg,#e8f4ff 0%,#f7fbff 45%,#e9fbf3 100%)}
.block-container{max-width:760px;padding-top:1.4rem}
.hero{background:linear-gradient(90deg,#3d9bff,#4fd1c5);color:#fff;border-radius:22px;padding:18px 22px;text-align:center;margin-bottom:14px}
.hero h1{margin:0;font-size:clamp(1.6rem,6vw,2.3rem);color:#fff}.hero p{margin:4px 0 0;opacity:.95}
.glass{width:100%;max-width:210px;display:block;margin:0 auto}
.glass .pct{font-size:24px;font-weight:800;fill:#1b3a63;paint-order:stroke;stroke:#ffffffcc;stroke-width:4px}
.glass .level{transition:all .6s}.glass .wave{animation:wave 3.2s linear infinite}
@keyframes wave{to{transform:translateX(60px)}}
.stat{background:#fff;border-radius:18px;padding:14px 8px;text-align:center;box-shadow:0 4px 14px rgba(61,155,255,.15)}
.stat b{display:block;font-size:clamp(1.2rem,5vw,1.7rem);color:#1b3a63}.stat span{color:#6a7f99;font-size:.85rem}
div.stButton>button{width:100%;border-radius:16px;padding:.7rem .4rem;font-weight:700;border:2px solid #cfe5ff;background:#fff;color:#1b3a63}
div.stButton>button:hover{border-color:#3d9bff;color:#3d9bff}
div.stButton>button:active{transform:scale(.97)}
</style>"""


# ---------------------------------- app ----------------------------------
def main():
    st.set_page_config(page_title="My Water Tracker", page_icon="💧", layout="centered")
    st.markdown(CSS, unsafe_allow_html=True)
    init_state()
    goal = st.session_state.goal
    total = sum(st.session_state.drinks)
    remaining = max(goal - total, 0)
    pct = total / goal * 100

    st.markdown(f'<div class="hero"><h1>💧 My Water Tracker</h1><p>Daily goal: <b>{fmt(goal)}</b> &nbsp;•&nbsp; {date.today():%A, %d %B}</p></div>',
                unsafe_allow_html=True)

    # Visual indicator + numbers
    st.markdown(bottle_svg(pct), unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.markdown(f'<div class="stat"><b>{fmt(total)}</b><span>Drunk today</span></div>', unsafe_allow_html=True)
    b.markdown(f'<div class="stat"><b>{fmt(remaining)}</b><span>Still to go</span></div>', unsafe_allow_html=True)
    c.markdown(f'<div class="stat"><b>{len(st.session_state.drinks)}</b><span>Drinks logged</span></div>', unsafe_allow_html=True)
    st.progress(min(pct / 100, 1.0), text=f"{min(pct, 100):.0f}% of your daily goal")

    # Encouraging message
    kind, text = message(pct)
    (st.success if kind == "success" else st.info)(text)
    if pct >= 100 and not st.session_state.celebrated:
        st.balloons()
        st.session_state.celebrated = True
    if pct > 150:
        st.warning("You are well past your goal. Great, but listen to your body and don't overdo it.")

    # Add water
    st.subheader("➕ Add water")
    cols = st.columns(len(QUICK_ADDS))
    for col, (label, ml) in zip(cols, QUICK_ADDS):
        col.button(f"{label}\n{ml} ml", key=f"add{ml}", on_click=add_water, args=(ml,))
    x, y = st.columns([2, 1])
    x.number_input("Custom amount (ml)", 50, 2000, 150, 50, key="custom_ml")
    y.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
    y.button("Add", key="add_custom", on_click=add_custom)

    # Bonus: custom goal, undo, reset
    with st.expander("⚙️ Settings: goal, undo and reset", expanded=False):
        st.number_input("Daily goal (ml)", 500, 6000, st.session_state.goal, 250,
                        key="goal_input", on_change=set_goal,
                        help="Typical advice is about 2000 ml a day, but needs vary.")
        u, r = st.columns(2)
        u.button("↩️ Undo last drink", on_click=undo_last, disabled=not st.session_state.drinks)
        r.button("🔄 Reset today", on_click=reset_day)

    if st.session_state.drinks:
        with st.expander("📜 Today's drinks"):
            for i, ml in enumerate(reversed(st.session_state.drinks), 1):
                st.write(f"{len(st.session_state.drinks) - i + 1}. 💧 {ml} ml")
    st.caption("Tip: your progress is kept while this page stays open and resets on a new day.")


if __name__ == "__main__":
    main()
