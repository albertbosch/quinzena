import calendar
import tkinter as tk
from datetime import date
from tkinter import font as tkfont

from quinzena import DAY_NAMES_CA, MONTH_NAMES_CA, quinzena_for_day, split_quinzenes


class QuinzenaCalendar(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Quinzena")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        self.minsize(450, 430)

        # State
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.today = today
        self.selected_day = today.day

        # Catalan day/month names shared with the CLI module
        self.day_names = list(DAY_NAMES_CA)
        self.month_names = list(MONTH_NAMES_CA)

        # Colors – macOS Calendar inspired
        self.BG = "#FFFFFF"
        self.HEADER_BG = "#F5F5F7"
        self.TEXT = "#1D1D1F"
        self.SECONDARY = "#86868B"
        self.GRID_LINE = "#E5E5EA"
        self.TODAY_RED = "#FF3B30"
        self.SELECTED_BLUE = "#0A84FF"
        self.WEEKEND_TEXT = "#86868B"
        self.QUINZENA_LABEL = "#AEAEB2"
        self.HOVER_BG = "#F2F2F7"

        # Fonts
        self._setup_fonts()

        # Keyboard shortcuts
        self.bind("<Left>", lambda _event: self._change_month(-1))
        self.bind("<Right>", lambda _event: self._change_month(1))
        self.bind("<Home>", lambda _event: self._go_today())
        self.bind("t", lambda _event: self._go_today())
        self.bind("T", lambda _event: self._go_today())
        self.bind("<Escape>", lambda _event: self.destroy())

        # Build UI
        self._build_header()
        self._build_calendar_area()
        self._build_status_bar()
        self._render_month()

        # Center on screen
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 3
        self.geometry(f"+{x}+{y}")

    # ── Fonts ──────────────────────────────────────────────
    def _setup_fonts(self):
        families = tkfont.families()
        # Prefer SF Pro (macOS) → Helvetica Neue → Helvetica → system
        for fam in (
            "SF Pro Display",
            "SF Pro Text",
            ".AppleSystemUIFont",
            "Helvetica Neue",
            "Helvetica",
        ):
            if fam in families:
                base = fam
                break
        else:
            base = "TkDefaultFont"

        self.font_month = tkfont.Font(family=base, size=22, weight="bold")
        self.font_year = tkfont.Font(family=base, size=22, weight="normal")
        self.font_nav = tkfont.Font(family=base, size=18)
        self.font_day_hdr = tkfont.Font(family=base, size=11)
        self.font_day = tkfont.Font(family=base, size=15)
        self.font_today = tkfont.Font(family=base, size=15, weight="bold")
        self.font_label = tkfont.Font(family=base, size=10, weight="bold")
        self.font_status = tkfont.Font(family=base, size=12)

    # ── Header (month / year / arrows) ─────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=self.HEADER_BG, pady=14)
        hdr.pack(fill="x")

        # Left arrow
        btn_left = tk.Label(
            hdr,
            text="‹",
            font=self.font_nav,
            fg=self.TODAY_RED,
            bg=self.HEADER_BG,
            cursor="hand2",
        )
        btn_left.pack(side="left", padx=(18, 6))
        btn_left.bind("<Button-1>", lambda _event: self._change_month(-1))

        # Right arrow
        btn_right = tk.Label(
            hdr,
            text="›",
            font=self.font_nav,
            fg=self.TODAY_RED,
            bg=self.HEADER_BG,
            cursor="hand2",
        )
        btn_right.pack(side="left", padx=(0, 12))
        btn_right.bind("<Button-1>", lambda _event: self._change_month(1))

        # Month + Year
        self.lbl_month = tk.Label(
            hdr, text="", font=self.font_month, fg=self.TEXT, bg=self.HEADER_BG
        )
        self.lbl_month.pack(side="left")
        self.lbl_year = tk.Label(
            hdr, text="", font=self.font_year, fg=self.TEXT, bg=self.HEADER_BG
        )
        self.lbl_year.pack(side="left", padx=(6, 0))

        # Today button
        btn_today = tk.Label(
            hdr,
            text="Avui",
            font=self.font_day_hdr,
            fg=self.TODAY_RED,
            bg=self.HEADER_BG,
            cursor="hand2",
        )
        btn_today.pack(side="right", padx=(0, 18))
        btn_today.bind("<Button-1>", lambda _event: self._go_today())

    # ── Calendar grid area ─────────────────────────────────
    def _build_calendar_area(self):
        self.cal_frame = tk.Frame(self, bg=self.BG)
        self.cal_frame.pack(fill="both", expand=True, padx=20, pady=(4, 10))

    def _build_status_bar(self):
        self.status_label = tk.Label(
            self,
            text="",
            font=self.font_status,
            fg=self.SECONDARY,
            bg=self.BG,
            anchor="w",
            padx=20,
            pady=10,
        )
        self.status_label.pack(fill="x")

    # ── Navigation ─────────────────────────────────────────
    def _change_month(self, delta):
        m = self.current_month + delta
        y = self.current_year
        if m < 1:
            m = 12
            y -= 1
        elif m > 12:
            m = 1
            y += 1
        self.current_month = m
        self.current_year = y

        last_day = calendar.monthrange(y, m)[1]
        if self.selected_day > last_day:
            self.selected_day = last_day

        self._render_month()

    def _go_today(self):
        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_day = self.today.day
        self._render_month()

    def _select_day(self, day):
        self.selected_day = day
        self._render_month()

    # ── Render month ───────────────────────────────────────
    def _render_month(self):
        # Update header labels
        self.lbl_month.config(text=self.month_names[self.current_month])
        self.lbl_year.config(text=str(self.current_year))

        # Clear old calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        year, month = self.current_year, self.current_month
        row = 0

        quinzenes = split_quinzenes(year, month)
        row = self._draw_quinzena(quinzenes[0], row, year, month)

        # Separator
        sep = tk.Frame(self.cal_frame, bg=self.GRID_LINE, height=1)
        sep.grid(row=row, column=0, columnspan=7, sticky="ew", pady=(10, 10))
        row += 1

        self._draw_quinzena(quinzenes[1], row, year, month)
        self._update_status()

    def _draw_quinzena(self, info, start_row, year, month):
        row = start_row
        cell_w = 52
        cell_h = 40

        # Quinzena label
        lbl = tk.Label(
            self.cal_frame,
            text=info.label,
            font=self.font_label,
            fg=self.QUINZENA_LABEL,
            bg=self.BG,
            anchor="w",
        )
        lbl.grid(row=row, column=0, columnspan=7, sticky="w", pady=(4, 6))
        row += 1

        # Day-of-week headers
        for col, name in enumerate(self.day_names):
            fg = self.WEEKEND_TEXT if col >= 5 else self.SECONDARY
            lbl = tk.Label(
                self.cal_frame, text=name, font=self.font_day_hdr, fg=fg, bg=self.BG, width=4
            )
            lbl.grid(row=row, column=col, pady=(0, 4))
        row += 1

        # Day cells
        col = date(year, month, info.start_day).weekday()
        for day in range(info.start_day, info.end_day + 1):
            is_today = (
                year == self.today.year and month == self.today.month and day == self.today.day
            )
            is_selected = day == self.selected_day
            is_weekend = col >= 5

            cell = tk.Frame(self.cal_frame, width=cell_w, height=cell_h, bg=self.BG)
            cell.grid(row=row, column=col, padx=1, pady=1)
            cell.grid_propagate(False)

            self._draw_day_cell(cell, day, cell_w, cell_h, is_today, is_selected, is_weekend)

            col += 1
            if col > 6:
                col = 0
                row += 1

        # If we ended mid-row, advance to next row
        if col != 0:
            row += 1

        return row

    def _draw_day_cell(self, cell, day, cell_w, cell_h, is_today, is_selected, is_weekend):
        fg = self.WEEKEND_TEXT if is_weekend else self.TEXT
        fill = None
        outline = ""
        font = self.font_day

        if is_selected:
            fill = self.SELECTED_BLUE
            fg = "#FFFFFF"
            font = self.font_today
        elif is_today:
            fill = self.TODAY_RED
            fg = "#FFFFFF"
            font = self.font_today

        canvas = tk.Canvas(cell, width=cell_w, height=cell_h, bg=self.BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.bind("<Button-1>", lambda _event, selected_day=day: self._select_day(selected_day))
        canvas.bind("<Enter>", lambda _event: canvas.configure(bg=self.HOVER_BG))
        canvas.bind("<Leave>", lambda _event: canvas.configure(bg=self.BG))

        cx, cy = cell_w // 2, cell_h // 2
        if fill:
            radius = 16
            canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                fill=fill,
                outline=outline,
            )
        canvas.create_text(cx, cy, text=str(day), font=font, fill=fg)

    def _update_status(self):
        info = quinzena_for_day(self.current_year, self.current_month, self.selected_day)
        month_name = self.month_names[self.current_month].lower()
        today_marker = " · avui" if (
            self.current_year == self.today.year
            and self.current_month == self.today.month
            and self.selected_day == self.today.day
        ) else ""
        self.status_label.config(
            text=(
                f"Dia {self.selected_day} de {month_name}: {info.label} "
                f"({info.start_day}-{info.end_day}){today_marker}. "
                "←/→ canvia mes · T torna a avui · Esc tanca"
            )
        )


if __name__ == "__main__":
    app = QuinzenaCalendar()
    app.mainloop()
