"""Inference engine package for GenStudio AI."""

from inference.base import BaseInferenceProvider, InferenceJobRequest, InferenceResult
from inference.demo_provider import DemoInferenceProvider
from inference.stable_diffusion_provider import StableDiffusionProvider

def get_inference_provider(provider_type: str = "demo", **kwargs) -> BaseInferenceProvider:
    """Factory to retrieve configured inference provider."""
    provider_type = provider_type.lower().strip()
    if provider_type in ("demo", "mock"):
        return DemoInferenceProvider(**kwargs)
    elif provider_type in ("stable_diffusion", "sd", "diffusers", "tensorflow"):
        return StableDiffusionProvider(**kwargs)
    else:
        raise ValueError(f"Unknown inference provider type: {provider_type}. Expected 'demo' or 'stable_diffusion'.")

__all__ = [
    "BaseInferenceProvider",
    "InferenceJobRequest",
    "InferenceResult",
    "DemoInferenceProvider",
    "StableDiffusionProvider",
    "get_inference_provider",
]
