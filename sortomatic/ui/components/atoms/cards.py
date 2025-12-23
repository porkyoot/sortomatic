from nicegui import ui
from typing import Optional

class AppCard(ui.card):
    """
    A premium themed card wrapper for NiceGUI.
    Consolidates rounding, shadows, borders, and glassmorphism.
    """
    def __init__(self, 
                 variant: str = 'glass', # 'solid', 'glass', 'subtle', 'vibrant'
                 padding: str = 'p-6',
                 tight: bool = False):
        """
        Args:
            variant: The visual style of the card.
            padding: Quasar/Tailwind padding classes.
            tight: If true, removes default card spacing between elements.
        """
        super().__init__()
        
        # Base alignment and rounding
        self.classes(f'rounded-app {padding} transition-all border border-white/10 w-full')
        
        if tight:
            self.classes('gap-0')
            
        if variant == 'glass':
            self.classes('glass bg-white/5')
        elif variant == 'solid':
            self.classes('bg-white/10 shadow-md')
        elif variant == 'vibrant':
            self.classes('bg-white/5 vibrant-shadow border-white/20')
        elif variant == 'subtle':
            self.classes('bg-white/[0.03] border-white/5 shadow-none')
            
        # Subtle hover interaction
        self.classes('hover:bg-white/[0.07]')
