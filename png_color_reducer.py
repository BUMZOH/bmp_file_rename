from pathlib import Path

from PIL import Image


# ================================================
#   Settings
# ================================================
DEFAULT_COLORS = 128
VALID_COLORS = (256, 128, 64)


# ================================================
#   Get folder path
# ================================================
def get_folder_path():
    folder_text = input("PNG folder path: ").strip()
    folder_text = folder_text.strip('"')

    return Path(folder_text)


# ================================================
#   Get color count
# ================================================
def get_color_count():
    print()
    print("Select number of colors.")
    print("  1: 256 colors")
    print("  2: 128 colors [default]")
    print("  3: 64 colors")
    print()

    choice = input("Select [1-3]: ").strip()

    color_map = {
        "1": 256,
        "2": 128,
        "3": 64,
        "": DEFAULT_COLORS,
    }

    return color_map.get(choice)


# ================================================
#   Reduce colors
# ================================================
def reduce_colors(source_path, output_path, colors):
    with Image.open(source_path) as image:
        image = image.convert("RGB")
        image = image.quantize(colors=colors)
        image.save(
            output_path,
            optimize=True,
            compress_level=9,
        )


# ================================================
#   Main
# ================================================
def main():
    print("========================================")
    print(" PNG Color Reducer")
    print("========================================")
    print()

    folder_path = get_folder_path()

    if not folder_path.is_dir():
        print()
        print("Error: Folder not found.")
        return

    colors = get_color_count()

    if colors not in VALID_COLORS:
        print()
        print("Error: Invalid selection.")
        return

    png_files = sorted(folder_path.glob("*.png"))

    if not png_files:
        print()
        print("Error: No PNG files found.")
        return

    output_dir = folder_path / f"reduced_{colors}colors"
    output_dir.mkdir(exist_ok=True)

    print()
    print(f"Colors : {colors}")
    print(f"Files  : {len(png_files)}")
    print(f"Output : {output_dir}")
    print()

    for index, source_path in enumerate(png_files, start=1):
        output_path = output_dir / source_path.name

        try:
            reduce_colors(source_path, output_path, colors)
            print(f"[{index}/{len(png_files)}] {source_path.name}")
        except Exception as error:
            print(f"[ERROR] {source_path.name}: {error}")

    print()
    print("Completed.")


if __name__ == "__main__":
    main()