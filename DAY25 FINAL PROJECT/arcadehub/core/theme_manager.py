#----- Theme Manager -----
class ThemeManager:
    def __init__(self):
        self.current_theme = 'default'
        self.themes = {
            'default': {
                'bg': '#ccf2ff',
                'button': '#b3e6b3',
                'button_hover': '#99d699',
                'text': '#000000',
                'accent': '#ffcccc',
                'secondary': '#d9b3ff'
            },
            'dark': {
                'bg': '#2c2c2c',
                'button': '#404040',
                'button_hover': '#555555',
                'text': '#ffffff',
                'accent': '#666666',
                'secondary': '#4a4a4a'
            },
            'ocean': {
                'bg': '#001f3f',
                'button': '#0074D9',
                'button_hover': '#0056b3',
                'text': '#ffffff',
                'accent': '#39CCCC',
                'secondary': '#7FDBFF'
            },
            'sunset': {
                'bg': '#ff6b35',
                'button': '#f7931e',
                'button_hover': '#e6820d',
                'text': '#ffffff',
                'accent': '#ffcc02',
                'secondary': '#c5d86d'
            }
        }
    
    def get_theme(self):
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
