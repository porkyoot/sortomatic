from nicegui import ui
from typing import List, Optional

class AppHistogram(ui.row):
    """
    A premium inline histogram (sparkline) for performance monitoring.
    Supports dynamic updates to prevent UI flickering/blinking.
    """
    def __init__(
        self,
        values: List[float], 
        color: str = 'var(--q-primary)',
        height: str = '24px',
        bar_width: str = '3px',
        gap: str = '1px',
        max_bars: int = 10,
        label: Optional[str] = None,
        icon: Optional[str] = None,
        transparent: bool = False
    ):
        super().__init__()
        self.max_bars = max_bars
        self.label = label
        self.color = color
        self.height_val = height
        self.bar_width = bar_width
        self.gap = gap
        
        container_classes = 's-histogram'
        if not transparent:
            container_classes += ' shadow-sm'
        
        container_style = f'color: {color};'
        if transparent:
            container_style += ' background-color: transparent; border: none;'
            
        self.classes(container_classes).style(container_style)
        
        with self:
            self.tooltip = ui.tooltip('').classes('text-[10px] font-bold')
            
            if icon:
                from ..icons import AppIcon
                AppIcon(icon, size="1.2em", color=color).classes('opacity-80')

            # Bars Container
            self.bars_container = ui.row().classes('items-end no-wrap shrink-0 group').style(f'height: {height}; gap: {gap};')
            with self.bars_container:
                # Pre-create bars
                self.bars = [ui.element('div').classes('s-histogram__bar') for _ in range(max_bars)]
        
        self.update_data(values)

    def update_data(self, values: List[float]):
        """Update histogram bars and tooltip text without re-creating elements."""
        display_values = values[-self.max_bars:] if len(values) > self.max_bars else values
        latest_val = display_values[-1] if display_values else 0
        
        # Update tooltip
        self.tooltip.text = f"{self.label}: {latest_val*100:.1f}%" if self.label else f"{latest_val*100:.1f}%"
        
        # Update bars
        for i, bar in enumerate(self.bars):
            if i < len(display_values):
                val = display_values[i]
                # Ensure value is clamped
                clamped_val = max(0.05, min(1.0, val))
                
                bar.style(
                    f'height: {clamped_val * 100}%; '
                    f'width: {self.bar_width}; '
                    f'opacity: {0.4 + (clamped_val * 0.6)};'
                )
                bar.set_visibility(True)
            else:
                bar.set_visibility(False)


