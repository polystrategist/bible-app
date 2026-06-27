"""NiceGUI admin for the default databases in defaults/Main/.

A pure-Python admin UI (rendered with Vue 3 + Quasar under the hood) with a left
drawer to switch between sections:

  - Strong's       full editor over data/strongs.json (the source of truth),
                   which builds defaults/Main/strongs.db + bumps its version.
  - Dictionary     searchable, paginated browser over defaults/Main/Dictionary.db
                   (read-only for now — 176k rows, no JSON source yet).
  - Cross Refs     searchable, paginated browser over cross_references.db
                   (read-only for now — 433k rows).

Run from this folder:
    python admin.py              # opens http://localhost:8080

Env overrides: MANAGE_PORT (default 8080), MANAGE_SHOW=0 to not open a browser.
"""

import datetime
import json
import math
import os
import shutil
import sqlite3

from nicegui import ui

import common

# Editing 14k Strong's rows at once is heavy, so the table only renders the
# first MAX_ROWS matches. Filter/search to narrow down.
MAX_ROWS = 1000
PAGE_SIZE = 50
LANGUAGES = ["greek", "hebrew"]

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
LOGS_DIR = os.path.join(HERE, "logs")
DEFAULTS_DIR = os.path.join(HERE, "..", "..", "defaults", "Main")

# Single shared Strong's dataset for this local, single-user tool.
state = {"rows": common.load_rows_from_json(), "dirty": False}

STRONGS_COLUMNS = [
    {"name": "strong_number", "label": "Strong #", "field": "strong_number",
     "sortable": True, "align": "left"},
    {"name": "language", "label": "Lang", "field": "language",
     "sortable": True, "align": "left"},
    {"name": "lemma", "label": "Lemma", "field": "lemma", "align": "left"},
    {"name": "translit", "label": "Translit", "field": "translit", "align": "left"},
    {"name": "pronunciation", "label": "Pron", "field": "pronunciation", "align": "left"},
    {"name": "strongs_def", "label": "Strong's def", "field": "strongs_def", "align": "left",
     "style": "max-width: 420px; white-space: normal; word-break: break-word;"},
    {"name": "kjv_def", "label": "KJV def", "field": "kjv_def", "align": "left",
     "style": "max-width: 240px; white-space: normal; word-break: break-word;"},
    {"name": "actions", "label": "Actions", "field": "actions", "align": "center"},
]


# ============================================================================
# Strong's section (full editor over the JSON source of truth)
# ============================================================================

def get_row(strong_number):
    """Resolve the live dict in state['rows'] (table events carry copies)."""
    for row in state["rows"]:
        if row["strong_number"] == strong_number:
            return row
    return None


def mark_dirty():
    state["dirty"] = True
    strongs_status.refresh()


def save_json():
    n = common.save_rows_to_json(state["rows"])
    state["dirty"] = False
    strongs_status.refresh()
    log_change("strongs", "SAVE", f"{n} entries", "wrote data/strongs.json")
    ui.notify(f"Saved {n} entries to strongs.json", type="positive")


def build_db():
    common.save_rows_to_json(state["rows"])
    state["dirty"] = False
    count = common.build_db(state["rows"])
    version = common.bump_version()
    strongs_status.refresh()
    log_change("strongs", "BUILD", f"version={version}",
               f"{count} entries -> defaults/Main/strongs.db")
    ui.notify(f"Built strongs.db ({count} entries) · version {version}",
              type="positive")


def reload_json():
    state["rows"] = common.load_rows_from_json()
    state["dirty"] = False
    refresh_strongs()
    ui.notify("Reloaded from strongs.json")


def _entry_form(values):
    """Render the shared entry fields (outlined); return a dict of inputs."""
    fields = {
        "language": ui.select(LANGUAGES, value=values.get("language", "greek"),
                              label="Language"),
        "lemma": ui.input("Lemma", value=values.get("lemma", "")),
        "translit": ui.input("Transliteration", value=values.get("translit", "")),
        "pronunciation": ui.input("Pronunciation (Hebrew only)",
                                 value=values.get("pronunciation", "")),
        "derivation": ui.textarea("Derivation", value=values.get("derivation", "")),
        "strongs_def": ui.textarea("Strong's definition",
                                  value=values.get("strongs_def", "")),
        "kjv_def": ui.input("KJV definition", value=values.get("kjv_def", "")),
    }
    for widget in fields.values():
        widget.props("outlined dense").classes("w-full")
    return fields


def edit_entry(row_copy):
    row = get_row(row_copy["strong_number"])
    if row is None:
        return
    with ui.dialog() as dialog, ui.card().classes("w-[640px]"):
        ui.label(f"Edit {row['strong_number']}").classes("text-lg font-bold")
        fields = _entry_form(row)

        def save():
            changes = {}
            for name, widget in fields.items():
                new_value = (widget.value or "").strip()
                if str(row.get(name) or "") != new_value:
                    changes[name] = (row.get(name), new_value)
                row[name] = new_value
            mark_dirty()
            strongs_table.update()
            if changes:
                log_change("strongs", "UPDATE", f"strong_number={row['strong_number']}",
                           "; ".join(f"{k}: {o!r} -> {n!r}"
                                     for k, (o, n) in changes.items()))
            ui.notify(f"Updated {row['strong_number']}", type="positive")
            dialog.close()

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Save", on_click=save).props("color=primary")
    dialog.open()


def delete_entry(row_copy):
    key = row_copy["strong_number"]
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete {key}?").classes("text-lg")
        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")

            def do_delete():
                state["rows"][:] = [r for r in state["rows"]
                                    if r["strong_number"] != key]
                mark_dirty()
                refresh_strongs()
                log_change("strongs", "DELETE", f"strong_number={key}")
                ui.notify(f"Deleted {key}", type="warning")
                dialog.close()

            ui.button("Delete", on_click=do_delete).props("color=negative")
    dialog.open()


def add_entry():
    with ui.dialog() as dialog, ui.card().classes("w-[640px]"):
        ui.label("Add entry").classes("text-lg font-bold")
        key_input = ui.input("Strong number (e.g. G5624 or H1234)")
        key_input.props("outlined dense").classes("w-full")
        fields = _entry_form({})

        def save():
            key = (key_input.value or "").strip()
            if not key:
                ui.notify("Strong number is required", type="negative")
                return
            if get_row(key) is not None:
                ui.notify(f"{key} already exists", type="negative")
                return
            entry = {"strong_number": key}
            entry.update({name: (w.value or "").strip() for name, w in fields.items()})
            state["rows"].append(entry)
            mark_dirty()
            refresh_strongs()
            log_change("strongs", "ADD", f"strong_number={key}",
                       ", ".join(f"{k}={v!r}" for k, v in entry.items()
                                 if k != "strong_number"))
            ui.notify(f"Added {key}", type="positive")
            dialog.close()

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Add", on_click=save).props("color=primary")
    dialog.open()


def refresh_strongs():
    needle = (strongs_search.value or "").strip().lower()
    lang = strongs_lang.value
    matched = []
    for row in state["rows"]:
        if lang != "all" and row["language"] != lang:
            continue
        if needle:
            hay = " ".join([
                row["strong_number"], row["lemma"], row["translit"],
                row["strongs_def"], row["kjv_def"],
            ]).lower()
            if needle not in hay:
                continue
        matched.append(row)
    strongs_table.rows = matched[:MAX_ROWS]
    strongs_table.update()
    strongs_status.refresh()
    strongs_shown.set_text(
        f"Showing {len(strongs_table.rows)} of {len(matched)} matches"
        + (f" (capped at {MAX_ROWS})" if len(matched) > MAX_ROWS else "")
    )


# ============================================================================
# Generic read-only DB browser (Dictionary, Cross References)
# ============================================================================

def working_db(name):
    """Path to the working copy in data/, copied from defaults/Main if missing."""
    dst = os.path.join(DATA_DIR, name)
    if not os.path.exists(dst):
        os.makedirs(DATA_DIR, exist_ok=True)
        shutil.copy2(os.path.join(DEFAULTS_DIR, name), dst)
    return dst


def query_page(database, table, columns, where_sql, params, page):
    """Return (rows_as_dicts, total) for one page of a table."""
    conn = sqlite3.connect(working_db(database))
    try:
        count_sql = f"SELECT COUNT(*) FROM {table}"
        if where_sql:
            count_sql += f" WHERE {where_sql}"
        total = conn.execute(count_sql, params).fetchone()[0]
        sql = f"SELECT {', '.join(columns)} FROM {table}"
        if where_sql:
            sql += f" WHERE {where_sql}"
        sql += f" LIMIT {PAGE_SIZE} OFFSET {(page - 1) * PAGE_SIZE}"
        rows = [dict(zip(columns, r)) for r in conn.execute(sql, params)]
    finally:
        conn.close()
    return rows, total


def db_write(database, sql, params):
    """Run a write statement against the working copy in data/ and commit.

    Returns the last inserted rowid (useful for logging new rows).
    """
    conn = sqlite3.connect(working_db(database))
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def log_change(section, action, identity, detail=""):
    """Append a change record to logs/<section>-<Y-m-d>.db.log for easy tracking."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    path = os.path.join(LOGS_DIR, f"{section}-{datetime.date.today().isoformat()}.db.log")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{stamp} | {action:6} | {identity}"
    if detail:
        line += f" | {detail}"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def bump_json_version(path):
    """Increment {"version": N} in a sibling version file. Returns new version."""
    version = 0
    if os.path.exists(path) and os.path.getsize(path):
        with open(path, encoding="utf-8") as fh:
            version = int(json.load(fh).get("version", 0))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"version": version + 1}, fh, indent=4)
        fh.write("\n")
    return version + 1


def next_dict_version():
    """Next value for Dictionary.db's in-DB `version` table (numeric if possible)."""
    conn = sqlite3.connect(working_db("Dictionary.db"))
    try:
        row = conn.execute("SELECT dictionary_version FROM version LIMIT 1").fetchone()
    finally:
        conn.close()
    current = row[0] if row else "0"
    try:
        return int(current) + 1
    except (TypeError, ValueError):
        return current


def confirm(message, on_yes, yes_label="Confirm", yes_color="primary"):
    """Open a Cancel / confirm dialog; run on_yes only if confirmed."""
    with ui.dialog() as dialog, ui.card():
        ui.label(message).classes("text-base")
        with ui.row().classes("w-full justify-end"):
            ui.button("Cancel", on_click=dialog.close).props("flat")

            def yes():
                dialog.close()
                on_yes()

            ui.button(yes_label, on_click=yes).props(f"color={yes_color}")
    dialog.open()


def build_browser(database, table, id_column, edit_columns, columns, table_columns,
                  filter_factory, hint, ship_label, ship_action):
    """Build a paginated, editable browser over a working-copy DB in data/.

    Edits (add / edit / delete) write straight to the data/ copy; `ship_action`
    copies that copy to defaults/Main and bumps the relevant version.
    """
    bstate = {"page": 1, "pages": 1}
    section = database[:-3].lower() if database.lower().endswith(".db") else database.lower()

    ui.label(hint).classes("text-sm text-gray-400")

    def reload(reset_page=True):
        if reset_page:
            bstate["page"] = 1
        where_sql, params = get_filter()
        rows, total = query_page(database, table, columns, where_sql, params,
                                 bstate["page"])
        tbl.rows = rows
        tbl.update()
        bstate["pages"] = max(1, math.ceil(total / PAGE_SIZE))
        info.text = f"Page {bstate['page']} / {bstate['pages']} · {total:,} rows"
        info.update()

    def coerce(value, ctype):
        if value is None or value == "":
            return None
        if ctype == "number":
            try:
                return int(value)
            except (TypeError, ValueError):
                return value
        return str(value).strip()

    def field_widget(col, value):
        if col["type"] == "number":
            widget = ui.number(col["label"],
                               value=value if value not in (None, "") else None,
                               format="%d")
        elif col["type"] == "textarea":
            widget = ui.textarea(col["label"], value="" if value is None else str(value))
        else:
            widget = ui.input(col["label"], value="" if value is None else str(value))
        return widget.props("outlined dense").classes("w-full")

    def open_form(title, row, on_save):
        with ui.dialog() as dialog, ui.card().classes("w-[640px]"):
            ui.label(title).classes("text-lg font-bold")
            inputs = {c["name"]: field_widget(c, (row or {}).get(c["name"]))
                      for c in edit_columns}

            def submit():
                values = {c["name"]: coerce(inputs[c["name"]].value, c["type"])
                          for c in edit_columns}
                on_save(values)
                dialog.close()

            with ui.row().classes("w-full justify-end"):
                ui.button("Cancel", on_click=dialog.close).props("flat")
                ui.button("Save", on_click=submit).props("color=primary")
        dialog.open()

    def open_edit(row):
        def save(values):
            sets = ", ".join(f"{name}=?" for name in values)
            db_write(database, f"UPDATE {table} SET {sets} WHERE {id_column}=?",
                     list(values.values()) + [row[id_column]])
            changes = "; ".join(
                f"{k}: {row.get(k)!r} -> {v!r}" for k, v in values.items()
                if str(row.get(k) or "") != str(v or "")
            ) or "(no change)"
            log_change(section, "UPDATE", f"{id_column}={row[id_column]}", changes)
            reload(reset_page=False)
            ui.notify(f"Updated #{row.get(id_column)}", type="positive")
        open_form(f"Edit #{row.get(id_column)}", row, save)

    def open_add():
        def save(values):
            names = list(values)
            new_id = db_write(database,
                              f"INSERT INTO {table} ({', '.join(names)}) "
                              f"VALUES ({', '.join('?' * len(names))})",
                              list(values.values()))
            log_change(section, "ADD", f"{id_column}={new_id}",
                       ", ".join(f"{k}={v!r}" for k, v in values.items()))
            reload(reset_page=True)
            ui.notify("Added entry", type="positive")
        open_form("Add entry", None, save)

    def open_delete(row):
        def do():
            db_write(database, f"DELETE FROM {table} WHERE {id_column}=?",
                     [row[id_column]])
            log_change(section, "DELETE", f"{id_column}={row[id_column]}",
                       ", ".join(f"{k}={row.get(k)!r}" for k in columns
                                 if k != id_column))
            reload(reset_page=False)
            ui.notify(f"Deleted #{row.get(id_column)}", type="warning")
        confirm(f"Delete entry #{row.get(id_column)} from the working copy?",
                do, yes_label="Delete", yes_color="negative")

    def do_ship():
        ship_action()
        log_change(section, "SHIP", "-> defaults/Main", "copied working copy + bumped version")
        ui.notify("Saved & shipped to defaults/Main", type="positive")

    def step(delta):
        bstate["page"] = max(1, min(bstate["pages"], bstate["page"] + delta))
        reload(reset_page=False)

    with ui.row().classes("w-full items-center gap-3"):
        get_filter = filter_factory(lambda: reload(reset_page=True))
        ui.space()
        ui.button("➕ Add", on_click=open_add).props("color=primary outline")
        ui.button(ship_label, on_click=lambda: confirm(
            "Copy your edits to defaults/Main and bump the shipped version?",
            do_ship, yes_label="Save & ship")).props("color=primary")

    # Load the first page synchronously and pass it into the constructors so it
    # renders on first paint (updating .rows from startup does not propagate).
    where0, params0 = get_filter()
    rows0, total0 = query_page(database, table, columns, where0, params0, 1)
    bstate["pages"] = max(1, math.ceil(total0 / PAGE_SIZE))

    with ui.row().classes("items-center gap-2"):
        ui.button(icon="chevron_left", on_click=lambda: step(-1)).props("flat dense")
        info = ui.label(f"Page 1 / {bstate['pages']} · {total0:,} rows").classes("text-sm")
        ui.button(icon="chevron_right", on_click=lambda: step(1)).props("flat dense")

    display_columns = table_columns + [
        {"name": "actions", "label": "Actions", "field": "actions", "align": "center"}]
    tbl = (ui.table(columns=display_columns, rows=rows0, row_key=id_column)
           .props("wrap-cells").classes("w-full"))
    tbl.add_slot("body-cell-actions", """
        <q-td :props="props" class="text-center">
            <q-btn dense flat round color="primary" icon="edit"
                   @click="() => $parent.$emit('edit', props.row)">
                <q-tooltip>Edit</q-tooltip>
            </q-btn>
            <q-btn dense flat round color="negative" icon="delete"
                   @click="() => $parent.$emit('delete', props.row)">
                <q-tooltip>Delete</q-tooltip>
            </q-btn>
        </q-td>
    """)
    tbl.on("edit", lambda e: open_edit(e.args))
    tbl.on("delete", lambda e: open_delete(e.args))


def build_dictionary():
    columns = ["rowid", "word", "wordtype", "definition"]
    table_columns = [
        {"name": "word", "label": "Word", "field": "word", "align": "left", "sortable": True},
        {"name": "wordtype", "label": "Type", "field": "wordtype", "align": "left"},
        {"name": "definition", "label": "Definition", "field": "definition", "align": "left",
         "style": "max-width: 720px; white-space: normal; word-break: break-word;"},
    ]
    edit_columns = [
        {"name": "word", "label": "Word", "type": "text"},
        {"name": "wordtype", "label": "Type", "type": "text"},
        {"name": "definition", "label": "Definition", "type": "textarea"},
    ]

    def filter_factory(on_change):
        search = ui.input("Search word", on_change=on_change)
        search.props("outlined dense clearable").classes("w-72")

        def get_filter():
            term = (search.value or "").strip()
            if term:
                return "word LIKE ?", [f"%{term}%"]
            return "", []

        return get_filter

    def ship():
        # Dictionary stores its version inside the DB (version table).
        db_write("Dictionary.db", "UPDATE version SET dictionary_version=?",
                 [str(next_dict_version())])
        shutil.copy2(working_db("Dictionary.db"),
                     os.path.join(DEFAULTS_DIR, "Dictionary.db"))

    build_browser(
        "Dictionary.db", "entries", "rowid", edit_columns, columns, table_columns,
        filter_factory,
        "Editing the working copy in data/Dictionary.db. Search matches the word column.",
        "Save & ship to defaults", ship,
    )


def build_cross_references():
    columns = ["id", "from_book", "from_chapter", "from_verse",
               "to_book", "to_chapter", "to_verse_start", "to_verse_end", "votes"]
    table_columns = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {"name": "from_book", "label": "From book", "field": "from_book", "align": "left"},
        {"name": "from_chapter", "label": "Ch", "field": "from_chapter", "align": "left"},
        {"name": "from_verse", "label": "V", "field": "from_verse", "align": "left"},
        {"name": "to_book", "label": "To book", "field": "to_book", "align": "left"},
        {"name": "to_chapter", "label": "Ch", "field": "to_chapter", "align": "left"},
        {"name": "to_verse_start", "label": "V start", "field": "to_verse_start", "align": "left"},
        {"name": "to_verse_end", "label": "V end", "field": "to_verse_end", "align": "left"},
        {"name": "votes", "label": "Votes", "field": "votes", "align": "left"},
    ]

    edit_columns = [
        {"name": "from_book", "label": "From book", "type": "number"},
        {"name": "from_chapter", "label": "From chapter", "type": "number"},
        {"name": "from_verse", "label": "From verse", "type": "number"},
        {"name": "to_book", "label": "To book", "type": "number"},
        {"name": "to_chapter", "label": "To chapter", "type": "number"},
        {"name": "to_verse_start", "label": "To verse start", "type": "number"},
        {"name": "to_verse_end", "label": "To verse end", "type": "number"},
        {"name": "votes", "label": "Votes", "type": "number"},
    ]

    def filter_factory(on_change):
        book = ui.number("Filter: from_book", on_change=on_change, format="%d")
        book.props("outlined dense clearable").classes("w-48")

        def get_filter():
            if book.value is not None:
                return "from_book = ?", [int(book.value)]
            return "", []

        return get_filter

    def ship():
        shutil.copy2(working_db("cross_references.db"),
                     os.path.join(DEFAULTS_DIR, "cross_references.db"))
        bump_json_version(os.path.join(DEFAULTS_DIR, "cross_references_version.json"))

    build_browser(
        "cross_references.db", "cross_references", "id", edit_columns, columns,
        table_columns, filter_factory,
        "Editing the working copy in data/cross_references.db. "
        "Filter by from_book (bibleBooks number, e.g. Matthew=470).",
        "Save & ship to defaults", ship,
    )


# ============================================================================
# Layout: header + left drawer + switchable section containers
# ============================================================================

ui.dark_mode().enable()

SECTIONS = [
    ("Strong's", "translate"),
    ("Dictionary", "menu_book"),
    ("Cross References", "hub"),
]

with ui.header().classes("items-center"):
    ui.button(icon="menu", on_click=lambda: drawer.toggle()).props("flat color=white")
    ui.label("Manage Defaults").classes("text-lg font-bold")

nav_buttons = {}
with ui.left_drawer(value=True, bordered=True).props("width=220") as drawer:
    ui.label("Sections").classes("text-xs uppercase text-gray-500 q-mb-sm")
    for name, icon in SECTIONS:
        nav_buttons[name] = ui.button(
            name, icon=icon, on_click=lambda n=name: select_section(n)
        ).props("flat align=left no-caps").classes("w-full")

containers = {}
with ui.column().classes("w-full p-4 gap-4"):
    for name, _ in SECTIONS:
        containers[name] = ui.column().classes("w-full gap-3")

# --- Strong's container (module-global widgets so handlers can see them) -----
with containers["Strong's"]:
    ui.label("Strong's Dictionary").classes("text-2xl font-bold")
    with ui.row().classes("w-full items-center gap-2"):
        ui.button("Save to strongs.json",
                  on_click=lambda: confirm("Save edits to data/strongs.json?", save_json)
                  ).props("color=primary outline")
        ui.button("Build strongs.db + bump version",
                  on_click=lambda: confirm(
                      "Build defaults/Main/strongs.db and bump the shipped version?",
                      build_db, yes_label="Build")).props("color=primary")
        ui.button("Reload", on_click=reload_json).props("flat")

    @ui.refreshable
    def strongs_status():
        counts = {}
        for row in state["rows"]:
            counts[row["language"]] = counts.get(row["language"], 0) + 1
        with ui.row().classes("items-center gap-4"):
            ui.label(f"Entries: {len(state['rows'])}").classes("text-sm")
            ui.label(f"greek: {counts.get('greek', 0)} · hebrew: {counts.get('hebrew', 0)}"
                     ).classes("text-sm text-gray-400")
            ui.label(f"Shipped version: {common.read_version()}").classes("text-sm text-gray-400")
            ui.badge("Unsaved changes" if state["dirty"] else "Saved",
                     color="orange" if state["dirty"] else "green")

    strongs_status()

    with ui.row().classes("w-full items-center gap-4"):
        strongs_lang = ui.select(["all"] + LANGUAGES, value="all", label="Language",
                                 on_change=lambda: refresh_strongs())
        strongs_lang.props("outlined dense").classes("w-40")
        strongs_search = ui.input("Search", placeholder="strong #, lemma, definition…",
                                  on_change=lambda: refresh_strongs())
        strongs_search.props("outlined dense clearable").classes("grow")
        ui.button("➕ Add entry", on_click=add_entry).props("color=primary")

    _initial_strongs = state["rows"][:MAX_ROWS]
    strongs_shown = ui.label(
        f"Showing {len(_initial_strongs)} of {len(state['rows'])} matches"
        + (f" (capped at {MAX_ROWS})" if len(state["rows"]) > MAX_ROWS else "")
    ).classes("text-sm text-gray-400")

    strongs_table = (ui.table(columns=STRONGS_COLUMNS, rows=_initial_strongs,
                              row_key="strong_number", pagination=25)
                     .props("wrap-cells").classes("w-full"))
    strongs_table.add_slot("body-cell-actions", """
        <q-td :props="props" class="text-center">
            <q-btn dense flat round color="primary" icon="edit"
                   @click="() => $parent.$emit('edit', props.row)">
                <q-tooltip>Edit</q-tooltip>
            </q-btn>
            <q-btn dense flat round color="negative" icon="delete"
                   @click="() => $parent.$emit('delete', props.row)">
                <q-tooltip>Delete</q-tooltip>
            </q-btn>
        </q-td>
    """)
    strongs_table.on("edit", lambda e: edit_entry(e.args))
    strongs_table.on("delete", lambda e: delete_entry(e.args))

# --- Dictionary + Cross References browsers ---------------------------------
with containers["Dictionary"]:
    ui.label("Dictionary").classes("text-2xl font-bold")
    build_dictionary()

with containers["Cross References"]:
    ui.label("Cross References").classes("text-2xl font-bold")
    build_cross_references()


def select_section(name):
    for key, container in containers.items():
        container.set_visibility(key == name)
    for key, button in nav_buttons.items():
        if key == name:
            button.props(remove="flat")
            button.props("color=primary")
        else:
            button.props(remove="color")
            button.props("flat")


select_section("Strong's")

ui.run(
    title="Manage Defaults",
    port=int(os.getenv("MANAGE_PORT", "8080")),
    show=os.getenv("MANAGE_SHOW", "1") != "0",
    reload=False,
)
