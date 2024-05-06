import json
import argparse
import os
import shutil  

# Function to convert bounding box to YOLO format
def convert_to_yolo(bbox, img_width, img_height):
    x_min, y_min, width, height = bbox
    x_center = (x_min + width / 2) / img_width
    y_center = (y_min + height / 2) / img_height
    normalized_width = width / img_width
    normalized_height = height / img_height
    return [x_center, y_center, normalized_width, normalized_height]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_directory", help='path should be given to specific folder containing different datat directories (ex: train)')     
    parser.add_argument("destination_directory", help= 'path for storing converted labels and images')
    args = parser.parse_args()

    root_dataset_path = args.dataset_directory
    destination_images_folder = os.path.join(args.destination_directory, 'images')
    destination_labels_folder = os.path.join(args.destination_directory, 'labels')

    # Ensure the destination folders exist
    os.makedirs(destination_images_folder, exist_ok=True)
    os.makedirs(destination_labels_folder, exist_ok=True)

    # Load the single JSON annotation file
    annotation_file_path = os.path.join(root_dataset_path, "index.json")
    with open(annotation_file_path, 'r') as f:
        data = json.load(f)

    image_file_map = {img["id"]: img["file_name"] for img in data["images"]}
    # place holder image dimensions
    width = 640.0
    height = 512.0

    image_annotation_map = {}

    for annotation in data["annotations"]:
        image_id = annotation["image_id"]  # Image ID from annotation
        bbox = annotation["bbox"]  # Bounding box coordinates
        class_id = annotation["category_id"]  # Class ID
        if class_id == 1 : class_id = 7 #changing the uav label to 7 for combining datasets in the future
        
        # Convert bounding box to YOLO format
        yolo_bbox = convert_to_yolo(bbox, width, height)

        # If the image_id exists in the map, append to the list of annotations
        if image_id not in image_annotation_map:
            image_annotation_map[image_id] = []
        
        annotation_text = f"{class_id} {' '.join(map(str, yolo_bbox))}"
        image_annotation_map[image_id].append(annotation_text)


    # Traverse all subdirectories
    for image_id, file_name in image_file_map.items():
    # Create unique names for image and annotation
        subdir_name = os.path.dirname(file_name).replace("/", "_")  # Unique subdir name
        base_name = os.path.splitext(os.path.basename(file_name))[0]  # Base name of the image
        unique_image_name = f"{subdir_name}_{base_name}.jpg"
        unique_annotation_name = f"{subdir_name}_{base_name}.txt"

        # Get the source image path
        source_image_path = os.path.join(root_dataset_path, file_name)
    
        # Copy the image to the destination images folder with the unique name
        destination_image_path = os.path.join(destination_images_folder, unique_image_name)
        shutil.copy2(source_image_path, destination_image_path)
        
         # Check if there are annotations for this image
        if image_id in image_annotation_map:
            # Get the corresponding annotations
            annotations_list = image_annotation_map[image_id]

            # Write the YOLO annotations to the text file in the destination labels folder
            destination_annotation_path = os.path.join(destination_labels_folder, unique_annotation_name)
            with open(destination_annotation_path, 'w') as f:
                f.write('\n'.join(annotations_list))