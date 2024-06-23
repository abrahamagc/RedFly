# RedFly
Red Fly Backup Tool is a simple and user-friendly application to create backups of your folders while excluding specified subfolders. This tool provides an simple graphical user interface (GUI) to select the parent folder, set a prefix name, and specify folders to exclude from the backup. I created it to create abackups of entire applicatins with their configs while ignoring very large LLM model files (example: stable diffusion - automatic111 and comfyUI Apps). This helps me to revert back easily to old baseline due to some corruption in folder. (note apps like ComfyUI and Automatic111 we do not checkin to GitHub) 

## Features

- Browse and select the parent folder for backup
- Set a prefix name for the backup folder
- Specify folders to exclude from the backup
- Dynamic logging of copied and excluded files/folders
- Displays the final backup folder name after completion

## Requirements

- Python 3.x
- Tkinter
- Pillow

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/abrahamagc/RedFly.git
    cd RedFly
    ```

2. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Place the logo image:**

    Ensure your logo image is saved as `redflylogo.png` in the same directory as `redfly.py`.

4. **Prepare the exclude.txt file:**

    Create a file named `exclude.txt` in the same directory as `redfly.py`. This file should contain the folder patterns to be excluded from the backup, one per line. For example:

    ```plaintext
    checkpoints/
    output/
    models/
    ```

## Usage

1. **Run the application:**

    ```sh
    python redfly.py
    ```

2. **Using the GUI:**

    - **Select Parent Folder:** Browse and select the folder you want to back up.
    - **Prefix Name:** Enter a prefix name for the backup folder. This name will be prefixed to the backup folder name along with a timestamp.
    - **Exclude Folders:** Specify folders to exclude from the backup, one per line. You can click the `Examples` button to see example patterns.
    - **Log Copied:** This section dynamically shows all copied files and folders during the backup process.
    - **Log Excluded:** This section dynamically shows all excluded files and folders during the backup process, highlighted in red.
    - **Final Backup Folder:** The final name of the backup folder will be displayed after the backup is completed.

## Creating an Executable

To create an executable from the Python script, follow these steps:

1. **Install PyInstaller:**

    ```sh
    pip install pyinstaller
    ```

2. **Uninstall the `typing` package if necessary:**

    ```sh
    pip uninstall typing
    ```

3. **Run PyInstaller:**

    ```sh
    pyinstaller redfly.spec
    ```

4. **Locate the Executable:**

    After running the PyInstaller command, the executable will be located in the `dist` directory.

## License

This project is licensed under the MIT License.
