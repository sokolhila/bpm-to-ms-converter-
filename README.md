# BPM to Milliseconds Converter

A Windows desktop application that converts music BPM (Beats Per Minute) to milliseconds for different note values.

## Android (APK) Build — Kivy + Buildozer

This project now includes a mobile UI built with Kivy (`main.py`) and a Buildozer configuration (`buildozer.spec`) plus a GitHub Actions workflow to build an Android APK in the cloud.

### Quick Steps (GitHub Actions)

1. Create a new GitHub repository and push this project to it.
2. Ensure the workflow file exists at `.github/workflows/android-build.yml` (already added).
3. Go to your repository on GitHub → Actions tab.
4. Run the workflow: "Android APK (Kivy/Buildozer)" (via "Run workflow"), or push to `main`/`master` to trigger automatically.
5. After it finishes, download the generated APK from the workflow "Artifacts" (named `bpm-converter-apk`).

The workflow uses the official `kivy/buildozer` Docker image to produce a debug APK located under `bin/`.

### Local Run (Kivy app)

If you want to test the Kivy UI on desktop before building the APK:

```bash
pip install -r requirements-kivy.txt
python main.py
```

Note: Kivy is cross‑platform but requires system dependencies on some OSes. For Android packaging, the GitHub Actions approach is recommended from Windows.

## Features

- **Easy-to-use GUI**: Clean and intuitive interface built with tkinter
- **Multiple Note Values**: Support for whole notes, half notes, quarter notes, eighth notes, sixteenth notes, and thirty-second notes
- **Real-time Conversion**: Instant conversion as you type
- **Input Validation**: Prevents invalid inputs and provides helpful error messages
- **Dual Output**: Shows results in both milliseconds and seconds
- **Formula Display**: Shows the conversion formula for educational purposes

## How to Use

1. Enter the BPM (Beats Per Minute) value
2. Select the desired note value from the dropdown
3. Click "Convert" or press Enter
4. View the results in milliseconds and seconds

## Formula

The conversion uses the following formula:
```
Milliseconds = (60,000 / BPM) × Note Value Multiplier
```

Where note value multipliers are:
- Whole Note (1/1): 4.0
- Half Note (1/2): 2.0
- Quarter Note (1/4): 1.0
- Eighth Note (1/8): 0.5
- Sixteenth Note (1/16): 0.25
- Thirty-second Note (1/32): 0.125

## Building the Executable

### Method 1: Using the build script
1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Run: `python build_exe.py`

### Method 2: Using the batch file
1. Double-click `build.bat`

### Method 3: Manual PyInstaller command
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=BPM-Converter bpm_converter.py
```

The executable will be created in the `dist` folder.

## Running the Application

### From Source
```bash
python bpm_converter.py
```

### From Executable
Simply double-click the `BPM-Converter.exe` file in the `dist` folder.

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- PyInstaller (for building executable)

## Examples

- **120 BPM Quarter Note**: 500.00 ms (0.500 s)
- **140 BPM Eighth Note**: 214.29 ms (0.214 s)
- **90 BPM Half Note**: 1333.33 ms (1.333 s)

## License

This project is open source and available under the MIT License.
