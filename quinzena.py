"""Calendari mensual separat per quinzenes.

Aquest mòdul conté la lògica compartida entre la versió de terminal i la GUI.
Es pot importar sense efectes col·laterals i també executar directament:

    python3 quinzena.py
    python3 quinzena.py --month 12 --year 2026
"""

from __future__ import annotations

import argparse
import calendar
from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional, Sequence

DAY_NAMES_CA: Sequence[str] = ("Dl", "Dt", "Dc", "Dj", "Dv", "Ds", "Dg")
MONTH_NAMES_CA: Sequence[str] = (
    "",
    "Gener",
    "Febrer",
    "Març",
    "Abril",
    "Maig",
    "Juny",
    "Juliol",
    "Agost",
    "Setembre",
    "Octubre",
    "Novembre",
    "Desembre",
)


@dataclass(frozen=True)
class QuinzenaInfo:
    """Informació bàsica d'una quinzena concreta."""

    number: int
    label: str
    start_day: int
    end_day: int


def validate_month(year: int, month: int) -> None:
    """Valida any i mes, aixecant ValueError amb un missatge llegible."""

    if year < 1:
        raise ValueError("L'any ha de ser igual o superior a 1.")
    if not 1 <= month <= 12:
        raise ValueError("El mes ha d'estar entre 1 i 12.")


def month_name(month: int) -> str:
    """Retorna el nom del mes en català."""

    if not 1 <= month <= 12:
        raise ValueError("El mes ha d'estar entre 1 i 12.")
    return MONTH_NAMES_CA[month]


def days_in_month(year: int, month: int) -> int:
    """Retorna el nombre de dies del mes."""

    validate_month(year, month)
    return calendar.monthrange(year, month)[1]


def quinzena_for_day(year: int, month: int, day: int) -> QuinzenaInfo:
    """Retorna a quina quinzena pertany un dia del mes."""

    last_day = days_in_month(year, month)
    if not 1 <= day <= last_day:
        raise ValueError(f"El dia ha d'estar entre 1 i {last_day}.")

    if day <= 15:
        return QuinzenaInfo(1, "1a quinzena", 1, 15)
    return QuinzenaInfo(2, "2a quinzena", 16, last_day)


def split_quinzenes(year: int, month: int) -> List[QuinzenaInfo]:
    """Retorna les dues quinzenes del mes."""

    last_day = days_in_month(year, month)
    return [
        QuinzenaInfo(1, "1a QUINZENA", 1, 15),
        QuinzenaInfo(2, "2a QUINZENA", 16, last_day),
    ]


def iter_quinzena_days(info: QuinzenaInfo) -> Iterable[int]:
    """Itera els dies inclosos en una quinzena."""

    return range(info.start_day, info.end_day + 1)


def render_quinzena_calendar(
    year: int,
    month: int,
    *,
    today: Optional[date] = None,
    mark_today: bool = True,
) -> str:
    """Construeix el calendari mensual separat per quinzenes.

    Si `today` cau dins del mes renderitzat, el dia actual queda marcat entre
    claudàtors, per exemple `[ 1]`.
    """

    validate_month(year, month)
    today = today or date.today()
    lines: List[str] = []
    header = f"{month_name(month)} {year}"

    for index, info in enumerate(split_quinzenes(year, month)):
        if index:
            lines.append("")

        lines.append(f"{header} - {info.label}")
        lines.append(" ".join(f"{name:>4}" for name in DAY_NAMES_CA))

        start_weekday = date(year, month, info.start_day).weekday()
        current_line = ["    "] * start_weekday

        for day in iter_quinzena_days(info):
            is_today = (
                mark_today
                and today.year == year
                and today.month == month
                and today.day == day
            )
            cell = f"[{day:2d}]" if is_today else f" {day:2d} "
            current_line.append(cell)

            if len(current_line) == 7:
                lines.append(" ".join(current_line).rstrip())
                current_line = []

        if current_line:
            lines.append(" ".join(current_line).rstrip())

    current = None
    if today.year == year and today.month == month:
        current = quinzena_for_day(year, month, today.day)

    if current:
        lines.append("")
        lines.append(
            f"Avui és dia {today.day}: {current.label} "
            f"({current.start_day}-{current.end_day} de {month_name(month).lower()})."
        )

    return "\n".join(lines)


def print_quinzena_calendar(year: int, month: int) -> None:
    """Mostra per pantalla el calendari de quinzenes."""

    print(render_quinzena_calendar(year, month))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mostra un calendari mensual separat en 1a i 2a quinzena."
    )
    current = date.today()
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=current.year,
        help=f"any a mostrar (per defecte: {current.year})",
    )
    parser.add_argument(
        "-m",
        "--month",
        type=int,
        default=current.month,
        help=f"mes a mostrar, 1-12 (per defecte: {current.month})",
    )
    parser.add_argument(
        "--no-today",
        action="store_true",
        help="no marca el dia d'avui ni mostra el resum final",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        text = render_quinzena_calendar(
            args.year,
            args.month,
            today=date.today(),
            mark_today=not args.no_today,
        )
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
