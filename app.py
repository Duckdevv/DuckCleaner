import sys
from pathlib import Path
from config_loader import load_rules
from file_mover import move_and_clean_project
from path_resolver import update_script_references


def main():
    target_dir = input("Enter target directory path: ").strip()

    if not target_dir:
        print("Error: Directory path cannot be empty.")
        sys.exit(1)

    target_path = Path(target_dir).resolve()
    if not target_path.exists():
        print(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)

    try:
        rules = load_rules("organizer.json")
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    clean_path, path_map = move_and_clean_project(str(target_path), rules)
    updated_scripts = update_script_references(clean_path, path_map)

    print(f"Clean copy created at: {clean_path}")
    print(f"Files moved: {len(path_map)}")
    print(f"Scripts updated: {updated_scripts}")


if __name__ == "__main__":
    main()
