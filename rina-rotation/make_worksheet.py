"""아린이의 빙글빙글 도형 돌리기 - 연습 문제 PDF 생성기.

플라토 A2 도형조작 3주차(도형 돌리기)와 같은 유형의 문제를 만든다.
  A. 돌린 모양 찾기 (원 안의 도형, 점과 화살표)
  B. 네모 모눈 돌리기 (시계 방향 1/4 바퀴씩)
  C. 세모 모눈 돌리기 (시계 방향 1/4 바퀴씩)

실행: python3 make_worksheet.py  -> rina_rotation_practice.pdf
"""
import math
import os
import random

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_DIR = "/usr/share/fonts/truetype/nanum"
pdfmetrics.registerFont(TTFont("R", os.path.join(FONT_DIR, "NanumSquareRoundR.ttf")))
pdfmetrics.registerFont(TTFont("B", os.path.join(FONT_DIR, "NanumSquareRoundB.ttf")))

W, H = A4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rina_rotation_practice.pdf")

# palette
GREEN = (0.63, 0.80, 0.50)
GREEN_D = (0.38, 0.60, 0.28)
PURPLE = (0.42, 0.36, 0.72)
PINK = (0.93, 0.42, 0.55)
GREY_BG = (0.92, 0.92, 0.94)
GREY_L = (0.55, 0.55, 0.6)
INK = (0.18, 0.18, 0.22)
TIP_BG = (1.0, 0.96, 0.84)
TIP_LINE = (0.95, 0.72, 0.25)

random.seed(20261122)
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("아린이의 빙글빙글 도형 돌리기")
c.setAuthor("Rina math")

answers_A = []   # (num, choice index 1..3)
answers_B = []   # (num, pattern, n, blanks)
answers_C = []   # (num, pattern, blanks)

CIRCLED = ["①", "②", "③", "④"]


# ---------------------------------------------------------------- helpers
def fill(rgb):
    c.setFillColorRGB(*rgb)


def stroke(rgb):
    c.setStrokeColorRGB(*rgb)


def text(x, y, s, size=12, font="R", color=INK, align="left"):
    fill(color)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)


def page_header(title, subtitle, section_color=PURPLE):
    fill(section_color)
    c.roundRect(30, H - 78, W - 60, 50, 14, stroke=0, fill=1)
    text(48, H - 58, title, 20, "B", (1, 1, 1))
    text(W - 48, H - 50, "이름: 아린", 11, "B", (1, 1, 1), "right")
    text(W - 48, H - 66, "날짜:     월     일", 10, "R", (1, 1, 1), "right")
    text(36, H - 100, subtitle, 12.5, "B", INK)


def tip_box(y_top, lines, title="풀이 비법"):
    h = 28 + 16 * len(lines)
    fill(TIP_BG)
    stroke(TIP_LINE)
    c.setLineWidth(1.2)
    c.roundRect(30, y_top - h, W - 60, h, 10, stroke=1, fill=1)
    text(44, y_top - 17, "★ " + title, 11, "B", (0.75, 0.45, 0.05))
    for i, ln in enumerate(lines):
        text(52, y_top - 34 - 16 * i, ln, 10.5, "R", INK)
    return y_top - h


def footer(n):
    text(W / 2, 22, f"- {n} -", 9, "R", GREY_L, "center")


def problem_number(x, y, n):
    text(x, y, str(n), 16, "B", PURPLE)


def small_arrow(x, y):
    fill((0.55, 0.55, 0.58))
    p = c.beginPath()
    p.moveTo(x - 7, y + 3)
    p.lineTo(x + 1, y + 3)
    p.lineTo(x + 1, y + 7)
    p.lineTo(x + 8, y)
    p.lineTo(x + 1, y - 7)
    p.lineTo(x + 1, y - 3)
    p.lineTo(x - 7, y - 3)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def dashed_circle(cx, cy, r):
    stroke(GREY_L)
    c.setLineWidth(0.8)
    c.setDash(2, 2)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setDash()


def dot(x, y, r=3.2):
    fill((0.25, 0.25, 0.28))
    c.circle(x, y, r, stroke=0, fill=1)


# ------------------------------------------------- A. 돌린 모양 찾기 (circle)
def arc_pts(t0, t1, r, n=12):
    return [(r * math.cos(math.radians(t0 + (t1 - t0) * i / n)),
             r * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]


SHAPES = {
    "rtri": [(-0.55, -0.5), (0.55, -0.5), (-0.55, 0.6)],
    "rtri2": [(-0.5, 0.55), (0.55, -0.55), (-0.5, -0.55)],
    "trap": [(-0.35, 0.7), (0.3, 0.35), (0.3, -0.35), (-0.35, -0.7)],
    "half": [(-0.3 + 0.68 * math.cos(math.radians(a)), 0.68 * math.sin(math.radians(a)))
             for a in range(-90, 91, 10)],
    "quarter": [(-0.45, -0.45)] + [(-0.45 + 1.0 * math.cos(math.radians(a)),
                                   -0.45 + 1.0 * math.sin(math.radians(a))) for a in range(0, 91, 10)],
    "L": [(-0.5, 0.6), (-0.1, 0.6), (-0.1, -0.2), (0.5, -0.2), (0.5, -0.6), (-0.5, -0.6)],
    "arrow": [(0, 0.72), (0.5, 0.17), (0.18, 0.17), (0.18, -0.65), (-0.18, -0.65), (-0.18, 0.17), (-0.5, 0.17)],
    "para": [(-0.55, -0.5), (0.15, -0.5), (0.55, 0.5), (-0.15, 0.5)],
    "rect": [(-0.3, -0.62), (0.3, -0.62), (0.3, 0.62), (-0.3, 0.62)],
    "house": [(-0.45, -0.55), (0.45, -0.55), (0.45, 0.15), (0, 0.68), (-0.45, 0.15)],
    "T": [(-0.6, 0.5), (0.6, 0.5), (0.6, 0.1), (0.2, 0.1), (0.2, -0.6), (-0.2, -0.6), (-0.2, 0.1), (-0.6, 0.1)],
    "flag": [(-0.4, -0.65), (-0.4, 0.65), (0.5, 0.35), (-0.2, 0.05), (-0.2, -0.65)],
    "isotri": [(0, 0.62), (0.58, -0.5), (-0.58, -0.5)],
    "ellipse": [(0.32 * math.cos(math.radians(a)) * math.cos(math.radians(30)) - 0.68 * math.sin(math.radians(a)) * math.sin(math.radians(30)),
                0.32 * math.cos(math.radians(a)) * math.sin(math.radians(30)) + 0.68 * math.sin(math.radians(a)) * math.cos(math.radians(30)))
                for a in range(0, 360, 12)],
}


def rot_cw(p, deg):
    t = math.radians(deg)
    x, y = p
    return (x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t))


TRANSFORMS = {
    "r0": lambda p: p,
    "r90": lambda p: rot_cw(p, 90),
    "r180": lambda p: rot_cw(p, 180),
    "r270": lambda p: rot_cw(p, 270),
    "fh": lambda p: (-p[0], p[1]),
    "fv": lambda p: (p[0], -p[1]),
    "fh90": lambda p: rot_cw((-p[0], p[1]), 90),
    "fh270": lambda p: rot_cw((-p[0], p[1]), 270),
    "r45": lambda p: rot_cw(p, 45),
}


def key(pts):
    return frozenset((round(x, 2) + 0.0, round(y, 2) + 0.0) for x, y in pts)


def draw_poly(cx, cy, pts, scale, col=GREEN):
    fill(col)
    stroke(GREEN_D)
    c.setLineWidth(0.6)
    p = c.beginPath()
    p.moveTo(cx + pts[0][0] * scale, cy + pts[0][1] * scale)
    for x, y in pts[1:]:
        p.lineTo(cx + x * scale, cy + y * scale)
    p.close()
    c.drawPath(p, stroke=1, fill=1)


def rotation_arrow(cx, cy, r, sweep_cw):
    """Arrow from the top along the circle. sweep_cw>0 clockwise, <0 counter-clockwise."""
    stroke(GREEN_D)
    c.setLineWidth(1.6)
    end = 90 - sweep_cw
    pts = arc_pts(90 - (8 if sweep_cw > 0 else -8), end, r, 24)
    p = c.beginPath()
    p.moveTo(cx + pts[0][0], cy + pts[0][1])
    for x, y in pts[1:]:
        p.lineTo(cx + x, cy + y)
    c.drawPath(p, stroke=1, fill=0)
    # arrowhead (tangent direction)
    t = math.radians(end)
    ex, ey = cx + r * math.cos(t), cy + r * math.sin(t)
    if sweep_cw > 0:
        tx, ty = math.sin(t), -math.cos(t)
    else:
        tx, ty = -math.sin(t), math.cos(t)
    nx, ny = -ty, tx
    fill(GREEN_D)
    p = c.beginPath()
    p.moveTo(ex + tx * 7, ey + ty * 7)
    p.lineTo(ex + nx * 4.5, ey + ny * 4.5)
    p.lineTo(ex - nx * 4.5, ey - ny * 4.5)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


DIR_LABEL = {90: "시계 방향 ¼바퀴", 180: "시계 방향 ½바퀴", 270: "시계 방향 ¾바퀴", -90: "시계 반대 방향 ¼바퀴"}


def problem_A(y, num, shape, sweep, show_label):
    """sweep: 90, 180, 270 clockwise or -90 counter-clockwise."""
    cw = sweep % 360
    base = SHAPES[shape]
    correct = [TRANSFORMS[f"r{cw}"](p) for p in base]
    ck = key(correct)
    # common mistakes first: wrong direction, no turn, mirror
    prefs = [f"r{(360 - cw) % 360}", "r0", "fh", "fv", "r180", "fh90", "fh270", "r90", "r270"]
    random.shuffle(prefs[2:])
    distract, seen = [], {ck}
    for name in prefs[:2] + random.sample(prefs[2:], len(prefs) - 2):
        pts = [TRANSFORMS[name](p) for p in base]
        k = key(pts)
        if k not in seen:
            seen.add(k)
            distract.append(pts)
        if len(distract) == 2:
            break
    for name in ["r45"]:  # symmetric shapes: add a tilted choice like the textbook
        if len(distract) < 2:
            distract.append([TRANSFORMS[name](p) for p in base])
    choices = distract + [correct]
    random.shuffle(choices)
    ans = [key(ch) for ch in choices].index(ck) + 1
    answers_A.append((num, ans))

    R = 44
    problem_number(36, y + 34, num)
    lx = 100
    dashed_circle(lx, y, R)
    rotation_arrow(lx, y, R + 6, sweep)
    dot(lx, y + R)
    draw_poly(lx, y, base, 36)
    if show_label:
        text(lx, y - R - 22, DIR_LABEL[sweep], 9.5, "B", GREEN_D, "center")
    # choices
    fill(GREY_BG)
    c.roundRect(175, y - R - 14, 385, 2 * R + 28, 14, stroke=0, fill=1)
    t = math.radians(90 - cw)
    for i, ch in enumerate(choices):
        x = 240 + i * 125
        fill((1, 1, 1))
        c.circle(x, y, R, stroke=0, fill=1)
        dashed_circle(x, y, R)
        dot(x + R * math.cos(t), y + R * math.sin(t))
        draw_poly(x, y, ch, 36)
        text(x - R - 8, y + R - 4, CIRCLED[i], 11, "B", GREY_L, "center")


# ------------------------------------------------ B. 네모 모눈 돌리기
def square_frame(cx, cy, cell, n, pattern, k, blank, show=False):
    """Draw an n x n grid rotated k quarter-turns clockwise around (cx,cy)."""
    half = n * cell / 2
    if blank:
        fill(GREY_BG)
        c.roundRect(cx - half - 7, cy - half - 7, 2 * half + 14, 2 * half + 14, 9, stroke=0, fill=1)
    c.saveState()
    c.translate(cx, cy)
    c.rotate(-90 * k)
    fill((1, 1, 1))
    c.rect(-half, -half, 2 * half, 2 * half, stroke=0, fill=1)
    if not blank or show:
        for (r, col) in pattern:
            fill(GREEN if not show else (0.98, 0.70, 0.78))
            c.rect(-half + col * cell, half - (r + 1) * cell, cell, cell, stroke=0, fill=1)
    stroke(GREY_L)
    c.setLineWidth(0.7)
    c.setDash(2, 2)
    for i in range(n + 1):
        c.line(-half + i * cell, -half, -half + i * cell, half)
        c.line(-half, -half + i * cell, half, -half + i * cell)
    c.setDash()
    dot(0 if n % 2 else cell / 2 * 0, half, 3)
    c.restoreState()


def problem_B(y, num, pattern, blanks, n=3):
    cell = 96 / n
    problem_number(36, y + 40, num)
    xs = [110, 238, 366, 494]
    for k, x in enumerate(xs):
        square_frame(x, y, cell, n, pattern, k, k in blanks)
        if k < 3:
            small_arrow(x + 64, y)
    answers_B.append((num, pattern, n, blanks))


# ------------------------------------------------ C. 세모 모눈 돌리기
S3 = math.sqrt(3)


def tri_lattice(s):
    h = s * S3 / 2
    top = 2 * h  # apex y, with centroid at origin (total height 3h)

    def P(i, k):
        return ((k - i / 2) * s, top - i * h)
    return P


def tri_cells():
    cells = []
    for i in range(3):
        for k in range(i + 1):
            cells.append(("u", i, k))
        for k in range(i):
            cells.append(("d", i, k))
    return cells


def tri_poly(P, cell):
    t, i, k = cell
    if t == "u":
        return [P(i, k), P(i + 1, k), P(i + 1, k + 1)]
    return [P(i, k), P(i, k + 1), P(i + 1, k + 1)]


def tri_frame(cx, cy, s, pattern, k, blank, show=False):
    P = tri_lattice(s)
    if blank:
        fill(GREY_BG)
        side = 3 * s * 0.5 + 18
        c.roundRect(cx - side, cy - side, 2 * side, 2 * side, 9, stroke=0, fill=1)
    c.saveState()
    c.translate(cx, cy)
    c.rotate(-90 * k)
    for cell in tri_cells():
        pts = tri_poly(P, cell)
        on = cell in pattern and (not blank or show)
        fill((1, 1, 1) if not on else (GREEN if not show else (0.98, 0.70, 0.78)))
        stroke(GREY_L)
        c.setLineWidth(0.7)
        c.setDash(2, 2)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
    c.setDash()
    dot(*P(0, 0), r=3)
    c.restoreState()


def problem_C(y, num, pattern, blanks):
    problem_number(36, y + 48, num)
    xs = [110, 238, 366, 494]
    for k, x in enumerate(xs):
        tri_frame(x, y, 31, pattern, k, k in blanks)
        if k < 3:
            small_arrow(x + 64, y)
    answers_C.append((num, pattern, blanks))


# ============================================================== PAGES
page = 1

# ---- Cover / 개념 정리
fill((0.96, 0.95, 1.0))
c.rect(0, 0, W, H, stroke=0, fill=1)
text(W / 2, H - 120, "아린이의", 22, "B", PURPLE, "center")
text(W / 2, H - 162, "빙글빙글 도형 돌리기", 34, "B", PURPLE, "center")
text(W / 2, H - 190, "플라토 A2 · 3주차 「도형 돌리기」 더 연습하기", 12, "R", INK, "center")

# 시계 그림: 위 → 오른쪽 → 아래 → 왼쪽
cx, cy, R = W / 2, H - 330, 85
fill((1, 1, 1))
c.circle(cx, cy, R, stroke=0, fill=1)
dashed_circle(cx, cy, R)
rotation_arrow(cx, cy, R + 10, 270)
labels = [(90, "출발! 위"), (0, "¼바퀴 → 오른쪽"), (-90, "½바퀴 → 아래"), (180, "¾바퀴 → 왼쪽")]
cols = [PURPLE, PINK, (0.2, 0.55, 0.85), (0.95, 0.6, 0.1)]
for (a, lab), col in zip(labels, cols):
    t = math.radians(a)
    x, y = cx + R * math.cos(t), cy + R * math.sin(t)
    fill(col)
    c.circle(x, y, 7, stroke=0, fill=1)
    lx = cx + (R + 40) * math.cos(t)
    ly = cy + (R + 32) * math.sin(t) - 4
    al = "center" if a in (90, -90) else ("left" if a == 0 else "right")
    if a == 0:
        lx -= 12
    if a == 180:
        lx += 12
    text(lx, ly, lab, 12, "B", col, al)
text(cx, cy + 6, "시계 방향 ↻", 14, "B", INK, "center")
text(cx, cy - 14, "= 시곗바늘이 도는 방향", 10, "R", INK, "center")

y0 = H - 470
tip_box(y0, [
    "① 점을 먼저 본다 : 점이 어디로 갔는지 찾으면 몇 바퀴 돌렸는지 알 수 있어요.",
    "     위 → 오른쪽 = ¼바퀴,   위 → 아래 = ½바퀴,   위 → 왼쪽 = ¾바퀴 (= 시계 반대로 ¼바퀴)",
    "② 점과 친한 부분 찾기 : 도형에서 점에 가장 가까운 부분(뾰족한 곳, 긴 변…)을 찾아요.",
    "③ 돌린 다음에도 그 부분은 점 옆에 있어요!  도형과 점은 꼭 붙어서 같이 돌아요.",
    "④ 헷갈리면 종이(책)를 직접 돌려 보세요. 마지막 장의 오려서 돌리기 카드를 써도 좋아요.",
    "⑤ 함정 조심 : 거울에 비친 모양(뒤집기)은 돌린 모양이 아니에요.",
], "아린이의 돌리기 비법 5가지")

text(W / 2, 175, "차례", 14, "B", PURPLE, "center")
toc = ["1. 점은 어디로 갈까? (준비 운동)",
       "2. 돌린 모양 찾기 (15문제)",
       "3. 네모 모눈 돌리기 (12문제)",
       "4. 세모 모눈 돌리기 (8문제)",
       "5. 오려서 돌려 보기 카드 · 정답"]
for i, t in enumerate(toc):
    text(W / 2 - 110, 150 - 20 * i, t, 11.5, "R", INK)
footer(page)
c.showPage()
page += 1

# ---- 준비 운동: 점은 어디로?
page_header("1. 점은 어디로 갈까?", "화살표를 따라 점을 돌리면 어디에 도착할까요? 알맞은 말에 ○표 하세요.")
warm = [90, 180, -90, 270, 90, 180, -90, 90, 270]
for i, sw in enumerate(warm):
    col, row = i % 3, i // 3
    x = 110 + col * 185
    y = H - 205 - row * 210
    problem_number(x - 85, y + 55, i + 1)
    fill((1, 1, 1))
    c.circle(x, y, 50, stroke=0, fill=1)
    dashed_circle(x, y, 50)
    rotation_arrow(x, y, 58, sw)
    dot(x, y + 50, 4)
    text(x, y - 85, "위 · 오른쪽 · 아래 · 왼쪽", 11, "B", INK, "center")
    if i < 3:
        text(x, y - 102, DIR_LABEL[sw], 9, "R", GREEN_D, "center")
answers_warm = {90: "오른쪽", 180: "아래", -90: "왼쪽", 270: "왼쪽"}
footer(page)
c.showPage()
page += 1

# ---- A pages
A_set = [
    # (shape, sweep, label?)
    ("rect", 90, True), ("rtri", 90, True), ("half", 180, True), ("trap", -90, True), ("L", 90, True),
    ("arrow", 90, False), ("rtri2", 180, False), ("para", 90, False), ("flag", -90, False), ("house", 180, False),
    ("quarter", 90, False), ("T", 270, False), ("half", -90, False), ("ellipse", 90, False), ("isotri", 180, False),
]
num = 1
for pg in range(3):
    page_header("2. 돌린 모양 찾기", "왼쪽 도형을 화살표 방향으로 돌린 모양을 찾아 ○표 하시오.", GREEN_D)
    if pg == 0:
        ytop = tip_box(H - 112, [
            "점이 어디로 갔는지 먼저 보고, '점 쪽에 있던 부분'이 돌린 뒤에도 점 쪽에 있는지 확인해요.",
            "이 쪽에는 몇 바퀴 돌렸는지 글자로도 적혀 있어요. 다음 쪽부터는 화살표만 보고 풀어요!",
        ])
        ys = [ytop - 68 - i * 126 for i in range(5)]
    else:
        ys = [H - 185 - i * 140 for i in range(5)]
    for y in ys:
        shape, sw, lab = A_set[num - 1]
        problem_A(y, num, shape, sw, lab)
        num += 1
    footer(page)
    c.showPage()
    page += 1

# ---- B pages
B_set = [
    ({(0, 0)}, {3}),
    ({(0, 0), (0, 1)}, {2}),
    ({(1, 0), (1, 1)}, {1}),
    ({(0, 0), (1, 0), (1, 1)}, {3}),
    ({(0, 2), (1, 2), (2, 2), (2, 1)}, {2}),
    ({(1, 0), (1, 1), (1, 2), (0, 1)}, {1}),
    ({(0, 0), (1, 1), (2, 2)}, {3}),
    ({(0, 1), (1, 1), (1, 2), (2, 0)}, {0}),
]
num = 1
for pg in range(2):
    page_header("3. 네모 모눈 돌리기", "모눈 전체를 시계 방향으로 ¼바퀴씩 돌린 모양을 그려 보시오.", (0.2, 0.55, 0.85))
    if pg == 0:
        ytop = tip_box(H - 112, [
            "점은  위 → 오른쪽 → 아래 → 왼쪽  순서로 움직여요. (토끼: 모눈과 도형과 점이 모두 같이 돌아요!)",
            "점 바로 옆 칸은 돌린 뒤에도 점 바로 옆 칸이에요. 점 옆 칸부터 색칠하면 쉬워요.",
            "윗줄 → 오른쪽 줄,  오른쪽 줄 → 아랫줄,  아랫줄 → 왼쪽 줄,  왼쪽 줄 → 윗줄 로 옮겨 가요.",
        ])
        ys = [ytop - 85 - i * 150 for i in range(4)]
    else:
        ys = [H - 190 - i * 155 for i in range(4)]
    for y in ys:
        pat, bl = B_set[num - 1]
        problem_B(y, num, pat, bl)
        num += 1
    footer(page)
    c.showPage()
    page += 1

page_header("3. 네모 모눈 돌리기 - 혼자 다 돌려 보기", "첫 번째 모양을 보고 다음 모양 세 개를 모두 그려 보시오.", (0.2, 0.55, 0.85))
ytop = tip_box(H - 112, [
    "한 번에 하나씩! 바로 앞 그림을 ¼바퀴만 돌리면 돼요. 점이 있는 쪽을 꼭 확인하세요.",
    "10번, 11번은 4칸짜리 큰 모눈이에요. 도전!",
], "도전 문제")
extra = [({(0, 0), (1, 0), (2, 0), (2, 1)}, 3), ({(0, 1), (0, 2), (1, 1)}, 3),
         ({(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)}, 4), ({(0, 3), (1, 2), (1, 3), (3, 0)}, 4)]
for i, (pat, n) in enumerate(extra):
    y = ytop - 85 - i * 150
    problem_B(y, num, pat, {1, 2, 3}, n)
    num += 1
footer(page)
c.showPage()
page += 1

# ---- C pages
C_set = [
    ({("u", 0, 0)}, {3}),
    ({("u", 1, 0), ("d", 1, 0), ("u", 1, 1)}, {2}),
    ({("u", 2, 0), ("d", 2, 0), ("u", 2, 1)}, {3}),
    ({("d", 1, 0), ("u", 2, 1)}, {1}),
    ({("u", 1, 0), ("d", 1, 0)}, {2}),
    ({("u", 0, 0), ("d", 1, 0), ("u", 1, 0)}, {3}),
    ({("u", 2, 2), ("d", 2, 1), ("u", 1, 1)}, {1}),
    ({("u", 1, 1), ("d", 2, 1)}, {0}),
]
num = 1
for pg in range(2):
    page_header("4. 세모 모눈 돌리기", "모눈 전체를 시계 방향으로 ¼바퀴씩 돌린 모양을 그려 보시오.", (0.95, 0.55, 0.1))
    if pg == 0:
        ytop = tip_box(H - 112, [
            "세모 모눈은 꼭짓점(점)이  위 → 오른쪽 → 아래 → 왼쪽  을 향해요.",
            "점이 있는 꼭짓점 쪽 작은 세모부터 찾고, 몇 번째 줄 몇 번째 세모인지 세어 보세요.",
            "점에서 가까운 세모는 돌린 뒤에도 점에서 가까워요!",
        ])
        ys = [ytop - 90 - i * 150 for i in range(4)]
    else:
        ys = [H - 195 - i * 160 for i in range(4)]
    for y in ys:
        pat, bl = C_set[num - 1]
        problem_C(y, num, pat, bl)
        num += 1
    footer(page)
    c.showPage()
    page += 1

# ---- 오려서 돌려 보기 카드
page_header("5. 오려서 돌려 보기 카드", "점선을 따라 오린 뒤, 문제 위에 올려놓고 직접 돌려 보세요.", PINK)
cards = [("rtri", None), ("trap", None), ("L", None), ("half", None)]
for i, (shape, _) in enumerate(cards):
    x = 165 + (i % 2) * 265
    y = H - 260 - (i // 2) * 250
    stroke(GREY_L)
    c.setDash(5, 4)
    c.setLineWidth(1)
    c.rect(x - 110, y - 110, 220, 220, stroke=1, fill=0)
    c.setDash()
    fill((1, 1, 1))
    c.circle(x, y, 90, stroke=0, fill=1)
    dashed_circle(x, y, 90)
    dot(x, y + 90, 6)
    draw_poly(x, y, SHAPES[shape], 72)
    text(x, y + 100, "점", 9, "B", INK, "center")
text(W / 2, 175, "돌릴 때는 점을 먼저 문제의 화살표 끝으로 옮겨 보세요.", 12, "B", PINK, "center")
text(W / 2, 155, "도형을 뒤집지 말고(뒷면이 보이면 안 돼요!) 바닥에 붙인 채로 빙글 돌려요.", 11, "R", INK, "center")
# 3x3 모눈 카드
for j, (x, y) in enumerate([(165, 70), (430, 70)]):
    pass
footer(page)
c.showPage()
page += 1

# ---- 정답
page_header("정답", "틀린 문제는 오려서 돌리기 카드나 게임의 '돌려 보기'로 다시 확인해요.", INK)
y = H - 130
text(36, y, "1. 점은 어디로 갈까?", 12, "B", PURPLE)
y -= 18
text(48, y, "   ".join(f"{i + 1}) {answers_warm[sw]}" for i, sw in enumerate(warm)), 10.5)
y -= 28
text(36, y, "2. 돌린 모양 찾기", 12, "B", GREEN_D)
y -= 18
row = "   ".join(f"{n}) {CIRCLED[a - 1]}" for n, a in answers_A[:8])
text(48, y, row, 10.5)
y -= 16
row = "   ".join(f"{n}) {CIRCLED[a - 1]}" for n, a in answers_A[8:])
text(48, y, row, 10.5)
y -= 30
text(36, y, "3. 네모 모눈 돌리기  (분홍색 칸이 정답)", 12, "B", (0.2, 0.55, 0.85))
y -= 50
x = 60
for n_, pat, n, blanks in answers_B:
    need = 30 + 62 * len(blanks)
    if x + need > W - 30:
        x = 60
        y -= 78
    text(x - 22, y + 18, f"{n_})", 10, "B", INK)
    for j, k in enumerate(sorted(blanks)):
        square_frame(x + 22 + j * 62, y, 48 / n, n, pat, k, False, show=True)
    x += need + 6
y -= 80
text(36, y, "4. 세모 모눈 돌리기  (분홍색 세모가 정답)", 12, "B", (0.95, 0.55, 0.1))
y -= 50
x = 60
for n_, pat, blanks in answers_C:
    need = 92
    if x + need > W - 30:
        x = 60
        y -= 80
    text(x - 22, y + 18, f"{n_})", 10, "B", INK)
    for k in sorted(blanks):
        tri_frame(x + 26, y, 17, pat, k, False, show=True)
    x += need + 30
footer(page)
c.showPage()
c.save()
print("saved", OUT, "pages", page)
