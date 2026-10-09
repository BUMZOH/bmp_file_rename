import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path


# ================================================
#   Select folder
# ================================================
def select_folder():
    folder_path = filedialog.askdirectory()

    if not folder_path:
        return

    folder_var.set(folder_path)


# ================================================
#   Get BMP files
# ================================================
def get_bmp_files(folder_path):
    folder = Path(folder_path)

    bmp_files = sorted(folder.glob("*.bmp"))

    return bmp_files


# ================================================
#   Get file names
# ================================================
def get_file_names(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        file_names = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return file_names


# ================================================
#   Select file name list
# ================================================
def select_file_name_list():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Text files", "*.txt"),
        ]
    )

    if not file_path:
        return

    file_name_var.set(file_path)


# ================================================
#   Rename files
# ================================================
def rename_files():
    folder_path = folder_var.get().strip().strip('"')
    file_name_path = file_name_var.get().strip().strip('"')

    try:
        start_number = int(start_number_var.get())
    except ValueError:
        messagebox.showerror(
            "エラー",
            "連番開始番号は整数で入力してください。",
        )
        return

    # --------------------------------------------
    #   Check input
    # --------------------------------------------
    if not folder_path:
        messagebox.showerror(
            "エラー",
            "対象フォルダを指定してください。",
        )
        return

    if not file_name_path:
        messagebox.showerror(
            "エラー",
            "ファイル名一覧を指定してください。",
        )
        return

    bmp_files = get_bmp_files(folder_path)
    file_names = get_file_names(file_name_path)

    # --------------------------------------------
    #   Check file count
    # --------------------------------------------
    if len(bmp_files) != len(file_names):
        messagebox.showerror(
            "エラー",
            "BMPファイル数とファイル名一覧の数が一致しません。\n\n"
            f"BMPファイル数: {len(bmp_files)}\n"
            f"ファイル名数: {len(file_names)}",
        )
        return

    # --------------------------------------------
    #   Check file names
    # --------------------------------------------
    invalid_chars = '<>:"/\\|?*'

    for file_name in file_names:
        if any(char in file_name for char in invalid_chars):
            messagebox.showerror(
                "エラー",
                "ファイル名に使用できない文字が含まれています。\n\n"
                f"{file_name}",
            )
            return

    # --------------------------------------------
    #   Create new paths
    # --------------------------------------------
    new_paths = []

    for index, (bmp_file, file_name) in enumerate(
        zip(bmp_files, file_names),
        start=start_number,
    ):
        new_name = f"{index:03d}_{file_name}.bmp"
        new_path = bmp_file.with_name(new_name)

        new_paths.append(new_path)

    # --------------------------------------------
    #   Rename to temporary names
    # --------------------------------------------
    temp_files = []

    for index, bmp_file in enumerate(
        bmp_files,
        start=1,
    ):
        temp_path = bmp_file.with_name(
            f"__rename_temp_{index:03d}.tmp"
        )

        bmp_file.rename(temp_path)
        temp_files.append(temp_path)

    # --------------------------------------------
    #   Rename to final names
    # --------------------------------------------
    for temp_file, new_path in zip(
        temp_files,
        new_paths,
    ):
        temp_file.rename(new_path)

    # --------------------------------------------
    #   Complete
    # --------------------------------------------
    messagebox.showinfo(
        "完了",
        f"{len(bmp_files)}個のファイル名を変更しました。",
    )


# ================================================
#   Main window
# ================================================
root = tk.Tk()
root.title("BMP File Rename")
root.geometry("700x250")


# ================================================
#   Variables
# ================================================
folder_var = tk.StringVar()
file_name_var = tk.StringVar()
start_number_var = tk.StringVar(value="1")


# ================================================
#   Main frame
# ================================================
main_frame = ttk.Frame(root)
main_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=30,
)


# ================================================
#   Target folder
# ================================================
ttk.Label(
    main_frame,
    text="対象フォルダ",
).grid(
    row=0,
    column=0,
    sticky="w",
)

folder_entry = ttk.Entry(
    main_frame,
    textvariable=folder_var,
)
folder_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(5, 20),
)

folder_button = ttk.Button(
    main_frame,
    text="参照...",
    command=select_folder,
)
folder_button.grid(
    row=1,
    column=1,
    pady=(5, 20),
)


# ================================================
#   File name list
# ================================================
ttk.Label(
    main_frame,
    text="ファイル名一覧",
).grid(
    row=2,
    column=0,
    sticky="w",
)

file_name_entry = ttk.Entry(
    main_frame,
    textvariable=file_name_var,
)
file_name_entry.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(5, 20),
)

file_name_button = ttk.Button(
    main_frame,
    text="参照...",
    command=select_file_name_list,
)
file_name_button.grid(
    row=3,
    column=1,
    pady=(5, 20),
)


# ================================================
#   Start number
# ================================================
start_number_frame = ttk.Frame(main_frame)
start_number_frame.grid(
    row=4,
    column=0,
    sticky="e",
    padx=(0, 10),
    pady=10,
)

ttk.Label(
    start_number_frame,
    text="連番開始番号",
).pack(
    side="left",
    padx=(0, 5),
)

start_number_entry = ttk.Entry(
    start_number_frame,
    textvariable=start_number_var,
    width=8,
)
start_number_entry.pack(side="left")


# ================================================
#   Rename button
# ================================================
rename_button = ttk.Button(
    main_frame,
    text="ファイル名変更",
    command=rename_files,
)
rename_button.grid(
    row=4,
    column=1,
    pady=10,
)


# ================================================
#   Grid settings
# ================================================
main_frame.columnconfigure(0, weight=1)


# ================================================
#   Start
# ================================================
root.mainloop()