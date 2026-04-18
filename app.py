import streamlit as st
import pandas as pd
import json, os, random
from datetime import datetime, timedelta

STATE_PATH = os.path.join(os.path.dirname(__file__), "sz_state.json")

# ══════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="ShoeZone — Step Into Style", page_icon="👟", layout="wide")

# ══════════════════════════════════════════════════════════════
# PREMIUM CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

:root {
  --ink:    #0a0a0a;
  --ink2:   #1c1c1c;
  --ink3:   #2e2e2e;
  --muted:  #6b7280;
  --faint:  #9ca3af;
  --smoke:  #f4f2ee;
  --cream:  #faf8f5;
  --white:  #ffffff;
  --gold:   #d4a843;
  --gold2:  #f0c060;
  --red:    #e53e3e;
  --green:  #0d7a4e;
  --border: #e8e4db;
  --radius: 18px;
  --radius-sm: 10px;
  --shadow: 0 4px 24px rgba(10,10,10,0.07);
  --shadow-lg: 0 16px 48px rgba(10,10,10,0.12);
  --shadow-xl: 0 32px 80px rgba(10,10,10,0.16);
}

*, html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  box-sizing: border-box;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1500px; padding-left: 2rem; padding-right: 2rem; }

/* ── ANNOUNCEMENT BAR ── */
.sz-announce {
  background: var(--ink);
  color: var(--gold2);
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
  padding: 9px 20px;
  margin: 0 -1rem;
}

/* ── NAVBAR ── */
.sz-nav {
  background: var(--white);
  padding: 0 40px;
  height: 72px;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 -1rem;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 16px rgba(10,10,10,0.05);
}
.sz-logo {
  font-family: 'Syne', sans-serif !important;
  font-size: 26px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -1px;
  white-space: nowrap;
  margin-right: 12px;
}
.sz-logo em { color: var(--gold); font-style: normal; }
.sz-nav-tag {
  font-size: 10px;
  font-weight: 700;
  background: var(--ink);
  color: var(--gold2);
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.1em;
  margin-top: -18px;
  margin-left: -8px;
}
.sz-nav-user {
  font-size: 12px;
  color: var(--muted);
  white-space: nowrap;
  padding-top: 8px;
  line-height: 1.4;
}
.sz-nav-user b { color: var(--ink); font-weight: 700; }

/* ── HERO ── */
.sz-hero {
  background: var(--ink);
  min-height: 560px;
  padding: 100px 80px 90px;
  margin: 0 -1rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 60px;
  position: relative;
  overflow: hidden;
}
.sz-hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 60% 80% at -10% 50%, rgba(212,168,67,0.15) 0%, transparent 60%),
    radial-gradient(ellipse 40% 40% at 110% 20%, rgba(212,168,67,0.08) 0%, transparent 50%);
  pointer-events: none;
}
.sz-hero-noise {
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  opacity: 0.4;
  pointer-events: none;
}
.sz-hero-left { position: relative; z-index: 1; }
.sz-hero-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(212,168,67,0.12);
  border: 1px solid rgba(212,168,67,0.3);
  color: var(--gold2);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 7px 16px;
  border-radius: 999px;
  margin-bottom: 28px;
}
.sz-hero-h1 {
  font-family: 'Syne', sans-serif !important;
  font-size: 72px !important;
  font-weight: 800 !important;
  color: var(--white) !important;
  letter-spacing: -3px !important;
  line-height: 0.92 !important;
  margin-bottom: 28px !important;
}
.sz-hero-h1 em { color: var(--gold); font-style: normal; display: block; }
.sz-hero-sub { font-size: 16px; color: #9ca3af; line-height: 1.75; max-width: 400px; margin-bottom: 40px; }
.sz-hero-ctas { display: flex; gap: 14px; flex-wrap: wrap; }
.sz-hero-btn-primary {
  background: var(--gold);
  color: var(--ink);
  font-weight: 800;
  font-size: 14px;
  padding: 14px 32px;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  letter-spacing: 0.02em;
  transition: all 0.2s;
  text-transform: uppercase;
}
.sz-hero-btn-primary:hover { background: var(--gold2); transform: translateY(-2px); }
.sz-hero-btn-ghost {
  background: transparent;
  color: var(--white);
  font-weight: 700;
  font-size: 14px;
  padding: 14px 28px;
  border-radius: var(--radius-sm);
  border: 1.5px solid rgba(255,255,255,0.2);
  cursor: pointer;
  transition: all 0.2s;
}
.sz-hero-btn-ghost:hover { border-color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.05); }
.sz-hero-right {
  position: relative; z-index: 1;
  display: flex; justify-content: center; align-items: center;
}
.sz-hero-img-frame {
  width: 420px; height: 420px;
  border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(212,168,67,0.12) 0%, transparent 70%);
  border: 1px solid rgba(212,168,67,0.15);
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.sz-hero-shoe-emoji {
  font-size: 180px;
  filter: drop-shadow(0 20px 40px rgba(212,168,67,0.3));
  animation: float 4s ease-in-out infinite;
}
@keyframes float {
  0%,100% { transform: translateY(0) rotate(-8deg); }
  50%      { transform: translateY(-16px) rotate(-5deg); }
}
.sz-hero-badge {
  position: absolute;
  background: var(--gold);
  color: var(--ink);
  font-size: 11px;
  font-weight: 800;
  padding: 8px 14px;
  border-radius: 999px;
  letter-spacing: 0.05em;
}
.sz-hero-badge-1 { top: 40px; right: -10px; }
.sz-hero-badge-2 { bottom: 60px; left: -20px; }
.sz-hero-stats {
  display: flex; gap: 40px; margin-top: 48px;
  padding-top: 40px; border-top: 1px solid #1e1e1e;
}
.sz-stat { text-align: left; }
.sz-stat-num {
  font-family: 'Syne', sans-serif !important;
  font-size: 26px; font-weight: 800; color: var(--white);
}
.sz-stat-lbl { font-size: 11px; color: #4b5563; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px; }

/* ── TRUST BAR ── */
.sz-trust {
  background: var(--cream);
  border-bottom: 1px solid var(--border);
  padding: 16px 0;
  display: flex;
  justify-content: center;
  gap: 56px;
  flex-wrap: wrap;
  margin: 0 -1rem;
}
.sz-trust-item { display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600; color: #374151; }
.sz-trust-icon { font-size: 18px; }

/* ── CATEGORY CHIPS ── */
.sz-cats {
  display: flex; gap: 10px; flex-wrap: wrap;
  padding: 28px 0 0;
}
.sz-cat-chip {
  padding: 9px 20px;
  border-radius: 999px;
  border: 1.5px solid var(--border);
  font-size: 13px; font-weight: 600; color: var(--muted);
  cursor: pointer; transition: all 0.18s;
  background: var(--white);
  white-space: nowrap;
}
.sz-cat-chip:hover { border-color: var(--gold); color: var(--ink); background: #fffbeb; }
.sz-cat-chip.active {
  background: var(--ink); color: var(--white);
  border-color: var(--ink);
}

/* ── FILTER BAR ── */
.sz-filter {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 28px 16px;
  margin-bottom: 28px;
  box-shadow: var(--shadow);
}
.sz-filter-label {
  font-size: 10px; font-weight: 800;
  text-transform: uppercase; letter-spacing: 0.2em;
  color: #b0a89a; margin-bottom: 14px;
}
.sz-active-chip {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--ink); color: var(--white);
  font-size: 11px; font-weight: 700;
  padding: 4px 12px; border-radius: 999px; margin: 4px;
}

/* ── PRODUCT CARD ── */
.sz-card {
  background: var(--white);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  transition: transform 0.3s cubic-bezier(.22,1,.36,1),
              box-shadow 0.3s, border-color 0.2s;
  margin-bottom: 28px;
  position: relative;
}
.sz-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border-color: rgba(212,168,67,0.35);
}
.sz-card-imgwrap {
  background: var(--smoke);
  height: 250px;
  overflow: hidden;
  position: relative;
}
.sz-card-imgwrap img {
  width: 100%; height: 250px;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(.22,1,.36,1);
}
.sz-card:hover .sz-card-imgwrap img { transform: scale(1.07); }
.sz-card-imgwrap::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(180deg, transparent 55%, rgba(10,10,10,0.12) 100%);
  opacity: 0; transition: opacity 0.3s;
}
.sz-card:hover .sz-card-imgwrap::after { opacity: 1; }

/* badge */
.sz-badge {
  position: absolute; top: 14px; left: 14px;
  padding: 5px 12px; border-radius: 999px;
  font-size: 10px; font-weight: 800;
  text-transform: uppercase; letter-spacing: 0.08em;
}
.b-bestseller { background: #fef9c3; color: #713f12; }
.b-new        { background: #dbeafe; color: #1e3a8a; }
.b-toprated   { background: #dcfce7; color: #14532d; }
.b-budget     { background: #fee2e2; color: #7f1d1d; }
.b-sale       { background: #ffedd5; color: #7c2d12; }
.b-exclusive  { background: var(--ink); color: var(--gold2); }

/* wishlist btn */
.sz-wish-btn {
  position: absolute; top: 12px; right: 12px;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(8px);
  border-radius: 50%;
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.10);
  cursor: pointer;
  transition: transform 0.2s;
}
.sz-wish-btn:hover { transform: scale(1.15); }

.sz-card-body { padding: 16px 18px 18px; }
.sz-card-meta {
  font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--faint); margin-bottom: 4px;
}
.sz-card-name {
  font-size: 16px; font-weight: 700; color: var(--ink);
  margin-bottom: 7px; line-height: 1.3;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.sz-stars { color: #f59e0b; font-size: 12px; }
.sz-rcount { color: var(--faint); font-size: 11px; margin-left: 4px; }
.sz-prices {
  display: flex; align-items: baseline; gap: 8px;
  margin: 10px 0 4px; flex-wrap: wrap;
}
.sz-price-now { font-size: 21px; font-weight: 800; color: var(--ink); font-family: 'Syne', sans-serif !important; }
.sz-price-was { font-size: 13px; color: #c4bdb0; text-decoration: line-through; }
.sz-price-off {
  font-size: 11px; font-weight: 800; color: var(--green);
  background: #dcfce7; padding: 2px 8px; border-radius: 999px;
}
.sz-free-tag { font-size: 11px; font-weight: 700; color: #0369a1; margin-top: 4px; }
.sz-card-sizes {
  display: flex; gap: 5px; flex-wrap: wrap; margin-top: 8px;
}
.sz-sz-dot {
  width: 28px; height: 28px; border-radius: 8px;
  border: 1px solid var(--border);
  font-size: 10px; font-weight: 700; color: var(--muted);
  display: flex; align-items: center; justify-content: center;
}

/* ── CART ── */
.sz-cart-item {
  background: var(--white);
  border-radius: 16px;
  border: 1px solid var(--border);
  padding: 18px;
  margin-bottom: 14px;
  box-shadow: var(--shadow);
}
.sz-cart-name  { font-size: 15px; font-weight: 800; color: var(--ink); margin-bottom: 3px; }
.sz-cart-meta  { font-size: 12px; color: var(--faint); margin-bottom: 8px; }
.sz-cart-price { font-size: 20px; font-weight: 900; color: var(--ink); font-family: 'Syne', sans-serif !important; }

/* ── ORDER SUMMARY PANEL ── */
.sz-panel {
  background: var(--ink);
  border-radius: 20px;
  padding: 28px;
  color: var(--white);
  position: sticky;
  top: 88px;
}
.sz-panel-title {
  font-size: 10px; font-weight: 800; color: #4b5563;
  text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 24px;
}
.sz-panel-row {
  display: flex; justify-content: space-between;
  font-size: 14px; color: #6b7280; margin-bottom: 12px;
}
.sz-panel-div { height: 1px; background: #1e1e1e; margin: 18px 0; }
.sz-panel-total {
  display: flex; justify-content: space-between;
  font-size: 22px; font-weight: 900; color: var(--white);
  font-family: 'Syne', sans-serif !important;
}
.sz-panel-free { color: #34d399; font-size: 12px; font-weight: 700; margin-top: 8px; }
.sz-coupon-hint {
  background: #111; border: 1px solid #222;
  border-radius: 12px; padding: 12px 16px; margin-top: 16px;
}
.sz-coupon-code {
  font-family: monospace; font-weight: 800; color: var(--gold2); font-size: 13px;
}

/* ── ORDER CARDS ── */
.sz-order-card {
  background: var(--white);
  border-radius: 20px;
  border: 1px solid var(--border);
  padding: 28px;
  margin-bottom: 20px;
  box-shadow: var(--shadow);
}
.sz-order-head { display: flex; justify-content: space-between; align-items: flex-start; }
.sz-order-id {
  font-family: 'Syne', sans-serif !important;
  font-size: 20px; font-weight: 800; color: var(--ink);
}
.sz-order-date { font-size: 12px; color: var(--faint); margin-top: 4px; }
.sz-order-status {
  padding: 6px 16px; border-radius: 999px;
  font-size: 11px; font-weight: 800; letter-spacing: 0.05em;
}
.status-delivered { background: #dcfce7; color: #14532d; }
.status-shipped   { background: #dbeafe; color: #1e3a8a; }
.sz-order-item {
  display: flex; align-items: center; gap: 14px;
  padding: 12px 0; border-bottom: 1px solid var(--smoke);
}
.sz-order-item:last-child { border-bottom: none; }
.sz-order-img {
  width: 60px; height: 60px; border-radius: 12px;
  object-fit: cover; background: var(--smoke);
}
.sz-order-item-name { font-size: 14px; font-weight: 700; color: var(--ink); }
.sz-order-item-sub  { font-size: 12px; color: var(--faint); margin-top: 2px; }
.sz-order-item-price{ font-size: 14px; font-weight: 800; color: var(--ink); margin-left: auto; white-space: nowrap; }

/* ── TRACKING ── */
.sz-track { display: flex; align-items: flex-start; gap: 0; margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--smoke); }
.sz-track-step { flex: 1; text-align: center; position: relative; }
.sz-track-dot {
  width: 16px; height: 16px; border-radius: 50%;
  margin: 0 auto 8px; position: relative; z-index: 1;
}
.sz-track-dot.done   { background: var(--green); }
.sz-track-dot.active { background: var(--gold); box-shadow: 0 0 0 4px rgba(212,168,67,0.2); }
.sz-track-dot.pending{ background: var(--border); }
.sz-track-line {
  position: absolute; top: 8px; left: 50%; right: -50%;
  height: 2px; background: var(--border); z-index: 0;
}
.sz-track-line.done { background: var(--green); }
.sz-track-label { font-size: 10px; font-weight: 700; color: var(--faint); }
.sz-track-label.done   { color: var(--green); }
.sz-track-label.active { color: var(--gold); }

/* ── DETAIL PAGE ── */
.sz-detail-wrap {
  background: var(--white);
  border-radius: 24px;
  border: 1px solid var(--border);
  padding: 32px;
  box-shadow: var(--shadow-lg);
}
.sz-detail-img-box {
  background: var(--smoke);
  border-radius: 18px;
  overflow: hidden;
  position: relative;
}
.sz-detail-img-box img {
  width: 100%;
  border-radius: 18px;
  transition: transform 0.5s cubic-bezier(.22,1,.36,1);
}
.sz-detail-img-box:hover img { transform: scale(1.04); }
.sz-detail-brand { font-size: 12px; font-weight: 800; color: var(--faint); text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 8px; }
.sz-detail-name {
  font-family: 'Syne', sans-serif !important;
  font-size: 34px; font-weight: 800; color: var(--ink);
  letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 14px;
}
.sz-detail-price-now {
  font-family: 'Syne', sans-serif !important;
  font-size: 38px; font-weight: 800; color: var(--ink);
}
.sz-detail-price-was { font-size: 20px; color: #c4bdb0; text-decoration: line-through; margin-left: 10px; }
.sz-detail-off {
  font-size: 14px; font-weight: 800; color: var(--green);
  background: #dcfce7; padding: 4px 12px;
  border-radius: 999px; margin-left: 10px;
}
.sz-size-grid { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
.sz-size-box {
  width: 54px; height: 54px; border-radius: 12px;
  border: 1.5px solid var(--border); background: var(--white);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 800; color: var(--muted);
  cursor: pointer; transition: all 0.18s;
}
.sz-size-box:hover  { border-color: var(--gold); color: #713f12; background: #fffbeb; }
.sz-size-box.active { border-color: var(--ink); background: var(--ink); color: var(--white); }
.sz-features-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 24px 0; }
.sz-feature-box {
  background: var(--smoke);
  border-radius: 14px;
  padding: 16px 12px;
  text-align: center;
}
.sz-feature-icon { font-size: 22px; margin-bottom: 6px; }
.sz-feature-label { font-size: 11px; font-weight: 700; color: var(--muted); }

/* ── REVIEWS ── */
.sz-review {
  background: var(--smoke);
  border-radius: 16px;
  padding: 18px 20px;
  margin-bottom: 14px;
}
.sz-review-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.sz-review-name { font-size: 14px; font-weight: 800; color: var(--ink); }
.sz-review-date { font-size: 12px; color: var(--faint); }
.sz-review-text { font-size: 14px; color: #374151; line-height: 1.65; }
.sz-review-verified { font-size: 11px; font-weight: 700; color: var(--green); margin-top: 8px; }
.sz-review-helpful {
  font-size: 12px; color: var(--faint); margin-top: 8px; cursor: pointer;
}

/* ── AUTH ── */
.sz-auth-wrap {
  max-width: 520px; margin: 40px auto;
}
.sz-auth-brand {
  font-family: 'Syne', sans-serif !important;
  font-size: 28px; font-weight: 800; color: var(--ink);
  text-align: center; margin-bottom: 4px;
}
.sz-auth-brand em { color: var(--gold); font-style: normal; }
.sz-auth-sub { font-size: 14px; color: var(--muted); text-align: center; margin-bottom: 32px; }
.sz-auth-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 36px 32px;
  box-shadow: var(--shadow-lg);
}

/* ── EMPTY STATES ── */
.sz-empty { text-align: center; padding: 80px 20px; }
.sz-empty-icon { font-size: 60px; margin-bottom: 18px; }
.sz-empty-title { font-family: 'Syne', sans-serif !important; font-size: 24px; font-weight: 800; color: var(--ink); margin-bottom: 8px; }
.sz-empty-sub { font-size: 14px; color: var(--faint); }

/* ── TOASTS ── */
.sz-toast-ok {
  background: #052e16; color: var(--white);
  padding: 14px 20px; border-radius: 14px;
  font-weight: 700; font-size: 14px;
  margin-bottom: 18px;
  border-left: 4px solid #22c55e;
  box-shadow: 0 8px 24px rgba(5,46,22,0.25);
}
.sz-toast-err {
  background: #450a0a; color: var(--white);
  padding: 14px 20px; border-radius: 14px;
  font-weight: 700; font-size: 14px;
  margin-bottom: 18px;
  border-left: 4px solid #f87171;
  box-shadow: 0 8px 24px rgba(69,10,10,0.25);
}

/* ── SECTION HEADS ── */
.sz-sh {
  display: flex; align-items: baseline;
  gap: 14px; margin-bottom: 28px; padding-top: 44px;
}
.sz-sh-title {
  font-family: 'Syne', sans-serif !important;
  font-size: 30px; font-weight: 800; color: var(--ink); letter-spacing: -1px;
}
.sz-sh-count { font-size: 13px; color: var(--faint); }

/* ── DEAL BANNER ── */
.sz-deal-banner {
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  border-radius: 20px;
  padding: 28px 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 32px 0;
  border: 1px solid #222;
  overflow: hidden;
  position: relative;
}
.sz-deal-banner::before {
  content: '';
  position: absolute; left: -60px; top: -60px;
  width: 200px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212,168,67,0.15) 0%, transparent 70%);
}
.sz-deal-left {}
.sz-deal-eyebrow { font-size: 11px; font-weight: 700; color: var(--gold); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px; }
.sz-deal-title { font-family: 'Syne', sans-serif !important; font-size: 28px; font-weight: 800; color: var(--white); letter-spacing: -1px; }
.sz-deal-sub { font-size: 14px; color: #6b7280; margin-top: 4px; }
.sz-deal-countdown {
  display: flex; gap: 12px; align-items: center;
}
.sz-deal-time {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 10px 14px;
  text-align: center;
  min-width: 58px;
}
.sz-deal-time-num { font-family: 'Syne', sans-serif !important; font-size: 22px; font-weight: 800; color: var(--gold2); line-height: 1; }
.sz-deal-time-lbl { font-size: 9px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

/* ── PAYMENT METHOD CARDS ── */
.sz-pay-card {
  border: 1.5px solid var(--border);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--white);
}
.sz-pay-card:hover    { border-color: var(--gold); background: #fffbeb; }
.sz-pay-card.selected { border-color: var(--ink); background: var(--smoke); }
.sz-pay-icon  { font-size: 26px; width: 36px; text-align: center; }
.sz-pay-label { font-size: 15px; font-weight: 700; color: var(--ink); }
.sz-pay-sub   { font-size: 12px; color: var(--faint); margin-top: 2px; }

/* ── PROGRESS BAR ── */
.sz-progress { background: #1e1e1e; border-radius: 999px; height: 4px; margin-top: 12px; }
.sz-progress-fill { background: linear-gradient(90deg, var(--gold), var(--gold2)); height: 4px; border-radius: 999px; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stButton"] > button {
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  transition: all 0.2s !important;
  font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(0,0,0,0.14) !important;
  border-color: var(--gold) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--ink) !important;
  color: var(--white) !important;
  border-color: var(--ink) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  background: var(--ink2) !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
  border-radius: 12px !important;
  border: 1.5px solid var(--border) !important;
  padding: 10px 16px !important;
  font-size: 14px !important;
  font-family: 'DM Sans', sans-serif !important;
  background: var(--cream) !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(212,168,67,0.14) !important;
  background: var(--white) !important;
}
div[data-testid="stSelectbox"] > div > div {
  border-radius: 12px !important;
  border: 1.5px solid var(--border) !important;
  background: var(--cream) !important;
}
div[data-testid="metric-container"] {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 22px;
  box-shadow: var(--shadow);
}
div[data-testid="stNumberInput"] input { border-radius: 12px !important; }
div[data-testid="stSlider"] > div { padding: 0 4px; }
.stDivider { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════
DEFAULTS = {
    "cart": {}, "orders": [], "page": "landing",
    "user": None, "users": [], "wishlist": [],
    "toast": None, "toast_type": "ok",
    "detail_pid": None, "coupon": None,
    "recently_viewed": [],
}

def load_state():
    try:
        if os.path.exists(STATE_PATH):
            with open(STATE_PATH) as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_state():
    try:
        data = {k: st.session_state.get(k, DEFAULTS[k])
                for k in ["cart","orders","users","wishlist","user","page","recently_viewed"]}
        with open(STATE_PATH, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

_saved = load_state()
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = _saved.get(k, v)

if isinstance(st.session_state.cart, dict):
    st.session_state.cart = {str(k): int(v) for k, v in st.session_state.cart.items()}

# ══════════════════════════════════════════════════════════════
# PRODUCT DATA
# ══════════════════════════════════════════════════════════════
REVIEWS_DB = {
    1: [
        {"name":"Arjun K.", "rating":5, "text":"Insane comfort — wore them on a 10km run. Zero blisters!", "date":"12 Jan 2025", "verified":True, "helpful":24},
        {"name":"Priya S.", "rating":4, "text":"Looks great, slightly heavy but very well-cushioned.", "date":"8 Feb 2025", "verified":True, "helpful":17},
        {"name":"Rohan M.", "rating":5, "text":"Best running shoe I've owned. Width fit is perfect.", "date":"3 Mar 2025", "verified":False, "helpful":9},
    ],
    2: [
        {"name":"Sneha R.", "rating":5, "text":"Ultra Boost lives up to the hype. Energy return is absolutely real.", "date":"20 Jan 2025", "verified":True, "helpful":38},
        {"name":"Vikram P.", "rating":4, "text":"Pricey but worth every rupee. Great for long runs.", "date":"14 Feb 2025", "verified":True, "helpful":21},
    ],
    3: [{"name":"Divya A.", "rating":4, "text":"Chunky look, very trendy. Got so many compliments!", "date":"5 Mar 2025", "verified":True, "helpful":12}],
    4: [{"name":"Karan B.", "rating":5, "text":"Classic never goes out of style. Very clean leather.", "date":"22 Jan 2025", "verified":True, "helpful":19}],
    6: [
        {"name":"Amit T.", "rating":5, "text":"Wore these on a 3-day trek. Completely waterproof, incredible grip.", "date":"10 Feb 2025", "verified":True, "helpful":44},
        {"name":"Neha V.", "rating":4, "text":"Heavy but solid. Perfect for monsoon hikes.", "date":"1 Mar 2025", "verified":True, "helpful":28},
    ],
    8: [
        {"name":"Suresh P.", "rating":5, "text":"The cushioning is next level. My feet don't hurt after 15km anymore.", "date":"5 Jan 2025", "verified":True, "helpful":56},
        {"name":"Ananya B.", "rating":5, "text":"Worth every paisa. The gel technology is real.", "date":"18 Feb 2025", "verified":True, "helpful":33},
    ],
}

@st.cache_data
def load_products():
    return pd.DataFrame([
        {"id":1,  "name":"Nike Air Max 270",       "brand":"Nike",     "price":7999,  "orig":9999,
         "category":"Running",  "rating":4.5, "reviews":1284, "badge":"Bestseller",
         "colors":["Triple Black","Summit White","University Red"],
         "sizes":[6,7,8,9,10,11],
         "desc":"The Nike Air Max 270 delivers unprecedented underfoot cushioning. Its large Air unit is Nike's tallest heel Air bag yet, providing all-day comfort for city exploration and light runs.",
         "image":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700&q=85&fit=crop"},
        {"id":2,  "name":"Adidas Ultra Boost 23",  "brand":"Adidas",   "price":9999,  "orig":12999,
         "category":"Running",  "rating":4.7, "reviews":2561, "badge":"New",
         "colors":["Cloud White","Core Black","Wonder Steel"],
         "sizes":[6,7,8,9,10,11],
         "desc":"The UltraBOOST 23 features a new upper material that adapts to your foot like a second skin. BOOST midsole cushioning returns energy with every single stride.",
         "image":"https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=700&q=85&fit=crop"},
        {"id":3,  "name":"Puma RS-X Runner",       "brand":"Puma",     "price":4999,  "orig":5999,
         "category":"Sports",   "rating":4.2, "reviews":893,  "badge":"",
         "colors":["Multi","White/Black","Electric Blue"],
         "sizes":[7,8,9,10],
         "desc":"The RS-X Runner brings retro-futurism to life with its chunky silhouette and RS cushioning technology. A bold statement in any setting.",
         "image":"https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=700&q=85&fit=crop"},
        {"id":4,  "name":"Reebok Classic Leather",  "brand":"Reebok",   "price":3999,  "orig":4999,
         "category":"Casual",   "rating":4.3, "reviews":741,  "badge":"",
         "colors":["White","Black","Chalk"],
         "sizes":[6,7,8,9,10,11,12],
         "desc":"The Reebok Classic Leather is one of the most iconic sneakers ever made. Supple leather upper with a classic profile that goes with anything.",
         "image":"https://images.unsplash.com/photo-1539185441755-769473a23570?w=700&q=85&fit=crop"},
        {"id":5,  "name":"Bata Formal Derby",      "brand":"Bata",     "price":2999,  "orig":3499,
         "category":"Formal",   "rating":4.0, "reviews":452,  "badge":"",
         "colors":["Black","Cognac Tan","Dark Brown"],
         "sizes":[7,8,9,10,11],
         "desc":"Premium full-grain leather upper with Blake stitch construction for durability. The cushioned footbed ensures comfort through long office hours.",
         "image":"https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=700&q=85&fit=crop"},
        {"id":6,  "name":"Woodland Trekker GTX",   "brand":"Woodland", "price":5499,  "orig":6999,
         "category":"Outdoor",  "rating":4.6, "reviews":1120, "badge":"Top Rated",
         "colors":["Camel Brown","Khaki","Olive Green"],
         "sizes":[7,8,9,10,11],
         "desc":"Gore-Tex waterproof membrane keeps feet completely dry. Vibram outsole delivers unbeatable grip on wet rock, mud, and loose terrain.",
         "image":"https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=700&q=85&fit=crop"},
        {"id":7,  "name":"Sparx Street Lite",      "brand":"Sparx",    "price":1999,  "orig":2499,
         "category":"Casual",   "rating":3.9, "reviews":334,  "badge":"Budget Pick",
         "colors":["Navy/White","All White","Charcoal Grey"],
         "sizes":[6,7,8,9,10],
         "desc":"Lightweight canvas upper with a flexible EVA midsole. The Street Lite is your go-to budget sneaker that doesn't compromise on daily comfort.",
         "image":"https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=700&q=85&fit=crop"},
        {"id":8,  "name":"ASICS Gel-Nimbus 25",    "brand":"ASICS",    "price":8999,  "orig":10999,
         "category":"Running",  "rating":4.8, "reviews":1983, "badge":"",
         "colors":["Indigo Blue","Black","White/Sky"],
         "sizes":[6,7,8,9,10,11,12],
         "desc":"FF BLAST+ cushioning technology delivers an incredibly plush, soft ride. PureGEL technology at the heel provides seamless, soft landings over long distances.",
         "image":"https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=700&q=85&fit=crop"},
        {"id":9,  "name":"Fila Disruptor II",      "brand":"Fila",     "price":4599,  "orig":5499,
         "category":"Casual",   "rating":4.1, "reviews":678,  "badge":"",
         "colors":["Triple White","Triple Black","White/Pink"],
         "sizes":[5,6,7,8,9,10],
         "desc":"The Disruptor II is THE platform sneaker icon. Its serrated rubber outsole and maximalist silhouette make it a bold fashion statement.",
         "image":"https://images.unsplash.com/photo-1584735175315-9d5df23be235?w=700&q=85&fit=crop"},
        {"id":10, "name":"Campus Activ X",         "brand":"Campus",   "price":1599,  "orig":1999,
         "category":"Sports",   "rating":3.8, "reviews":291,  "badge":"",
         "colors":["Blue/White","Red/Black","Green/Grey"],
         "sizes":[7,8,9,10],
         "desc":"Breathable mesh upper keeps air flowing during activity. The rubber outsole provides grip on most surfaces for casual sports use.",
         "image":"https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=700&q=85&fit=crop"},
        {"id":11, "name":"Red Tape Oxford Pro",    "brand":"RedTape",  "price":3499,  "orig":4499,
         "category":"Formal",   "rating":4.2, "reviews":512,  "badge":"",
         "colors":["Cognac","Dark Brown","Oxford Black"],
         "sizes":[7,8,9,10,11],
         "desc":"Brogue detailing on full-grain leather upper for a distinguished formal look. Memory foam insole provides superior all-day comfort.",
         "image":"https://images.unsplash.com/photo-1603487742131-4160ec999306?w=700&q=85&fit=crop"},
        {"id":12, "name":"HRX Training Edge",      "brand":"HRX",      "price":2799,  "orig":3499,
         "category":"Sports",   "rating":4.0, "reviews":423,  "badge":"Sale",
         "colors":["Black/Neon Lime","Black/Red","Steel Grey"],
         "sizes":[7,8,9,10,11],
         "desc":"High-density foam midsole absorbs impact during intense training. Perforated mesh upper promotes airflow keeping your feet cool through any workout.",
         "image":"https://images.unsplash.com/photo-1556906781-9a412961a28c?w=700&q=85&fit=crop"},
    ])

products   = load_products()
CATEGORIES = ["All"] + sorted(products["category"].unique().tolist())
BRANDS     = ["All"] + sorted(products["brand"].unique().tolist())
COUPONS    = {"SHOE10": 10, "NEWUSER": 15, "SALE20": 20, "FIRST50": 50}

# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def nav(page):
    st.session_state.page = page
    save_state()
    st.rerun()

def toast(msg, t="ok"):
    st.session_state.toast      = msg
    st.session_state.toast_type = t

def show_toast():
    if st.session_state.toast:
        cls = "sz-toast-ok" if st.session_state.toast_type == "ok" else "sz-toast-err"
        st.markdown(f'<div class="{cls}">{st.session_state.toast}</div>', unsafe_allow_html=True)
        st.session_state.toast = None

def cart_count():
    return sum(int(v) for v in st.session_state.cart.values())

def cart_subtotal():
    t = 0
    for pid, qty in st.session_state.cart.items():
        row = products[products["id"] == int(pid)]
        if not row.empty:
            t += row.iloc[0]["price"] * int(qty)
    return t

def fmt(p):  return f"₹{int(p):,}"
def stars_h(r, size=13):
    full = int(r); empty = 5 - full
    return f'<span style="color:#f59e0b;font-size:{size}px">{"★"*full}{"☆"*empty}</span>'

def disc_pct(p, o):
    return int((o - p) / o * 100) if o and o > p else 0

BADGE_CLS = {"Bestseller":"b-bestseller","New":"b-new","Top Rated":"b-toprated",
             "Budget Pick":"b-budget","Sale":"b-sale","Exclusive":"b-exclusive"}

def add_to_cart(pid, qty=1):
    if not st.session_state.user:
        toast("Please login to add items to cart", "err")
        nav("login"); return
    key = str(pid)
    st.session_state.cart[key] = int(st.session_state.cart.get(key, 0)) + int(qty)
    save_state()
    toast("Added to cart 🛒")
    st.rerun()

def toggle_wish(pid):
    if not st.session_state.user:
        toast("Login to save to wishlist", "err"); nav("login"); return
    pid_i = int(pid)
    if pid_i in st.session_state.wishlist:
        st.session_state.wishlist.remove(pid_i)
        toast("Removed from wishlist")
    else:
        st.session_state.wishlist.append(pid_i)
        toast("Saved to wishlist ❤️")
    save_state(); st.rerun()

def open_detail(pid):
    st.session_state.detail_pid = int(pid)
    # track recently viewed
    rv = st.session_state.recently_viewed
    if int(pid) not in rv:
        rv.insert(0, int(pid))
        st.session_state.recently_viewed = rv[:8]
    nav("detail")

def coupon_discount(subtotal):
    code = (st.session_state.coupon or "").upper()
    if code in COUPONS:
        return int(subtotal * COUPONS[code] / 100)
    return 0

# ══════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════
def render_navbar():
    cc = cart_count()
    wc = len(st.session_state.wishlist)
    oc = len(st.session_state.orders)

    # Announcement bar
    msgs = [
        "🎉 Use code NEWUSER for 15% off your first order",
        "🚚 Free delivery on all orders above ₹5,000",
        "🔥 SALE20 — Flat 20% off sitewide today only",
    ]
    st.markdown(f'<div class="sz-announce">{random.choice(msgs)}</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sz-nav">'
        '<div class="sz-logo">Shoe<em>Zone</em></div>'
        '<div class="sz-nav-tag">PREMIUM</div>'
        '</div>',
        unsafe_allow_html=True
    )

    c = st.columns([3.5, 1, 1, 1, 1, 1.4, 0.8])
    with c[0]:
        q = st.text_input("", placeholder="🔍  Search — Nike, running, formal…",
                          label_visibility="collapsed", key="nav_q")
    with c[1]:
        if st.button("🏠 Home"):  nav("home")
    with c[2]:
        lbl = f"🛒  {cc}" if cc else "🛒  Cart"
        if st.button(lbl):        nav("cart")
    with c[3]:
        wlbl = f"❤️  {wc}" if wc else "❤️"
        if st.button(wlbl):       nav("wishlist")
    with c[4]:
        olbl = f"📦  {oc}" if oc else "📦"
        if st.button(olbl):       nav("orders")
    with c[5]:
        name = (st.session_state.user or "Guest")[:12]
        st.markdown(f'<div class="sz-nav-user">👤 <b>{name}</b></div>', unsafe_allow_html=True)
    with c[6]:
        if st.button("🚪"):
            st.session_state.user = None; nav("landing")

    return q or ""

# ══════════════════════════════════════════════════════════════
# FILTERS
# ══════════════════════════════════════════════════════════════
def render_filters():
    st.markdown('<div class="sz-filter"><div class="sz-filter-label">🎛 Refine Results</div></div>',
                unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([2, 2, 3, 2, 2])
    with c1:
        cat   = st.selectbox("Category", CATEGORIES, key="f_cat")
    with c2:
        brand = st.selectbox("Brand", BRANDS, key="f_brand")
    with c3:
        pmin, pmax = st.slider("Price Range (₹)", 500, 12000, (500, 12000), step=250, key="f_price")
    with c4:
        min_r = st.slider("Min Rating ⭐", 0.0, 5.0, 0.0, step=0.5, key="f_rating")
    with c5:
        sort  = st.selectbox("Sort By",
                    ["Featured","Price ↑","Price ↓","Top Rated","Most Reviewed"], key="f_sort")
        ncols = st.selectbox("Grid View", [2, 3, 4], index=1, key="f_ncols")
    return cat, brand, (pmin, pmax), min_r, sort, ncols

def apply_filters(df, q, cat, brand, price_range, min_r, sort):
    if q:
        toks = q.lower().split()
        mask = pd.Series([False] * len(df), index=df.index)
        for t in toks:
            mask = mask | df["name"].str.lower().str.contains(t) | \
                          df["brand"].str.lower().str.contains(t) | \
                          df["category"].str.lower().str.contains(t)
        df = df[mask]
    if cat   != "All": df = df[df["category"] == cat]
    if brand != "All": df = df[df["brand"]    == brand]
    pmin, pmax = price_range
    df = df[(df["price"] >= pmin) & (df["price"] <= pmax)]
    df = df[df["rating"] >= min_r]
    sm = {"Price ↑":("price",True),"Price ↓":("price",False),
          "Top Rated":("rating",False),"Most Reviewed":("reviews",False)}
    if sort in sm:
        col, asc = sm[sort]; df = df.sort_values(col, ascending=asc)
    return df.reset_index(drop=True)

# ══════════════════════════════════════════════════════════════
# PRODUCT CARD
# ══════════════════════════════════════════════════════════════
def render_card(row, key_sfx=""):
    pid   = row["id"]
    price = float(row["price"])
    orig  = float(row.get("orig", 0) or 0)
    d     = disc_pct(price, orig)
    wl    = int(pid) in (st.session_state.wishlist or [])
    bdg   = str(row.get("badge", "") or "")
    sizes = row.get("sizes", [])[:4]  # show first 4 sizes

    badge_h = (f'<div class="sz-badge {BADGE_CLS.get(bdg,"")}">{bdg}</div>' if bdg else "")
    free_h  = '<div class="sz-free-tag">🚚 Free delivery</div>' if price >= 5000 else ""
    disc_h  = (f'<span class="sz-price-was">{fmt(orig)}</span>'
               f'<span class="sz-price-off"> −{d}%</span>') if d > 0 else ""
    sizes_h = "".join(f'<div class="sz-sz-dot">{s}</div>' for s in sizes)
    if len(row.get("sizes",[]))>4:
        sizes_h += f'<div class="sz-sz-dot" style="color:#9ca3af">+{len(row["sizes"])-4}</div>'

    st.markdown(f"""
    <div class="sz-card">
      <div class="sz-card-imgwrap">
        <img src="{row['image']}" alt="{row['name']}"
             onerror="this.src='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=70'">
        {badge_h}
        <div class="sz-wish-btn" title="{'Remove from wishlist' if wl else 'Add to wishlist'}">
          {'❤️' if wl else '🤍'}
        </div>
      </div>
      <div class="sz-card-body">
        <div class="sz-card-meta">{row['brand']}  ·  {row['category']}</div>
        <div class="sz-card-name">{row['name']}</div>
        <div>{stars_h(row['rating'])}
          <span class="sz-rcount">({int(row['reviews']):,})</span>
        </div>
        <div class="sz-prices">
          <span class="sz-price-now">{fmt(price)}</span>{disc_h}
        </div>
        {free_h}
        <div class="sz-card-sizes">{sizes_h}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    ca, cb, cc_ = st.columns([5, 2, 2])
    with ca:
        if st.button("🛒 Add to Cart", key=f"atc_{pid}_{key_sfx}", use_container_width=True, type="primary"):
            add_to_cart(pid, 1)
    with cb:
        if st.button("👁 View", key=f"view_{pid}_{key_sfx}", use_container_width=True):
            open_detail(pid)
    with cc_:
        if st.button("❤️" if wl else "🤍", key=f"wl_{pid}_{key_sfx}", use_container_width=True):
            toggle_wish(pid)
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PRODUCT GRID
# ══════════════════════════════════════════════════════════════
def render_grid(df, ncols=3, key_pfx="g"):
    if df.empty:
        st.markdown('<div class="sz-empty"><div class="sz-empty-icon">🔍</div>'
                    '<div class="sz-empty-title">Nothing found</div>'
                    '<div class="sz-empty-sub">Try different keywords or adjust filters</div></div>',
                    unsafe_allow_html=True)
        return
    for i in range(0, len(df), ncols):
        cols = st.columns(ncols)
        for j, (_, row) in enumerate(df.iloc[i:i+ncols].iterrows()):
            with cols[j]:
                render_card(row, key_sfx=f"{key_pfx}_{i}_{j}")

# ══════════════════════════════════════════════════════════════
# PAGE: LANDING
# ══════════════════════════════════════════════════════════════
def page_landing():
    # Announcement
    msgs = ["🎉  Use code NEWUSER — 15% off  ·  Free shipping above ₹5,000  ·  30-day returns"]
    st.markdown(f'<div class="sz-announce">{msgs[0]}</div>', unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="sz-hero">
      <div class="sz-hero-noise"></div>
      <div class="sz-hero-left">
        <div class="sz-hero-label">✦ India's #1 Shoe Destination</div>
        <div class="sz-hero-h1">Step Into<em>Your Style</em></div>
        <div class="sz-hero-sub">
          12,000+ shoes. 50+ brands. Unbeatable prices.<br>
          Free delivery. 30-day returns. Always.
        </div>
        <div class="sz-hero-stats">
          <div class="sz-stat"><div class="sz-stat-num">12K+</div><div class="sz-stat-lbl">Products</div></div>
          <div class="sz-stat"><div class="sz-stat-num">50+</div><div class="sz-stat-lbl">Brands</div></div>
          <div class="sz-stat"><div class="sz-stat-num">4.8★</div><div class="sz-stat-lbl">Rating</div></div>
          <div class="sz-stat"><div class="sz-stat-num">2M+</div><div class="sz-stat-lbl">Customers</div></div>
        </div>
      </div>
      <div class="sz-hero-right">
        <div class="sz-hero-img-frame">
          <div class="sz-hero-shoe-emoji">👟</div>
          <div class="sz-hero-badge sz-hero-badge-1">🔥 Up to 50% OFF</div>
          <div class="sz-hero-badge sz-hero-badge-2">🚚 Free Delivery</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Trust bar
    st.markdown("""
    <div class="sz-trust">
      <div class="sz-trust-item"><span class="sz-trust-icon">🚚</span> Free delivery on ₹5k+</div>
      <div class="sz-trust-item"><span class="sz-trust-icon">↩️</span> 30-day easy returns</div>
      <div class="sz-trust-item"><span class="sz-trust-icon">🔒</span> Secure payments</div>
      <div class="sz-trust-item"><span class="sz-trust-icon">⚡</span> Ships in 24 hrs</div>
      <div class="sz-trust-item"><span class="sz-trust-icon">✅</span> 100% Genuine brands</div>
      <div class="sz-trust-item"><span class="sz-trust-icon">🎁</span> Gift wrapping</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, _, _ = st.columns([1,1,1,1])
    with c1:
        if st.button("🛍️  Shop All Shoes →", use_container_width=True, type="primary"):
            nav("register" if not st.session_state.user else "home")
    with c2:
        if st.button("🔐  Login to Your Account", use_container_width=True):
            nav("login")

    # Deal Banner
    now   = datetime.now()
    end   = now.replace(hour=23, minute=59, second=59)
    delta = end - now
    hrs   = delta.seconds // 3600
    mins  = (delta.seconds % 3600) // 60
    secs  = delta.seconds % 60
    st.markdown(f"""
    <div class="sz-deal-banner">
      <div class="sz-deal-left">
        <div class="sz-deal-eyebrow">⚡ Flash Sale — Today Only</div>
        <div class="sz-deal-title">Up to 50% Off</div>
        <div class="sz-deal-sub">On 200+ premium styles. Use code <b style="color:#f0c060">SALE20</b> for extra 20% off.</div>
      </div>
      <div class="sz-deal-countdown">
        <div class="sz-deal-time"><div class="sz-deal-time-num">{hrs:02d}</div><div class="sz-deal-time-lbl">Hours</div></div>
        <div style="color:#4b5563;font-size:24px;font-weight:800;padding-top:4px">:</div>
        <div class="sz-deal-time"><div class="sz-deal-time-num">{mins:02d}</div><div class="sz-deal-time-lbl">Mins</div></div>
        <div style="color:#4b5563;font-size:24px;font-weight:800;padding-top:4px">:</div>
        <div class="sz-deal-time"><div class="sz-deal-time-num">{secs:02d}</div><div class="sz-deal-time-lbl">Secs</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🔥 Deals Today",     "Up to 50% off")
    m2.metric("📦 Orders Today",    f"{random.randint(520,720)}")
    m3.metric("⭐ Avg Rating",       "4.8 / 5.0")
    m4.metric("🏆 Top Brands",       "Nike, Adidas & more")

    # Featured
    st.markdown('<div class="sz-sh"><div class="sz-sh-title">🔥 Featured Picks</div></div>',
                unsafe_allow_html=True)
    render_grid(products.sample(frac=1, random_state=42).head(6), ncols=3, key_pfx="land")

    # Category showcase
    st.markdown('<div class="sz-sh"><div class="sz-sh-title">Shop by Category</div></div>',
                unsafe_allow_html=True)
    cats = ["Running", "Casual", "Sports", "Formal", "Outdoor"]
    cat_cols = st.columns(len(cats))
    cat_icons = {"Running":"🏃","Casual":"👟","Sports":"⚽","Formal":"👔","Outdoor":"🏕️"}
    for i, cat in enumerate(cats):
        with cat_cols[i]:
            cnt = len(products[products["category"]==cat])
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e8e4db;border-radius:16px;padding:20px 16px;
                        text-align:center;cursor:pointer;transition:all 0.2s;box-shadow:0 2px 8px rgba(0,0,0,0.04)">
              <div style="font-size:32px;margin-bottom:8px">{cat_icons.get(cat,'👟')}</div>
              <div style="font-size:14px;font-weight:800;color:#0a0a0a">{cat}</div>
              <div style="font-size:12px;color:#9ca3af;margin-top:2px">{cnt} styles</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Shop {cat}", key=f"cat_{cat}", use_container_width=True):
                nav("register" if not st.session_state.user else "home")

# ══════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
def page_home(query=""):
    show_toast()
    cat, brand, price_range, min_r, sort, ncols = render_filters()
    filtered = apply_filters(products, query, cat, brand, price_range, min_r, sort)

    active = []
    if cat   != "All": active.append(cat)
    if brand != "All": active.append(brand)
    if min_r >  0:     active.append(f"⭐ {min_r}+")
    chips_html = "".join(f'<span class="sz-active-chip">{a}</span>' for a in active)

    st.markdown(f"""
    <div class="sz-sh">
      <div class="sz-sh-title">All Shoes</div>
      <div class="sz-sh-count">{len(filtered)} results</div>
    </div>
    <div style="margin-bottom:16px">{chips_html}</div>
    """, unsafe_allow_html=True)

    render_grid(filtered, ncols=ncols, key_pfx="home")

    # Recently Viewed
    rv_ids = [i for i in st.session_state.recently_viewed if i not in [row["id"] for _, row in filtered.iterrows()]]
    rv_df  = products[products["id"].isin(rv_ids[:4])].reset_index(drop=True)
    if not rv_df.empty:
        st.markdown('<div class="sz-sh"><div class="sz-sh-title">Recently Viewed</div></div>',
                    unsafe_allow_html=True)
        render_grid(rv_df, ncols=4, key_pfx="rv")

# ══════════════════════════════════════════════════════════════
# PAGE: PRODUCT DETAIL
# ══════════════════════════════════════════════════════════════
def page_detail():
    show_toast()
    pid = st.session_state.get("detail_pid")
    if not pid: nav("home"); return
    row = products[products["id"] == int(pid)]
    if row.empty: nav("home"); return
    p = row.iloc[0]

    price  = float(p["price"])
    orig   = float(p.get("orig", 0) or 0)
    d      = disc_pct(price, orig)
    sizes  = p.get("sizes", [7,8,9,10])
    colors = p.get("colors", [])

    if st.button("← Back"):
        st.session_state.detail_pid = None; nav("home")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sz-detail-wrap">', unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sz-detail-img-box">', unsafe_allow_html=True)
        st.image(p["image"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sz-features-grid">
          <div class="sz-feature-box"><div class="sz-feature-icon">🚚</div><div class="sz-feature-label">Free Delivery</div></div>
          <div class="sz-feature-box"><div class="sz-feature-icon">↩️</div><div class="sz-feature-label">30-Day Return</div></div>
          <div class="sz-feature-box"><div class="sz-feature-icon">✅</div><div class="sz-feature-label">100% Genuine</div></div>
          <div class="sz-feature-box"><div class="sz-feature-icon">🎁</div><div class="sz-feature-label">Gift Ready</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Rating breakdown
        rev_list = REVIEWS_DB.get(int(pid), [])
        if rev_list:
            avg = sum(r["rating"] for r in rev_list) / len(rev_list)
            st.markdown(f"""
            <div style="background:#f4f2ee;border-radius:16px;padding:18px 20px;margin-top:8px">
              <div style="font-size:11px;font-weight:800;color:#b0a89a;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:12px">Rating Breakdown</div>
              <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px">
                <div style="font-size:44px;font-weight:900;color:#0a0a0a;line-height:1">{avg:.1f}</div>
                <div>
                  <div>{stars_h(avg, 18)}</div>
                  <div style="font-size:12px;color:#9ca3af;margin-top:4px">{len(rev_list)} reviews</div>
                </div>
              </div>
              {"".join(f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px"><span style="font-size:11px;color:#6b7280;width:12px">{5-i}</span><div style="flex:1;background:#e8e4db;border-radius:999px;height:6px"><div style="background:#f59e0b;width:{random.randint(30,100)}%;height:6px;border-radius:999px"></div></div></div>' for i in range(5))}
            </div>
            """, unsafe_allow_html=True)

    with right:
        bdg = str(p.get("badge","") or "")
        if bdg:
            st.markdown(f'<span class="sz-badge {BADGE_CLS.get(bdg,"")}" '
                        f'style="position:static;margin-bottom:14px;display:inline-block">{bdg}</span>',
                        unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sz-detail-brand">{p['brand']}  ·  {p['category']}</div>
        <div class="sz-detail-name">{p['name']}</div>
        <div>{stars_h(p['rating'], 16)}
          <span style="color:#b0a89a;font-size:13px;margin-left:8px">{p['rating']} · {int(p['reviews']):,} reviews</span>
        </div>
        <div style="margin-top:20px;display:flex;align-items:baseline;gap:4px;flex-wrap:wrap">
          <span class="sz-detail-price-now">{fmt(price)}</span>
          {"<span class='sz-detail-price-was'>" + fmt(orig) + "</span><span class='sz-detail-off'>−" + str(d) + "% OFF</span>" if d > 0 else ""}
        </div>
        {"<div style='font-size:13px;color:#0d7a4e;font-weight:700;margin-top:6px'>🎉 You save " + fmt(orig-price) + "!</div>" if d > 0 else ""}
        """, unsafe_allow_html=True)

        # EMI
        emi = int(price / 6)
        st.markdown(f"""
        <div style="background:#f4f2ee;border-radius:12px;padding:12px 16px;margin-top:14px;display:inline-block">
          <span style="font-size:13px;color:#4b5563">💳 EMI from <b style="color:#0a0a0a">₹{emi:,}/mo</b> · No Cost EMI available</span>
        </div>
        """, unsafe_allow_html=True)

        # Colors
        if colors:
            st.markdown("<div style='margin-top:20px;font-size:11px;font-weight:800;color:#b0a89a;text-transform:uppercase;letter-spacing:0.14em'>Available Colors</div>",
                        unsafe_allow_html=True)
            c_html = "".join(
                f'<span style="background:#f4f2ee;border:1px solid #e8e4db;padding:5px 14px;border-radius:999px;'
                f'font-size:12px;font-weight:700;color:#374151;margin:4px 4px 0 0;display:inline-block">{c}</span>'
                for c in colors
            )
            st.markdown(f'<div style="margin-top:8px">{c_html}</div>', unsafe_allow_html=True)

        # Size selector
        st.markdown("<div style='margin-top:22px;font-size:11px;font-weight:800;color:#b0a89a;text-transform:uppercase;letter-spacing:0.14em'>Select Size (UK)</div>",
                    unsafe_allow_html=True)
        size_key = f"sz_{pid}"
        if size_key not in st.session_state:
            st.session_state[size_key] = None

        sc = st.columns(min(len(sizes), 7))
        for si, sz in enumerate(sizes):
            with sc[si % len(sc)]:
                is_sel = st.session_state[size_key] == sz
                lbl = f"**{sz}**" if is_sel else str(sz)
                if st.button(lbl, key=f"sz_{pid}_{sz}"):
                    st.session_state[size_key] = sz; st.rerun()
        selected_size = st.session_state.get(size_key)
        if selected_size:
            st.markdown(f"<div style='font-size:12px;color:#0d7a4e;font-weight:700;margin-top:4px'>✅ Size UK {selected_size} selected</div>",
                        unsafe_allow_html=True)

        # Description
        if p.get("desc"):
            st.markdown(f"""
            <div style="margin-top:22px;background:#f4f2ee;border-radius:16px;padding:18px 20px">
              <div style="font-size:11px;font-weight:800;color:#b0a89a;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px">About This Shoe</div>
              <div style="font-size:14px;color:#374151;line-height:1.75">{p['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, key=f"dqty_{pid}")

        ca, cb = st.columns(2)
        with ca:
            if st.button("🛒 Add to Cart", use_container_width=True, type="primary", key=f"datc_{pid}"):
                if not selected_size:
                    toast("Please select a size first!", "err"); st.rerun()
                else:
                    add_to_cart(pid, int(qty))
        with cb:
            wl    = int(pid) in (st.session_state.wishlist or [])
            heart = "❤️ Saved" if wl else "🤍 Save"
            if st.button(heart, use_container_width=True, key=f"dwl_{pid}"):
                toggle_wish(pid)

        st.markdown("""
        <div style="margin-top:16px;display:flex;gap:16px;font-size:12px;font-weight:600;color:#6b7280">
          <span>🔒 Secure Checkout</span>
          <span>✅ 100% Genuine</span>
          <span>📞 24/7 Support</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Reviews
    st.markdown('<div class="sz-sh" style="margin-top:36px"><div class="sz-sh-title">Customer Reviews</div></div>',
                unsafe_allow_html=True)
    revs = REVIEWS_DB.get(int(pid), [])
    if revs:
        for rv in revs:
            st.markdown(f"""
            <div class="sz-review">
              <div class="sz-review-head">
                <div>
                  <div class="sz-review-name">{rv['name']}</div>
                  <div style="margin-top:3px">{stars_h(rv['rating'], 13)}</div>
                </div>
                <div class="sz-review-date">{rv['date']}</div>
              </div>
              <div class="sz-review-text">"{rv['text']}"</div>
              {"<div class='sz-review-verified'>✅ Verified Purchase</div>" if rv.get('verified') else ""}
              <div class="sz-review-helpful">👍 {rv.get('helpful',0)} people found this helpful</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#b0a89a;font-size:14px;padding:16px 0'>No reviews yet — be the first to review!</div>",
                    unsafe_allow_html=True)

    # Similar
    sim = products[(products["category"]==p["category"]) & (products["id"]!=int(pid))].head(3)
    if not sim.empty:
        st.markdown('<div class="sz-sh" style="margin-top:36px"><div class="sz-sh-title">You May Also Like</div></div>',
                    unsafe_allow_html=True)
        render_grid(sim.reset_index(drop=True), ncols=3, key_pfx=f"sim_{pid}")

# ══════════════════════════════════════════════════════════════
# PAGE: WISHLIST
# ══════════════════════════════════════════════════════════════
def page_wishlist():
    show_toast()
    wc = len(st.session_state.wishlist)
    st.markdown(f'<div class="sz-sh"><div class="sz-sh-title">❤️ My Wishlist</div>'
                f'<div class="sz-sh-count">{wc} item{"s" if wc!=1 else ""}</div></div>',
                unsafe_allow_html=True)
    if not wc:
        st.markdown('<div class="sz-empty"><div class="sz-empty-icon">🤍</div>'
                    '<div class="sz-empty-title">Your wishlist is empty</div>'
                    '<div class="sz-empty-sub">Tap 🤍 on any shoe to save it here</div></div>',
                    unsafe_allow_html=True)
        if st.button("Browse Shoes", type="primary"): nav("home")
        return
    wdf = products[products["id"].isin(st.session_state.wishlist)].reset_index(drop=True)
    render_grid(wdf, ncols=3, key_pfx="wl")

# ══════════════════════════════════════════════════════════════
# PAGE: CART
# ══════════════════════════════════════════════════════════════
def page_cart():
    show_toast()
    cc = cart_count()
    st.markdown(f'<div class="sz-sh"><div class="sz-sh-title">🛒 Your Cart</div>'
                f'<div class="sz-sh-count">{cc} item{"s" if cc!=1 else ""}</div></div>',
                unsafe_allow_html=True)

    if not st.session_state.cart:
        st.markdown('<div class="sz-empty"><div class="sz-empty-icon">🛒</div>'
                    '<div class="sz-empty-title">Your cart is empty</div>'
                    '<div class="sz-empty-sub">Discover shoes you\'ll love!</div></div>',
                    unsafe_allow_html=True)
        if st.button("Start Shopping", type="primary"): nav("home")
        return

    left, right = st.columns([3, 1], gap="large")
    to_remove = []

    with left:
        for pid, qty in list(st.session_state.cart.items()):
            row = products[products["id"] == int(pid)]
            if row.empty: continue
            p   = row.iloc[0]
            qty = int(qty)

            st.markdown(f'<div class="sz-cart-item">', unsafe_allow_html=True)
            ic, nc, bc = st.columns([1, 3, 2])
            with ic:
                st.image(p["image"], use_container_width=True)
            with nc:
                st.markdown(f"""
                <div class="sz-cart-name">{p['name']}</div>
                <div class="sz-cart-meta">{p['brand']} · {p['category']}</div>
                <div class="sz-cart-price">{fmt(p['price']*qty)}</div>
                """, unsafe_allow_html=True)
                st.caption(f"Unit: {fmt(p['price'])}")
            with bc:
                r1, r2, r3 = st.columns([1,1,1])
                with r1:
                    if st.button("−", key=f"m_{pid}"):
                        if int(st.session_state.cart[pid]) > 1:
                            st.session_state.cart[pid] = int(st.session_state.cart[pid]) - 1
                        else: to_remove.append(pid)
                        save_state(); st.rerun()
                with r2:
                    st.markdown(f"<div style='text-align:center;font-size:22px;font-weight:900;padding-top:2px'>{qty}</div>",
                                unsafe_allow_html=True)
                with r3:
                    if st.button("+", key=f"p_{pid}"):
                        st.session_state.cart[pid] = int(st.session_state.cart[pid]) + 1
                        save_state(); st.rerun()
                if st.button("🗑 Remove", key=f"rm_{pid}", use_container_width=True):
                    to_remove.append(pid); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        for pid in to_remove:
            st.session_state.cart.pop(pid, None)
        if to_remove: save_state(); st.rerun()

    with right:
        subtotal = cart_subtotal()
        c_disc   = coupon_discount(subtotal)
        after_c  = subtotal - c_disc
        delivery = 0 if after_c >= 5000 else 99
        grand    = after_c + delivery

        # Free delivery progress
        if delivery > 0:
            needed = 5000 - after_c
            pct    = min(int(after_c / 5000 * 100), 100)
            st.markdown(f"""
            <div style="background:#f4f2ee;border-radius:14px;padding:14px 16px;margin-bottom:16px">
              <div style="font-size:12px;font-weight:700;color:#374151;margin-bottom:8px">
                🚚 Add <b style="color:#0a0a0a">{fmt(needed)}</b> more for free delivery!
              </div>
              <div class="sz-progress"><div class="sz-progress-fill" style="width:{pct}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

        free_l   = '<div class="sz-panel-free">🎉 Free delivery applied!</div>' if delivery == 0 else ""
        coup_l   = (f'<div class="sz-panel-row"><span>Coupon ({st.session_state.coupon})</span>'
                    f'<span style="color:#34d399">−{fmt(c_disc)}</span></div>') if c_disc else ""

        st.markdown(f"""
        <div class="sz-panel">
          <div class="sz-panel-title">Order Summary</div>
          <div class="sz-panel-row"><span>Subtotal ({cart_count()} items)</span><span>{fmt(subtotal)}</span></div>
          {coup_l}
          <div class="sz-panel-row"><span>Delivery</span>
            <span style="color:#34d399">{'FREE' if delivery==0 else fmt(delivery)}</span></div>
          {free_l}
          <div class="sz-panel-div"></div>
          <div class="sz-panel-total"><span>Total</span><span>{fmt(grand)}</span></div>
          <div class="sz-coupon-hint">
            <div style="font-size:10px;font-weight:700;color:#4b5563;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px">💡 Available Coupons</div>
            <div style="font-size:12px;color:#9ca3af;line-height:2">
              <span class="sz-coupon-code">SHOE10</span> — 10% off &nbsp;
              <span class="sz-coupon-code">NEWUSER</span> — 15% off<br>
              <span class="sz-coupon-code">SALE20</span> — 20% off &nbsp;
              <span class="sz-coupon-code">FIRST50</span> — 50% off
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        coupon_input = st.text_input("🎟 Enter Coupon Code", placeholder="e.g. SALE20",
                                     value=st.session_state.coupon or "")
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("Apply", use_container_width=True):
                code = coupon_input.strip().upper()
                if code in COUPONS:
                    st.session_state.coupon = code
                    toast(f"✅ {code} applied — {COUPONS[code]}% off!"); st.rerun()
                else:
                    toast("❌ Invalid coupon code", "err"); st.rerun()
        with c_btn2:
            if st.session_state.coupon and st.button("Remove", use_container_width=True):
                st.session_state.coupon = None; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Checkout →", use_container_width=True, type="primary"):
            nav("checkout")
        if st.button("← Keep Shopping", use_container_width=True):
            nav("home")

# ══════════════════════════════════════════════════════════════
# PAGE: CHECKOUT
# ══════════════════════════════════════════════════════════════
def page_checkout():
    show_toast()
    st.markdown('<div class="sz-sh"><div class="sz-sh-title">💳 Secure Checkout</div></div>',
                unsafe_allow_html=True)
    if not st.session_state.cart: st.warning("Cart is empty!"); nav("home"); return

    subtotal = cart_subtotal()
    c_disc   = coupon_discount(subtotal)
    after_c  = subtotal - c_disc
    delivery = 0 if after_c >= 5000 else 99
    grand    = after_c + delivery

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("#### 📦 Order Items")
        for pid, qty in st.session_state.cart.items():
            row = products[products["id"] == int(pid)]
            if row.empty: continue
            p = row.iloc[0]
            st.markdown(f"""
            <div class="sz-order-item">
              <img class="sz-order-img" src="{p['image']}" alt="{p['name']}"
                   onerror="this.src='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&q=60'">
              <div>
                <div class="sz-order-item-name">{p['name']}</div>
                <div class="sz-order-item-sub">{p['brand']} · Qty {qty}</div>
              </div>
              <div class="sz-order-item-price">{fmt(p['price']*int(qty))}</div>
            </div>
            """, unsafe_allow_html=True)

        coup_h = f'<div class="sz-panel-row"><span>Coupon</span><span style="color:#34d399">−{fmt(c_disc)}</span></div>' if c_disc else ""
        st.markdown(f"""
        <div class="sz-panel" style="margin-top:16px">
          <div class="sz-panel-row"><span>Subtotal</span><span>{fmt(subtotal)}</span></div>
          {coup_h}
          <div class="sz-panel-row"><span>Delivery</span>
            <span style="color:#34d399">{'FREE' if delivery==0 else fmt(delivery)}</span></div>
          <div class="sz-panel-div"></div>
          <div class="sz-panel-total"><span>Total Payable</span><span>{fmt(grand)}</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📍 Delivery Address")
        addr = st.text_area("", placeholder="Flat / House No., Street, Locality, City, State, PIN Code",
                            height=110, label_visibility="collapsed", key="co_addr")

    with right:
        st.markdown("#### 💰 Payment Method")
        method = st.radio("", ["💵 Cash on Delivery","📱 UPI","💳 Card","🏦 Net Banking"],
                          label_visibility="collapsed")

        if "UPI" in method:
            st.markdown("""
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;
                        padding:12px 16px;margin-bottom:14px;font-size:13px;color:#1e40af;font-weight:600">
              💡 Supports GPay, PhonePe, Paytm, BHIM, Amazon Pay & all UPI apps
            </div>""", unsafe_allow_html=True)
            upi = st.text_input("UPI ID", placeholder="yourname@okaxis or @ybl")
            if st.button(f"Pay  {fmt(grand)}  →", use_container_width=True, type="primary"):
                if "@" not in upi:   toast("❌ Enter a valid UPI ID", "err"); st.rerun()
                elif not addr:       toast("❌ Enter delivery address", "err"); st.rerun()
                else: complete_order(grand)

        elif "Card" in method:
            card    = st.text_input("Card Number", placeholder="•••• •••• •••• ••••", max_chars=16)
            ec1, ec2 = st.columns(2)
            with ec1: expiry = st.text_input("Expiry (MM/YY)", placeholder="12/27")
            with ec2: cvv    = st.text_input("CVV", type="password", max_chars=3, placeholder="•••")
            name_on = st.text_input("Name on Card", placeholder="As printed on card")
            if st.button(f"Pay  {fmt(grand)}  →", use_container_width=True, type="primary"):
                if not card.isdigit() or len(card)!=16: toast("❌ Invalid card number (16 digits)", "err"); st.rerun()
                elif not cvv.isdigit()  or len(cvv)!=3:  toast("❌ Invalid CVV (3 digits)", "err"); st.rerun()
                elif not name_on:  toast("❌ Enter name on card", "err"); st.rerun()
                elif not addr:     toast("❌ Enter delivery address", "err"); st.rerun()
                else: complete_order(grand)

        elif "Net Banking" in method:
            bank = st.selectbox("Select Your Bank",
                                ["— Select —","SBI","HDFC Bank","ICICI Bank","Axis Bank",
                                 "Kotak Bank","PNB","Bank of Baroda","Other"])
            if st.button(f"Pay  {fmt(grand)}  →", use_container_width=True, type="primary"):
                if bank == "— Select —": toast("❌ Select your bank", "err"); st.rerun()
                elif not addr:           toast("❌ Enter delivery address", "err"); st.rerun()
                else: complete_order(grand)

        else:
            st.markdown("""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;
                        padding:16px 18px;margin-bottom:16px">
              <div style="font-weight:800;font-size:14px;color:#14532d;margin-bottom:4px">Cash on Delivery</div>
              <div style="font-size:13px;color:#0d7a4e">Pay in cash when your order arrives. No advance payment required.</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Place Order  ({fmt(grand)})  →", use_container_width=True, type="primary"):
                if not addr: toast("❌ Enter delivery address", "err"); st.rerun()
                else: complete_order(grand)

        st.markdown("""
        <div style="margin-top:20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap">
          <span style="font-size:12px;font-weight:700;color:#9ca3af">🔒 SSL Encrypted</span>
          <span style="font-size:12px;font-weight:700;color:#9ca3af">🛡️ Buyer Protection</span>
          <span style="font-size:12px;font-weight:700;color:#9ca3af">✅ 100% Genuine</span>
        </div>
        """, unsafe_allow_html=True)

def complete_order(total):
    oid  = f"SZ{len(st.session_state.orders)+1:04d}"
    est  = (datetime.now() + timedelta(days=random.randint(3,6))).strftime("%d %b %Y")
    st.session_state.orders.append({
        "id": oid,
        "items": dict(st.session_state.cart),
        "total": total,
        "date":  datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "est_delivery": est,
    })
    st.session_state.cart   = {}
    st.session_state.coupon = None
    st.balloons()
    toast(f"🎉 Order #{oid} confirmed! Estimated delivery: {est}", "ok")
    save_state()
    nav("orders")

# ══════════════════════════════════════════════════════════════
# PAGE: ORDERS
# ══════════════════════════════════════════════════════════════
TRACK_STEPS = ["Placed","Confirmed","Shipped","Out for Delivery","Delivered"]

def page_orders():
    show_toast()
    cnt = len(st.session_state.orders)
    st.markdown(f'<div class="sz-sh"><div class="sz-sh-title">📦 My Orders</div>'
                f'<div class="sz-sh-count">{cnt} order{"s" if cnt!=1 else ""}</div></div>',
                unsafe_allow_html=True)

    if not cnt:
        st.markdown('<div class="sz-empty"><div class="sz-empty-icon">📦</div>'
                    '<div class="sz-empty-title">No orders yet</div>'
                    '<div class="sz-empty-sub">Place your first order today!</div></div>',
                    unsafe_allow_html=True)
        if st.button("Start Shopping", type="primary"): nav("home")
        return

    for order in reversed(st.session_state.orders):
        est = order.get("est_delivery", "3–6 business days")
        st.markdown(f"""
        <div class="sz-order-card">
          <div class="sz-order-head">
            <div>
              <div class="sz-order-id">#{order['id']}</div>
              <div class="sz-order-date">🕐 Placed: {order['date']}</div>
            </div>
            <div>
              <div class="sz-order-status status-delivered">✅ Delivered</div>
              <div style="font-size:11px;color:#9ca3af;margin-top:6px;text-align:right">Est: {est}</div>
            </div>
          </div>
          <div style="margin:18px 0">
        """, unsafe_allow_html=True)

        for pid, qty in order["items"].items():
            row = products[products["id"] == int(pid)]
            if row.empty: continue
            p = row.iloc[0]
            st.markdown(f"""
            <div class="sz-order-item">
              <img class="sz-order-img" src="{p['image']}" alt="{p['name']}"
                   onerror="this.src='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&q=60'">
              <div>
                <div class="sz-order-item-name">{p['name']}</div>
                <div class="sz-order-item-sub">{p['brand']} · Qty {qty}</div>
              </div>
              <div class="sz-order-item-price">{fmt(p['price']*int(qty))}</div>
            </div>
            """, unsafe_allow_html=True)

        # Tracking
        steps_html = ""
        for i, step in enumerate(TRACK_STEPS):
            dot_cls = "done" if i < 4 else "active"
            lbl_cls = "done" if i < 4 else "active"
            line    = (f'<div class="sz-track-line {"done" if i<4 else ""}"></div>'
                       if i < len(TRACK_STEPS)-1 else "")
            steps_html += (f'<div class="sz-track-step">'
                           f'<div style="position:relative"><div class="sz-track-dot {dot_cls}"></div>{line}</div>'
                           f'<div class="sz-track-label {lbl_cls}">{step}</div>'
                           f'</div>')

        st.markdown(f"""
          </div>
          <div style="border-top:1px solid #f4f2ee;padding-top:14px;
                      display:flex;justify-content:space-between;font-size:18px;font-weight:900;color:#0a0a0a;margin-bottom:4px">
            <span>Total Paid</span><span>{fmt(order['total'])}</span>
          </div>
          <div class="sz-track">{steps_html}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: REGISTER
# ══════════════════════════════════════════════════════════════
def page_register():
    show_toast()
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown("""
        <div class="sz-auth-brand">Shoe<em>Zone</em></div>
        <div class="sz-auth-sub">Create your free account and step into style</div>
        <div class="sz-auth-card">
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full Name *",       placeholder="Rahul Sharma")
            phone    = st.text_input("Phone Number *",    placeholder="10-digit mobile")
            password = st.text_input("Password *",        type="password", placeholder="Min 6 characters")
        with c2:
            email    = st.text_input("Email Address *",   placeholder="you@email.com")
            address  = st.text_area("Delivery Address *", placeholder="Street, City, State, PIN", height=108)
            confirm  = st.text_input("Confirm Password *", type="password")

        if st.button("✅  Create My Account", use_container_width=True, type="primary"):
            errs = []
            if not all([name,email,phone,address,password,confirm]): errs.append("All fields are required")
            if email and "@" not in email:                            errs.append("Enter a valid email address")
            if phone and (not phone.isdigit() or len(phone)!=10):    errs.append("Phone must be exactly 10 digits")
            if password and len(password) < 6:                       errs.append("Password must be at least 6 characters")
            if password and confirm and password != confirm:          errs.append("Passwords do not match")
            if any(u["email"]==email for u in st.session_state.users): errs.append("Email already registered")
            if errs:
                for e in errs: st.error(e)
            else:
                st.session_state.users.append({"name":name,"email":email,"password":password})
                toast("🎉 Account created! Welcome to ShoeZone — please login.", "ok")
                save_state(); nav("login")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _, lc, _ = st.columns([1,2,1])
        with lc:
            if st.button("Already have an account? Login →", use_container_width=True):
                nav("login")

# ══════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ══════════════════════════════════════════════════════════════
def page_login():
    show_toast()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="sz-auth-brand">Shoe<em>Zone</em></div>
        <div class="sz-auth-sub">Welcome back — login to continue</div>
        <div class="sz-auth-card">
        """, unsafe_allow_html=True)

        email    = st.text_input("Email Address", placeholder="you@email.com")
        password = st.text_input("Password",      type="password")

        if st.button("Login →", use_container_width=True, type="primary"):
            user = next((u for u in st.session_state.users
                         if u["email"]==email and u["password"]==password), None)
            if user:
                st.session_state.user = user["name"]
                toast(f"👋 Welcome back, {user['name'].split()[0]}!", "ok")
                save_state(); nav("home")
            else:
                st.error("❌ Incorrect email or password")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 Don't have an account? Register first — it's free!")
        _, lc, _ = st.columns([1,2,1])
        with lc:
            if st.button("Create Free Account →", use_container_width=True):
                nav("register")

# ══════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════
pg = st.session_state.page

if pg == "landing":
    page_landing()
elif pg == "register":
    page_register()
elif pg == "login":
    page_login()
else:
    search_q = render_navbar()
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if   pg == "home":     page_home(search_q)
    elif pg == "cart":     page_cart()
    elif pg == "checkout": page_checkout()
    elif pg == "orders":   page_orders()
    elif pg == "wishlist": page_wishlist()
    elif pg == "detail":   page_detail()
    else:                  nav("home")

save_state()
