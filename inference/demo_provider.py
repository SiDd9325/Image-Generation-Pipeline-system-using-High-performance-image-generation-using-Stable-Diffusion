"""Demo / Mock generative inference provider.

Generates deterministic, visually rich algorithmic canvases using PIL.
Enables zero-GPU, zero-heavy-dependency operation for local development,
automated testing, CI/CD pipelines, and portfolio demonstrations.
"""

import hashlib
import io
import math
import random
import time
from typing import Any, Callable, Dict, Optional, Tuple

import psutil
from PIL import Image, ImageDraw, ImageFont

from inference.base import BaseInferenceProvider, InferenceJobRequest, InferenceResult


class DemoInferenceProvider(BaseInferenceProvider):
    """Zero-GPU procedural generative art provider simulating diffusion synthesis."""

    def __init__(self, simulate_latency_per_step: float = 0.02):
        self.simulate_latency_per_step = simulate_latency_per_step
        self._provider_name = "DemoProceduralEngine-v1.0"
        self._device = "CPU (Procedural Synth)"

    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "demo",
            "name": self._provider_name,
            "device": self._device,
            "gpu_required": False,
            "capabilities": ["text-to-image", "deterministic-seed", "progress-reporting"],
            "status": "ready",
        }

    def _derive_seed(self, prompt: str, seed: Optional[int]) -> int:
        if seed is not None and seed >= 0:
            return seed
        # Deterministic seed from prompt hash if none given
        hasher = hashlib.sha256(prompt.encode("utf-8"))
        return int(hasher.hexdigest()[:8], 16)

    def _generate_palette(self, rng: random.Random) -> Tuple[Tuple[int, int, int], ...]:
        """Generate a harmonious 4-color palette based on RNG seed."""
        base_hue = rng.uniform(0, 1)
        colors = []
        for offset in (0.0, 0.25, 0.5, 0.75):
            h = (base_hue + offset + rng.uniform(-0.05, 0.05)) % 1.0
            s = rng.uniform(0.65, 0.95)
            v = rng.uniform(0.75, 1.0)
            # HSV to RGB
            i = int(h * 6.0)
            f = (h * 6.0) - i
            p = v * (1.0 - s)
            q = v * (1.0 - s * f)
            t = v * (1.0 - s * (1.0 - f))
            i = i % 6
            if i == 0:
                r, g, b = v, t, p
            elif i == 1:
                r, g, b = q, v, p
            elif i == 2:
                r, g, b = p, v, t
            elif i == 3:
                r, g, b = p, q, v
            elif i == 4:
                r, g, b = t, p, v
            else:
                r, g, b = v, p, q
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        return tuple(colors)

    def generate(
        self,
        request: InferenceJobRequest,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> InferenceResult:
        start_time = time.perf_counter()
        mem_before = psutil.Process().memory_info().rss / (1024 * 1024)

        effective_seed = self._derive_seed(request.prompt, request.seed)
        rng = random.Random(effective_seed)

        # Simulate diffusion steps progression
        total_steps = max(1, request.steps)
        for step in range(1, total_steps + 1):
            if self.simulate_latency_per_step > 0:
                time.sleep(self.simulate_latency_per_step)
            if progress_callback:
                progress_callback(step, total_steps)

        # Render algorithmic procedural canvas
        w, h = request.width, request.height
        image = Image.new("RGB", (w, h), (15, 18, 26))
        draw = ImageDraw.Draw(image, "RGBA")

        palette = self._generate_palette(rng)
        c1, c2, c3, c4 = palette

        # Radial / harmonic background glow
        center_x = w * rng.uniform(0.35, 0.65)
        center_y = h * rng.uniform(0.35, 0.65)
        max_radius = int(math.hypot(w, h) * 0.75)

        for r in range(max_radius, 0, -max(4, max_radius // 60)):
            factor = 1.0 - (r / max_radius)
            blend_r = int(c1[0] * factor + 15 * (1 - factor))
            blend_g = int(c1[1] * factor + 18 * (1 - factor))
            blend_b = int(c1[2] * factor + 26 * (1 - factor))
            alpha = int(120 * factor)
            draw.ellipse(
                [center_x - r, center_y - r, center_x + r, center_y + r],
                fill=(blend_r, blend_g, blend_b, alpha),
            )

        # Generative cosmic filaments / harmonic curves
        num_curves = rng.randint(18, 36)
        for i in range(num_curves):
            col = rng.choice([c2, c3, c4])
            alpha = rng.randint(60, 200)
            points = []
            phase = rng.uniform(0, 2 * math.pi)
            freq = rng.uniform(1.5, 4.5)
            y_base = (h / num_curves) * i

            for x_sample in range(0, w + 16, 16):
                y_offset = math.sin((x_sample / w) * freq * math.pi + phase) * (h * 0.18)
                points.append((x_sample, y_base + y_offset))

            if len(points) > 1:
                draw.line(points, fill=(col[0], col[1], col[2], alpha), width=rng.randint(2, 5))

        # Constellation nodes / particle blooms
        num_particles = rng.randint(40, 100)
        for _ in range(num_particles):
            px = rng.randint(0, w)
            py = rng.randint(0, h)
            pr = rng.randint(2, 7)
            col = rng.choice(palette)
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(col[0], col[1], col[2], 220))

        # Overlay metadata banner at bottom
        banner_h = 42
        draw.rectangle([0, h - banner_h, w, h], fill=(10, 12, 18, 220))
        truncated_prompt = (
            (request.prompt[:55] + "...") if len(request.prompt) > 55 else request.prompt
        )
        tag_text = f"GenStudio AI | Seed: {effective_seed} | Steps: {request.steps} | \"{truncated_prompt}\""
        draw.text((12, h - banner_h + 12), tag_text, fill=(210, 220, 235, 255))

        # Convert to PNG bytes
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        image_bytes = buffer.getvalue()

        latency = time.perf_counter() - start_time
        mem_after = psutil.Process().memory_info().rss / (1024 * 1024)

        return InferenceResult(
            image_bytes=image_bytes,
            format="PNG",
            latency_seconds=round(latency, 4),
            memory_mb=round(max(0.0, mem_after - mem_before), 2),
            metadata={
                "provider": "demo",
                "engine": self._provider_name,
                "device": self._device,
                "seed": effective_seed,
                "width": w,
                "height": h,
                "steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "prompt": request.prompt,
                "negative_prompt": request.negative_prompt,
            },
        )
