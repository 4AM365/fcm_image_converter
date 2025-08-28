import sys, traceback, tempfile
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

from PIL import Image
# FORCE-INCLUDE Pillow’s PGM/PPM plugin so PyInstaller bundles it
from PIL import PpmImagePlugin  # noqa: F401 (import used for side effects)

LOGFILE = Path(tempfile.gettempdir()) / "pgm2jpg_flip_gui_error.log"

def log_exception(e: BaseException):
    try:
        with open(LOGFILE, "w", encoding="utf-8") as f:
            f.write("Exception:\n")
            f.write("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    except Exception:
        pass

def flip_tb(im: Image.Image) -> Image.Image:
    """Flip image top↔bottom with Pillow version compatibility."""
    try:
        return im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)  # Pillow ≥ 9.1
    except AttributeError:
        return im.transpose(Image.FLIP_TOP_BOTTOM)            # Older Pillow

def ensure_jpeg_mode(im: Image.Image) -> Image.Image:
    """
    JPEG wants 8-bit 'L' or 'RGB'.
    - 16-bit grayscale (I;16/I) → L
    - Paletted (P) or anything else → RGB
    """
    if im.mode in ("L", "RGB"):
        return im
    if im.mode in ("I;16", "I"):
        return im.convert("L")
    return im.convert("RGB")

def convert_dir(folder: Path) -> int:
    folder = Path(folder)
    out_dir = folder / "converted_jpg"
    out_dir.mkdir(exist_ok=True)
    count = 0

    for pgm in folder.glob("*.pgm"):
        try:
            with Image.open(pgm) as im:
                im = ensure_jpeg_mode(im)
                im = flip_tb(im)
                out = out_dir / (pgm.stem + ".jpg")
                im.save(out, "JPEG", quality=95, optimize=True)
                count += 1
        except Exception as e:
            print(f"Failed on {pgm}: {e}")
    return count

def main():
    root = Tk()
    root.withdraw()
    root.update()

    folder = filedialog.askdirectory(title="Select folder with .pgm files")
    if not folder:
        messagebox.showinfo("Canceled", "No folder selected.")
        return

    folder = Path(folder)
    if not folder.exists():
        messagebox.showerror("Error", f"Folder does not exist:\n{folder}")
        return

    n = convert_dir(folder)
    messagebox.showinfo("Done", f"Converted {n} file(s).\nOutput: {folder/'converted_jpg'}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_exception(e)
        messagebox.showerror(
            "Unexpected Error",
            f"An error occurred. Details were written to:\n{LOGFILE}\n\n{e}"
        )
        raise
