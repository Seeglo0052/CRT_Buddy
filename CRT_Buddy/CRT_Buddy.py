# -*- coding: utf-8 -*-
"""CRT Buddy - Y2K Desktop Pet & Meme Generator

Encoding sanitized: original file contained invalid UTF-8 bytes causing
SyntaxError under Python 3.13. Replaced garbled non-ASCII banner text with
plain ASCII to ensure interpreter loads the module.
"""
import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from core.pet_window_v7 import CRTBuddyWindow
from generators.meme_engine import MemeEngine

# Maximum allowed length for user-entered text to avoid layout/performance issues
MAX_TEXT_LEN = 200


class CRTBuddyApp:
    """Main application class for CRT Buddy."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("CRT Buddy")
        
    # Initialize meme engine
        self.meme_engine = MemeEngine(output_dir="output")
        
    # Create main window
        self.window = CRTBuddyWindow()
        
    # Setup signal connections
        self.setup_connections()
        
    # Show welcome message after short delay
        QTimer.singleShot(500, self.show_welcome)
    
    def setup_connections(self):
        """Connect Qt signals to handlers."""
        # Image drop handler
        self.window.image_dropped.connect(self.handle_image_drop)
        
    # Button click handlers
        self.window.generate_btn.clicked.connect(self.handle_generate)
        self.window.effect_btn.clicked.connect(self.handle_random_effect)
    
    def show_welcome(self):
        """Display initial welcome status and mood."""
        self.window.set_status("WELCOME TO CRT BUDDY")
        self.window.set_mood("happy")
        QTimer.singleShot(3000, lambda: self.window.set_status(
            "READY TO GENERATE Y2K VIBES"
        ))
    
    def handle_image_drop(self, image_path):
        """Handle when an image is dropped onto the window."""
        self.window.set_mood("processing")
        self.window.set_status("PROCESSING IMAGE...")
        # Delay processing to show animated status
        QTimer.singleShot(500, lambda: self.process_image(image_path))
    
    def process_image(self, image_path):
        """Process the dropped image and apply a random effect + optional text."""
        try:
            # Get user input text and validate centrally
            raw_text = self.window.get_input_text()
            if raw_text:
                ok, cleaned, reason = self.meme_engine.validate_text(raw_text, max_len=MAX_TEXT_LEN)
                if not ok:
                    self.window.set_status(reason)
                    self.window.set_mood("idle")
                    return
                text = cleaned
            else:
                text = ""
            # Validate image first
            try:
                _ = self.meme_engine.validate_image(image_path)  # returns PIL.Image but we re-open in generate
            except self.meme_engine.ImageValidationError as ve:
                self.window.set_status(f"IMAGE INVALID: {ve}")
                self.window.set_mood("idle")
                return
            
            # Generate meme from image
            result_img = self.meme_engine.generate_image_meme(
                image_path, 
                text=text,
                effect='random'
            )
            
            if result_img:
                # Save resulting meme image
                output_path = self.meme_engine.save_meme(result_img, "y2k_image")
                
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)}")
                    
                    # Schedule success message
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to process image")
                self.window.set_mood("idle")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
            self.window.set_mood("idle")
    
    def handle_generate(self):
        """Handle click to generate a text meme."""
        raw_text = self.window.get_input_text()
        ok, cleaned, reason = self.meme_engine.validate_text(raw_text, max_len=MAX_TEXT_LEN)
        if not ok:
            self.window.set_status(reason)
            return
        text = cleaned
        
        self.window.set_mood("processing")
        self.window.set_status("GENERATING Y2K MEME...")
        # Delay for processing animation
        QTimer.singleShot(500, lambda: self.generate_text_meme(text))
    
    def generate_text_meme(self, text):
        """Generate meme from input text with random style and animated gif."""
        try:
            # Generate static meme
            result_img = self.meme_engine.generate_text_meme(text, style='random')
            # Generate animated meme gif
            gif_path = self.meme_engine.generate_text_meme_animated(text, style='gradient', size=(800,600), frames=32, duration=50)
            if result_img:
                output_path = self.meme_engine.save_meme(result_img, "y2k_text")
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)} | GIF: {os.path.basename(gif_path)}")
                    self.window.clear_input()
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to generate meme")
        except self.meme_engine.TextValidationError as ve:
            self.window.set_status(str(ve))
        except Exception as e:
            print(f"Error generating text meme: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
        finally:
            QTimer.singleShot(3000, lambda: self.window.set_mood("idle"))
    
    def handle_random_effect(self):
        """Handle click to generate a completely random meme."""
        self.window.set_mood("processing")
        self.window.set_status("GENERATING RANDOM Y2K MAGIC...")
        # Delay generation for UI feedback
        QTimer.singleShot(500, self.generate_random_meme)
    
    def generate_random_meme(self):
        """Generate a meme with random phrase, size and style, and animated gif."""
        try:
            phrase = random.choice(self.meme_engine.y2k_phrases)
            result_img = self.meme_engine.generate_text_meme(phrase, style='random')
            gif_path = self.meme_engine.generate_text_meme_animated(phrase, style='gradient', size=(800,600), frames=32, duration=50, out_prefix="y2k_random_animated")
            if result_img:
                output_path = self.meme_engine.save_meme(result_img, "y2k_random")
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)} | GIF: {os.path.basename(gif_path)}")
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to generate meme")
        except Exception as e:
            print(f"Error generating random meme: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
        finally:
            QTimer.singleShot(3000, lambda: self.window.set_mood("idle"))
    
    def show_success_message(self):
        """Show success status then revert to ready state."""
        self.window.set_status("CHECK THE 'output' FOLDER!")
        QTimer.singleShot(3000, lambda: self.window.set_status(
            "READY TO GENERATE Y2K VIBES"
        ))
    
    def run(self):
        """Show window and start Qt event loop."""
        self.window.show()
        return self.app.exec()


def main():
    """Module entry point."""
    print("=" * 50)
    print("  CRT BUDDY - Y2K Desktop Pet")
    print("  Y2K Desktop Pet & Meme Generator")
    print("=" * 50)
    print("\n✓ Starting CRT Buddy...\n")
    
    app = CRTBuddyApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
