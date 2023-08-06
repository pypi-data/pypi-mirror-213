"""Example OctoAI service scaffold: Wav2Vec."""
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from octoai.service import Service
from octoai.types import Audio, Text


class Wav2VecService(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Download model weights to disk."""
        self.processor = Wav2Vec2Processor.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    def infer(self, audio: Audio) -> Text:
        """Perform inference with the model."""
        audio_array, sampling_rate = audio.to_numpy()
        input_values = self.processor(
            audio_array,
            sampling_rate=sampling_rate,
            return_tensors="pt",
            padding="longest",
        ).input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)

        return Text(text=transcription[0])
