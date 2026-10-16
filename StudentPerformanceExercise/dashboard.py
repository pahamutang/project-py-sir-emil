
import html
import json

import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon=":material/school:",
    layout="centered"
)

API_URL = "http://127.0.0.1:5000/predict"

# ---------------------------------------------------------------------------
# Design layer (glassmorphism) - styling and presentation helpers only
# ---------------------------------------------------------------------------

ICONS = {
    "cap": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 1.2 2.7 3 6 3s6-1.8 6-3v-5"/><path d="M22 10v6"/>',
    "server": '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/>',
    "window": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/>',
    "tree": '<circle cx="12" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/><path d="M12 7v4M12 11 6 17M12 11l6 6"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 3 3 5-6"/>',
    "cross": '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "alert": '<path d="M10.3 3.9 2.4 17.5A2 2 0 0 0 4.1 20.5h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "plug": '<path d="M9 2v6M15 2v6"/><path d="M6 8h12v4a6 6 0 0 1-12 0V8z"/><path d="M12 18v4"/>',
    "braces": '<path d="M8 3H7a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1M16 3h1a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v4a2 2 0 0 1-2 2h-1"/>',
}


def icon(name, size=20):
    return (
        f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Sora:wght@600;700&display=swap');

:root {
    --ink: #eaf1f7;
    --ink-soft: rgba(226, 236, 246, 0.68);
    --ink-faint: rgba(226, 236, 246, 0.44);
    --glass: rgba(255, 255, 255, 0.07);
    --glass-strong: rgba(255, 255, 255, 0.11);
    --glass-edge: rgba(255, 255, 255, 0.16);
    --well: rgba(6, 12, 24, 0.42);
    --teal: #36d7c3;
    --amber: #f4b36a;
    --pass: #4fe3a4;
    --fail: #ff7a8c;
    --mono: 'IBM Plex Mono', ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace;
    --sans: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
    --display: 'Sora', 'IBM Plex Sans', system-ui, sans-serif;
}

/* Backdrop: deep ink with soft colour fields and a faint engineering grid */
.stApp {
    background:
        radial-gradient(620px 460px at 12% 8%, rgba(54, 215, 195, 0.34), transparent 70%),
        radial-gradient(560px 440px at 92% 22%, rgba(244, 179, 106, 0.26), transparent 70%),
        radial-gradient(700px 520px at 70% 96%, rgba(70, 110, 255, 0.30), transparent 70%),
        radial-gradient(500px 400px at 4% 90%, rgba(255, 122, 140, 0.16), transparent 70%),
        #0a1020;
    background-attachment: fixed;
    color: var(--ink);
    font-family: var(--sans);
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: radial-gradient(ellipse at 50% 30%, #000 20%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse at 50% 30%, #000 20%, transparent 75%);
}

header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], footer, #MainMenu { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 2.6rem; padding-bottom: 3rem; }

/* Base text */
.stApp p, .stApp span, .stApp label, .stApp li { font-family: var(--sans); }
.stApp [data-testid="stMarkdownContainer"] p { color: var(--ink-soft); }
hr { border-color: rgba(255,255,255,0.12) !important; margin: 1.6rem 0 !important; }
.ic { flex: none; display: block; }

/* Glass surface */
.glass, [data-testid="stForm"] {
    background: linear-gradient(145deg, var(--glass-strong), var(--glass));
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    backdrop-filter: blur(24px) saturate(150%);
    border: 1px solid var(--glass-edge);
    border-radius: 22px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.22),
        inset 0 -1px 0 rgba(255,255,255,0.04),
        0 24px 60px -18px rgba(0,0,0,0.55);
}

/* Header block */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; flex-wrap: wrap; padding: 10px 14px; margin-bottom: 18px;
    border-radius: 16px;
}
.dots { display: flex; gap: 7px; }
.dots i { width: 11px; height: 11px; border-radius: 50%; background: rgba(255,255,255,0.22); display: block; }
.endpoint {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--mono); font-size: 0.8rem; color: var(--ink-soft);
    background: var(--well); border: 1px solid rgba(255,255,255,0.10);
    padding: 5px 11px; border-radius: 10px;
}
.endpoint b { color: var(--amber); font-weight: 500; }
.hero { display: flex; gap: 18px; align-items: center; margin: 6px 2px 4px; }
.hero-mark {
    width: 58px; height: 58px; border-radius: 17px; flex: none;
    display: grid; place-items: center; color: #06231f;
    background: linear-gradient(145deg, #7ff0e0, var(--teal));
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.55), 0 12px 30px -8px rgba(54,215,195,0.55);
}
.hero h1 {
    font-family: var(--display); font-weight: 700; font-size: 2rem; line-height: 1.12;
    letter-spacing: -0.02em; margin: 0; padding: 0; color: var(--ink);
}
.hero p { margin: 6px 0 0; color: var(--ink-soft); font-size: 0.98rem; }

/* Stack pipeline */
.pipeline { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 18px 2px 4px; }
.node {
    display: inline-flex; align-items: center; gap: 8px; padding: 7px 12px;
    font-family: var(--mono); font-size: 0.78rem; color: var(--ink);
    background: var(--glass); border: 1px solid var(--glass-edge); border-radius: 11px;
}
.node .ic { color: var(--teal); }
.link { width: 22px; height: 1px; background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.45)); }

/* Form */
[data-testid="stForm"] { padding: 1.5rem 1.6rem 1.4rem; margin-top: 1.4rem; }
.sect { display: flex; align-items: center; gap: 10px; margin: 0 0 6px; }
.sect .ic { color: var(--amber); }
.sect h3 { font-family: var(--display); font-size: 1.12rem; font-weight: 600; margin: 0; padding: 0; color: var(--ink); letter-spacing: -0.01em; }

[data-testid="stWidgetLabel"] p {
    color: var(--ink-soft) !important; font-size: 0.88rem; font-weight: 500;
}
[data-testid="stNumberInputContainer"],
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="base-input"] {
    background: var(--well) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 13px !important;
    overflow: hidden;
}
[data-testid="stNumberInputContainer"]:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(54,215,195,0.22);
}
[data-testid="stNumberInput"] input {
    color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important;
    font-family: var(--mono) !important; font-size: 1rem; background: transparent !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.06) !important; color: var(--ink-soft) !important;
    border: 0 !important;
}
[data-testid="stNumberInput"] button:hover { background: rgba(255,255,255,0.14) !important; color: var(--ink) !important; }

[data-testid="stFormSubmitButton"] button {
    width: 100%; height: 3rem; border-radius: 14px; margin-top: 6px;
    font-family: var(--sans); font-weight: 600; letter-spacing: 0.01em;
    color: #04221e !important;
    background: linear-gradient(135deg, #8af3e4, var(--teal)) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), 0 14px 30px -10px rgba(54,215,195,0.6);
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
}
[data-testid="stFormSubmitButton"] button p { color: #04221e !important; font-weight: 600; }
[data-testid="stFormSubmitButton"] button:hover { transform: translateY(-1px); filter: brightness(1.06); }
[data-testid="stFormSubmitButton"] button:active { transform: translateY(0); }
[data-testid="stFormSubmitButton"] button:focus-visible { outline: 2px solid #fff; outline-offset: 3px; }

/* Result */
.result { padding: 1.4rem 1.5rem; margin-top: 1.6rem; }
.result-head { display: flex; align-items: center; gap: 14px; }
.badge {
    width: 50px; height: 50px; border-radius: 15px; display: grid; place-items: center; flex: none;
}
.result.pass .badge { color: var(--pass); background: rgba(79,227,164,0.14); border: 1px solid rgba(79,227,164,0.4); }
.result.fail .badge { color: var(--fail); background: rgba(255,122,140,0.14); border: 1px solid rgba(255,122,140,0.4); }
.result .result-title { font-family: var(--display); font-size: 1.5rem !important; font-weight: 700; letter-spacing: -0.01em; margin: 0; padding: 0; }
.result.pass .result-title { color: var(--pass) !important; }
.result.fail .result-title { color: var(--fail) !important; }
.result .result-sub { color: var(--ink-faint) !important; font-size: 0.82rem !important; margin: 2px 0 0; font-family: var(--mono); }
.status {
    margin-left: auto; font-family: var(--mono); font-size: 0.76rem; color: var(--ink-soft);
    background: var(--well); border: 1px solid rgba(255,255,255,0.10); border-radius: 9px; padding: 4px 9px;
}
.metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 18px 0 14px; }
.metric {
    display: flex; align-items: center; gap: 12px; padding: 13px 14px; border-radius: 15px;
    background: var(--well); border: 1px solid rgba(255,255,255,0.09);
}
.metric .ic { color: var(--teal); }
.metric small { display: block; color: var(--ink-faint); font-size: 0.78rem; }
.metric strong { font-family: var(--mono); font-weight: 500; font-size: 1.2rem; color: var(--ink); }
.payload {
    margin: 0; padding: 13px 15px; border-radius: 14px; background: var(--well);
    border: 1px solid rgba(255,255,255,0.09); color: var(--ink-soft);
    font-family: var(--mono); font-size: 0.8rem; line-height: 1.6; overflow-x: auto; white-space: nowrap;
}
.result .payload-label { font-size: 0.8rem !important; display: flex; align-items: center; gap: 8px; color: var(--ink-faint); font-size: 0.8rem; margin: 0 0 8px; }
.note, .alert {
    display: flex; gap: 11px; align-items: flex-start; margin-top: 14px; padding: 12px 14px;
    border-radius: 14px; font-size: 0.9rem; line-height: 1.5;
}
.note { color: var(--ink-soft); background: rgba(244,179,106,0.09); border: 1px solid rgba(244,179,106,0.28); }
.note .ic { color: var(--amber); margin-top: 2px; }
.alert { color: #ffd9de; background: rgba(255,122,140,0.11); border: 1px solid rgba(255,122,140,0.38); margin-top: 1.6rem; }
.alert .ic { color: var(--fail); margin-top: 2px; }

.foot { display: flex; gap: 10px; align-items: flex-start; color: var(--ink-faint); font-size: 0.82rem; line-height: 1.5; padding: 0 4px; }
.foot .ic { margin-top: 2px; }

@media (max-width: 640px) {
    .hero h1 { font-size: 1.5rem; }
    .hero-mark { width: 48px; height: 48px; }
    .link { display: none; }
    .metrics { grid-template-columns: 1fr; }
    .status { margin-left: 0; }
    .result-head { flex-wrap: wrap; }
    [data-testid="stForm"] { padding: 1.1rem; }
}
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


def render(markup):
    st.markdown(markup.replace("\n", ""), unsafe_allow_html=True)


def show_error(message):
    render(
        f'<div class="alert glass">{icon("alert", 20)}'
        f'<div>{html.escape(str(message))}</div></div>'
    )


# Dashboard heading
render(
    f'<div class="topbar glass">'
    f'<div class="dots"><i></i><i></i><i></i></div>'
    f'<div class="endpoint">{icon("server", 15)}<b>POST</b> {html.escape(API_URL.replace("http://", ""))}</div>'
    f'</div>'
    f'<div class="hero">'
    f'<div class="hero-mark">{icon("cap", 28)}</div>'
    f'<div><h1>Student Performance Prediction</h1>'
    f'<p>Enter the student\'s information below to predict their academic performance.</p></div>'
    f'</div>'
    f'<div class="pipeline">'
    f'<span class="node">{icon("window", 15)}Streamlit UI</span><span class="link"></span>'
    f'<span class="node">{icon("server", 15)}Flask API</span><span class="link"></span>'
    f'<span class="node">{icon("tree", 15)}Decision tree</span>'
    f'</div>'
)

# Student input form
with st.form("prediction_form"):
    render(f'<div class="sect">{icon("sliders", 20)}<h3>Student Information</h3></div>')

    study_hours = st.number_input(
        "Study Hours per Day",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5
    )

    attendance = st.number_input(
        "Attendance Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=1.0
    )

    submitted = st.form_submit_button(
        "Predict Student Performance",
        use_container_width=True
    )

# Send inputs to Flask API
if submitted:
    payload = {
        "study_hours": study_hours,
        "attendance_percentage": attendance
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        if response.ok:
            result = response.json()

            is_pass = result["prediction"] == "Pass"
            state = "pass" if is_pass else "fail"
            label = "PASS" if is_pass else "FAIL"
            raw = json.dumps(result, indent=2)
            sent = json.dumps(payload, indent=2)

            body = (
                html.escape(sent + "\n\n" + raw)
                .replace("  ", "&nbsp;&nbsp;")
                .replace("\n", "<br>")
            )

            render(
                f'<div class="result glass {state}">'
                f'<div class="result-head">'
                f'<div class="badge">{icon("check" if is_pass else "cross", 28)}</div>'
                f'<div><p class="result-title">Prediction: {label}</p>'
                f'<p class="result-sub">Prediction Result</p></div>'
                f'<span class="status">{response.status_code} {html.escape(response.reason or "")}</span>'
                f'</div>'
                f'<div class="metrics">'
                f'<div class="metric">{icon("clock", 22)}<div><small>Study Hours</small>'
                f'<strong>{result["study_hours"]:.1f} hours</strong></div></div>'
                f'<div class="metric">{icon("calendar", 22)}<div><small>Attendance</small>'
                f'<strong>{result["attendance_percentage"]:.1f}%</strong></div></div>'
                f'</div>'
                f'<p class="payload-label">{icon("braces", 16)}Request and response</p>'
                f'<div class="payload">{body}</div>'
                f'<div class="note">{icon("info", 18)}<div>{html.escape(result.get("note", ""))}</div></div>'
                f'</div>'
            )

        else:
            try:
                error_message = response.json().get(
                    "error", "The API returned an error."
                )
            except ValueError:
                error_message = "The API returned an unexpected response."

            show_error(f"Prediction failed: {error_message}")

    except requests.exceptions.ConnectionError:
        show_error(
            "Cannot connect to the Flask API. "
            "Please make sure app.py is running on port 5000."
        )

    except requests.exceptions.Timeout:
        show_error("The API took too long to respond. Please try again.")

    except requests.exceptions.RequestException as exc:
        show_error(f"Request failed: {exc}")

st.divider()

render(
    f'<div class="foot">{icon("info", 16)}<div>Note: Predictions are based on study hours only. '
    f'Attendance does not currently affect the trained model.</div></div>'
)
