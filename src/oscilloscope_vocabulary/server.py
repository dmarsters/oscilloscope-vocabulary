"""
Oscilloscope Vocabulary MCP Server

A FastMCP server that translates between visual color language and 
oscilloscope frequency patterns, enabling bidirectional image transformation 
and guided generation.
"""

from fastmcp import FastMCP
import json
from typing import Dict, List

from oscilloscope_vocabulary.layers import (
    HarmonicProfiles,
    ConstraintLevels,
    ColorExtractor,
    HarmonicMapper,
    ConstraintTranslator,
    OscilloscopeRenderer,
    PromptContextAssembler,
)


def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    mcp = FastMCP("oscilloscope-vocabulary")

    # ========================================================================
    # LAYER 1: DETERMINISTIC EXTRACTION & TAXONOMY TOOLS
    # ========================================================================

    @mcp.tool()
    def extract_image_colors(image_path: str) -> dict:
        """
        Extract color composition from an image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Color analysis with warm/cool/neutral ratios and dominant colors
        """
        return ColorExtractor.extract(image_path)

    @mcp.tool()
    def get_harmonic_profile(
        warm_ratio: float,
        cool_ratio: float,
        neutral_ratio: float,
        complexity_preference: str = "balanced"
    ) -> dict:
        """
        Map color ratios to a harmonic frequency profile.
        
        Args:
            warm_ratio: Proportion of warm tones (0.0-1.0)
            cool_ratio: Proportion of cool tones (0.0-1.0)
            neutral_ratio: Proportion of neutral tones (0.0-1.0)
            complexity_preference: One of 'simple', 'balanced', 'complex'
            
        Returns:
            Harmonic profile with frequencies and amplitudes
        """
        color_ratios = {
            "warm_ratio": warm_ratio,
            "cool_ratio": cool_ratio,
            "neutral_ratio": neutral_ratio,
            "color_balance": {
                "warm_heavy": warm_ratio > 0.4,
                "cool_heavy": cool_ratio > 0.4,
                "balanced": abs(warm_ratio - cool_ratio) < 0.15
            }
        }
        return HarmonicMapper.map_colors(color_ratios, complexity_preference)

    @mcp.tool()
    def get_constraint_parameters(constraint_level: str, direction: str) -> dict:
        """
        Get human-readable constraint parameters for prompt synthesis.
        
        Args:
            constraint_level: One of 'very_loose', 'loose', 'balanced', 
                            'strict', 'very_strict'
            direction: Either 'forward' (image->freq->image) or 
                      'reverse' (prompt->freq->image)
            
        Returns:
            Readable parameters and instructions for Claude synthesis
        """
        return ConstraintTranslator.translate(constraint_level, direction)

    # ========================================================================
    # LAYER 2: OSCILLOSCOPE PATTERN RENDERING TOOLS
    # ========================================================================

    @mcp.tool()
    def render_scope_pattern(
        frequencies: list,
        amplitudes: list,
        pattern_type: str = "waveform"
    ) -> dict:
        """
        Render an oscilloscope pattern visualization.
        
        Args:
            frequencies: List of frequency values (1.0 is fundamental)
            amplitudes: List of amplitude values for each frequency
            pattern_type: Either 'waveform' or 'lissajous'
            
        Returns:
            Base64-encoded PNG image data and description
        """
        if pattern_type == "lissajous":
            image_data = OscilloscopeRenderer.render_lissajous(frequencies, amplitudes)
            description = "Lissajous curve - inharmonic relationships create complex patterns"
        else:
            image_data = OscilloscopeRenderer.render_waveform(frequencies, amplitudes)
            description = "Waveform pattern - harmonic series with overtones"
        
        return {
            "image": image_data,
            "description": description,
            "pattern_type": pattern_type,
            "frequencies": frequencies,
            "amplitudes": amplitudes
        }

    # ========================================================================
    # LAYER 3: PROMPT SYNTHESIS & CONTEXT ASSEMBLY TOOLS
    # ========================================================================

    @mcp.tool()
    def synthesize_prompt_context(
        image_colors: dict,
        harmonic_profile: dict,
        constraint_params: dict,
        user_intent: str,
        direction: str
    ) -> dict:
        """
        Synthesize all context into structured format for Claude.
        This is the final assembly before Claude's creative synthesis.
        
        Args:
            image_colors: Output from extract_image_colors
            harmonic_profile: Output from get_harmonic_profile
            constraint_params: Output from get_constraint_parameters
            user_intent: What the user wants to do or create
            direction: 'forward' or 'reverse'
            
        Returns:
            Complete context packet for Claude synthesis
        """
        return PromptContextAssembler.assemble(
            image_colors,
            harmonic_profile,
            constraint_params,
            user_intent,
            direction
        )

    # ========================================================================
    # UTILITY TOOLS
    # ========================================================================

    @mcp.tool()
    def list_available_profiles() -> dict:
        """
        List all available harmonic profiles and constraint levels.
        
        Returns:
            Dictionary describing available options
        """
        return {
            "harmonic_profiles": HarmonicProfiles.list_all(),
            "constraint_levels": ConstraintLevels.list_all()
        }

    return mcp


def main():
    """Run the MCP server."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
