"""Tests for oscilloscope_vocabulary.layers module."""

import pytest
import numpy as np
from oscilloscope_vocabulary.layers import (
    HarmonicProfiles,
    ConstraintLevels,
    ColorExtractor,
    HarmonicMapper,
    ConstraintTranslator,
    OscilloscopeRenderer,
    PromptContextAssembler,
)


class TestHarmonicProfiles:
    """Test harmonic profile taxonomy."""
    
    def test_get_simple_profile(self):
        profile = HarmonicProfiles.get("simple")
        assert profile["complexity"] == "low"
        assert len(profile["frequencies"]) == 1
        assert profile["frequencies"][0] == 1.0
    
    def test_get_harmonic_rich_profile(self):
        profile = HarmonicProfiles.get("harmonic_rich")
        assert profile["complexity"] == "medium"
        assert len(profile["frequencies"]) == 4
        assert profile["frequencies"] == [1.0, 2.0, 3.0, 4.0]
    
    def test_get_complex_lissajous_profile(self):
        profile = HarmonicProfiles.get("complex_lissajous")
        assert profile["complexity"] == "high"
        assert profile["frequencies"] == [1.0, 1.5, 2.3]
    
    def test_get_chaotic_profile(self):
        profile = HarmonicProfiles.get("chaotic")
        assert profile["complexity"] == "very_high"
        assert len(profile["frequencies"]) == 5
    
    def test_get_nonexistent_defaults_to_harmonic_rich(self):
        profile = HarmonicProfiles.get("nonexistent")
        assert profile == HarmonicProfiles.get("harmonic_rich")
    
    def test_list_all_profiles(self):
        profiles = HarmonicProfiles.list_all()
        assert "simple" in profiles
        assert "harmonic_rich" in profiles
        assert "complex_lissajous" in profiles
        assert "chaotic" in profiles


class TestConstraintLevels:
    """Test constraint level taxonomy."""
    
    def test_get_balanced_constraint(self):
        constraint = ConstraintLevels.get("balanced")
        assert constraint["fidelity"] == 0.65
        assert constraint["color_tolerance"] == 0.75
    
    def test_very_strict_constraint(self):
        constraint = ConstraintLevels.get("very_strict")
        assert constraint["fidelity"] == 0.95
        assert constraint["color_tolerance"] == 0.98
    
    def test_very_loose_constraint(self):
        constraint = ConstraintLevels.get("very_loose")
        assert constraint["fidelity"] == 0.3
        assert constraint["color_tolerance"] == 0.5
    
    def test_constraint_progression(self):
        """Verify constraints follow expected progression."""
        levels = ["very_strict", "strict", "balanced", "loose", "very_loose"]
        fidelities = [ConstraintLevels.get(level)["fidelity"] for level in levels]
        
        # Fidelity should decrease
        for i in range(len(fidelities) - 1):
            assert fidelities[i] > fidelities[i + 1]
    
    def test_list_all_constraints(self):
        constraints = ConstraintLevels.list_all()
        assert len(constraints) == 5
        assert "balanced" in constraints


class TestHarmonicMapper:
    """Test color-to-harmonic mapping."""
    
    def test_balanced_colors_map_to_harmonic_rich(self):
        color_ratios = {
            "warm_ratio": 0.33,
            "cool_ratio": 0.33,
            "neutral_ratio": 0.34,
            "color_balance": {"balanced": True, "warm_heavy": False, "cool_heavy": False}
        }
        result = HarmonicMapper.map_colors(color_ratios)
        assert result["base_profile"] == "harmonic_rich"
    
    def test_warm_heavy_colors_map_to_lissajous(self):
        color_ratios = {
            "warm_ratio": 0.52,
            "cool_ratio": 0.28,
            "neutral_ratio": 0.20,
            "color_balance": {"balanced": False, "warm_heavy": True, "cool_heavy": False}
        }
        result = HarmonicMapper.map_colors(color_ratios)
        assert result["base_profile"] == "complex_lissajous"
    
    def test_complexity_preference_simple(self):
        color_ratios = {
            "warm_ratio": 0.33,
            "cool_ratio": 0.33,
            "neutral_ratio": 0.34,
            "color_balance": {"balanced": True, "warm_heavy": False, "cool_heavy": False}
        }
        result = HarmonicMapper.map_colors(color_ratios, "simple")
        assert result["frequencies"] == [1.0]
    
    def test_returns_correct_structure(self):
        color_ratios = {
            "warm_ratio": 0.4,
            "cool_ratio": 0.3,
            "neutral_ratio": 0.3,
            "color_balance": {}
        }
        result = HarmonicMapper.map_colors(color_ratios)
        
        assert "base_profile" in result
        assert "frequencies" in result
        assert "amplitudes" in result
        assert "description" in result
        assert "complexity" in result
        assert "color_mapping" in result


class TestConstraintTranslator:
    """Test constraint parameter translation."""
    
    def test_forward_direction_narrative(self):
        params = ConstraintTranslator.translate("balanced", "forward")
        assert "Transform the input image" in params["narrative"]
    
    def test_reverse_direction_narrative(self):
        params = ConstraintTranslator.translate("balanced", "reverse")
        assert "Guide image generation from user prompt" in params["narrative"]
    
    def test_returns_correct_fidelity(self):
        params = ConstraintTranslator.translate("balanced", "forward")
        assert params["fidelity"] == 0.65
        assert params["color_tolerance"] == 0.75
    
    def test_instruction_format(self):
        params = ConstraintTranslator.translate("balanced", "forward")
        instructions = params["instructions"]
        
        assert "fidelity" in instructions
        assert "color" in instructions
        assert "complexity" in instructions
        assert "%" in instructions["fidelity"]


class TestOscilloscopeRenderer:
    """Test oscilloscope pattern rendering."""
    
    def test_render_waveform_produces_base64(self):
        frequencies = [1.0, 2.0]
        amplitudes = [1.0, 0.5]
        
        result = OscilloscopeRenderer.render_waveform(frequencies, amplitudes)
        assert result.startswith("data:image/png;base64,")
        assert len(result) > 100  # Should be substantial base64 data
    
    def test_render_lissajous_produces_base64(self):
        frequencies = [1.0, 1.5]
        amplitudes = [1.0, 0.7]
        
        result = OscilloscopeRenderer.render_lissajous(frequencies, amplitudes)
        assert result.startswith("data:image/png;base64,")
        assert len(result) > 100
    
    def test_waveform_with_single_frequency(self):
        frequencies = [1.0]
        amplitudes = [1.0]
        
        result = OscilloscopeRenderer.render_waveform(frequencies, amplitudes)
        assert result.startswith("data:image/png;base64,")
    
    def test_lissajous_with_custom_size(self):
        frequencies = [1.0, 1.5]
        amplitudes = [1.0, 0.7]
        
        result = OscilloscopeRenderer.render_lissajous(
            frequencies, amplitudes, width=200, height=200
        )
        assert result.startswith("data:image/png;base64,")


class TestPromptContextAssembler:
    """Test context assembly for Claude."""
    
    def test_forward_context_structure(self):
        image_colors = {
            "warm_ratio": 0.45,
            "cool_ratio": 0.35,
            "neutral_ratio": 0.20,
            "dominant_colors": []
        }
        harmonic = {
            "frequencies": [1.0, 2.0],
            "amplitudes": [1.0, 0.5],
            "description": "Test",
            "complexity": "medium"
        }
        constraints = {
            "constraint_level": "balanced",
            "narrative": "Transform",
            "fidelity": 0.65,
            "color_tolerance": 0.75,
            "instructions": {}
        }
        
        context = PromptContextAssembler.assemble(
            image_colors, harmonic, constraints,
            "test intent", "forward"
        )
        
        assert context["direction"] == "forward"
        assert "color_foundation" in context
        assert "harmonic_structure" in context
        assert "constraints" in context
        assert "synthesis_guidance" in context
    
    def test_color_ratios_preserved(self):
        image_colors = {
            "warm_ratio": 0.52,
            "cool_ratio": 0.28,
            "neutral_ratio": 0.20,
            "dominant_colors": []
        }
        harmonic = {
            "frequencies": [1.0],
            "amplitudes": [1.0],
            "description": "Test",
            "complexity": "low"
        }
        constraints = {
            "constraint_level": "balanced",
            "narrative": "Test",
            "fidelity": 0.65,
            "color_tolerance": 0.75,
            "instructions": {}
        }
        
        context = PromptContextAssembler.assemble(
            image_colors, harmonic, constraints, "", "forward"
        )
        
        assert context["color_foundation"]["warm"] == 0.52
        assert context["color_foundation"]["cool"] == 0.28
        assert context["color_foundation"]["neutral"] == 0.20
    
    def test_synthesis_guidance_includes_percentages(self):
        image_colors = {
            "warm_ratio": 0.45,
            "cool_ratio": 0.35,
            "neutral_ratio": 0.20,
            "dominant_colors": []
        }
        harmonic = {
            "frequencies": [1.0],
            "amplitudes": [1.0],
            "description": "Test description",
            "complexity": "medium"
        }
        constraints = {
            "constraint_level": "balanced",
            "narrative": "Test",
            "fidelity": 0.65,
            "color_tolerance": 0.75,
            "instructions": {}
        }
        
        context = PromptContextAssembler.assemble(
            image_colors, harmonic, constraints, "", "forward"
        )
        
        guidance = context["synthesis_guidance"]
        assert "45%" in guidance  # warm percentage
        assert "35%" in guidance  # cool percentage
        assert "20%" in guidance  # neutral percentage


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
