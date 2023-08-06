"""Example OctoAI service scaffold: Flan-T5-Small."""
from transformers import T5ForConditionalGeneration, T5Tokenizer

from octoai.service import Service
from octoai.types import Text


class T5Service(Service):
    """An OctoAI service extends octoai.service.Service."""

    def setup(self):
        """Download model weights to disk."""
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

    def infer(self, prompt: Text) -> Text:
        """Perform inference with the model."""
        inputs = self.tokenizer(prompt.text, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return Text(text=response[0])
