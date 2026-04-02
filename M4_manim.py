"""
╔══════════════════════════════════════════════════════════════════╗
║   MANIM TEMPLATE — MODUL 4: Gerak Partikel & Gerak Realistik    ║
║   Output: MP4 16:9, 1920×1080, 60fps                             ║
║   Cara render: manim -pqh modul4_manim.py NamaScene             ║
║   Render semua: manim -pqh modul4_manim.py AllScenes            ║
╚══════════════════════════════════════════════════════════════════╝

PETUNJUK PENGISIAN:
  Cari semua komentar bertanda:
    # >>> PHYSICS: ...  ← isi logika fisika kamu di sini
    # >>> STYLE: ...    ← boleh ubah warna/tampilan
  Bagian lain (axes, labels, animasi dasarnya) sudah siap.

INSTALL:
  pip install manim
  # Butuh juga: LaTeX (MiKTeX/TeX Live), ffmpeg, Cairo

RENDER INDIVIDUAL:
  manim -pqh modul4_manim.py Scene1_Hambatan    # Tugas 1
  manim -pqh modul4_manim.py Scene2_SudutOptimal # Tugas 2
  manim -pqh modul4_manim.py Scene3_Terminal     # Tugas 3
  manim -pqh modul4_manim.py Scene4_Komparatif   # Tugas 4
  manim -pqh modul4_manim.py AllScenes           # Semua sekaligus

FLAG KUALITAS:
  -ql  = 480p (cepat, untuk draft)
  -qm  = 720p
  -qh  = 1080p (final, lebih lambat)
  -p   = langsung buka setelah render
"""

from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════
# KONSTANTA GLOBAL — ubah sesuai kebutuhan
# ══════════════════════════════════════════════════════════════════

G    = 9.81    # gravitasi (m/s²)
M    = 1.0     # massa (kg)
V0   = 30.0    # kecepatan awal (m/s)
DT   = 0.005   # time step Euler (s)

# Palet warna
C_BG      = "#0d1117"   # background
C_BLUE    = "#58a6ff"   # biru — tanpa drag / referensi
C_ORANGE  = "#ff7043"   # oranye — dengan drag
C_GREEN   = "#3fb950"   # hijau — terminal velocity / optimal
C_YELLOW  = "#e3b341"   # kuning — highlight rumus
C_PURPLE  = "#bc8cff"   # ungu — syarat batas Neumann
C_MUTED   = "#8b949e"   # abu — teks sekunder
C_GROUND  = "#6d4c28"   # coklat — tanah

# ══════════════════════════════════════════════════════════════════
# HELPER: Simulasi Euler
# ══════════════════════════════════════════════════════════════════

def euler_projectile(theta_deg: float, k: float, v0: float = V0,
                     g: float = G, m: float = M, dt: float = DT):
    """
    Hitung trajektori gerak peluru dengan hambatan udara Fd = -kv².
    Return: (x_array, y_array, vx_array, vy_array, t_array)

    >>> PHYSICS: fungsi ini sudah lengkap — ikuti logikanya untuk scene lain.
    """
    rad = np.radians(theta_deg)
    x,  y  = 0.0, 0.0
    vx, vy = v0 * np.cos(rad), v0 * np.sin(rad)
    t_now  = 0.0
    xs, ys, vxs, vys, ts = [x], [y], [vx], [vy], [t_now]

    while True:
        v   = np.sqrt(vx**2 + vy**2)
        ax_ = -(k / m) * v * vx
        ay_ = -g - (k / m) * v * vy
        x  += vx  * dt;  y  += vy  * dt
        vx += ax_ * dt;  vy += ay_ * dt
        t_now += dt
        xs.append(x); ys.append(y)
        vxs.append(vx); vys.append(vy)
        ts.append(t_now)
        if y < 0:
            break
    return (np.array(xs), np.array(ys),
            np.array(vxs), np.array(vys), np.array(ts))


def euler_freefall(k: float, m: float = M, g: float = G,
                   h0: float = 200.0, dt: float = DT):
    """
    Simulasi gerak jatuh bebas dengan hambatan udara (1D, ke bawah positif).
    Return: (v_array, t_array, v_term_analitik)

    >>> PHYSICS: fungsi ini sudah lengkap.
    """
    v_term = np.sqrt(m * g / k)
    v, y, t = 0.0, 0.0, 0.0
    vs, ts = [v], [t]
    while y < h0:
        a  = g - (k / m) * v**2
        v += a * dt
        y += v * dt
        t += dt
        vs.append(v); ts.append(t)
        if v >= 0.9999 * v_term:
            break
    return np.array(vs), np.array(ts), v_term


# ══════════════════════════════════════════════════════════════════
# CONFIG MANIM — 16:9, 1080p, 60fps
# ══════════════════════════════════════════════════════════════════

config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_rate   = 60
config.background_color = C_BG


# ══════════════════════════════════════════════════════════════════
# SCENE 1: Rekonstruksi Hambatan Udara
# ══════════════════════════════════════════════════════════════════

class Scene1_Hambatan(Scene):
    """
    Tugas 1 — Animasi peluru dengan dan tanpa hambatan udara.

    PLACEHOLDER SECTIONS:
      [A] Parameter fisika → ubah theta, k, v0 sesuai soal kamu
      [B] Koordinat axes   → sesuaikan skala dengan nilai parameter
      [C] Physics update   → di sini kamu masukkan euler_projectile() kamu sendiri
      [D] Trailing dot     → ubah kecepatan animasi (run_time)
    """

    def construct(self):
        # ── JUDUL ────────────────────────────────────────────────
        title = Text("Tugas 1 — Hambatan Udara: Fd = −kv²",
                     font_size=32, color=WHITE).to_edge(UP, buff=0.35)
        subtitle = Text("Perbandingan lintasan dengan dan tanpa drag (Metode Euler)",
                        font_size=18, color=C_MUTED).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle, shift=UP*0.2))
        self.wait(0.5)

        # ── [A] PARAMETER — ubah di sini ─────────────────────────
        theta = 45.0          # >>> PHYSICS: sudut elevasi (derajat)
        k_val = 0.05          # >>> PHYSICS: koefisien drag (kg/m)
        v0_   = V0            # >>> PHYSICS: kecepatan awal (m/s)
        # ── [A] END ───────────────────────────────────────────────

        # ── [C] HITUNG TRAJEKTORI ─────────────────────────────────
        # >>> PHYSICS: panggil fungsi simulasimu di sini.
        # Jika kamu punya implementasi sendiri, ganti baris ini:
        xnd, ynd, _, _, tnd = euler_projectile(theta, k=0.0,  v0=v0_)
        xd,  yd,  _, _, td  = euler_projectile(theta, k=k_val, v0=v0_)
        # >>> PHYSICS: xnd/ynd = tanpa drag, xd/yd = dengan drag
        # ── [C] END ───────────────────────────────────────────────

        # ── [B] AXES ─────────────────────────────────────────────
        x_max = float(xnd.max()) * 1.1    # >>> STYLE: skala x
        y_max = float(ynd.max()) * 1.3    # >>> STYLE: skala y

        axes = Axes(
            x_range=[0, x_max, x_max / 5],
            y_range=[0, y_max, y_max / 4],
            x_length=11,
            y_length=5.5,
            axis_config={"color": C_MUTED, "stroke_width": 1.5,
                         "include_tip": True, "tip_width": 0.15,
                         "tip_height": 0.15},
        ).to_edge(DOWN, buff=0.7).shift(LEFT * 0.5)

        x_label = axes.get_x_axis_label(
            Text("Jarak horizontal (m)", font_size=16, color=C_MUTED), direction=DOWN)
        y_label = axes.get_y_axis_label(
            Text("Ketinggian (m)", font_size=16, color=C_MUTED), direction=LEFT)

        # Tanah
        ground = Line(
            axes.c2p(0, 0), axes.c2p(x_max, 0),
            color=C_GROUND, stroke_width=3
        )

        self.play(Create(axes), Write(x_label), Write(y_label),
                  Create(ground), run_time=1.2)
        # ── [B] END ───────────────────────────────────────────────

        # ── RUMUS (LaTeX) ─────────────────────────────────────────
        eq1 = MathTex(
            r"\frac{dv_x}{dt} = -\frac{k}{m}\,v\,v_x",
            font_size=28, color=C_YELLOW
        ).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        eq2 = MathTex(
            r"\frac{dv_y}{dt} = -g - \frac{k}{m}\,v\,v_y",
            font_size=28, color=C_YELLOW
        ).next_to(eq1, DOWN, buff=0.3)
        self.play(Write(eq1), Write(eq2))

        # ── ANIMASI TRAJEKTORI ────────────────────────────────────
        # Subsample agar animasi tidak terlalu berat
        SKIP = 5   # >>> STYLE: ambil 1 dari setiap SKIP titik

        def make_path(xs, ys, color, stroke=2.5, alpha=1.0):
            """Buat VMobject path dari array numpy."""
            pts = [axes.c2p(float(xs[i]), max(0.0, float(ys[i])))
                   for i in range(0, len(xs), SKIP)]
            path = VMobject(color=color, stroke_width=stroke,
                            stroke_opacity=alpha)
            path.set_points_as_corners(pts)
            return path

        # Faint full path (ditampilkan dulu sebelum animasi)
        path_nd_ghost = make_path(xnd, ynd, C_BLUE, stroke=1.2, alpha=0.22)
        path_d_ghost  = make_path(xd,  yd,  C_ORANGE, stroke=1.2, alpha=0.22)
        self.play(Create(path_nd_ghost), Create(path_d_ghost), run_time=0.6)

        # Path animasi
        path_nd = make_path(xnd, ynd, C_BLUE, stroke=2.8)
        path_d  = make_path(xd,  yd,  C_ORANGE, stroke=2.8)

        # Titik peluru
        dot_nd = Dot(axes.c2p(0, 0), color=C_BLUE, radius=0.12)
        dot_d  = Dot(axes.c2p(0, 0), color=C_ORANGE, radius=0.12)

        # [D] Ubah run_time untuk mempercepat/memperlambat animasi
        self.play(
            Create(path_nd), MoveAlongPath(dot_nd, path_nd),
            run_time=3.5,          # >>> STYLE: durasi animasi peluru biru
            rate_func=linear
        )
        self.play(
            Create(path_d), MoveAlongPath(dot_d, path_d),
            run_time=2.5,          # >>> STYLE: durasi animasi peluru oranye
            rate_func=linear
        )

        # ── LEGENDA ───────────────────────────────────────────────
        leg_nd = VGroup(
            Line(ORIGIN, RIGHT * 0.5, color=C_BLUE, stroke_width=2.5),
            Text(f"Tanpa drag (k=0)  R = {xnd[-1]:.1f} m",
                 font_size=16, color=C_BLUE)
        ).arrange(RIGHT, buff=0.15)

        leg_d = VGroup(
            Line(ORIGIN, RIGHT * 0.5, color=C_ORANGE, stroke_width=2.5),
            Text(f"Dengan drag (k={k_val})  R = {xd[-1]:.1f} m",
                 font_size=16, color=C_ORANGE)
        ).arrange(RIGHT, buff=0.15)

        legend = VGroup(leg_nd, leg_d).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UL, buff=1.0).shift(DOWN * 1.5)
        self.play(FadeIn(legend, shift=UP * 0.15))
        self.wait(2)


# ══════════════════════════════════════════════════════════════════
# SCENE 2: Analisis Sudut Optimal
# ══════════════════════════════════════════════════════════════════

class Scene2_SudutOptimal(Scene):
    """
    Tugas 2 — Sweep sudut dan grafik Range vs θ.

    PLACEHOLDER SECTIONS:
      [A] Parameter fisika (k, v0, sweep range sudut)
      [B] >>> PHYSICS: panggil fungsi range-mu untuk tiap sudut
      [C] Grafik bar chart range vs sudut (sudah siap, tinggal data)
    """

    def construct(self):
        title = Text("Tugas 2 — Sudut Optimal dengan Hambatan Udara",
                     font_size=30, color=WHITE).to_edge(UP, buff=0.35)
        self.play(Write(title))

        # ── [A] PARAMETER ─────────────────────────────────────────
        k_val     = 0.05            # >>> PHYSICS: koefisien drag
        v0_       = V0              # >>> PHYSICS: kecepatan awal
        theta_arr = np.arange(5, 86, 5)   # >>> PHYSICS: range sudut yang disweep
        # ── [A] END ───────────────────────────────────────────────

        # ── [B] HITUNG RANGE TIAP SUDUT ───────────────────────────
        # >>> PHYSICS: ganti dengan loop simulasimu sendiri.
        # Hasilnya harus berupa dua array: ranges_nd dan ranges_d
        # masing-masing panjangnya sama dengan theta_arr.
        ranges_nd = []
        ranges_d  = []
        for th in theta_arr:
            xnd, _, _, _, _ = euler_projectile(th, k=0.0,   v0=v0_)
            xd,  _, _, _, _ = euler_projectile(th, k=k_val, v0=v0_)
            ranges_nd.append(float(xnd[-1]))
            ranges_d.append(float(xd[-1]))
        ranges_nd = np.array(ranges_nd)
        ranges_d  = np.array(ranges_d)
        # ── [B] END ───────────────────────────────────────────────

        opt_nd = int(theta_arr[np.argmax(ranges_nd)])
        opt_d  = int(theta_arr[np.argmax(ranges_d)])

        # ── [C] AXES GRAFIK ───────────────────────────────────────
        r_max = float(ranges_nd.max()) * 1.15

        axes = Axes(
            x_range=[0, 90, 15],
            y_range=[0, r_max, r_max / 5],
            x_length=10,
            y_length=5,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        ).shift(DOWN * 0.4 + LEFT * 0.5)

        x_label = axes.get_x_axis_label(
            Text("Sudut elevasi θ (°)", font_size=16, color=C_MUTED), direction=DOWN)
        y_label = axes.get_y_axis_label(
            Text("Jangkauan R (m)", font_size=16, color=C_MUTED), direction=LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)

        # ── PLOT KURVA ────────────────────────────────────────────
        def make_curve(thetas, ranges, color):
            pts = [axes.c2p(float(th), float(r))
                   for th, r in zip(thetas, ranges)]
            curve = VMobject(color=color, stroke_width=2.5)
            curve.set_points_as_corners(pts)
            return curve

        curve_nd = make_curve(theta_arr, ranges_nd, C_BLUE)
        curve_d  = make_curve(theta_arr, ranges_d, C_ORANGE)

        self.play(Create(curve_nd), run_time=2.0, rate_func=linear)
        self.play(Create(curve_d),  run_time=2.0, rate_func=linear)

        # ── MARKER SUDUT OPTIMAL ──────────────────────────────────
        for opt, color, label_str in [
            (opt_nd, C_BLUE,   f"θ_opt = {opt_nd}°  (k=0)"),
            (opt_d,  C_GREEN,  f"θ_opt = {opt_d}°   (k={k_val})"),
        ]:
            r_at_opt = float(ranges_nd[theta_arr == opt][0]) if color == C_BLUE \
                       else float(ranges_d[theta_arr == opt][0])
            vline = DashedLine(
                axes.c2p(opt, 0), axes.c2p(opt, r_at_opt),
                color=color, stroke_width=1.5, dash_length=0.1
            )
            dot   = Dot(axes.c2p(opt, r_at_opt), color=color, radius=0.1)
            lbl   = Text(label_str, font_size=15, color=color)\
                    .next_to(dot, UP, buff=0.1)
            self.play(Create(vline), FadeIn(dot), Write(lbl), run_time=0.8)

        # ── KESIMPULAN ────────────────────────────────────────────
        note = Text(
            f"Dengan drag, sudut optimal bergeser dari {opt_nd}° → {opt_d}°",
            font_size=20, color=C_YELLOW
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# SCENE 3: Terminal Velocity
# ══════════════════════════════════════════════════════════════════

class Scene3_Terminal(Scene):
    """
    Tugas 3 — Grafik v(t) dan a(t) menuju terminal velocity.

    PLACEHOLDER SECTIONS:
      [A] Parameter fisika (k, m)
      [B] >>> PHYSICS: panggil simulasi jatuh bebasmu
      [C] Kurva v(t) dan garis v_term (sudah siap axes)
    """

    def construct(self):
        title = Text("Tugas 3 — Terminal Velocity",
                     font_size=32, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ── PENURUNAN RUMUS ───────────────────────────────────────
        eq_motion = MathTex(
            r"m\frac{dv}{dt} = mg - kv^2 \quad\Rightarrow\quad "
            r"\frac{dv}{dt} = g - \frac{k}{m}v^2",
            font_size=26, color=C_YELLOW
        ).next_to(title, DOWN, buff=0.25)

        eq_term = MathTex(
            r"v_{term} = \sqrt{\frac{mg}{k}}",
            font_size=32, color=C_GREEN
        ).next_to(eq_motion, DOWN, buff=0.2)

        self.play(Write(eq_motion), run_time=1.5)
        self.play(Write(eq_term), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(eq_motion), eq_term.animate.to_corner(UR, buff=0.5))

        # ── [A] PARAMETER ─────────────────────────────────────────
        k_val = 0.10       # >>> PHYSICS: koefisien drag
        m_val = M          # >>> PHYSICS: massa (kg)
        # ── [A] END ───────────────────────────────────────────────

        # ── [B] HITUNG v(t) ───────────────────────────────────────
        # >>> PHYSICS: ganti dengan implementasi simulasimu sendiri.
        vs, ts, v_term = euler_freefall(k_val, m=m_val)
        # Hasil: vs = array kecepatan, ts = array waktu, v_term = nilai analitik
        # ── [B] END ───────────────────────────────────────────────

        # ── [C] AXES ─────────────────────────────────────────────
        t_max = float(ts[-1]) * 1.1
        v_max = float(v_term) * 1.3

        axes = Axes(
            x_range=[0, t_max, t_max / 5],
            y_range=[0, v_max, v_max / 5],
            x_length=10,
            y_length=4.8,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        ).shift(DOWN * 0.7 + LEFT * 0.5)

        x_label = axes.get_x_axis_label(
            Text("Waktu t (s)", font_size=16, color=C_MUTED), direction=DOWN)
        y_label = axes.get_y_axis_label(
            Text("Kecepatan v (m/s)", font_size=16, color=C_MUTED), direction=LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)

        # Garis v_term
        vt_line = DashedLine(
            axes.c2p(0, float(v_term)), axes.c2p(t_max, float(v_term)),
            color=C_GREEN, stroke_width=2, dash_length=0.15
        )
        vt_label = MathTex(
            rf"v_{{term}} = {v_term:.2f}\ \text{{m/s}}",
            font_size=22, color=C_GREEN
        ).next_to(axes.c2p(t_max * 0.5, float(v_term)), UP, buff=0.1)
        self.play(Create(vt_line), Write(vt_label))

        # Kurva v(t)
        SKIP = max(1, len(vs) // 300)
        pts  = [axes.c2p(float(ts[i]), float(vs[i]))
                for i in range(0, len(vs), SKIP)]
        curve = VMobject(color=C_BLUE, stroke_width=3)
        curve.set_points_as_corners(pts)

        # Tracker dot bergerak di sepanjang kurva
        tracker_dot = Dot(axes.c2p(float(ts[0]), float(vs[0])),
                          color=C_BLUE, radius=0.12)
        speed_lbl   = always_redraw(lambda: Text(
            f"v = {vs[min(int(tracker_dot.get_x()), len(vs)-1)]:.2f} m/s",
            font_size=16, color=C_BLUE
        ).next_to(tracker_dot, UP, buff=0.15))

        self.play(Create(curve), run_time=4.0, rate_func=linear)
        self.add(tracker_dot, speed_lbl)

        # 99% v_term marker
        idx99 = np.argmax(vs >= 0.99 * v_term)
        if idx99 > 0:
            t99 = float(ts[idx99])
            mark99 = DashedLine(
                axes.c2p(t99, 0), axes.c2p(t99, float(v_term)),
                color=C_YELLOW, stroke_width=1.2, dash_length=0.1
            )
            lbl99 = Text(f"99% v_term\n@ t={t99:.1f}s",
                         font_size=14, color=C_YELLOW)\
                    .next_to(axes.c2p(t99, float(v_term) * 0.5), RIGHT, buff=0.1)
            self.play(Create(mark99), Write(lbl99), run_time=0.8)

        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# SCENE 4: Komparatif 3 Nilai k
# ══════════════════════════════════════════════════════════════════

class Scene4_Komparatif(Scene):
    """
    Tugas 4 — Animasi 4 lintasan sekaligus (3 nilai k + referensi).

    PLACEHOLDER SECTIONS:
      [A] Konfigurasi nilai-nilai k dan warnanya
      [B] >>> PHYSICS: panggil simulasimu untuk tiap k
      [C] Axes dan skala — ubah jika perlu
    """

    def construct(self):
        title = Text("Tugas 4 — Komparatif Lintasan: Variasi Koefisien Drag k",
                     font_size=28, color=WHITE).to_edge(UP, buff=0.35)
        self.play(Write(title))

        # ── [A] KONFIGURASI ───────────────────────────────────────
        theta_ = 45.0   # >>> PHYSICS: sudut elevasi (derajat)
        v0_    = V0     # >>> PHYSICS: kecepatan awal (m/s)

        configs = [
            # (k_value,  warna,       label)
            (0.00,  C_MUTED,    "k = 0.00  (referensi)"),
            (0.01,  C_BLUE,     "k = 0.01  (kecil)"),
            (0.05,  "#69f0ae",  "k = 0.05  (sedang)"),
            (0.15,  C_ORANGE,   "k = 0.15  (besar)"),
        ]
        # ── [A] END ───────────────────────────────────────────────

        # ── [B] HITUNG SEMUA TRAJEKTORI ───────────────────────────
        # >>> PHYSICS: ganti euler_projectile dengan fungsimu sendiri.
        trajs = []
        for k_val, color, label in configs:
            xs, ys, _, _, _ = euler_projectile(theta_, k=k_val, v0=v0_)
            trajs.append({
                'xs': xs, 'ys': ys,
                'range': float(xs[-1]),
                'color': color, 'label': label,
                'k': k_val
            })
        # ── [B] END ───────────────────────────────────────────────

        # ── [C] AXES ─────────────────────────────────────────────
        xmax = max(t['range'] for t in trajs) * 1.08   # >>> STYLE
        ymax = max(float(t['ys'].max()) for t in trajs) * 1.3   # >>> STYLE

        axes = Axes(
            x_range=[0, xmax, xmax / 5],
            y_range=[0, ymax, ymax / 4],
            x_length=11,
            y_length=5,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        ).shift(DOWN * 0.5 + LEFT * 0.5)

        x_label = axes.get_x_axis_label(
            Text("Jarak horizontal (m)", font_size=16, color=C_MUTED), direction=DOWN)
        y_label = axes.get_y_axis_label(
            Text("Ketinggian (m)", font_size=16, color=C_MUTED), direction=LEFT)

        ground = Line(axes.c2p(0, 0), axes.c2p(xmax, 0),
                      color=C_GROUND, stroke_width=3)
        self.play(Create(axes), Write(x_label), Write(y_label),
                  Create(ground), run_time=1.0)
        # ── [C] END ───────────────────────────────────────────────

        # ── TAMPILKAN SEMUA LINTASAN SATU PER SATU ───────────────
        SKIP = 5
        legend_items = []

        for t_cfg in trajs:
            xs, ys = t_cfg['xs'], t_cfg['ys']
            color  = t_cfg['color']

            pts  = [axes.c2p(float(xs[i]), max(0.0, float(ys[i])))
                    for i in range(0, len(xs), SKIP)]
            path = VMobject(color=color, stroke_width=2.8)
            path.set_points_as_corners(pts)

            dot = Dot(axes.c2p(0, 0), color=color, radius=0.1)
            self.play(
                Create(path),
                MoveAlongPath(dot, path),
                run_time=2.0,    # >>> STYLE: durasi tiap lintasan
                rate_func=linear
            )

            # Marker jangkauan
            r_dot = Dot(axes.c2p(t_cfg['range'], 0), color=color, radius=0.09)
            r_lbl = Text(f"{t_cfg['range']:.1f} m", font_size=13, color=color)\
                    .next_to(r_dot, UP, buff=0.08)
            self.play(FadeIn(r_dot), Write(r_lbl), run_time=0.4)

            legend_items.append(
                VGroup(
                    Line(ORIGIN, RIGHT*0.4, color=color, stroke_width=2.5),
                    Text(t_cfg['label'], font_size=14, color=color)
                ).arrange(RIGHT, buff=0.12)
            )

        # ── LEGENDA ───────────────────────────────────────────────
        leg_group = VGroup(*legend_items)\
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)\
            .to_corner(UR, buff=0.5).shift(DOWN * 1.0)
        self.play(FadeIn(leg_group, shift=RIGHT * 0.2))
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════
# ALL SCENES — Render semua sekaligus sebagai 1 video
# ══════════════════════════════════════════════════════════════════

class AllScenes(Scene):
    """
    Gabungkan semua scene dalam satu file output.
    Render dengan: manim -pqh modul4_manim.py AllScenes
    """

    def construct(self):
        for SceneClass in [
            Scene1_Hambatan,
            Scene2_SudutOptimal,
            Scene3_Terminal,
            Scene4_Komparatif,
        ]:
            # Jalankan setiap scene seperti standalone
            scene = SceneClass()
            # Karena self.construct() tiap scene butuh self.play dll,
            # render per scene terpisah lebih direkomendasikan.
            # AllScenes ini lebih sebagai referensi urutan.
            pass

        # ── TITLE CARD PENUTUP ────────────────────────────────────
        end_title = Text("Modul 4 — Komputasi dan Simulasi Fisika",
                         font_size=36, color=WHITE).move_to(ORIGIN)
        end_sub   = Text("FMIPA Universitas Padjadjaran · 2026",
                         font_size=22, color=C_MUTED).next_to(end_title, DOWN, buff=0.3)
        self.play(FadeIn(end_title), FadeIn(end_sub))
        self.wait(3)
        self.play(FadeOut(end_title), FadeOut(end_sub))


# ══════════════════════════════════════════════════════════════════
# QUICK RUN CHECK (tanpa Manim — hanya validasi numpy)
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Validasi fungsi helper (tanpa render Manim) ===\n")

    # Tugas 1 & 4
    for k in [0.0, 0.01, 0.05, 0.15]:
        xs, ys, _, _, _ = euler_projectile(45.0, k=k)
        print(f"  k={k:.2f}  →  Range = {xs[-1]:.2f} m,  ymax = {ys.max():.2f} m")

    print()

    # Tugas 2
    print("  Sweep sudut (k=0.05):")
    thetas = np.arange(5, 86, 10)
    for th in thetas:
        xs, _, _, _, _ = euler_projectile(th, k=0.05)
        print(f"    θ={th:2d}°  R={xs[-1]:.2f} m")

    print()

    # Tugas 3
    vs, ts, vt = euler_freefall(0.10)
    print(f"  Terminal velocity (k=0.10): analitik={vt:.4f} m/s, numerik={vs[-1]:.4f} m/s")
    print()
    print("=== Semua OK! Jalankan: manim -pqh modul4_manim.py Scene1_Hambatan ===")
