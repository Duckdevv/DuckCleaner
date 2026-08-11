import os
import re
from pathlib import Path

PATH_REGEX = re.compile(r"""(['"])([^'"]+\.[a-zA-Z0-9]+)\1""")


def update_script_references(clean_folder_path, path_map):
    if not path_map:
        return 0

    clean_path = Path(clean_folder_path).resolve()

    script_extensions = {
        ".py",
        ".js",
        ".gd",
        ".cs",
        ".ts",
        ".cpp",
        ".c",
        ".html",
        ".css",
        ".json",
    }

    updated_files_count = 0

    normalized_path_map = {}
    for old_p, new_p in path_map.items():
        clean_old = old_p.replace("\\", "/").lstrip("./").strip().lower()
        normalized_path_map[clean_old] = new_p.replace("\\", "/")

    for script_file in clean_path.rglob("*"):
        if (
            script_file.is_file()
            and script_file.suffix.lower() in script_extensions
        ):
            try:
                content = script_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            modified = False

            def replace_match(match):
                nonlocal modified
                quote = match.group(1)
                raw_path = match.group(2).replace("\\", "/")

                clean_extracted = raw_path.lstrip("./").strip().lower()

                if clean_extracted in normalized_path_map:
                    new_target_rel_to_root = normalized_path_map[clean_extracted]
                    target_full_path = clean_path / new_target_rel_to_root
                    script_dir = script_file.parent

                    new_rel = os.path.relpath(
                        target_full_path, start=script_dir
                    ).replace("\\", "/")

                    modified = True
                    return f"{quote}{new_rel}{quote}"

                return match.group(0)

            new_content = PATH_REGEX.sub(replace_match, content)

            if modified:
                script_file.write_text(new_content, encoding="utf-8")
                updated_files_count += 1

    return updated_files_count
