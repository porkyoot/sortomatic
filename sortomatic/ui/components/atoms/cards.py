from nicegui import ui
from typing import Optional

class AppCard(ui.card):
    """
    A premium themed card wrapper for NiceGUI.
    Consolidates rounding, shadows, borders, and glassmorphism.
    """
    def __init__(self, 
                 variant: str = 'glass', # 'solid', 'glass', 'subtle', 'vibrant'
                 padding: str = '',      # Optional override, s-card has default p-6 equivalent
                 tight: bool = False):
        """
        Args:
            variant: The visual style of the card.
            padding: Quasar/Tailwind padding classes to override default.
            tight: If true, removes default card padding/gap.
        """
        super().__init__()
        
        # Base Class
        css_classes = ["s-card"]
        
        # Variants
        if variant != 'solid': # solid is default s-card style basically
             css_classes.append(f"s-card--{variant}")

        # Padding/Tightness
        if tight:
            css_classes.append('p-0 gap-0')
        elif padding:
             css_classes.append(padding)

        self.classes(" ".join(css_classes))

