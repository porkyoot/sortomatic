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
        self.classes(f'rounded-app {padding} transition-all border w-full border-app')
        # self.style('border-color: var(--app-text-sec); opacity: 0.5;') # Default border opacity handled by class or global
        
        if tight:
            self.classes('gap-0')
            
        if variant == 'glass':
            self.classes('glass bg-app-surface')
        elif variant == 'solid':
            self.classes('shadow-md bg-app-surface')
        elif variant == 'vibrant':
            self.classes('vibrant-shadow bg-app-surface')
            self.style('border-color: var(--app-primary);')
        elif variant == 'subtle':
            self.classes('shadow-none')
            self.style('background-color: transparent;')
            
        # Subtle hover interaction
        # We can't easily use hover with vars in classes without tailwind config, 
        # so we'll skip the hover bg change or rely on global CSS if set.
        # Removing manual white hover for strict adherence.
