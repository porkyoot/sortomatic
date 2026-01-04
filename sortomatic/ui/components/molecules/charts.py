from nicegui import ui
from typing import List, Dict, Optional, Callable
from sortomatic.ui.style import theme

class DonutChart(ui.card):
    """
    A generic Donut Chart component using ECharts with an update_data method.
    """
    
    def __init__(self, title: str, legend_on_right: bool = True, on_click: Optional[Callable] = None, icon_color: Optional[str] = None):
        super().__init__()
        
        # Defaults
        icon_color = icon_color or theme.PRIMARY
        
        # Standard card styling
        self.classes('p-4 rounded-lg premium-glass flex flex-col gap-4 w-full h-full p-0 gap-0')
        self.classes('remove-default-card-padding')
        self.style('display: flex; flex-direction: column;')
        
        with self:
            # Header
            with ui.row().classes('w-full items-center gap-2 px-4 py-2 border-b thin-border'):
                ui.icon('donut_large', color=icon_color).classes('text-xl')
                ui.label(title).classes('text-lg font-bold uppercase tracking-wider text-muted')
                ui.element('div').classes('flex-1') # Spacer
            
            # Configure responsive layout
            if legend_on_right:
                # Desktop: legend on right, chart centered-left
                desktop_legend = {'type': 'scroll', 'orient': 'vertical', 'right': '5%', 'top': 'middle', 'textStyle': {'color': theme.TEXT_MAIN}}
                desktop_center = ['30%', '50%']
                
                # Mobile
                mobile_legend = {'type': 'scroll', 'orient': 'horizontal', 'bottom': '0%', 'left': 'center', 'textStyle': {'color': theme.TEXT_MAIN}}
                mobile_center = ['50%', '45%']
            else:
                desktop_legend = {'type': 'scroll', 'orient': 'horizontal', 'top': '5%', 'left': 'center', 'textStyle': {'color': theme.TEXT_MAIN}}
                desktop_center = ['50%', '50%']
                mobile_legend = desktop_legend
                mobile_center = desktop_center
    
            chart_config = {
                'backgroundColor': 'transparent',
                'baseOption': {
                    'tooltip': {'show': False},
                    'legend': desktop_legend,
                    'series': [{
                        'name': title,
                        'type': 'pie',
                        'radius': ['40%', '70%'],
                        'center': desktop_center,
                        'avoidLabelOverlap': False,
                        'padAngle': 5,
                        'itemStyle': {'borderRadius': 5, 'borderColor': 'transparent', 'borderWidth': 0},
                        'label': {'show': False, 'position': 'center', 'color': theme.TEXT_MAIN},
                        'emphasis': {'label': {'show': True, 'fontSize': '20', 'fontWeight': 'bold', 'color': theme.TEXT_MAIN}},
                        'labelLine': {'show': False},
                        'data': []
                    }]
                },
                'media': [
                    {
                        'query': {'maxWidth': 600},
                        'option': {
                            'legend': mobile_legend,
                            'series': [{'center': mobile_center, 'radius': ['35%', '60%']}]
                        }
                    },
                    {
                        'query': {'minWidth': 601},
                        'option': {
                            'legend': desktop_legend,
                            'series': [{'center': desktop_center, 'radius': ['40%', '70%']}]
                        }
                    }
                ]
            }
            
            # Click Handler
            def _handle_click_event(e):
                if on_click:
                    on_click(e)
                    
            # Chart Element
            self.chart = ui.echart(
                chart_config, 
                on_point_click=_handle_click_event if on_click else None
            ).classes('w-full flex-1 min-h-0').style('min-height: 200px;')

    def update_data(self, data: List[Dict]):
        """
        Update the chart data.
        data: List of dicts with 'name' and 'value' keys.
        """
        if not hasattr(self, 'chart') or not self.chart:
            return

        if 'baseOption' in self.chart.options:
            options = self.chart.options['baseOption']
        else:
            options = self.chart.options
            
        if 'series' in options and options['series']:
            options['series'][0]['data'] = data
        
        self.chart.update()


def donut_chart(title: str, legend_on_right: bool = True, on_click: Optional[Callable] = None, icon_color: Optional[str] = None) -> DonutChart:
    """
    Factory function for DonutChart.
    
    Returns a DonutChart element with an `update_data(data: List[Dict])` method.
    """
    return DonutChart(title, legend_on_right, on_click, icon_color)
