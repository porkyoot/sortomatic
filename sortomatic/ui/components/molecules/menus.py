from nicegui import ui
from typing import List, Dict, Optional, Callable, Union
from ...theme import Theme, StatusStyles
from ..atoms.buttons import AppButton
from ..atoms.dangerous_buttons import DangerousButton

def ChevronStep(
    label: str,
    color: str,
    is_first: bool = False,
    is_last: bool = False,
    is_locked: bool = True,
    is_active: bool = False,
    on_click: Optional[Callable] = None,
):
    """
    A single chevron step in the workflow menu.
    Now uses semantic states: enable, disable, active.
    """
    # Determine shape based on position
    shape = 'chevron'
    if is_first: shape = 'chevron-first'
    elif is_last: shape = 'chevron-last'

    # Determine state
    state = 'enable'
    if is_locked: state = 'disable'
    if is_active: state = 'active'
    
    # Use AppButton with semantic shapes and states
    return AppButton(
        label=label,
        on_click=on_click if not is_locked else None,
        variant='primary',
        shape=shape,
        state=state,
        color=color
    ).classes('s-workflow-step')


class WorkflowMenu(ui.row):
    """
    A menu with buttons that is fixed on scroll and is a row on top of the screen.
    Each step is a chevron that unlocks as the workflow progresses.
    """
    def __init__(self, theme: Theme, on_step_click: Optional[Callable[[str], None]] = None, on_nuke: Optional[Callable] = None):
        super().__init__()
        self.theme = theme
        self.on_step_click = on_step_click
        self.on_nuke = on_nuke
        
        # State
        self._current_step_index = 0
        self._unlocked_up_to = 0
        
        # Build UI with theme context
        with self:
            self.classes('s-workflow-menu no-wrap items-center')
            
            # Using DangerousButton for the nuke action with hold-to-confirm mechanism
            self.nuke_btn = DangerousButton(
                icon='mdi-nuke',
                on_click=self.on_nuke,
                color=self.theme.colors.orange,
                tooltip='Hold to Nuke Database',
                size='md'
            ).classes('mr-2')
            
            # Keep nuke shadow variable
            self.nuke_btn.btn.style(f'--nuke-color: {self.theme.colors.orange};')


                
            with ui.row().classes('s-workflow-steps-container no-wrap') as self.steps_container:
                self._render_steps()


    def _get_steps_data(self):
        # Explicitly use colors from our theme object
        return [
            ("Indexing", self.theme.colors.blue),
            ("Duplicates", self.theme.colors.cyan),
            ("Category", self.theme.colors.green),
            ("Context", self.theme.colors.yellow),
            ("War Room", self.theme.colors.red),
            ("Sorting", self.theme.colors.magenta),
            ("Views", self.theme.colors.violet),
        ]



    def _render_steps(self):
        self.steps_container.clear()
        steps_data = self._get_steps_data()
        
        with self.steps_container:
            for i, (label, color) in enumerate(steps_data):
                is_first = (i == 0)
                is_last = (i == len(steps_data) - 1)
                is_locked = (i > self._unlocked_up_to)
                is_active = (i == self._current_step_index)
                
                ChevronStep(
                    label=label,
                    color=color,
                    is_first=is_first,
                    is_last=is_last,
                    is_locked=is_locked,
                    is_active=is_active,
                    on_click=lambda l=label, idx=i: self._on_step_clicked(l, idx)
                )

    def _on_step_clicked(self, label: str, index: int):
        if index <= self._unlocked_up_to:
            self._current_step_index = index
            self._render_steps()
            if self.on_step_click:
                self.on_step_click(label)

    def unlock_next(self):
        """Unlocks the next step in the workflow."""
        steps_data = self._get_steps_data()
        if self._unlocked_up_to < len(steps_data) - 1:
            self._unlocked_up_to += 1
            self._render_steps()

    def set_progress(self, index: int):
        """Sets the current active step and unlocks up to it."""
        self._unlocked_up_to = max(self._unlocked_up_to, index)
        self._current_step_index = index
        self._render_steps()

    def reset(self):
        """Resets the workflow to the first step."""
        self._current_step_index = 0
        self._unlocked_up_to = 0
        self._render_steps()

