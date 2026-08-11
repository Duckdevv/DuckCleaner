<img src="cover.jpg" alt="DuckCleaner Cover" width="100%">


# Duck Cleaner

A tool that organizes messy project folders (code + assets all mixed together) into clean subfolders — and automatically fixes any file paths in your code so nothing breaks.

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/59057626-086d-4d81-a405-dc2235d85b22" />
<img width="1291" height="610" alt="Image" src="https://github.com/user-attachments/assets/34aceab0-6d3f-4ec7-ac4f-7092ed5b6adf" />

## The problem

If you just drag files into folders manually, you break every `import` or `open()` pointing to them. Duck Cleaner sorts everything by file type AND updates the references in your code, so the project still runs after.

## How to use it

1. Download this repo
2. Run `app.py`
3. Give it the path to the project folder you want cleaned up
4. It creates a new folder called `yourproject_clean` next to it, fully organized. Your original folder isn't touched.

## What it also handles

- If two files have the same name and would collide, it renames one instead of overwriting it
- Original project stays untouched, everything happens in a copy


Feedback/issues welcome, still early.
