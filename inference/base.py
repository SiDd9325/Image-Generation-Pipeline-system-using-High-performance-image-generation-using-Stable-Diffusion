"""Abstract base provider and models for generative model inference."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class InferenceJobRequest:
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    steps: int = 25
    seed: Optional[int] = None
    guidance_scale: float = 7.5


@dataclass
class InferenceResult:
    image_bytes: bytes
    format: str = "PNG"
    latency_seconds: float = 0.0
    memory_mb: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseInferenceProvider(ABC):
    """Isolated provider interface for generative image synthesis."""

    @abstractmethod
    def generate(
        self,
        request: InferenceJobRequest,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> InferenceResult:
        """
        Execute image generation.

        :param request: Inference request parameters.
        :param progress_callback: Optional callback receiving (current_step, total_steps).
        :return: InferenceResult containing raw image bytes and diagnostic metadata.
        """
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Return runtime diagnostic metadata (backend name, hardware device, model ID)."""
        pass
