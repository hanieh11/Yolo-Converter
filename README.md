## antiuav2yolo.py
This script processes the [3rd anti-uav dataset challenge](https://anti-uav.github.io/dataset/) and converts its annotations to the YOLO format, organizing the output into separate directories for images and labels.
### Features

- Converts annotations from the dataset's `index.json` file to YOLO format.
- Normalizes bounding boxes to fit YOLO specifications.
- Maps the UAV class ID to `7` for consistency in future dataset combinations.
- Copies images into a centralized folder and ensures unique filenames to avoid conflicts.
- Generates corresponding `.txt` label files with YOLO annotations.

### Prerequisites

- A properly structured dataset directory containing:
    - `index.json`: The annotation file.
    - Image files organized in subdirectories.

### Usage
1. **Run the Script** Use the following command:
    ```bash
    python <script_name>.py <dataset_directory> <destination_directory>
    ```
    - `<dataset_directory>`: Path to the root folder of the dataset (e.g., `train`, `val`).
    - `<destination_directory>`: Path to the output folder where converted images and labels will be stored.

    Example:
    ```bash
    python convert_anti_uav_to_yolo.py ./train ./output
    ```

2. **Output Directory Structure** After execution, the destination directory will have the following structure:
    ```lua
        output/
        ├── images/
        │   ├── subdir1_image1.jpg
        │   ├── subdir2_image2.jpg
        │   ...
        ├── labels/
            ├── subdir1_image1.txt
            ├── subdir2_image2.txt
            ...
    ```
### Details

- **Unique Filenames:** Filenames are prefixed with their subdirectory names to ensure uniqueness across the dataset.
- **Class ID Mapping:** The script remaps class ID `1` (UAV) to `7` for future dataset compatibility. Adjust this mapping in the code if needed.
- **Bounding Box Conversion:** Bounding boxes are normalized to YOLO format using placeholder dimensions (`640x512`). Update these values in the script if your dataset uses different image resolutions.

