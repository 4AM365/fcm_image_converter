# fcm_image_converter.exe

Batch-converts all .pgm images in a given directory to .jpg and flips them vertically. Useful for processing Chevy Forward Camera Module pre-cash images. There's an exe located in the 'Dist' folder.

## How to use:

Double-click pgm2jpg_flip.exe.

When prompted, select the folder that contains your .pgm files.

The program converts them and saves results to a subfolder named converted_jpg inside the folder you selected.

A message box will confirm how many files were processed.

## What it does

Reads all *.pgm in the chosen folder (no subfolders).

Flips each image top ↔ bottom.

Saves as .jpg with quality=95 and optimize enabled.

## Requirements

Windows 10/11.

No Python needed (it’s a standalone EXE).

## Notes

The folder picker returns a valid path—no need for r"..." or escaping backslashes.

Output files keep the original base name (e.g., image.pgm → image.jpg).

16-bit grayscale PGM files are automatically converted to an 8-bit JPEG-compatible format.

## Troubleshooting

If nothing seems to happen, check the selected folder for converted_jpg.

Still stuck? Run the debug build (if provided) from Command Prompt to see error messages.
