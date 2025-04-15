from __future__ import annotations
from ultralytics import YOLO
import os
import shutil

model = YOLO("tuta_detection_model/best.pt")

def allstat(SOURCE_IMAGE_PATH, TARGET_IMAGE_PATH):
    # Lancer la prédiction
    results = model.predict(source=SOURCE_IMAGE_PATH, save=True, conf=0.25)
    r = results[0]

    # Récupérer le chemin de l’image générée par YOLO
    predicted_image_path = r.save_dir +"/"+ os.path.basename(SOURCE_IMAGE_PATH)

    # Copier dans le dossier assets/
    os.makedirs("assets/results", exist_ok=True)
    final_path = os.path.join("assets", "results", os.path.basename(predicted_image_path))
    shutil.copy(predicted_image_path, final_path)

    # Détection ?
    detected = any(
        model.names[int(box.cls[0])].lower() == "tuta absoluta" for box in r.boxes
    )

    return {
        "detected": detected,
        "image_path": f"results/{os.path.basename(predicted_image_path)}"  # relatif à assets/
    }
