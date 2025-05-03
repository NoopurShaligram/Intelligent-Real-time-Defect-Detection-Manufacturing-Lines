import os
import numpy as np
from PIL import Image
import albumentations as A
from ultralytics import YOLO

# Paths
DATASET_DIR = r"C:\Users\vimud\Downloads\dataset"
OUTPUT_DIR = r"./output"
YAML_PATH = r"C:\Users\vimud\Downloads\dataset\data.yaml"
AUGMENTED_DIR = r"./augmented_images"

# Augmentation (Simplified)
transform = A.Compose([
    A.RandomRotate90(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.Blur(blur_limit=3, p=0.2),
    A.Affine(rotate=(-10, 10), scale=(0.95, 1.05), translate_percent=(-0.05, 0.05), p=0.4),
    A.GaussNoise(p=0.2),
    A.MotionBlur(p=0.1),
    A.CLAHE(p=0.1),
])



# Augment "imagebolt" and "washer" images
def augment_bolt_images():
    os.makedirs(AUGMENTED_DIR, exist_ok=True)
    for filename in os.listdir(DATASET_DIR):
        if filename.startswith(('imagebolt', 'washer')):  # Augment only these
            img_path = os.path.join(DATASET_DIR, filename)
            img = np.array(Image.open(img_path))
            augmented = transform(image=img)['image']
            Image.fromarray(augmented).save(os.path.join(AUGMENTED_DIR, f"aug_{filename}"))
    print("Augmentation done.")

# Train YOLOv8n on custom dataset
def train_model(yaml_path, epochs=150, batch_size=16, imgsz=640, lr0=0.001,lrf=0.01, optimizer="AdamW", patience = 20, augment =True):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    best_model_path = os.path.join(OUTPUT_DIR, 'bolt_model5', 'weights', 'best.pt')

    if os.path.exists(best_model_path):
        print(f"Best model found at {best_model_path}, skipping training.")
        return YOLO(best_model_path)

    model = YOLO('yolov8n.pt')

    model.train(
        data=yaml_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        save=True,
        project=OUTPUT_DIR,
        name='bolt_model',
    )

    print("Training done.")
    return YOLO(best_model_path)

# Main function
def main():
    augment_bolt_images()
    model = train_model(YAML_PATH)

if __name__ == "__main__":
    main()
