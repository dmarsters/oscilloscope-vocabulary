"""
Layer implementations for Oscilloscope Vocabulary MCP Server.

Layer 1: Deterministic Extraction & Taxonomy
Layer 2: Oscilloscope Pattern Rendering
Layer 3: Prompt Synthesis Parameters
"""

import json
import numpy as np
from PIL import Image, ImageDraw
import base64
from io import BytesIO
from typing import Optional, Dict, List, Tuple


# ============================================================================
# LAYER 1: DETERMINISTIC EXTRACTION & TAXONOMY
# ============================================================================

class HarmonicProfiles:
    """Predefined harmonic frequency profiles."""
    
    PROFILES = {
        "simple": {
            "frequencies": [1.0],
            "amplitudes": [1.0],
            "description": "Pure fundamental tone, clean sine wave",
            "complexity": "low"
        },
        "harmonic_rich": {
            "frequencies": [1.0, 2.0, 3.0, 4.0],
            "amplitudes": [1.0, 0.5, 0.33, 0.25],
            "description": "Rich harmonic series, complex waveform with overtones",
            "complexity": "medium"
        },
        "complex_lissajous": {
            "frequencies": [1.0, 1.5, 2.3],
            "amplitudes": [1.0, 0.7, 0.4],
            "description": "Inharmonic ratios create Lissajous patterns",
            "complexity": "high"
        },
        "chaotic": {
            "frequencies": [1.0, 2.7, 3.2, 4.8, 5.1],
            "amplitudes": [1.0, 0.6, 0.4, 0.3, 0.2],
            "description": "Dense frequency content, intricate waveform",
            "complexity": "very_high"
        }
    }
    
    @classmethod
    def get(cls, name: str) -> Dict:
        return cls.PROFILES.get(name, cls.PROFILES["harmonic_rich"])
    
    @classmethod
    def list_all(cls) -> Dict:
        return {name: {
            "description": profile["description"],
            "complexity": profile["complexity"]
        } for name, profile in cls.PROFILES.items()}


class ConstraintLevels:
    """Predefined constraint parameters."""
    
    LEVELS = {
        "very_loose": {
            "fidelity": 0.3,
            "color_tolerance": 0.5,
            "complexity_delta": 0.6,
            "description": "Loose interpretation, significant creative freedom",
            "profile": "chaotic"
        },
        "loose": {
            "fidelity": 0.5,
            "color_tolerance": 0.65,
            "complexity_delta": 0.4,
            "description": "Relaxed constraints, creative exploration",
            "profile": "complex_lissajous"
        },
        "balanced": {
            "fidelity": 0.65,
            "color_tolerance": 0.75,
            "complexity_delta": 0.25,
            "description": "Balanced between constraint and freedom",
            "profile": "harmonic_rich"
        },
        "strict": {
            "fidelity": 0.8,
            "color_tolerance": 0.9,
            "complexity_delta": 0.1,
            "description": "Tight harmonic adherence, minimal deviation",
            "profile": "harmonic_rich"
        },
        "very_strict": {
            "fidelity": 0.95,
            "color_tolerance": 0.98,
            "complexity_delta": 0.05,
            "description": "Strict fidelity to structure and color ratios",
            "profile": "simple"
        }
    }
    
    @classmethod
    def get(cls, name: str) -> Dict:
        return cls.LEVELS.get(name, cls.LEVELS["balanced"])
    
    @classmethod
    def list_all(cls) -> Dict:
        return {name: {
            "description": constraint["description"],
            "fidelity": constraint["fidelity"],
            "color_tolerance": constraint["color_tolerance"]
        } for name, constraint in cls.LEVELS.items()}


class ColorExtractor:
    """Extract color composition from images."""
    
    @staticmethod
    def extract(image_path: str) -> Dict:
        """Extract warm/cool/neutral ratios and dominant colors."""
        try:
            img = Image.open(image_path).convert('RGB')
            img = img.resize((256, 256))
            pixels = list(img.getdata())
            
            # Categorize by hue
            warm_count = 0
            cool_count = 0
            neutral_count = 0
            
            for r, g, b in pixels:
                if r > g and r > b:
                    warm_count += 1
                elif b > g and b > r:
                    cool_count += 1
                else:
                    neutral_count += 1
            
            total = len(pixels)
            warm_ratio = warm_count / total
            cool_ratio = cool_count / total
            neutral_ratio = neutral_count / total
            
            # Get dominant colors
            img_small = img.resize((64, 64))
            pixels_small = list(img_small.getdata())
            
            color_counts = {}
            for color in pixels_small:
                color_counts[color] = color_counts.get(color, 0) + 1
            
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "warm_ratio": round(warm_ratio, 3),
                "cool_ratio": round(cool_ratio, 3),
                "neutral_ratio": round(neutral_ratio, 3),
                "dominant_colors": [
                    {"rgb": color, "percentage": round(count / len(pixels_small), 3)}
                    for color, count in sorted_colors
                ],
                "color_balance": {
                    "warm_heavy": warm_ratio > 0.4,
                    "cool_heavy": cool_ratio > 0.4,
                    "balanced": abs(warm_ratio - cool_ratio) < 0.15
                }
            }
        except Exception as e:
            return {"error": str(e)}


class HarmonicMapper:
    """Map color ratios to harmonic frequency profiles."""
    
    @staticmethod
    def map_colors(color_ratios: Dict, complexity_preference: str = "balanced") -> Dict:
        """Map color ratios to harmonic profile."""
        warm = color_ratios.get("warm_ratio", 0.33)
        cool = color_ratios.get("cool_ratio", 0.33)
        neutral = color_ratios.get("neutral_ratio", 0.34)
        
        # Simple heuristic: color balance suggests harmonic complexity
        if color_ratios.get("color_balance", {}).get("balanced"):
            base_profile = "harmonic_rich"
        elif warm > 0.45:
            base_profile = "complex_lissajous"
        elif cool > 0.45:
            base_profile = "complex_lissajous"
        else:
            base_profile = "harmonic_rich"
        
        profile = HarmonicProfiles.get(base_profile)
        
        # Modulate by complexity preference
        if complexity_preference == "simple":
            profile = HarmonicProfiles.get("simple")
        elif complexity_preference == "complex":
            profile = HarmonicProfiles.get("chaotic")
        
        return {
            "base_profile": base_profile,
            "frequencies": profile["frequencies"],
            "amplitudes": profile["amplitudes"],
            "description": profile["description"],
            "complexity": profile["complexity"],
            "color_mapping": {
                "warm_ratio": warm,
                "cool_ratio": cool,
                "neutral_ratio": neutral
            }
        }


class ConstraintTranslator:
    """Translate constraint levels to readable parameters."""
    
    @staticmethod
    def translate(constraint_level: str, direction: str) -> Dict:
        """Translate constraint slider into readable parameters."""
        constraint = ConstraintLevels.get(constraint_level)
        
        if direction == "forward":
            narrative = f"Transform the input image with {constraint['description'].lower()}"
        else:
            narrative = f"Guide image generation from user prompt with {constraint['description'].lower()}"
        
        return {
            "constraint_level": constraint_level,
            "narrative": narrative,
            "fidelity": constraint["fidelity"],
            "color_tolerance": constraint["color_tolerance"],
            "complexity_delta": constraint["complexity_delta"],
            "suggested_harmonic_profile": constraint["profile"],
            "instructions": {
                "fidelity": f"Maintain {int(constraint['fidelity'] * 100)}% structural fidelity to source",
                "color": f"Keep color ratios within {int(constraint['color_tolerance'] * 100)}% tolerance",
                "complexity": f"Allow {int(constraint['complexity_delta'] * 100 * 10)}% complexity variation"
            }
        }


# ============================================================================
# LAYER 2: OSCILLOSCOPE PATTERN RENDERING
# ============================================================================

class OscilloscopeRenderer:
    """Render oscilloscope waveform patterns as visualizations."""
    
    @staticmethod
    def render_waveform(frequencies: List[float], amplitudes: List[float],
                       width: int = 400, height: int = 300) -> str:
        """Render waveform pattern and return base64-encoded PNG."""
        # Generate waveform
        t = np.linspace(0, 4 * np.pi, width)
        waveform = np.zeros_like(t)
        
        for freq, amp in zip(frequencies, amplitudes):
            waveform += amp * np.sin(freq * t)
        
        # Normalize
        if np.max(np.abs(waveform)) > 0:
            waveform = waveform / np.max(np.abs(waveform))
        
        # Convert to image coordinates
        y_coords = ((waveform + 1) / 2 * (height - 40)) + 20
        
        # Create image
        img = Image.new('RGB', (width, height), color=(20, 20, 30))
        draw = ImageDraw.Draw(img)
        
        # Draw grid
        for i in range(0, width, 50):
            draw.line([(i, 0), (i, height)], fill=(40, 40, 60), width=1)
        for i in range(0, height, 30):
            draw.line([(0, i), (width, i)], fill=(40, 40, 60), width=1)
        
        # Draw waveform
        points = list(zip(range(width), y_coords))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=(0, 255, 150), width=2)
        
        # Draw axes
        draw.line([(0, height // 2), (width, height // 2)], fill=(100, 100, 120), width=1)
        draw.line([(0, 0), (0, height)], fill=(100, 100, 120), width=1)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def render_lissajous(frequencies: List[float], amplitudes: List[float],
                        width: int = 400, height: int = 400) -> str:
        """Render Lissajous curve pattern and return base64-encoded PNG."""
        freq_x = frequencies[0] if len(frequencies) > 0 else 1.0
        freq_y = frequencies[1] if len(frequencies) > 1 else 1.0
        amp_x = amplitudes[0] if len(amplitudes) > 0 else 1.0
        amp_y = amplitudes[1] if len(amplitudes) > 1 else 1.0
        
        # Generate Lissajous curve
        t = np.linspace(0, 2 * np.pi, 1000)
        x = amp_x * np.sin(freq_x * t)
        y = amp_y * np.sin(freq_y * t + np.pi / 4)
        
        # Convert to image coordinates
        x_coords = ((x + 1) / 2 * (width - 40)) + 20
        y_coords = ((y + 1) / 2 * (height - 40)) + 20
        
        # Create image
        img = Image.new('RGB', (width, height), color=(20, 20, 30))
        draw = ImageDraw.Draw(img)
        
        # Draw grid
        for i in range(0, width, 50):
            draw.line([(i, 0), (i, height)], fill=(40, 40, 60), width=1)
        for i in range(0, height, 50):
            draw.line([(0, i), (width, i)], fill=(40, 40, 60), width=1)
        
        # Draw Lissajous curve
        points = list(zip(x_coords, y_coords))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=(255, 100, 200), width=2)
        
        # Draw axes
        draw.line([(width // 2, 0), (width // 2, height)], fill=(100, 100, 120), width=1)
        draw.line([(0, height // 2), (width, height // 2)], fill=(100, 100, 120), width=1)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"


# ============================================================================
# LAYER 3: PROMPT SYNTHESIS
# ============================================================================

class PromptContextAssembler:
    """Assemble complete context for Claude synthesis."""
    
    @staticmethod
    def assemble(image_colors: Dict, harmonic_profile: Dict, 
                constraint_params: Dict, user_intent: str,
                direction: str) -> Dict:
        """Assemble all context into structured prompt for Claude."""
        return {
            "direction": direction,
            "user_intent": user_intent,
            "color_foundation": {
                "warm": image_colors.get("warm_ratio", 0.33),
                "cool": image_colors.get("cool_ratio", 0.33),
                "neutral": image_colors.get("neutral_ratio", 0.34),
                "dominant_colors": image_colors.get("dominant_colors", [])
            },
            "harmonic_structure": {
                "frequencies": harmonic_profile.get("frequencies", []),
                "amplitudes": harmonic_profile.get("amplitudes", []),
                "description": harmonic_profile.get("description", ""),
                "complexity": harmonic_profile.get("complexity", "medium")
            },
            "constraints": {
                "level": constraint_params.get("constraint_level", "balanced"),
                "narrative": constraint_params.get("narrative", ""),
                "fidelity": constraint_params.get("fidelity", 0.65),
                "color_tolerance": constraint_params.get("color_tolerance", 0.75),
                "instructions": constraint_params.get("instructions", {})
            },
            "synthesis_guidance": f"""
Use these constraints when synthesizing the image prompt:
- Direction: {direction}
- Intent: {user_intent}
- {constraint_params.get('narrative', 'balanced approach')}
- Color ratios: ~{int(image_colors.get('warm_ratio', 0.33)*100)}% warm, 
  ~{int(image_colors.get('cool_ratio', 0.33)*100)}% cool, 
  ~{int(image_colors.get('neutral_ratio', 0.34)*100)}% neutral
- Harmonic complexity: {harmonic_profile.get('description', 'moderate')}
"""
        }
