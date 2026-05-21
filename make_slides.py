"""
Generate a 3-slide PowerPoint summary of the HTSplotter analysis.
Run: python make_slides.py
Output: HTSplotter_Summary.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Colour palette ─────────────────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x1A, 0x37, 0x5E)
MID_BLUE    = RGBColor(0x2E, 0x75, 0xB6)
LIGHT_BLUE  = RGBColor(0xBD, 0xD7, 0xEE)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY  = RGBColor(0xF2, 0xF2, 0xF2)
GREEN       = RGBColor(0x37, 0x96, 0x37)
ORANGE      = RGBColor(0xC5, 0x5A, 0x11)
PURPLE      = RGBColor(0x70, 0x30, 0xA0)
TEAL        = RGBColor(0x1F, 0x86, 0x78)
TEXT_DARK   = RGBColor(0x1A, 0x1A, 0x1A)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


# ── Helpers ────────────────────────────────────────────────────────────────
def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, l, t, w, h, fill=None, line=None, lw=0):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = line; s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    return s

def txt(slide, text, l, t, w, h, size=13, bold=False, color=TEXT_DARK,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return tb

def para(tf, text, size=12, bold=False, color=TEXT_DARK,
         before=5, italic=False, align=PP_ALIGN.LEFT):
    p = tf.add_paragraph(); p.alignment = align; p.space_before = Pt(before)
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return p

def footer(slide, n):
    box(slide, 0, 7.3, 13.33, 0.2, fill=DARK_BLUE)
    txt(slide, f"Slide {n} of 3", 11.5, 7.3, 1.7, 0.2,
        size=9, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1 — Title, HTSplotter overview, citation
# ══════════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank)
bg(s1, DARK_BLUE)
box(s1, 0, 0, 13.33, 0.12, fill=MID_BLUE)

txt(s1, "HTSplotter Analysis Summary",
    0.5, 0.75, 12.3, 1.1, size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s1, "All Example Datasets  |  MCF7 Cells  |  Confluency Readout  |  + AI Chat Interface",
    0.5, 1.85, 12.3, 0.5, size=18, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
box(s1, 1.5, 2.5, 10.33, 0.04, fill=MID_BLUE)

# Left — about HTSplotter
box(s1, 0.4, 2.65, 7.9, 3.7, fill=RGBColor(0x0F, 0x23, 0x40))
tb = s1.shapes.add_textbox(Inches(0.6), Inches(2.7), Inches(7.5), Inches(3.55))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "About HTSplotter"
r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = LIGHT_BLUE

para(tf, "HTSplotter is an open-source Python tool for end-to-end processing, "
         "analysis, and visualisation of chemical and genetic in vitro perturbation screens. "
         "It automates dose-response fitting, IC value calculation, and synergy scoring "
         "(Bliss, HSA, ZIP) across four experiment types:",
    size=12, color=WHITE, before=8)

for label, desc, col in [
    ("Drug screen",               "Single-agent dose-response, IC values, growth rates", MID_BLUE),
    ("Drug combination",          "Synergy scoring (Bliss/HSA/ZIP) over 7×7 dose matrices", MID_BLUE),
    ("Genetic perturbagen",       "siRNA/shRNA screen, normalised confluency + growth rates", MID_BLUE),
    ("Genetic-chemical",          "Combined gene-knockdown + drug treatment", MID_BLUE),
]:
    p2 = tf.add_paragraph(); p2.space_before = Pt(4)
    r1 = p2.add_run(); r1.text = f"  ●  {label}: "
    r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = col
    r2 = p2.add_run(); r2.text = desc
    r2.font.size = Pt(11); r2.font.color.rgb = WHITE

para(tf, "●  Web tool: htsplotter.cmgg.be\n●  GitHub: github.com/CBIGR/HTSplotter",
    size=11, color=LIGHT_BLUE, before=10)

# Right — citation
box(s1, 8.6, 2.65, 4.45, 3.7, fill=RGBColor(0x0F, 0x23, 0x40))
tb2 = s1.shapes.add_textbox(Inches(8.8), Inches(2.7), Inches(4.1), Inches(3.55))
tf2 = tb2.text_frame; tf2.word_wrap = True
p2 = tf2.paragraphs[0]
r2 = p2.add_run(); r2.text = "Citation"
r2.font.size = Pt(18); r2.font.bold = True; r2.font.color.rgb = LIGHT_BLUE

para(tf2, "Nunes C, Anckaert J, De Vloed F, De Wyn J, "
          "Durinck K, Vandesompele J, Speleman F, Vermeirssen V.",
    size=11, color=WHITE, before=8)
para(tf2, "HTSplotter: An end-to-end data processing, analysis and visualisation "
          "tool for chemical and genetic in vitro perturbation screening.",
    size=11, bold=True, color=WHITE, before=6)
para(tf2, "PLoS One. 2024;19(1):e0296322",
    size=11, italic=True, color=LIGHT_BLUE, before=6)
para(tf2, "DOI: 10.1371/journal.pone.0296322",
    size=11, color=LIGHT_BLUE, before=4)
para(tf2, "PMID: 38181013", size=11, color=LIGHT_BLUE, before=2)

footer(s1, 1)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2 — Drug screen & combination results
# ══════════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank)
bg(s2, WHITE)
box(s2, 0, 0, 13.33, 0.9, fill=DARK_BLUE)
txt(s2, "Drug Screen & Combination Results  —  MCF7 / 72 h",
    0.3, 0.15, 12.5, 0.6, size=24, bold=True, color=WHITE)

# ── LEFT: single-agent IC50 table ───────────────────────────────────────────
txt(s2, "Single-Agent Dose-Response  (1 time point)", 0.3, 1.0, 6.2, 0.38,
    size=14, bold=True, color=DARK_BLUE)

col_w  = [1.9, 1.35, 0.85, 1.3]
col_x  = [0.3, 2.2, 3.55, 4.4]
hdrs   = ["Drug", "IC₅₀ (nM)", "R²", "Fit"]
for i, (hd, cx) in enumerate(zip(hdrs, col_x)):
    box(s2, cx, 1.42, col_w[i], 0.38, fill=DARK_BLUE)
    txt(s2, hd, cx+0.05, 1.46, col_w[i]-0.1, 0.3,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ("Prexasertib", "9.98",   "0.967", "Good",      GREEN,     True),
    ("BAY1895344",  "272.87", "0.957", "Good",      TEXT_DARK, False),
    ("MK-1775",     "657.30", "0.989", "Excellent", TEXT_DARK, False),
]
for ri, (drug, ic50, r2, fit, badge_col, highlight) in enumerate(rows):
    y = 1.8 + ri * 0.55
    row_fill = RGBColor(0xE2, 0xEF, 0xDA) if highlight else (LIGHT_GREY if ri % 2 else WHITE)
    for ci, (val, cx) in enumerate(zip([drug, ic50, r2, fit], col_x)):
        box(s2, cx, y, col_w[ci], 0.52,
            fill=row_fill, line=RGBColor(0xCC, 0xCC, 0xCC), lw=0.5)
        txt(s2, val, cx+0.06, y+0.08, col_w[ci]-0.1, 0.38,
            size=12 if ci != 1 else 13,
            bold=(ci == 0),
            color=badge_col if ci == 0 and highlight else TEXT_DARK,
            align=PP_ALIGN.CENTER if ci > 0 else PP_ALIGN.LEFT)

# Most potent badge
box(s2, 5.0, 1.83, 1.5, 0.38, fill=GREEN)
txt(s2, "★ Most Potent", 5.02, 1.85, 1.46, 0.34,
    size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Multi-timepoint note
box(s2, 0.3, 3.5, 5.7, 0.55,
    fill=RGBColor(0xEF, 0xF4, 0xFB), line=MID_BLUE, lw=1)
txt(s2, "📈  Multi-timepoint datasets (37 time points, 74 h) also analysed — "
        "IC values and growth rates computed at each time point, showing potency "
        "increases over time for all three drugs.",
    0.4, 3.55, 5.5, 0.45, size=10, color=DARK_BLUE)

# Key takeaways box
box(s2, 0.3, 4.15, 5.7, 2.8,
    fill=RGBColor(0xF5, 0xF9, 0xFF), line=MID_BLUE, lw=1)
txt(s2, "Key Takeaways", 0.5, 4.22, 4.0, 0.35,
    size=14, bold=True, color=DARK_BLUE)
tb3 = s2.shapes.add_textbox(Inches(0.5), Inches(4.63), Inches(5.3), Inches(2.2))
tf3 = tb3.text_frame; tf3.word_wrap = True; first = True
for tk in [
    "Prexasertib is ~27× more potent than BAY1895344 and ~66× more potent than MK-1775 in MCF7 cells.",
    "Prexasertib's curve plateaus at ~40–50% inhibition — did not reach full inhibition across the tested range.",
    "MK-1775 has the best curve fit (R² = 0.989), indicating a clean sigmoidal dose-response.",
    "Growth rate analysis (multi-timepoint) confirms sustained inhibition with increasing effect over 74 h.",
]:
    p = tf3.paragraphs[0] if first else tf3.add_paragraph()
    first = False; p.space_before = Pt(5)
    r = p.add_run(); r.text = "▶  " + tk
    r.font.size = Pt(11); r.font.color.rgb = TEXT_DARK

# ── RIGHT: Combination synergy ───────────────────────────────────────────────
txt(s2, "Drug Combination Synergy  —  Bliss Model", 6.35, 1.0, 6.6, 0.38,
    size=14, bold=True, color=DARK_BLUE)

for label, badge, badge_fill, scores, y0 in [
    ("MK-1775  +  Prexasertib", "SYNERGISTIC",    GREEN,
     ["Max Bliss: +0.56  (MK-1775 1235 nM + Prexasertib 4.7 nM)",
      "Strong synergy at mid-range MK-1775 (137–1235 nM) with low Prexasertib",
      "Effect diminishes at saturating MK-1775 doses — ceiling effect"],
     1.42),
    ("MK-1775  +  BAY1895344",  "WEAK / ADDITIVE", ORANGE,
     ["Max Bliss: +0.42  (MK-1775 137 nM + BAY1895344 167 nM)",
      "Most scores near zero — interaction is largely additive",
      "No consistent synergy pattern across the 7×7 matrix"],
     3.55),
]:
    box(s2, 6.35, y0, 6.6, 1.9,
        fill=RGBColor(0xE2, 0xEF, 0xDA) if badge_fill == GREEN else RGBColor(0xFF, 0xF3, 0xE8),
        line=badge_fill, lw=1)
    txt(s2, label, 6.5, y0+0.08, 4.8, 0.35, size=13, bold=True, color=DARK_BLUE)
    box(s2, 11.3, y0+0.08, 1.5, 0.35, fill=badge_fill)
    txt(s2, badge, 11.31, y0+0.1, 1.48, 0.3,
        size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tbb = s2.shapes.add_textbox(Inches(6.5), Inches(y0+0.52), Inches(6.2), Inches(1.3))
    tff = tbb.text_frame; tff.word_wrap = True; first2 = True
    for sc in scores:
        pp = tff.paragraphs[0] if first2 else tff.add_paragraph()
        first2 = False; pp.space_before = Pt(3)
        rr = pp.add_run(); rr.text = "•  " + sc
        rr.font.size = Pt(11); rr.font.color.rgb = TEXT_DARK

# Bliss legend
box(s2, 6.35, 5.55, 6.6, 1.35, fill=LIGHT_GREY)
txt(s2, "Bliss Score Key", 6.55, 5.6, 3.0, 0.28, size=11, bold=True, color=DARK_BLUE)
for i, (val, desc, col) in enumerate([
    ("> 0", "Synergy — exceeds expected additive effect", GREEN),
    ("= 0", "Additivity — drugs act independently",       TEXT_DARK),
    ("< 0", "Antagonism — weaker than predicted",         ORANGE),
]):
    y = 5.93 + i * 0.3
    txt(s2, val,  6.45, y, 0.7, 0.27, size=11, bold=True, color=col)
    txt(s2, desc, 7.15, y, 5.6, 0.27, size=11, color=TEXT_DARK)

footer(s2, 2)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3 — Genetic screens + AI chat
# ══════════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank)
bg(s3, WHITE)
box(s3, 0, 0, 13.33, 0.9, fill=DARK_BLUE)
txt(s3, "Genetic Perturbagen Screens & AI-Assisted Interpretation",
    0.3, 0.15, 12.5, 0.6, size=23, bold=True, color=WHITE)

# ── LEFT: Genetic perturbagen results ───────────────────────────────────────
box(s3, 0.3, 1.0, 6.1, 5.85,
    fill=RGBColor(0xF5, 0xF9, 0xFF), line=MID_BLUE, lw=1)
txt(s3, "Genetic Perturbagen Screen", 0.5, 1.08, 5.7, 0.4,
    size=15, bold=True, color=DARK_BLUE)

# 1 timepoint block
box(s3, 0.45, 1.55, 5.7, 1.65,
    fill=RGBColor(0xF0, 0xF7, 0xFF), line=MID_BLUE, lw=0.8)
txt(s3, "1 Time Point  |  1 Control", 0.6, 1.62, 4.0, 0.3,
    size=13, bold=True, color=DARK_BLUE)
box(s3, 4.8, 1.62, 1.25, 0.3, fill=TEAL)
txt(s3, "COMPLETE", 4.81, 1.63, 1.23, 0.27,
    size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
tbb = s3.shapes.add_textbox(Inches(0.6), Inches(2.0), Inches(5.4), Inches(1.12))
tff = tbb.text_frame; tff.word_wrap = True; first3 = True
for pt in [
    "Multiple siRNA/shRNA gene perturbagens tested at 40 ng/well in MCF7 cells",
    "Normalised confluency computed per perturbagen relative to control",
    "Single endpoint readout (48 h) — no dose-response, binary knockdown effect",
]:
    p = tff.paragraphs[0] if first3 else tff.add_paragraph()
    first3 = False; p.space_before = Pt(3)
    r = p.add_run(); r.text = "•  " + pt
    r.font.size = Pt(11); r.font.color.rgb = TEXT_DARK

# Multi-timepoint block
box(s3, 0.45, 3.28, 5.7, 2.05,
    fill=RGBColor(0xF0, 0xF7, 0xFF), line=MID_BLUE, lw=0.8)
txt(s3, "Several Time Points  |  Multiple Controls", 0.6, 3.35, 4.0, 0.3,
    size=13, bold=True, color=DARK_BLUE)
box(s3, 4.8, 3.35, 1.25, 0.3, fill=TEAL)
txt(s3, "COMPLETE", 4.81, 3.36, 1.23, 0.27,
    size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
tbb2 = s3.shapes.add_textbox(Inches(0.6), Inches(3.72), Inches(5.4), Inches(1.5))
tff2 = tbb2.text_frame; tff2.word_wrap = True; first4 = True
for pt in [
    "23 time points over ~69 h (3 h intervals) with multiple control groups",
    "Growth rate computed at each time point for every perturbagen",
    "Growth rate ratios close to 1.0 = no effect; <1 = inhibition; >1 = enhanced growth",
    "Allows identification of perturbagens with time-dependent effects",
]:
    p = tff2.paragraphs[0] if first4 else tff2.add_paragraph()
    first4 = False; p.space_before = Pt(3)
    r = p.add_run(); r.text = "•  " + pt
    r.font.size = Pt(11); r.font.color.rgb = TEXT_DARK

# Note on genetic-chemical
box(s3, 0.45, 5.42, 5.7, 1.25, fill=RGBColor(0xFF, 0xF8, 0xE1), line=ORANGE, lw=1)
txt(s3, "⚠  Genetic-Chemical Perturbagen", 0.6, 5.48, 5.3, 0.3,
    size=12, bold=True, color=ORANGE)
txt(s3, "Example datasets encountered a known HTSplotter compatibility issue "
        "with unequal cell-line condition counts. "
        "All other experiment types (drug, drug combination, genetic) ran successfully.",
    0.6, 5.82, 5.4, 0.75, size=10, color=TEXT_DARK)

# ── RIGHT: AI chat ───────────────────────────────────────────────────────────
box(s3, 6.75, 1.0, 6.25, 5.85,
    fill=RGBColor(0xF0, 0xF4, 0xF9), line=MID_BLUE, lw=1)
txt(s3, "🤖  AI-Assisted Results Interpretation",
    6.95, 1.08, 5.85, 0.4, size=15, bold=True, color=DARK_BLUE)

txt(s3, "An interactive chat interface built on top of HTSplotter using the "
        "Anthropic Claude API. After any analysis, researchers can ask plain-English "
        "questions about their results — IC values, synergy, curve fit, or biological context.",
    6.95, 1.56, 5.85, 0.95, size=12, color=TEXT_DARK)

# Chat examples
def bubble(slide, speaker, text, top):
    is_user = speaker == "You"
    fill_c  = MID_BLUE if is_user else RGBColor(0xE8, 0xF1, 0xFB)
    text_c  = WHITE    if is_user else TEXT_DARK
    box(slide, 7.0, top, 5.8, 0.52, fill=fill_c,
        line=RGBColor(0xBB, 0xCC, 0xDD), lw=0.5)
    txt(slide, f"{speaker}:  {text}", 7.1, top+0.06, 5.65, 0.42,
        size=10, color=text_c)

bubble(s3, "You",    "Which drug was most potent?",                     2.62)
bubble(s3, "Claude", "Prexasertib — IC₅₀ ≈ 10 nM, ~66× more potent than MK-1775.",
       3.22)
bubble(s3, "You",    "Is there synergy between MK-1775 and Prexasertib?",
       3.82)
bubble(s3, "Claude", "Yes — Bliss scores up to +0.56. Strongest at mid-range\nMK-1775 doses combined with low Prexasertib.",
       4.42)
bubble(s3, "You",    "What does a growth rate > 1 mean in the genetic screen?",
       5.1)
bubble(s3, "Claude", "Growth rate > 1 means cells grew faster than control —\na perturbagen may be releasing a growth brake.",
       5.7)

# How to run
box(s3, 6.85, 6.4, 6.1, 0.35, fill=DARK_BLUE)
txt(s3, "github.com/aaronwils246/HTSplotter-chat  |  python chat_results.py  [results_dir]",
    6.9, 6.42, 5.9, 0.28, size=10, bold=True, color=LIGHT_BLUE)

footer(s3, 3)


# ── Save ────────────────────────────────────────────────────────────────────
out = "/Users/aaronwilson/HTSplotter/HTSplotter_Summary.pptx"
prs.save(out)
print(f"Saved: {out}")
