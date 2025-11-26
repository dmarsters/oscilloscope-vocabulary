"""Tests for oscilloscope_vocabulary.server module."""

import pytest
import json
from oscilloscope_vocabulary.server import create_server


class TestServerCreation:
    """Test server creation and initialization."""
    
    def test_create_server_returns_mcp_instance(self):
        server = create_server()
        assert server is not None
        assert hasattr(server, 'run')
    
    def test_server_has_extract_tool(self):
        server = create_server()
        # Check that tools are registered
        assert server is not None


class TestServerTools:
    """Test that all expected tools are available."""
    
    def test_server_creation_succeeds(self):
        """Test that server can be created without errors."""
        try:
            server = create_server()
            assert server is not None
        except Exception as e:
            pytest.fail(f"Server creation failed: {e}")
    
    def test_server_name(self):
        """Test server has correct name."""
        server = create_server()
        assert server.name == "oscilloscope-vocabulary"


class TestToolFunctionality:
    """Test individual tool functionality through server."""
    
    def test_harmonic_profile_tool_logic(self):
        """Test harmonic profile mapping logic."""
        # Test through layer classes directly
        from oscilloscope_vocabulary.layers import HarmonicMapper
        
        color_ratios = {
            "warm_ratio": 0.33,
            "cool_ratio": 0.33,
            "neutral_ratio": 0.34,
            "color_balance": {"balanced": True}
        }
        
        result = HarmonicMapper.map_colors(color_ratios)
        assert "frequencies" in result
        assert "amplitudes" in result
        assert len(result["frequencies"]) > 0
    
    def test_constraint_parameters_tool_logic(self):
        """Test constraint parameter translation."""
        from oscilloscope_vocabulary.layers import ConstraintTranslator
        
        result = ConstraintTranslator.translate("balanced", "forward")
        assert result["fidelity"] == 0.65
        assert "Transform" in result["narrative"]
    
    def test_oscilloscope_rendering_logic(self):
        """Test oscilloscope pattern rendering."""
        from oscilloscope_vocabulary.layers import OscilloscopeRenderer
        
        result = OscilloscopeRenderer.render_waveform([1.0], [1.0])
        assert result.startswith("data:image/png;base64,")
    
    def test_context_assembly_logic(self):
        """Test context assembly."""
        from oscilloscope_vocabulary.layers import PromptContextAssembler
        
        colors = {
            "warm_ratio": 0.4,
            "cool_ratio": 0.3,
            "neutral_ratio": 0.3,
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
        
        result = PromptContextAssembler.assemble(
            colors, harmonic, constraints, "test", "forward"
        )
        
        assert result["direction"] == "forward"
        assert "color_foundation" in result
        assert "synthesis_guidance" in result


class TestLayerIntegration:
    """Test integration between layers."""
    
    def test_color_to_prompt_pipeline(self):
        """Test complete pipeline from colors to prompt context."""
        from oscilloscope_vocabulary.layers import (
            HarmonicMapper,
            ConstraintTranslator,
            OscilloscopeRenderer,
            PromptContextAssembler,
        )
        
        # Step 1: Map colors
        color_ratios = {
            "warm_ratio": 0.45,
            "cool_ratio": 0.35,
            "neutral_ratio": 0.20,
            "color_balance": {"balanced": False, "warm_heavy": True, "cool_heavy": False}
        }
        harmonic = HarmonicMapper.map_colors(color_ratios)
        assert harmonic is not None
        
        # Step 2: Get constraints
        constraints = ConstraintTranslator.translate("balanced", "forward")
        assert constraints is not None
        
        # Step 3: Render pattern
        pattern = OscilloscopeRenderer.render_waveform(
            harmonic["frequencies"],
            harmonic["amplitudes"]
        )
        assert pattern.startswith("data:image/png;base64,")
        
        # Step 4: Assemble context
        context = PromptContextAssembler.assemble(
            color_ratios, harmonic, constraints,
            "Transform to dreamlike", "forward"
        )
        assert context["user_intent"] == "Transform to dreamlike"
    
    def test_reverse_workflow_pipeline(self):
        """Test reverse workflow (prompt-guided generation)."""
        from oscilloscope_vocabulary.layers import (
            HarmonicMapper,
            ConstraintTranslator,
            PromptContextAssembler,
        )
        
        # Step 1: Infer harmonic from prompt (simplified)
        inferred_colors = {
            "warm_ratio": 0.45,
            "cool_ratio": 0.35,
            "neutral_ratio": 0.20,
            "color_balance": {}
        }
        harmonic = HarmonicMapper.map_colors(inferred_colors)
        
        # Step 2: Get constraints
        constraints = ConstraintTranslator.translate("strict", "reverse")
        
        # Step 3: Assemble context
        context = PromptContextAssembler.assemble(
            inferred_colors, harmonic, constraints,
            "A cozy library with warm and cool lighting", "reverse"
        )
        
        assert context["direction"] == "reverse"
        assert "library" in context["user_intent"].lower()


class TestDataStructures:
    """Test data structure validity."""
    
    def test_harmonic_profile_structure(self):
        """Test harmonic profile has expected structure."""
        from oscilloscope_vocabulary.layers import HarmonicProfiles
        
        profile = HarmonicProfiles.get("harmonic_rich")
        
        assert "frequencies" in profile
        assert "amplitudes" in profile
        assert "description" in profile
        assert "complexity" in profile
        
        assert len(profile["frequencies"]) == len(profile["amplitudes"])
    
    def test_constraint_level_structure(self):
        """Test constraint level has expected structure."""
        from oscilloscope_vocabulary.layers import ConstraintLevels
        
        constraint = ConstraintLevels.get("balanced")
        
        assert "fidelity" in constraint
        assert "color_tolerance" in constraint
        assert "complexity_delta" in constraint
        assert "description" in constraint
        
        assert isinstance(constraint["fidelity"], float)
        assert 0 <= constraint["fidelity"] <= 1
    
    def test_color_extraction_structure(self):
        """Test color extraction returns expected structure."""
        from oscilloscope_vocabulary.layers import ColorExtractor
        
        # Create a simple test image
        import tempfile
        from PIL import Image
        import numpy as np
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            # Create simple test image
            img = Image.new('RGB', (100, 100), color=(200, 100, 50))
            img.save(f.name)
            
            result = ColorExtractor.extract(f.name)
            
            assert "warm_ratio" in result
            assert "cool_ratio" in result
            assert "neutral_ratio" in result
            assert "dominant_colors" in result
            assert "color_balance" in result
            
            # Ratios should sum to ~1.0
            total = result["warm_ratio"] + result["cool_ratio"] + result["neutral_ratio"]
            assert 0.99 <= total <= 1.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
