#!/usr/bin/env python3
"""
Space Quest: The Retro Adventure
A Sierra-style adventure game with retro graphics and humor
"""

from graphics_engine import RetroGraphicsEngine

def main():
    """Main entry point"""
    print("=" * 50)
    print("SPACE QUEST: THE RETRO ADVENTURE")
    print("A Sierra-style graphic adventure game")
    print("=" * 50)
    print()
    print("Controls:")
    print("  Arrow Keys: Move character")
    print("  Mouse: Click on verbs and objects")
    print("  Q: Quit")
    print()
    
    # Create and run graphics engine
    engine = RetroGraphicsEngine()
    engine.run()

if __name__ == "__main__":
    main()
