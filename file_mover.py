import os
import shutil
from pathlib import Path


def _resolve_name_conflict(dest_dir, file_name, taken_names):
    candidate = file_name
    if (dest_dir / candidate).exists() or candidate in taken_names:
        original_path = Path(file_name)
        base_name = original_path.stem
        file_ext = original_path.suffix

        candidate = f"{base_name}_moved{file_ext}"
        counter = 2
        while (dest_dir / candidate).exists() or candidate in taken_names:
            candidate = f"{base_name}_moved{counter}{file_ext}"
            counter += 1

    return candidate


def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_to_check = Path(root) / dir_name
            try:
                if not any(dir_to_check.iterdir()):
                    dir_to_check.rmdir()
            except OSError:
                pass


def move_and_clean_project(target_dir, rules, ignore_folders=None):
    if ignore_folders is None:
        ignore_folders = {".git", "node_modules", "venv", ".godot", "__pycache__"}
    else:
        ignore_folders = set(ignore_folders)

    original_path = Path(target_dir).resolve()

    if not original_path.exists():
        raise FileNotFoundError(f"Directory not found: {target_dir}")

    clean_path = original_path.parent / f"{original_path.name}_clean"

    if clean_path.exists():
        shutil.rmtree(clean_path)

    def ignore_filter(src, names):
        return [name for name in names if name in ignore_folders]

    shutil.copytree(original_path, clean_path, ignore=ignore_filter)

    ext_to_folder = {}
    target_destinations = set()

    for folder_name, extensions in rules.items():
        target_destinations.add(folder_name.split("/")[0])
        for ext in extensions:
            clean_ext = str(ext).strip().lower()
            if not clean_ext.startswith("."):
                clean_ext = f".{clean_ext}"
            ext_to_folder[clean_ext] = folder_name

    files_to_move = []

    for root, dirs, files in os.walk(clean_path, topdown=True):
        dirs[:] = [
            d for d in dirs 
            if d not in ignore_folders and d not in target_destinations
        ]

        for file_name in files:
            if file_name.startswith(".") or file_name == "organizer.json":
                continue

            file_path = Path(root) / file_name

            if file_name.endswith(".import") or file_name.endswith(".uid"):
                base_file_name = file_name.rsplit(".", 1)[0]
                actual_ext = Path(base_file_name).suffix.lower().strip()
            else:
                actual_ext = file_path.suffix.lower().strip()

            if actual_ext in ext_to_folder:
                files_to_move.append((file_path, ext_to_folder[actual_ext]))

    path_map = {}
    taken_names_by_dir = {}

    for old_file_path, dest_subfolder in files_to_move:
        dest_dir = clean_path / dest_subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_dir_key = str(dest_dir)
        taken_names = taken_names_by_dir.setdefault(dest_dir_key, set())

        new_file_name = old_file_path.name

        if old_file_path.parent.resolve() != dest_dir.resolve():
            new_file_name = _resolve_name_conflict(
                dest_dir, old_file_path.name, taken_names
            )

        new_file_path = dest_dir / new_file_name

        if old_file_path.resolve() != new_file_path.resolve():
            taken_names.add(new_file_name)

            rel_old = str(old_file_path.relative_to(clean_path)).replace("\\", "/")
            rel_new = str(new_file_path.relative_to(clean_path)).replace("\\", "/")

            shutil.move(str(old_file_path), str(new_file_path))
            path_map[rel_old] = rel_new

    remove_empty_folders(clean_path)

    return str(clean_path), path_map
