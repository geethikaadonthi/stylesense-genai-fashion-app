import os
import pickle
from feature_extractor import extract_features
import numpy as np

image_folder = "dataset/images"

features_list = []
image_paths = []

print("⏳ Extracting features... Please wait...")

for file in os.listdir(image_folder):
    if file.endswith(".jpg"):
        path = os.path.join(image_folder, file)
        try:
            features = extract_features(path)
            features_list.append(features.flatten())
            image_paths.append(path)
        except:
            print(f"Error processing {file}")

# Save features
pickle.dump(features_list, open("features.pkl", "wb"))
pickle.dump(image_paths, open("image_paths.pkl", "wb"))

print("✅ Feature extraction complete!")
print(f"Total images processed: {len(features_list)}")