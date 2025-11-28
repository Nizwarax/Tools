from rich.panel import Panel
from rich.table import Table
from rich.box import MINIMAL_DOUBLE_HEAD

from app.theme import _c, console
from app.menus.util import clear_screen, pause
from app.service.history import get_history, add_to_history, clear_history

def show_family_code_menu(is_enterprise: bool = False):
    """
    Displays the family code menu with history and input option.
    Returns the selected or input family code, or None if cancelled.
    """
    while True:
        clear_screen()
        history = get_history(is_enterprise)
        title_suffix = " (Enterprise)" if is_enterprise else ""

        table = Table(box=MINIMAL_DOUBLE_HEAD, expand=True)
        table.add_column("No", justify="right", style=_c("text_number"), width=4)
        table.add_column("Family Code", style=_c("text_body"))

        table.add_row("[bold]0[/]", f"[{_c('text_ok')}]Input New Code[/{_c('text_ok')}]")
        table.add_row("[bold]00[/]", f"[{_c('text_warn')}]Hapus Semua Riwayat[/{_c('text_warn')}]")

        for idx, code in enumerate(history, 1):
            table.add_row(f"[bold]{idx}[/]", code)

        table.add_row("[bold]99[/]", f"[{_c('text_err')}]Back to Main Menu[/{_c('text_err')}]")

        panel = Panel(
            table,
            title=f"[{_c('text_title')}]Pilih Family Code{title_suffix}[/]",
            border_style=_c("border_primary"),
            padding=(1, 0),
            expand=True
        )
        console.print(panel)

        choice = console.input(f"\n[{_c('text_sub')}]Pilih opsi (0-{len(history)}):[/{_c('text_sub')}] ").strip()

        if choice == "99":
            return None

        if choice == "0":
            new_code = console.input(f"[{_c('text_sub')}]Masukkan family code baru:[/{_c('text_sub')}] ").strip()
            if new_code:
                add_to_history(new_code, is_enterprise)
                return new_code
            else:
                return None

        if choice == "00":
            clear_history(is_enterprise)
            console.print(f"[{_c('text_ok')}]Riwayat berhasil dihapus.[/{_c('text_ok')}]")
            pause()
            continue

        try:
            idx = int(choice)
            if 1 <= idx <= len(history):
                selected_code = history[idx - 1]
                # Move to top of history (refresh recency)
                add_to_history(selected_code, is_enterprise)
                return selected_code
            else:
                console.print(f"[{_c('text_err')}]Pilihan tidak valid.[/{_c('text_err')}]")
                pause()
        except ValueError:
            console.print(f"[{_c('text_err')}]Input harus berupa angka.[/{_c('text_err')}]")
            pause()
