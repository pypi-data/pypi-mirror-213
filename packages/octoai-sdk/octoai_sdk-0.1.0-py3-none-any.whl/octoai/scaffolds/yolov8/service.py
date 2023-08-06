"""Example OctoAI service scaffold: YOLOv8."""
import json
from typing import List

import numpy as np
from PIL import Image as PImage
from pydantic import BaseModel, Field
from ultralytics import YOLO

from octoai.service import Service
from octoai.types import Image

# This model has an elaborate prediction schema
# (labels, probabilities, and box coordinates).
# Since we can't rely on `octoai` predefined types
# we define our own to capture that structure.


class Box(BaseModel):
    """Represents corners of a detection box."""

    x1: float
    x2: float
    y1: float
    y2: float


class Detection(BaseModel):
    """Represents a detection."""

    name: str
    class_: int = Field(..., alias="class")
    confidence: float
    box: Box


class YOLOResponse(BaseModel):
    """Response includes list of detections and rendered image."""

    detections: List[Detection]
    image_with_boxes: Image


class YOLOv8Service(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Download model weights to disk."""
        self.model = YOLO("yolov8l.pt")

    def infer(self, image: Image) -> YOLOResponse:
        """Perform inference with the model."""
        image_pil = image.to_pil()
        output = self.model(image_pil)

        # no Python dict available directly from the model
        detections = json.loads(output[0].tojson())

        # get the rendered image with bounding boxes and labels
        # - Result.plot() generates BGR; flip to RGB
        img_out_numpy = np.flip(output[0].plot(), axis=2)
        img_out_pil = PImage.fromarray(img_out_numpy)

        # Return detection data and a rendered image with boxes
        return YOLOResponse(
            detections=[Detection(**d) for d in detections],
            image_with_boxes=Image.from_pil(img_out_pil),
        )
