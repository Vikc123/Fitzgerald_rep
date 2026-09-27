# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

Personal academic Python monorepo — no single application, no package manifest, no CI. Three distinct zones:

- `Sem_3/`, `Sem_4/` — semester coursework, one folder per lab (`Lab_1`, `Lab_2`, ...), covering sorting/search, graphs, AVL/Red-Black trees, hashing.
- `Course_project/` — the one real application: a PyQt6 desktop GUI backed by hand-rolled data structures. This is the only folder marked as the PyCharm source root (`.idea/Fitzgerald.iml`).
- `knowledge_recovery/` — small throwaway scripts for practicing/reviewing Python (basic syntax, collections, classes), including unfinished/buggy code. Not meant to be correct or complete.

There is no `requirements.txt`/`pyproject.toml`/etc. The only dependency signal is the checked-in `venv/` (Python 3.12, with PyQt6 installed for `Course_project`).

## Running code

Activate the existing virtualenv first: `source venv/bin/activate`.

- **Course_project**: run from inside the directory — `cd Course_project && python main.py`. Imports (`from mods...`, `from gui...`) and data paths (`data/users.txt`, `data/views.txt`) are relative to this directory. Each run regenerates random sample data into `data/users.txt`/`data/views.txt` before opening the GUI.
- **Lab folders** (`Sem_3/Lab_N`, `Sem_4/Lab_N`): each is self-contained — run from inside the specific lab directory, e.g. `cd Sem_4/Lab_2 && python main.py`. The lab's local package (`mods/` or `modules/`) and its `data/` paths are relative to that directory, so running from the repo root or another lab's directory will break imports.
- **knowledge_recovery scripts**: standalone, run directly, e.g. `python knowledge_recovery/classes/BST.py`.

## Testing

There is no automated test framework (no pytest/unittest anywhere in the repo). Verification is manual: every script ends with `if __name__ == "__main__": main()` and is run directly, with correctness checked by reading the printed output. A file named `test.py` (e.g. `knowledge_recovery/classes/test.py`) is a scratch experiment, not a test suite — don't assume `test_*.py`/`*_test.py` naming means pytest is in use anywhere in this repo.

## Course_project architecture

`Course_project/main.py` wires together:

- `mods/movie_service.py` (`MovieService`) — facade over two managers, used directly by the GUI.
  - `mods/users_manager.py` (`UsersManager`) — backed by a hand-rolled hash table (`mods/hash_table.py`, `initial_capacity` configurable via the GUI capacity dialog), keyed by email.
  - `mods/views_manager.py` (`ViewsManager`) — backed by a hand-rolled red-black tree (`mods/red_black_tree.py`), keyed by release date (`ViewDate.to_number()`).
- `mods/models.py` — `UserRecord`/`ViewRecord` dataclasses with `from_line`/`to_line` for the `;`-delimited text file format used in `data/*.txt`.
- `gui/users_window.py`, `gui/views_window.py` (+ `user_dialog.py`, `view_dialog.py`) — PyQt6 windows; `main.py` opens both side by side.
- `mods/array_storage.py` (`ArrayStorage`) and `mods/linked_list.py` also exist in `mods/` but are not mentioned above because their current role in the data flow (e.g. whether they hold the "исходный массив записей" referenced by the tree/hash table, per the requirements below) has not been audited yet — confirm before relying on this description.

Lookup methods (`find_by_email`, `find_by_year`, etc.) return `(result, steps)` tuples — `steps` counts comparisons/probes made by the underlying tree/hash table. This is intentional and load-bearing: the point of the project is implementing and evaluating the data structures, not just the CRUD GUI on top. Preserve the `steps` return value when touching these methods.

Business-rule error messages (e.g. duplicate user IDs, deleting a user who still has views) are raised as `ValueError` with Russian-language text — match this convention in that module rather than switching to English.

## Conventions to be aware of

- Comments, identifiers, and folder names are mixed English/Russian throughout (e.g. `Sem_4/Lab_2/задача` alongside `task/`). This is pre-existing and expected, not something to "fix".
- There is no root `.gitignore`, so `__pycache__/`, `.pyc`, and `.DS_Store` files show up as untracked in `git status`. Don't `git add` these; a root `.gitignore` covering them would be a reasonable improvement to suggest if asked.

## Курсовая работа (Course_project) — правила работы

Эти правила приоритетнее общих договорённостей выше, когда речь идёт о работе над курсовой.

**Границы изменений:**
- `Course_project/` — это сама курсовая работа. Основные изменения кода вносятся только здесь.
- `Sem_3/` и `Sem_4/` — лабораторные работы, на основе которых сделана курсовая. Их можно читать и использовать как справочный материал (готовые реализации структур данных, подходы), но **нельзя изменять без отдельного явного разрешения** пользователя.
- Не менять предметную область проекта (пользователи/подписки/просмотры фильмов) без подтверждения пользователя.
- Не переписывать проект с нуля без необходимости — правки должны быть точечными, в рамках существующей архитектуры.
- Не удалять файлы без отдельного разрешения.
- Не выполнять долгие или потенциально опасные команды без подтверждения пользователя.

**Источник требований:**
- Главный источник требований — ТЗ/задание внутри `Course_project/task/` (`1_постановка_задачи.pdf`, `2_идз_КП.pdf`, `3_ПО.pdf`, `4_варианты.pdf`).
- Замечания преподавателя — дополнительные обязательные требования поверх ТЗ.
- Если требования ТЗ и текущая реализация противоречат друг другу — **сначала явно указать противоречие и предложить вариант исправления**, не исправлять молча.

**Процесс работы:**
- Перед изменением файлов — сначала аудит текущего состояния, затем план, затем список файлов, которые будут затронуты. Только после этого — правки.
- После любых изменений — показать список изменённых файлов.
- Если найдена ошибка — сначала объяснить её причину, потом предлагать исправление (не наоборот).
- Все объяснения должны быть на уровне, достаточном для защиты курсовой преподавателю: что сделано, зачем, как это соответствует ТЗ.
- Отвечать пользователю на русском языке.

**Обязательные технические требования к курсовой:**

1. В проекте должно быть два справочника: пользователей и просмотров/фильмов.
2. Справочник пользователей — собственная хэш-таблица с открытой адресацией и двойным хешированием (`mods/hash_table.py` / `mods/users_manager.py`), не встроенный `dict` Python.
3. Ключ хэш-таблицы — email пользователя (для строковых ключей используется полиномиальная нормализация в `HashTable._normalize_key` перед вычислением первичной/вторичной хеш-функции).
4. При совпадающих ключах записи хранятся списком внутри слота хэш-таблицы, а не затирают друг друга.
5. В хэш-таблице должна быть реализована обработка коллизий.
6. Справочник просмотров/фильмов — красно-чёрное дерево (`mods/red_black_tree.py` / `mods/views_manager.py`), ключ — дата выпуска фильма (`ViewDate.to_number()`).
7. При совпадающих ключах записи хранятся списком внутри узла дерева, а не затирают друг друга.
8. Удаление узла с двумя потомками — через замену на **predecessor** (максимальный элемент в левом поддереве), а не successor.
9. Для обоих справочников должны быть реализованы операции: добавление, поиск, удаление, вывод.
10. Должна быть прослеживаемая связь между исходными массивами записей и структурами данных (деревом/хэш-таблицей), построенными на их основе — см. пункт про `mods/array_storage.py` выше, требует проверки при аудите.
11. Нужно чётко понимать и уметь объяснить, хранят ли структуры **ссылки на записи** или **независимые копии** — это должно быть согласовано между `ArrayStorage`/списками записей и деревом/хэш-таблицей.
12. После удаления записи не должно оставаться неактуальных (висячих) ссылок ни в дереве, ни в хэш-таблице.
13. На защите нужно уметь показать конкретное место в коде, где реализована каждая из операций выше (добавление/поиск/удаление/вывод для обеих структур, обработка коллизий, замена на predecessor, хранение списка при дубликатах ключей).
