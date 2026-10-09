"""
XG-Xシミュレータのトリガ実行と画面キャプチャを自動化するツール。

使い方
------
1. XG-Xシミュレータを起動しておく。
2. このプログラムを実行する。
3. キャプチャする回数を入力する。
4. カウントダウン中にXG-Xシミュレータをアクティブにする。
5. 「T」キーを送信してトリガを実行する。
6. 処理完了後、アクティブウィンドウをキャプチャする。
7. 指定回数までトリガとキャプチャを自動で繰り返す。
8. 画像はPictures/XGX_Captureフォルダに保存される。
9. 実行を途中で停止する場合はCtrl+Cを押す。
"""

import time
from datetime import datetime
from pathlib import Path

import pyautogui
from PIL import ImageGrab


# ================================================
#   Settings
# ================================================
START_WAIT_SECONDS = 5
TRIGGER_WAIT_SECONDS = 1.0

SAVE_DIR = Path.home() / "Pictures" / "XGX_Capture"


# ================================================
#   Capture active window
# ================================================
def capture_active_window(file_path):
    # Capture the active window to the clipboard.
    pyautogui.hotkey("alt", "printscreen")

    # Wait for the clipboard to update.
    time.sleep(0.3)

    # Get the image from the clipboard.
    image = ImageGrab.grabclipboard()

    if image is None:
        raise RuntimeError("Failed to get image from clipboard.")

    image.save(file_path)


# ================================================
#   Main
# ================================================
def main():
    print("=" * 50)
    print(" XG-X Send Key and Capture")
    print("=" * 50)

    # Number of repetitions
    while True:
        try:
            repeat_count = int(input("Number of captures: "))

            if repeat_count > 0:
                break

            print("Enter a number greater than 0.")

        except ValueError:
            print("Enter an integer.")

    # Create save directory.
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # Create a folder for this run.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = SAVE_DIR / timestamp
    output_dir.mkdir()

    print()
    print(f"Save folder: {output_dir}")
    print()
    print(f"Starting in {START_WAIT_SECONDS} seconds.")
    print("Activate the XG-X Simulator window.")
    print()

    # Countdown
    for seconds in range(START_WAIT_SECONDS, 0, -1):
        print(f"{seconds}...")
        time.sleep(1)

    print()
    print("Start")
    print()

    # Trigger and capture
    try:
        for index in range(1, repeat_count + 1):
            # Send trigger key.
            pyautogui.press("t")

            # Wait for XG-X processing.
            time.sleep(TRIGGER_WAIT_SECONDS)

            # File name
            file_name = f"capture_{index:04d}.png"
            file_path = output_dir / file_name

            # Capture active window.
            capture_active_window(file_path)

            print(
                f"[{index:4d} / {repeat_count}] "
                f"Trigger -> Capture -> {file_name}"
            )

    except KeyboardInterrupt:
        print()
        print("Stopped by user.")
        return

    print()
    print("=" * 50)
    print(" Completed")
    print("=" * 50)
    print(f"Saved to: {output_dir}")


if __name__ == "__main__":
    main()