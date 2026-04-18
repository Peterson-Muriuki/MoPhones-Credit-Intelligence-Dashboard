"""
MoPhones Credit Intelligence Dashboard  v2
==========================================
• Warm blue/orange gradient card palette
• AI Insights via Ollama (Mistral) — local, no API key needed
• Case Study Q1/Q2/Q3 answer cards on every relevant page
• Full AI Analyst page with prompt library + custom questions
• streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, warnings, zipfile, io, requests
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MoPhones · Credit Intelligence",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header  { visibility: hidden; }
.block-container { padding: 1rem 2rem 3rem; max-width: 1440px; }

/* ══ KPI cards with gradient borders ══ */
.kpi-outer { border-radius: 14px; padding: 2px; margin-bottom: 4px; }
.kpi-outer.danger  { background: linear-gradient(135deg,#FF4D4D 0%,#FF8C00 100%); }
.kpi-outer.warning { background: linear-gradient(135deg,#F59E0B 0%,#FB923C 100%); }
.kpi-outer.ok      { background: linear-gradient(135deg,#10B981 0%,#0EA5E9 100%); }
.kpi-outer.info    { background: linear-gradient(135deg,#3B82F6 0%,#6366F1 100%); }
.kpi-outer.neutral { background: linear-gradient(135deg,#334155 0%,#475569 100%); }
.kpi-inner { background: #0F172A; border-radius: 12px; padding: 18px 20px 14px; }
.kpi-label { font-size: 10px; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: #475569; margin-bottom: 4px; }
.kpi-value { font-size: 32px; font-weight: 800; line-height: 1.05; }
.kpi-value.danger  { background: linear-gradient(135deg,#FF6B6B,#FF8C00);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.kpi-value.warning { background: linear-gradient(135deg,#FCD34D,#FB923C);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.kpi-value.ok      { background: linear-gradient(135deg,#34D399,#0EA5E9);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.kpi-value.info    { background: linear-gradient(135deg,#60A5FA,#A78BFA);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.kpi-value.neutral { color: #94A3B8; }
.kpi-delta { font-size: 11px; margin-top: 6px; font-family: 'DM Mono', monospace; }
.kpi-delta.up   { color: #FF6B6B; }
.kpi-delta.down { color: #34D399; }
.kpi-delta.neutral { color: #475569; }

/* ══ Case Study cards ══ */
.cs-card { border-radius: 12px; padding: 20px 22px; margin: 10px 0;
  border-left: 4px solid; background: #0C1220; }
.cs-card.q1 { border-color: #3B82F6; }
.cs-card.q2 { border-color: #F59E0B; }
.cs-card.q3 { border-color: #10B981; }
.cs-tag { display:inline-block; font-size:9px; font-weight:800;
  letter-spacing:.1em; text-transform:uppercase;
  padding:3px 9px; border-radius:20px; margin-bottom:8px; }
.cs-tag.q1 { background:rgba(59,130,246,.12); color:#60A5FA; }
.cs-tag.q2 { background:rgba(245,158,11,.12);  color:#FCD34D; }
.cs-tag.q3 { background:rgba(16,185,129,.12);  color:#34D399; }
.cs-title { font-size:14px; font-weight:700; color:#E2E8F0; margin-bottom:8px; }
.cs-body  { font-size:12px; color:#94A3B8; line-height:1.75; }
.cs-body b { color:#CBD5E1; }
.cs-finding { background:rgba(255,255,255,.03); border-radius:8px;
  padding:10px 14px; margin-top:10px; font-size:11px; color:#64748B;
  border-top:1px solid rgba(255,255,255,.05); }
.cs-finding strong { color:#F59E0B; }

/* ══ AI panel ══ */
.ai-wrap { background: linear-gradient(135deg,#070F20,#0C1525);
  border:1px solid rgba(59,130,246,.2); border-radius:14px;
  padding:18px 22px; margin:10px 0;
  box-shadow: 0 0 48px rgba(59,130,246,.05); }
.ai-header { display:flex; align-items:center; gap:10px; margin-bottom:12px; }
.ai-dot { width:8px; height:8px; border-radius:50%; background:#3B82F6;
  box-shadow:0 0 8px #3B82F6; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }
.ai-lbl { font-size:11px; font-weight:800; color:#60A5FA;
  letter-spacing:.08em; text-transform:uppercase; }
.ai-mdl { font-size:9px; color:#1E3A5F; margin-left:auto;
  font-family:'DM Mono',monospace; }
.ai-q   { font-size:11px; color:#1E40AF; font-style:italic; margin-bottom:4px; }
.ai-txt { font-size:12.5px; color:#CBD5E1; line-height:1.85; }
.ai-txt b, .ai-txt strong { color:#FCD34D; }

/* ══ Section headers ══ */
.sh { display:flex; align-items:center; gap:10px;
  margin:26px 0 12px; padding-bottom:9px;
  border-bottom:1px solid rgba(255,255,255,.05); }
.sh-icon { font-size:16px; }
.sh-title { font-size:10.5px; font-weight:800; color:#64748B;
  text-transform:uppercase; letter-spacing:.1em; }
.sh-badge { font-size:9px; font-weight:700; color:#1E293B;
  background:#0F172A; padding:3px 8px; border-radius:4px; }

/* ══ Alerts ══ */
.al { border-radius:8px; padding:11px 15px; font-size:12px;
  line-height:1.65; margin:10px 0; border-left:3px solid; }
.al-red   { background:#1A0808; border-color:#EF4444; color:#FCA5A5; }
.al-amber { background:#1A1200; border-color:#F59E0B; color:#FDE68A; }
.al-blue  { background:#07101F; border-color:#3B82F6; color:#93C5FD; }
.al-green { background:#061410; border-color:#10B981; color:#6EE7B7; }

/* ══ Rec cards ══ */
.rc { background:#0C1220; border-radius:10px; padding:15px 18px;
  margin:6px 0; border:1px solid rgba(255,255,255,.04); }
.rc h4 { font-size:12px; font-weight:700; color:#FCD34D; margin:0 0 5px; }
.rc p  { font-size:11px; color:#475569; margin:0; line-height:1.6; }
.rc .imp { font-size:10px; color:#34D399; font-weight:600; margin-top:7px; }

/* ══ Sidebar ══ */
section[data-testid="stSidebar"] {
  background:#060C18 !important;
  border-right:1px solid rgba(255,255,255,.04); }
.sb-brand { padding:18px 14px 10px;
  border-bottom:1px solid rgba(255,255,255,.05); margin-bottom:14px; }
.sb-brand h1 { font-size:20px; font-weight:900; color:#F59E0B;
  margin:0; letter-spacing:-1px; }
.sb-brand p  { font-size:10px; color:#1E293B; margin:2px 0 0; }

.divider { height:1px; background:rgba(255,255,255,.05); margin:22px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#475569", size=11),
    margin=dict(l=8,r=8,t=40,b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)",bordercolor="rgba(0,0,0,0)",font=dict(size=10)),
    xaxis=dict(gridcolor="rgba(255,255,255,.04)",zerolinecolor="rgba(255,255,255,.07)",linecolor="rgba(255,255,255,.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,.04)",zerolinecolor="rgba(255,255,255,.07)",linecolor="rgba(255,255,255,.04)"),
)
def T(fig, title="", h=310):
    fig.update_layout(**_BASE, height=h,
        title=dict(text=title,font=dict(size=12,color="#94A3B8"),x=0.01,y=0.97))
    return fig

P = dict(
    blue="#3B82F6", orange="#F59E0B", red="#EF4444",
    green="#10B981", purple="#8B5CF6", cyan="#06B6D4",
    rose="#F43F5E", amber="#FB923C",
)
SCOL = {
    "Active":"#10B981","PAR 7":"#F59E0B","PAR 30":"#EF4444",
    "FPD":"#DC2626","FMD":"#7C3AED","Inactive":"#475569",
    "Return":"#1E3A5F","Paid Off":"#3B82F6","Unknown":"#1E293B",
}

# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def kpi(val, label, delta=None, kind="info"):
    dh = ""
    if delta:
        d,t = delta
        dh = f'<div class="kpi-delta {d}">{t}</div>'
    st.markdown(f"""<div class="kpi-outer {kind}"><div class="kpi-inner">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {kind}">{val}</div>{dh}
    </div></div>""", unsafe_allow_html=True)

def sh(icon, title, badge=""):
    b = f'<span class="sh-badge">{badge}</span>' if badge else ""
    st.markdown(f'<div class="sh"><span class="sh-icon">{icon}</span>'
                f'<span class="sh-title">{title}</span>{b}</div>',
                unsafe_allow_html=True)

def al(text, kind="blue"):
    st.markdown(f'<div class="al al-{kind}">{text}</div>', unsafe_allow_html=True)

def div():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def cs(q, tag, title, body, finding):
    st.markdown(f"""<div class="cs-card {q}">
      <span class="cs-tag {q}">{tag}</span>
      <div class="cs-title">{title}</div>
      <div class="cs-body">{body}</div>
      <div class="cs-finding"><strong>Key finding:</strong> {finding}</div>
    </div>""", unsafe_allow_html=True)

def rc(title, body, impact):
    st.markdown(f"""<div class="rc">
      <h4>★ {title}</h4><p>{body}</p>
      <div class="imp">↗ {impact}</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# OLLAMA / MISTRAL
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA = "http://localhost:11434/api/generate"

def ollama_ok():
    try:
        return requests.get("http://localhost:11434/api/tags", timeout=2).status_code == 200
    except Exception:
        return False

def mistral(prompt: str, context: str) -> str:
    system = (
        "You are a senior credit analyst specialising in African fintech and PAYG device financing. "
        "Analyse MoPhones portfolio data and give concise, actionable insights. "
        "Respond in 3-5 bullet points. Each bullet starts with a bold keyword. "
        "Be direct — no fluff. Use plain language a CCO can follow."
    )
    try:
        r = requests.post(OLLAMA, json={
            "model": "mistral",
            "prompt": f"{system}\n\nPortfolio data:\n{context}\n\nQuestion: {prompt}",
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 450},
        }, timeout=90)
        return r.json().get("response","No response.") if r.status_code==200 \
               else f"Ollama error {r.status_code}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot reach Ollama — run `ollama serve` in a terminal."
    except Exception as e:
        return f"⚠️ Error: {e}"

def ai_block(prompt: str, ctx: str, key: str):
    ok = ollama_ok()
    dot_col = "#10B981" if ok else "#EF4444"
    status  = "mistral · online" if ok else "offline — run: ollama serve"
    st.markdown(f"""<div class="ai-wrap">
      <div class="ai-header">
        <div class="ai-dot" style="background:{dot_col};box-shadow:0 0 8px {dot_col}"></div>
        <span class="ai-lbl">🤖 AI Analyst — Mistral</span>
        <span class="ai-mdl">{status}</span>
      </div>
      <div class="ai-q">"{prompt}"</div>
    </div>""", unsafe_allow_html=True)

    bc, _ = st.columns([2,8])
    with bc:
        clicked = st.button("Generate Insight", key=f"b_{key}",
                            disabled=not ok, type="primary")
    sk = f"r_{key}"
    if sk not in st.session_state:
        st.session_state[sk] = ""
    if clicked:
        with st.spinner("Mistral is thinking…"):
            st.session_state[sk] = mistral(prompt, ctx)
    if st.session_state[sk]:
        html = st.session_state[sk].replace("\n","<br>")
        st.markdown(f"""<div class="ai-wrap" style="margin-top:-6px;border-top-left-radius:0;
          border-top-right-radius:0;padding-top:12px">
          <div class="ai-txt">{html}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
SNAP_FILES = {
    "Jan-25": ("Credit Data/Credit Data - 01-01-2025.csv", "2025-01-01"),
    "Mar-25": ("Credit Data/Credit Data - 30-03-2025.csv", "2025-03-31"),
    "Jun-25": ("Credit Data/Credit Data - 30-06-2025.csv", "2025-06-30"),
    "Sep-25": ("Credit Data/Credit Data - 30-09-2025.csv", "2025-09-30"),
    "Dec-25": ("Credit Data/Credit Data - 30-12-2025.csv", "2025-12-31"),
}

def _csv(fname):
    for p in [fname, os.path.basename(fname),
              os.path.join("Credit Data", os.path.basename(fname))]:
        if os.path.exists(p):
            return pd.read_csv(p)
    if os.path.exists("Credit Data.zip"):
        with zipfile.ZipFile("Credit Data.zip") as z:
            m = [n for n in z.namelist() if os.path.basename(fname) in n]
            if m: return pd.read_csv(io.BytesIO(z.read(m[0])))
    return None

def _xl(sheet, n=60000):
    for p in ["Sales and Customer Data.xlsx","Sales and Customer Data.zip"]:
        if not os.path.exists(p): continue
        if p.endswith(".zip"):
            with zipfile.ZipFile(p) as z:
                xl = [x for x in z.namelist() if x.endswith(".xlsx")][0]
                return pd.read_excel(io.BytesIO(z.read(xl)),sheet_name=sheet,nrows=n).dropna(how="all")
        return pd.read_excel(p,sheet_name=sheet,nrows=n).dropna(how="all")
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_all():
    # Credit snapshots
    snaps = {}
    for period,(fname,date) in SNAP_FILES.items():
        df = _csv(fname)
        if df is not None:
            df["period"] = period
            df["snap_date"] = pd.Timestamp(date)
            snaps[period] = df

    # Demographics
    gender = _xl("Gender",55000)
    dob    = _xl("DOB",60000)
    income = _xl("Income Level",25000)

    if not gender.empty: gender = gender[gender["Loan Id"].notna()].drop_duplicates("Loan Id")
    if not dob.empty:    dob = (dob[dob["Loan Id "].notna()]
                                .drop_duplicates("Loan Id ")
                                .rename(columns={"Loan Id ":"Loan Id"}))
    if not income.empty: income = income[income["Loan Id"].notna()].drop_duplicates("Loan Id")

    cust = gender.copy() if not gender.empty else pd.DataFrame()
    if not cust.empty and not dob.empty:
        cust = cust.merge(dob[["Loan Id","date_of_birth"]],on="Loan Id",how="left")
    if not cust.empty and not income.empty:
        cust = cust.merge(income,on="Loan Id",how="left")

    if not cust.empty and "date_of_birth" in cust.columns:
        REF = pd.Timestamp("2025-12-31")
        cust["DOB"] = pd.to_datetime(cust["date_of_birth"],utc=True,errors="coerce").dt.tz_localize(None)
        cust["age"] = ((REF-cust["DOB"]).dt.days/365.25).round(1)
        cust["age_band"] = pd.cut(cust["age"],[0,18,25,35,45,55,999],
            labels=["<18","18-25","26-35","36-45","46-55","55+"]).astype(str).replace("nan","Unknown")
        if "Received" in cust.columns and "Duration" in cust.columns:
            cust["avg_monthly_income"] = cust["Received"]/cust["Duration"].replace(0,np.nan)
            cust["income_band"] = pd.cut(cust["avg_monthly_income"],
                [0,5000,10000,20000,30000,50000,100000,150000,1e9],
                labels=["<5K","5K-9.9K","10K-19.9K","20K-29.9K",
                        "30K-49.9K","50K-99.9K","100K-149.9K","150K+"]
            ).astype(str).replace("nan","Unknown")

    # NPS
    nps = pd.DataFrame()
    for p in ["NPS Data.xlsx","NPS_Data__1_.xlsx"]:
        if os.path.exists(p): nps = pd.read_excel(p); break
    if not nps.empty:
        c = list(nps.columns)
        nps = nps.rename(columns={
            c[3]:"loan_id",c[4]:"nps_score",c[5]:"reason",
            c[6]:"improvement",c[7]:"device_happy",c[8]:"service_happy",
            c[9]:"payment_delay",c[10]:"support_difficulty",c[15]:"phone_locked",
        })
        nps["nps_cat"] = nps["nps_score"].apply(
            lambda s: "Unknown" if pd.isna(s) else
                      ("Promoter" if s>=9 else ("Passive" if s>=7 else "Detractor"))
        )
    return snaps, cust, nps

# ─────────────────────────────────────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────────────────────────────────────
CLOSED = {"Paid Off","Return","Unknown"}

def compute(df):
    pool = df[~df["ACCOUNT_STATUS_L2"].isin(CLOSED)]
    n    = len(pool)
    def c(s): return (df["ACCOUNT_STATUS_L2"]==s).sum()
    par30,par7,fpd,fmd = c("PAR 30"),c("PAR 7"),c("FPD"),c("FMD")
    ret,paid,active    = c("Return"),c("Paid Off"),c("Active")
    tb = df["CLOSING_BALANCE"].sum()
    ta = df["ARREARS"].sum()
    dpd = df.loc[df["DAYS_PAST_DUE"]>0,"DAYS_PAST_DUE"]
    return dict(
        total=len(df), active=active,
        par30=par30, par30r=round(par30/n*100,1) if n else 0,
        par7=par7,   par7r=round(par7/n*100,1)  if n else 0,
        fpd=fpd,     fpdr=round(fpd/n*100,1)    if n else 0,
        fmd=fmd, ret=ret, paid=paid,
        tot_bal=tb, tot_arr=ta,
        arr_ratio=round(ta/tb*100,1) if tb else 0,
        avg_dpd=round(dpd.mean(),1)  if len(dpd) else 0,
    )

def seg_tbl(df, col):
    rows=[]
    for s,g in df.groupby(col,observed=True):
        pool = g[~g["ACCOUNT_STATUS_L2"].isin(CLOSED)]; n=len(pool)
        par30=(g["ACCOUNT_STATUS_L2"]=="PAR 30").sum()
        fpd  =(g["ACCOUNT_STATUS_L2"]=="FPD").sum()
        dpd  =g.loc[g["DAYS_PAST_DUE"]>0,"DAYS_PAST_DUE"]
        rows.append(dict(segment=s, n=n,
            par30r=round(par30/n*100,1) if n else 0,
            fpdr  =round(fpd/n*100,1)   if n else 0,
            avg_dpd=round(dpd.mean(),1) if len(dpd) else 0))
    return pd.DataFrame(rows).set_index("segment")

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Loading datasets…"):
    snaps, cust, nps = load_all()

if not snaps:
    st.error("⚠️  Credit data not found. Place Credit Data/ folder (or Credit Data.zip) next to app.py and restart.")
    st.stop()

PERIODS = list(snaps.keys())
ALL_M   = {p: compute(df) for p,df in snaps.items()}
METS    = pd.DataFrame(ALL_M).T
DEC     = snaps.get("Dec-25", snaps[PERIODS[-1]])

DEC_M = DEC.copy()
if not cust.empty and "age_band" in cust.columns:
    cols = ["Loan Id","age_band"]
    if "income_band" in cust.columns: cols.append("income_band")
    if "Gender"      in cust.columns: cols.append("Gender")
    DEC_M = DEC.merge(cust[cols], left_on="LOAN_ID", right_on="Loan Id", how="left")

NPS_C = pd.DataFrame()
if not nps.empty:
    NPS_C = nps.merge(
        DEC[["LOAN_ID","ACCOUNT_STATUS_L2","ARREARS","DAYS_PAST_DUE"]],
        left_on="loan_id", right_on="LOAN_ID", how="left"
    )

def ctx():
    m = ALL_M["Dec-25"]
    return "\n".join([
        f"Portfolio Dec-25: {m['total']:,} accounts, {m['active']:,} active.",
        f"PAR 30: {m['par30r']}% (Jan-25 was 22.9% — +10pp YTD).",
        f"FPD rate: {m['fpdr']}% (stable ~8% all year).",
        f"Arrears ratio: {m['arr_ratio']}% — KSh {m['tot_arr']/1e6:.0f}M in arrears.",
        f"Avg DPD: {m['avg_dpd']} days (Jan was 170 — +66% YTD).",
        f"Returns: {m['ret']:,} (Jan was 604 — +189%).",
        f"NPS (4,129 responses): overall +5.9. Return accounts: -46.8.",
        f"13.6% of customers locked despite on-time payment. 17.5% payment delay.",
        f"18-25 cohort: PAR30 21.3%, FPD 7.0% — both above portfolio average.",
        f"Demographic linkage: ~51% of accounts matched to demographics.",
        f"Data gaps: no monthly history, 49% linkage gap, ambiguous income fields.",
    ])

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="sb-brand">
      <h1>📱 MoPhones</h1>
      <p>Credit Intelligence · 2025</p>
    </div>""", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Overview",
        "📈  Portfolio Health",
        "👥  Segment Analysis",
        "💬  Customer Experience",
        "🔍  Data Quality",
        "⭐  Case Study Answers",
        "🤖  AI Analyst",
    ], label_visibility="collapsed")
    page = page.split("  ")[1]

    st.markdown("---")
    sel  = st.selectbox("Snapshot", PERIODS, index=len(PERIODS)-1)
    sel_m = ALL_M[sel]

    ok = ollama_ok()
    bc  = "rgba(16,185,129,.15)" if ok else "rgba(239,68,68,.1)"
    fc  = "#10B981"              if ok else "#EF4444"
    msg = "Mistral ready"        if ok else "run: ollama serve"
    st.markdown(f"""
    <div style="margin-top:14px;padding:9px 12px;background:#060C18;
                border-radius:8px;border:1px solid {bc}">
      <div style="font-size:9px;font-weight:700;color:{fc};
                  letter-spacing:.1em;text-transform:uppercase">
        {'🟢 AI Online' if ok else '🔴 AI Offline'}
      </div>
      <div style="font-size:9px;color:#1E293B;margin-top:2px">{msg}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("""<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;
      margin:16px 0 2px;letter-spacing:-1px">Credit Portfolio Intelligence</h1>
      <p style="color:#1E293B;font-size:12px;margin-bottom:14px">
      Full-year 2025 · 5 quarterly snapshots · 20,742 accounts as at Dec-25</p>""",
      unsafe_allow_html=True)

    al("⚠️ <b>PAR 30 grew +10pp YTD</b> (22.9% → 32.8%). Avg Days Past Due up 66% to 283 days. Immediate portfolio intervention is warranted.", "red")

    sh("📊","KEY METRICS", f"as at {sel}")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi(f"{sel_m['total']:,}", "Total Accounts", kind="info")
    with c2: kpi(f"{sel_m['par30r']}%", "PAR 30 Rate",
                 ("up","↑ +10pp YTD") if sel=="Dec-25" else None, kind="danger")
    with c3: kpi(f"{sel_m['fpdr']}%", "FPD Rate",
                 ("neutral","→ Stable ~8%"), kind="warning")
    with c4: kpi(f"{sel_m['arr_ratio']}%", "Arrears Ratio",
                 ("up","↑ Structurally high"), kind="danger")
    with c5: kpi(f"{int(sel_m['avg_dpd'])}d", "Avg Days Past Due",
                 ("up","↑ +66% YTD") if sel=="Dec-25" else None, kind="warning")

    div()
    sh("📉","PORTFOLIO TREND","Jan → Dec 2025")
    cl, cr = st.columns(2)

    with cl:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=PERIODS, y=METS["par30r"],
            name="PAR 30 %", mode="lines+markers",
            line=dict(color=P["orange"],width=3),
            marker=dict(size=9,color=P["orange"],line=dict(color="#0F172A",width=2)),
            text=[f"{v}%" for v in METS["par30r"]], textposition="top center",
            textfont=dict(size=9,color=P["orange"])))
        fig.add_trace(go.Scatter(x=PERIODS, y=METS["fpdr"],
            name="FPD %", mode="lines+markers",
            line=dict(color=P["blue"],width=2.5,dash="dot"),
            marker=dict(size=7,color=P["blue"],line=dict(color="#0F172A",width=2))))
        fig.add_hline(y=30, line_dash="dash", line_color=P["red"], opacity=.4,
                      annotation_text="30% threshold",annotation_font_color=P["red"],annotation_font_size=9)
        T(fig,"PAR 30 & FPD Rate Over Time")
        fig.update_layout(legend=dict(orientation="h",y=-0.22))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(x=PERIODS, y=METS["arr_ratio"],
            name="Arrears %", marker_color=P["blue"],
            marker_line=dict(color="#0F172A",width=1), opacity=.85), secondary_y=False)
        fig.add_trace(go.Scatter(x=PERIODS, y=METS["avg_dpd"],
            name="Avg DPD", mode="lines+markers",
            line=dict(color=P["orange"],width=2.5),
            marker=dict(size=8,color=P["orange"],line=dict(color="#0F172A",width=2))),
            secondary_y=True)
        fig.update_yaxes(gridcolor="rgba(255,255,255,.04)", secondary_y=False)
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", secondary_y=True)
        T(fig,"Arrears Ratio (bars) vs Avg DPD (line)")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#475569", size=11),
            margin=dict(l=8,r=8,t=40,b=8),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
                        font=dict(size=10), orientation="h", y=-0.22),
        )
        st.plotly_chart(fig, use_container_width=True)

    cl, cr = st.columns([3,2])
    ORDER = ["Active","PAR 7","PAR 30","FPD","FMD","Inactive","Return","Paid Off"]
    with cl:
        sh("📊","ACCOUNT COMPOSITION OVER TIME")
        fig = go.Figure()
        for s in ORDER:
            vals = [(snaps[p]["ACCOUNT_STATUS_L2"]==s).sum() for p in PERIODS]
            fig.add_trace(go.Bar(name=s, x=PERIODS, y=vals,
                marker_color=SCOL.get(s,"#334155"),
                marker_line=dict(color="#0F172A",width=1)))
        T(fig,"",h=300)
        fig.update_layout(barmode="stack",legend=dict(orientation="h",y=-0.28,font=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        sh("🍩","DEC-25 MIX")
        vc = DEC["ACCOUNT_STATUS_L2"].value_counts()
        fig = go.Figure(go.Pie(
            labels=vc.index, values=vc.values, hole=0.62,
            marker=dict(colors=[SCOL.get(s,"#334155") for s in vc.index],
                        line=dict(color="#0F172A",width=2)),
            textfont=dict(size=9),
            pull=[0.05 if s=="PAR 30" else 0 for s in vc.index],
        ))
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=9)),
            margin=dict(l=0,r=0,t=0,b=0),
            annotations=[dict(text="<b>20,742</b>",x=0.5,y=0.5,
                font_size=14,font_color="#E2E8F0",showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    div()
    sh("🤖","AI ANALYST","Mistral · local")
    ai_block("What are the 3 most critical actions MoPhones should take based on this portfolio data?", ctx(), "ov")

# ═══════════════════════════════════════════════════════════════════════════
# PORTFOLIO HEALTH
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Portfolio Health":
    st.markdown('<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 14px;letter-spacing:-1px">Portfolio Health Monitor</h1>', unsafe_allow_html=True)

    cs("q1","Q1 — Portfolio Health · 40%","5 Metrics to Track Credit Performance Over Time",
       """We track <b>① PAR 30 Rate</b> (30+ days overdue vs open portfolio — global standard KPI),
       <b>② FPD Rate</b> (First Payment Default — underwriting quality signal at origination),
       <b>③ Arrears Ratio</b> (total arrears ÷ closing balance — impairment depth, critical for provisioning),
       <b>④ Avg Days Past Due</b> (collection lag among delinquent accounts — higher = chronic stagnation),
       and <b>⑤ Return Rate</b> (device recoveries — double-loss events signalling CX or affordability failure).""",
       "PAR 30: 22.9%→32.8% (+10pp). Avg DPD: 170→283 days (+66%). Returns: 604→1,744 (+189%).")

    MMAP = {"PAR 30 Rate (%)":"par30r","FPD Rate (%)":"fpdr",
            "Arrears Ratio (%)":"arr_ratio","Avg Days Past Due":"avg_dpd",
            "Active Accounts":"active","Return Count":"ret","Total Accounts":"total"}
    chosen = st.multiselect("Select metrics:", list(MMAP.keys()),
                             default=["PAR 30 Rate (%)","FPD Rate (%)","Arrears Ratio (%)"])
    if chosen:
        fig = go.Figure()
        clrs=[P["orange"],P["blue"],P["red"],P["green"],P["purple"],P["cyan"],P["rose"],P["amber"]]
        for i,m in enumerate(chosen):
            vals=[ALL_M[p].get(MMAP[m],0) for p in PERIODS]
            fig.add_trace(go.Scatter(x=PERIODS, y=vals, name=m,
                mode="lines+markers",
                line=dict(width=2.5,color=clrs[i%len(clrs)]),
                marker=dict(size=8,color=clrs[i%len(clrs)],line=dict(color="#0F172A",width=2)),
                fill="tozeroy" if len(chosen)==1 else None,
                fillcolor="rgba(59,130,246,.06)" if len(chosen)==1 else None))
        T(fig,"Selected Metrics — Jan–Dec 2025",h=340)
        fig.update_layout(legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    sh("📋","STATUS ROLL-FORWARD TABLE")
    tbl = pd.DataFrame({
        s:{p:(snaps[p]["ACCOUNT_STATUS_L2"]==s).sum() for p in PERIODS}
        for s in ["Active","PAR 7","PAR 30","FPD","FMD","Inactive","Return","Paid Off"]
    }).T
    st.dataframe(tbl.style
        .background_gradient(axis=1,cmap="RdYlGn_r",
            subset=pd.IndexSlice[["PAR 30","FPD","FMD","Return"],:])
        .format("{:,}"), use_container_width=True)

    cl,cr = st.columns(2)
    with cl:
        sh("💰","ARREARS WATERFALL","Dec-25")
        tb,ta = DEC["CLOSING_BALANCE"].sum(), DEC["ARREARS"].sum()
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute","relative","total"],
            x=["Closing Balance","Performing","Arrears"],
            y=[tb,-(tb-ta),ta],
            decreasing=dict(marker_color=P["green"]),
            increasing=dict(marker_color=P["red"]),
            totals=dict(marker_color=P["blue"]),
            connector=dict(line=dict(color="rgba(255,255,255,.08)")),
            text=[f"KSh {tb/1e6:.0f}M",f"−{(tb-ta)/1e6:.0f}M",f"KSh {ta/1e6:.0f}M"],
            textposition="outside", textfont=dict(color="#E2E8F0",size=10),
        ))
        T(fig,"",h=290); fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        sh("📦","RETURN ACCOUNT TREND")
        rv=[(snaps[p]["ACCOUNT_STATUS_L2"]=="Return").sum() for p in PERIODS]
        fig = go.Figure(go.Bar(x=PERIODS,y=rv,
            marker=dict(color=P["purple"],line=dict(color="#0F172A",width=1)),
            text=rv,textposition="outside",textfont=dict(size=10,color="#E2E8F0")))
        T(fig,"Device Returns — 2.9× increase YTD",h=290)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    div()
    sh("🤖","AI INSIGHT — Q1","Mistral")
    ai_block("PAR 30 grew +10pp YTD and Avg DPD rose from 170 to 283 days. What does this signal about the collections strategy and what single change would have the highest impact?", ctx(), "ph")

# ═══════════════════════════════════════════════════════════════════════════
# SEGMENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Segment Analysis":
    st.markdown('<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 14px;letter-spacing:-1px">Segment Risk Analysis</h1>', unsafe_allow_html=True)

    cs("q1","Q1 — Segment Spotlight","18–25 Age Cohort Differs Meaningfully from Portfolio Average",
       """The <b>18–25 age band</b> carries a PAR 30 rate of <b>21.3%</b> and FPD of <b>7.0%</b> —
       both above the portfolio averages of ~19% and ~6.1% respectively. The <b>55+ cohort</b>
       shows the highest PAR 30 (24.8%) but has only 113 accounts, making it statistically thin.
       Across income bands, accounts with monthly income <b>below KSh 30K</b> show PAR 30 of 20–22%
       versus 15–18% for higher-income segments. <b>Why it matters operationally:</b> the 18–25
       cohort is likely to be the fastest-growing acquisition segment — if underwriting isn't
       tightened now, the PAR 30 trajectory will worsen as that cohort matures into the portfolio.""",
       "Apply stricter deposit (e.g. 20%) or shorter initial terms for 18–25. Add financial literacy step at onboarding.")

    ptf_par30 = ALL_M["Dec-25"]["par30r"]
    ptf_fpd   = ALL_M["Dec-25"]["fpdr"]
    al(f"Portfolio average — PAR 30: <b>{ptf_par30}%</b> · FPD: <b>{ptf_fpd}%</b>. <span style='color:#EF4444'>Red bars = above average.</span>","blue")

    seg_choice = st.radio("Group by:", ["Age Band","Income Band","Gender"], horizontal=True)
    seg_col = {"Age Band":"age_band","Income Band":"income_band","Gender":"Gender"}[seg_choice]

    AGE_ORD = ["18-25","26-35","36-45","46-55","55+"]
    INC_ORD = ["<5K","5K-9.9K","10K-19.9K","20K-29.9K","30K-49.9K","50K-99.9K","100K-149.9K","150K+"]

    if seg_col not in DEC_M.columns:
        al("Demographics not loaded — ensure Sales and Customer Data.xlsx is present.","amber")
        st.stop()

    sg = DEC_M[DEC_M[seg_col].notna() & ~DEC_M[seg_col].isin(["Unknown","nan"])]
    st_df = seg_tbl(sg, seg_col).reset_index()
    if seg_choice=="Age Band":
        st_df["segment"]=pd.Categorical(st_df["segment"],AGE_ORD,ordered=True)
        st_df=st_df.sort_values("segment")
    elif seg_choice=="Income Band":
        st_df["segment"]=pd.Categorical(st_df["segment"],INC_ORD,ordered=True)
        st_df=st_df.sort_values("segment")

    cl,cr = st.columns(2)
    with cl:
        sh("📊","PAR 30 BY SEGMENT","Dec-25")
        bc=[P["red"] if v>ptf_par30 else P["blue"] for v in st_df["par30r"]]
        fig=go.Figure(go.Bar(y=st_df["segment"].astype(str),x=st_df["par30r"],
            orientation="h",marker_color=bc,
            marker_line=dict(color="#0F172A",width=1),
            text=[f"{v}%" for v in st_df["par30r"]],textposition="outside",
            textfont=dict(size=10,color="#E2E8F0")))
        fig.add_vline(x=ptf_par30,line_dash="dash",line_color=P["orange"],
                      annotation_text=f"Avg {ptf_par30}%",
                      annotation_font_color=P["orange"],annotation_font_size=9)
        T(fig,h=max(280,len(st_df)*52))
        fig.update_layout(showlegend=False,xaxis=dict(title="PAR 30 Rate (%)"))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        sh("⚠️","FPD BY SEGMENT","Dec-25")
        bc2=[P["red"] if v>ptf_fpd else P["orange"] for v in st_df["fpdr"]]
        fig=go.Figure(go.Bar(y=st_df["segment"].astype(str),x=st_df["fpdr"],
            orientation="h",marker_color=bc2,
            marker_line=dict(color="#0F172A",width=1),
            text=[f"{v}%" for v in st_df["fpdr"]],textposition="outside",
            textfont=dict(size=10,color="#E2E8F0")))
        fig.add_vline(x=ptf_fpd,line_dash="dash",line_color=P["orange"],
                      annotation_text=f"Avg {ptf_fpd}%",
                      annotation_font_color=P["orange"],annotation_font_size=9)
        T(fig,h=max(280,len(st_df)*52))
        fig.update_layout(showlegend=False,xaxis=dict(title="FPD Rate (%)"))
        st.plotly_chart(fig, use_container_width=True)

    sh("🫧","RISK MATRIX","PAR 30 vs FPD · bubble size = account count")
    fig=go.Figure()
    for _,row in st_df.iterrows():
        risk = ("high"   if (row["par30r"]>ptf_par30 and row["fpdr"]>ptf_fpd) else
                "medium" if (row["par30r"]>ptf_par30 or  row["fpdr"]>ptf_fpd) else "low")
        clr  = {("high"):P["red"],("medium"):P["orange"],("low"):P["green"]}[risk]
        fig.add_trace(go.Scatter(x=[row["fpdr"]],y=[row["par30r"]],
            mode="markers+text",name=str(row["segment"]),
            marker=dict(size=max(14,min(62,row["n"]//18+14)),color=clr,opacity=.78,
                        line=dict(color="white",width=1.5)),
            text=[str(row["segment"])],textposition="top center",
            textfont=dict(size=10,color="#E2E8F0")))
    fig.add_hline(y=ptf_par30,line_dash="dash",line_color=P["orange"],opacity=.35)
    fig.add_vline(x=ptf_fpd,  line_dash="dash",line_color=P["orange"],opacity=.35)
    T(fig,h=360)
    fig.update_layout(showlegend=False,
        xaxis=dict(title="FPD Rate (%)"),yaxis=dict(title="PAR 30 Rate (%)"))
    st.plotly_chart(fig, use_container_width=True)

    div()
    sh("🤖","AI INSIGHT — SEGMENT","Mistral")
    ai_block("The 18-25 cohort has PAR30=21.3% and FPD=7.0%, both above average, and is likely the fastest-growing acquisition segment. What underwriting changes would reduce risk without excluding young Kenyans?", ctx(), "sg")

# ═══════════════════════════════════════════════════════════════════════════
# CUSTOMER EXPERIENCE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Customer Experience":
    st.markdown('<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 14px;letter-spacing:-1px">Customer Experience & NPS</h1>', unsafe_allow_html=True)

    if NPS_C.empty:
        al("NPS data not loaded. Ensure NPS Data.xlsx is present.","amber"); st.stop()

    n_tot = nps["nps_score"].notna().sum()
    n_pro = (nps["nps_cat"]=="Promoter").sum()
    n_det = (nps["nps_cat"]=="Detractor").sum()
    n_pas = (nps["nps_cat"]=="Passive").sum()
    score = round((n_pro-n_det)/n_tot*100,1) if n_tot else 0
    pct_lock  = round((nps["phone_locked"]=="Yes").mean()*100,1)
    pct_delay = round((nps["payment_delay"]=="Yes").mean()*100,1)
    pct_sup   = round((nps["support_difficulty"]=="Yes").mean()*100,1)

    cs("q2","Q2 — Credit Outcomes × Customer Experience · 35%","NPS Reveals a Direct Link to Account Status — With a Fixable Root Cause",
       """Active accounts score Net NPS <b>+11.3</b>; PAR 30 scores <b>+4.9</b>; but <b>Return accounts score −46.8</b>
       — a 58-point collapse. Critically: <b>13.6% of customers report phone locked despite on-time payment</b>,
       driven by a <b>17.5% payment reflection delay rate</b>. This is a system processing lag
       being felt as a collections enforcement action. It converts good-standing customers into
       detractors. Collections contact itself has <em>not</em> broken the PAR 30 relationship (+4.9 NPS)
       — the damage comes from false positives in the locking mechanism.
       <b>Tension:</b> PAYG locking is MoPhones' primary collections lever — necessary for portfolio health —
       but the current implementation lacks a payment-verification buffer.""",
       "Recommendation: 4-hour payment-reflection grace period before lock triggers. Track 'locked on-time payer' as a standalone KPI.")

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi(f"{score:+.1f}", "Net NPS Score", kind="warning")
    with c2: kpi(f"{int(n_pro):,}", f"Promoters  {round(n_pro/n_tot*100)}%", kind="ok")
    with c3: kpi(f"{int(n_pas):,}", f"Passives  {round(n_pas/n_tot*100)}%",  kind="info")
    with c4: kpi(f"{int(n_det):,}", f"Detractors  {round(n_det/n_tot*100)}%",kind="danger")
    with c5: kpi(f"{pct_lock}%", "Locked on-time",("up","⚠️ False-positive locks"),kind="danger")

    al(f"<b>Return account NPS = −46.8.</b> PAR 30 accounts still have positive NPS (+4.9) — collections contact hasn't broken the relationship. The real issue is the {pct_lock}% of customers locked despite paying on time ({pct_delay}% payment delay rate).", "red")

    div()
    cl,cr = st.columns(2)

    with cl:
        sh("📊","NET NPS BY ACCOUNT STATUS")
        SORD=["Return","FMD","Inactive","PAR 30","Active","Paid Off","PAR 7","FPD"]
        rows=[]
        for s in SORD:
            g=NPS_C[NPS_C["ACCOUNT_STATUS_L2"]==s]; n=len(g)
            if n==0: continue
            pro=(g["nps_cat"]=="Promoter").sum(); det=(g["nps_cat"]=="Detractor").sum()
            rows.append({"status":s,"net_nps":round((pro-det)/n*100,1),"n":n})
        ns=pd.DataFrame(rows)
        bc=[P["red"] if v<0 else P["green"] for v in ns["net_nps"]]
        fig=go.Figure(go.Bar(y=ns["status"],x=ns["net_nps"],orientation="h",
            marker_color=bc,marker_line=dict(color="#0F172A",width=1),
            text=[f"{v:+.1f}" for v in ns["net_nps"]],textposition="outside",
            textfont=dict(size=10,color="#E2E8F0")))
        fig.add_vline(x=0,line_color="rgba(255,255,255,.12)",line_width=1)
        fig.add_vline(x=score,line_dash="dash",line_color=P["orange"],
                      annotation_text=f"Overall {score:+.1f}",
                      annotation_font_color=P["orange"],annotation_font_size=9)
        T(fig,h=310); fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        sh("📊","NPS SCORE DISTRIBUTION")
        sc=nps["nps_score"].dropna().value_counts().sort_index().reset_index()
        sc.columns=["score","count"]
        sc["color"]=sc["score"].apply(
            lambda s: P["red"] if s<=6 else (P["orange"] if s<=8 else P["green"]))
        fig=go.Figure(go.Bar(x=sc["score"],y=sc["count"],
            marker_color=sc["color"],marker_line=dict(color="#0F172A",width=1),
            text=sc["count"],textposition="outside",textfont=dict(size=9,color="#E2E8F0")))
        T(fig,h=310); fig.update_layout(showlegend=False,
            xaxis=dict(tickmode="linear",tick0=0,dtick=1,title="Score"))
        st.plotly_chart(fig, use_container_width=True)

    sh("🔒","OPERATIONAL FRICTION BY ACCOUNT STATUS")
    fr_rows=[]
    for s in ["Active","PAR 7","PAR 30","FPD","Paid Off","Return","Inactive"]:
        g=NPS_C[NPS_C["ACCOUNT_STATUS_L2"]==s]
        if len(g)==0: continue
        fr_rows.append({
            "Status":s,"n":len(g),
            "Locked on-time (%)":round((g["phone_locked"]=="Yes").mean()*100,1),
            "Payment delay (%)" :round((g["payment_delay"]=="Yes").mean()*100,1),
            "Support difficulty (%)":round((g["support_difficulty"]=="Yes").mean()*100,1),
        })
    fr=pd.DataFrame(fr_rows)

    cl,cr = st.columns([3,2])
    with cl:
        fig=go.Figure()
        for col,clr in [("Locked on-time (%)",P["red"]),
                        ("Payment delay (%)",P["orange"]),
                        ("Support difficulty (%)",P["purple"])]:
            fig.add_trace(go.Bar(name=col,x=fr["Status"],y=fr[col],
                marker_color=clr,marker_line=dict(color="#0F172A",width=1)))
        T(fig,"Friction Points — % of respondents",h=290)
        fig.update_layout(barmode="group",legend=dict(orientation="h",y=-0.28))
        st.plotly_chart(fig, use_container_width=True)
    with cr:
        st.markdown("<div style='height:24px'></div>",unsafe_allow_html=True)
        st.dataframe(fr.drop("n",axis=1).style.background_gradient(
            subset=["Locked on-time (%)","Payment delay (%)","Support difficulty (%)"],
            cmap="RdYlGn_r"),use_container_width=True,hide_index=True)

    div()
    sh("🤖","AI INSIGHT — Q2","Mistral")
    ai_block("13.6% of MoPhones customers have their phone locked despite paying on time. Return accounts NPS is -46.8. How should MoPhones redesign the PAYG lock policy to protect both collections effectiveness and customer trust?", ctx(), "cx")

# ═══════════════════════════════════════════════════════════════════════════
# DATA QUALITY
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Data Quality":
    st.markdown('<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 14px;letter-spacing:-1px">Data Quality Audit</h1>', unsafe_allow_html=True)

    cs("q3","Q3 — Data Quality & Recommendations · 25%","5 Limitations Found — 3 Structural Fixes Proposed",
       """<b>L1 [High]</b> ~49% demographic linkage gap. Gender/DOB/Income sheets incompletely populated with Loan Id.
       Segment analyses are sub-sample only.<br>
       <b>L2 [High]</b> Ambiguous income fields — 'Received' overlaps with 'Banks Received' and 'Paybills Received'.
       Monthly income unreliable for credit decisioning.<br>
       <b>L3 [Medium]</b> Snapshot-only data — 5 quarterly files, no monthly history. Roll rates, cure rates,
       seasonal patterns unmeasurable.<br>
       <b>L4 [Medium]</b> NPS single campaign (~Apr 2025) — not longitudinal. Causal direction unclear.<br>
       <b>L5 [Low]</b> CUSTOMER_AGE mislabelled — it is loan tenure in days, not borrower age.""",
       "Fix priority: ① CUSTOMER_ID at KYC → ② monthly fact_loan_history → ③ standardised income schema")

    match_n = DEC_M["age_band"].notna().sum() if "age_band" in DEC_M.columns else 0
    link_pct = round(match_n/len(DEC)*100,1)

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi(f"{link_pct}%","Demographic Linkage",("up",f"{match_n:,}/{len(DEC):,}"),
                 kind="danger" if link_pct<60 else "ok")
    with c2: kpi("5","Quarterly Snapshots",("neutral","No monthly history"),kind="warning")
    with c3: kpi("4,129","NPS Responses",("neutral","Single campaign Apr-25"),kind="warning")
    with c4: kpi("0","Persistent CUSTOMER_IDs",("up","No CUSTOMER_ID exists"),kind="danger")

    al("<b>Critical:</b> ~49% linkage gap · No persistent CUSTOMER_ID · Monthly payment history absent — roll rates and cure rates cannot be measured.", "red")
    div()

    sh("🔍","ISSUE REGISTER")
    issues=[
        ("L1","Demographic Linkage Gap","High",
         "~49% of Dec-25 accounts have no demographic match. Segment analyses are sub-sample only.",
         "Enforce CUSTOMER_ID at KYC; link all records — loans, income, NPS, device — to it"),
        ("L2","Ambiguous Income Fields","High",
         "'Received', 'Persons Received', 'Banks Received', 'Paybills Received' overlap. Income unreliable for credit decisioning.",
         "Define: gross_received, verified_bank_income, duration_months (int). Add verified_monthly_income derived field."),
        ("L3","Snapshot-Only Credit Data","Medium",
         "5 quarterly snapshots. No monthly history means roll rates, cure rates, seasonal patterns unmeasurable.",
         "Build monthly fact_loan_history table: one row per loan × month with status, balance, DPD, payment, collections action."),
        ("L4","NPS Point-in-Time Bias","Medium",
         "All 4,129 responses from ~3-week campaign (April 2025). Cannot confirm causal direction.",
         "Run NPS at 3 fixed points: 30d post-sale, 90d, and at payoff."),
        ("L5","CUSTOMER_AGE Mislabelled","Low",
         "CUSTOMER_AGE is loan tenure in days — not borrower age. Required separate DOB derivation.",
         "Rename to LOAN_TENURE_DAYS. Add BORROWER_AGE as derived field."),
    ]
    si={"High":"🔴","Medium":"🟡","Low":"🔵"}
    for no,issue,sev,detail,fix in issues:
        with st.expander(f"{si[sev]}  [{no}] {issue}  ·  {sev}"):
            a,b=st.columns([3,2])
            with a: st.markdown(f"**Detail:** {detail}")
            with b: st.markdown(f"**Fix:** {fix}")

    div()
    sh("📊","MISSING VALUE ANALYSIS","Dec-25")
    null_pct=(DEC.isnull().sum()/len(DEC)*100).round(1)
    null_pct=null_pct[null_pct>0].sort_values(ascending=False).head(14)
    if len(null_pct):
        fig=go.Figure(go.Bar(x=null_pct.values,y=null_pct.index,orientation="h",
            marker_color=[P["red"] if v>30 else (P["orange"] if v>10 else P["blue"]) for v in null_pct.values],
            marker_line=dict(color="#0F172A",width=1),
            text=[f"{v}%" for v in null_pct.values],textposition="outside",
            textfont=dict(size=9,color="#E2E8F0")))
        T(fig,"Fields with Missing Data — Dec-25",h=max(240,len(null_pct)*28))
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    div()
    sh("🤖","AI INSIGHT — Q3","Mistral")
    ai_block("Given a 49% demographic linkage gap, no monthly payment history, and ambiguous income fields, what is the most impactful data infrastructure investment MoPhones should make first, and why?", ctx(), "dq")

# ═══════════════════════════════════════════════════════════════════════════
# CASE STUDY ANSWERS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Case Study Answers":
    st.markdown("""<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 2px;letter-spacing:-1px">
      Case Study — Full Written Answers</h1>
      <p style="color:#1E293B;font-size:12px;margin-bottom:16px">
      Evidence-based responses to all three questions — every claim traceable to the data.</p>""",
      unsafe_allow_html=True)

    # Q1
    st.markdown("---")
    cs("q1","Q1 · Portfolio Health · 40%","Metric Selection, Trend Analysis & Segment Spotlight",
       """<b>Metrics selected (5):</b><br>
       <b>① PAR 30 Rate</b> — accounts 30+ days past due as % of non-closed portfolio.
       The global standard credit KPI. Breaching 30% is a material risk threshold.
       Grew <b>22.9% → 32.8%</b> YTD (+10pp). Industry microfinance benchmarks typically target &lt;25%.<br><br>
       <b>② FPD Rate</b> — First Payment Default. Did the customer ever intend to pay?
       Stable at <b>~8%</b> throughout 2025 — indicates acquisition-side risk is embedded
       but not actively worsening. A structural 8% FPD floor suggests underwriting calibration is needed.<br><br>
       <b>③ Arrears Ratio</b> — total arrears ÷ closing balance. At <b>~46%</b>, roughly half the
       outstanding book is in arrears. Critical for provisioning and investor reporting.<br><br>
       <b>④ Avg Days Past Due</b> (arrears accounts) — collection lag metric.
       Rose from <b>170 → 283 days</b> (+66% YTD). This means chronic defaulters are being
       rolled forward rather than resolved — a collections strategy failure.<br><br>
       <b>⑤ Return Rate</b> — device recoveries represent double losses. Grew from
       <b>604 → 1,744 accounts</b> (+189%). Signals CX failures and/or affordability stress.<br><br>
       <b>Segment spotlight — 18–25 age cohort:</b>
       PAR 30 = 21.3% (vs portfolio avg 19%) and FPD = 7.0% (vs avg 6.1%).
       Operationally: younger borrowers likely underestimate the weekly repayment commitment
       or experience greater income volatility. This cohort is also likely the fastest-growing
       acquisition segment — if underwriting isn't differentiated now, PAR 30 will worsen
       as younger originations mature into the portfolio. <b>Recommended actions:</b>
       (a) Apply 20% deposit requirement for 18–25 applicants vs standard.
       (b) Offer 6M initial term with 12M upgrade after good payment standing.
       (c) Add a financial literacy module at onboarding explaining the weekly commitment.""",
       "PAR 30 crossed 30% in Mar-25 and reached 32.8% by Dec-25. Avg DPD at 283 days signals collection stagnation — not just delinquency volume.")

    # Q2
    st.markdown("---")
    cs("q2","Q2 · Credit Outcomes × Customer Experience · 35%","NPS–Credit Status Linkage & the Collections–CX Tension",
       """<b>Relationship found:</b> Account status and NPS are strongly correlated.
       Return accounts: Net NPS = <b>−46.8</b> (68% detractors, 331 respondents).
       Active: <b>+11.3</b>. PAR 30: <b>+4.9</b>. Overall: <b>+5.9</b>.<br><br>
       <b>Critical insight:</b> PAR 30 customers still have net-positive NPS (+4.9).
       This tells us that collections contact itself — calls, SMS, payment reminders — has
       <em>not</em> destroyed the customer relationship. The real damage is more specific.<br><br>
       <b>The core tension identified in the data:</b>
       MoPhones uses device locking (PAYG model) as its primary collections enforcement mechanism.
       This is structurally sound — but <b>13.6% of customers report their phone being locked
       despite making an on-time payment</b>. This is driven by a <b>17.5% payment reflection
       delay rate</b> — payments are processed by the customer but not immediately reflected in
       the system, triggering the lock. A system processing lag is being experienced as an
       enforcement action against a paying customer. This is the most damaging friction point.<br><br>
       Additional tension signals: 15% support access difficulty, battery/device issues
       (contributing to the Return surge), and lack of payment visibility in the app.<br><br>
       <b>One concrete recommendation:</b>
       Implement a <b>4-hour payment-reflection SLA with a grace window</b> before the device
       lock triggers. If a payment is logged in any channel (M-Pesa, bank, MoApp) but not yet
       processed in the loan system within 4 hours, suppress the lock. Track "locked on-time payer"
       as a standalone operational KPI in the collections dashboard — separate from intentional
       lock actions. This directly targets the 13.6% detractor signal without reducing collections
       effectiveness on genuinely non-paying accounts.""",
       "The PAYG lock is the right tool — but false-positive locks on paying customers are the single highest-leverage CX fix available.")

    # Q3
    st.markdown("---")
    cs("q3","Q3 · Data Quality & Recommendations · 25%","Limitations Encountered & 3 Structural Fixes",
       """<b>Limitations encountered:</b><br>
       <b>L1 [High]</b> ~49% demographic linkage gap. The Gender, DOB, and Income sheets in
       Sales and Customer Data.xlsx are incompletely populated with Loan Id — meaning nearly half
       of the credit portfolio cannot be linked to any demographic data. Segment analyses in this
       submission are based on the ~51% sub-sample, which may not represent portfolio-wide risk.<br><br>
       <b>L2 [High]</b> Income definition is ambiguous. 'Received', 'Persons Received From Total',
       'Banks Received', and 'Paybills Received Others' overlap substantially in their values.
       It is unclear whether 'Received' is gross or net of the sub-components. This makes
       monthly income computation unreliable for credit scoring or affordability assessment.<br><br>
       <b>L3 [Medium]</b> Snapshot-only credit data. Five quarterly point-in-time files cannot reveal
       month-by-month roll rates (Active→PAR 7→PAR 30), cure rates, or seasonal delinquency patterns.
       The Avg DPD rising to 283 days is visible, but <em>why</em> and <em>when</em> accounts
       transitioned cannot be determined without monthly history.<br><br>
       <b>L4 [Medium]</b> NPS is a single-campaign point-in-time survey (~April 2025, ~3 weeks).
       Cannot establish causal direction between credit performance and satisfaction. Cannot track
       NPS changes as a result of operational improvements.<br><br>
       <b>L5 [Low]</b> CUSTOMER_AGE in credit files is loan tenure in days, not borrower age.
       Borrower age had to be derived separately from DOB — a confusing field name.<br><br>
       <b>3 Structural improvements:</b><br>
       <b>① Persistent CUSTOMER_ID at KYC (foundational)</b> — Assign a UUID at the KYC step
       that links all downstream records: loans, income checks, NPS responses, and device history.
       This enables repeat-customer tracking, multi-loan risk profiling, and demographic
       enrichment at scale. Currently impossible.<br><br>
       <b>② Monthly fact_loan_history table (analytics)</b> — One row per loan × month tracking:
       status_l1, status_l2, balance, closing_balance, arrears, dpd, payment, collections_action.
       Enables roll-rate matrices, cure rates, vintage analysis, and early-warning triggers.
       Currently limited to 5 quarterly snapshots.<br><br>
       <b>③ Standardised income schema (underwriting)</b> — Define exactly:
       gross_received = total inflows; verified_bank_income = confirmed bank-channel income;
       duration_months = integer (not float). Add derived field:
       verified_monthly_income = verified_bank_income / duration_months.
       Enables income-band credit scoring and affordability assessment at underwriting.""",
       "Priority: CUSTOMER_ID is foundational — without it, improvements 2 and 3 cannot be fully leveraged.")

    div()
    sh("🤖","AI SYNTHESIS","Mistral · all three questions")
    ai_block(
        "Synthesise all three case study questions: what is the single most important finding from this 2025 MoPhones credit portfolio analysis, and what is the one action that would have the highest combined impact on portfolio health, customer experience, and data quality?",
        ctx(), "synthesis"
    )

# ═══════════════════════════════════════════════════════════════════════════
# AI ANALYST
# ═══════════════════════════════════════════════════════════════════════════
elif page == "AI Analyst":
    st.markdown("""<h1 style="font-size:26px;font-weight:900;color:#E2E8F0;margin:16px 0 2px;letter-spacing:-1px">
      🤖 AI Analyst — Powered by Mistral</h1>
      <p style="color:#1E293B;font-size:12px;margin-bottom:10px">
      Local inference via Ollama · no API key · your data never leaves the machine</p>""",
      unsafe_allow_html=True)

    avail = ollama_ok()
    if not avail:
        al("Ollama is not running. Open a terminal and run: <code style='background:#0F172A;padding:2px 6px;border-radius:4px'>ollama serve</code> — then refresh this page.", "amber")
    else:
        al("✅ Mistral is online via Ollama. All inference is local — portfolio data stays on your machine.", "green")

    div()
    sh("📚","PROMPT LIBRARY","6 pre-built analyst prompts")
    prebuilt = {
        "Portfolio Risk Diagnosis":
            "Given PAR 30 at 32.8% and Avg DPD rising to 283 days, diagnose the most likely root cause and recommend a 30-day action plan for the collections team.",
        "18–25 Cohort Deep Dive":
            "The 18-25 age cohort has PAR30=21.3% and FPD=7.0%, both above portfolio average. What specific product design and underwriting changes would reduce this risk without excluding young Kenyans from access?",
        "Collections vs CX Tension":
            "13.6% of customers are locked despite paying on time. Return accounts NPS is -46.8. Design a PAYG lock policy that protects collections effectiveness while eliminating false-positive locks.",
        "Return Account Surge Analysis":
            "Returns grew from 604 to 1,744 accounts (+189%) in 2025. What are the 3 most likely causes — device quality, affordability stress, or CX failure — and what data would confirm each hypothesis?",
        "Data Infrastructure Roadmap":
            "Given a 49% demographic linkage gap, no monthly payment history, and ambiguous income fields, design a prioritised 6-month data infrastructure roadmap for MoPhones.",
        "CCO Investor Narrative":
            "Prepare a concise 5-bullet narrative a CCO could present to investors about the 2025 portfolio trajectory, the root causes, and the 3-step remediation plan.",
    }

    chosen = st.selectbox("Choose a prompt:", list(prebuilt.keys()))
    st.markdown(f'<div style="background:#0C1220;border-radius:8px;padding:11px 14px;'
                f'font-size:11px;color:#334155;margin:8px 0;font-style:italic">'
                f'"{prebuilt[chosen]}"</div>', unsafe_allow_html=True)

    if st.button("▶  Run Selected Prompt", type="primary", disabled=not avail):
        with st.spinner("Mistral is analysing…"):
            st.session_state["lib_resp"] = mistral(prebuilt[chosen], ctx())

    if st.session_state.get("lib_resp"):
        html = st.session_state["lib_resp"].replace("\n","<br>")
        st.markdown(f"""<div class="ai-wrap" style="margin-top:6px">
          <div class="ai-header">
            <div class="ai-dot"></div>
            <span class="ai-lbl">Mistral Response</span>
          </div>
          <div class="ai-txt">{html}</div>
        </div>""", unsafe_allow_html=True)

    div()
    sh("✏️","CUSTOM QUESTION")
    custom = st.text_area("Ask anything about the MoPhones portfolio:",height=90,
        placeholder="e.g. What PAR 30 rate should we expect in Q1 2026 if no action is taken?")

    if st.button("▶  Ask Mistral", disabled=not avail or not custom.strip()):
        with st.spinner("Thinking…"):
            st.session_state["custom_resp"] = mistral(custom, ctx())

    if st.session_state.get("custom_resp"):
        html = st.session_state["custom_resp"].replace("\n","<br>")
        st.markdown(f"""<div class="ai-wrap" style="margin-top:6px">
          <div class="ai-header">
            <div class="ai-dot"></div>
            <span class="ai-lbl">Mistral Response</span>
          </div>
          <div class="ai-txt">{html}</div>
        </div>""", unsafe_allow_html=True)

    with st.expander("📋 Portfolio context sent to Mistral"):
        st.code(ctx(), language="text")