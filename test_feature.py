from feature_extractor import extract_features
import os

# 👇 dataset/images lo unna correct filename ivvali
img_path = "dataset/images/10000.jpg"

if os.path.exists(img_path):
    features = extract_features(img_path)
    print("✅ Feature shape:", features.shape)
else:
    print("❌ Image not found. Filename/path check cheyyi.")