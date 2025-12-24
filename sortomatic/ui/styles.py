from nicegui import ui
from .theme import Theme


def generate_css_variables(theme: Theme) -> str:
    """Converts the Python Theme object into CSS Variables."""
    
    # Generate Accent Vars programmatically
    accents = {
        'green': theme.colors.green,
        'red': theme.colors.red,
        'cyan': theme.colors.cyan,
        'orange': theme.colors.orange,
        'yellow': theme.colors.yellow,
        'blue': theme.colors.blue,
        'magenta': theme.colors.magenta,
        'violet': theme.colors.violet,
    }
    accents.update(theme.colors.accents)
    accent_vars = "\\n".join([f"--c-accent-{k}: {v};" for k, v in accents.items()])
    
    return f"""
    :root {{
        /* COLORS */
        --c-surface-1: {theme.colors.surface_1};
        --c-surface-2: {theme.colors.surface_2};
        --c-surface-3: {theme.colors.surface_3};
        --c-text-main: {theme.colors.text_main};
        --c-text-subtle: {theme.colors.text_subtle};
        --c-primary: {theme.colors.primary};
        --c-secondary: {theme.colors.secondary};
        --c-success: {theme.colors.success};
        --c-warning: {theme.colors.warning};
        --c-error: {theme.colors.error};
        {accent_vars}

        /* LAYOUT (Responsive) */
        --unit: {theme.layout.spacing_unit};
        --r-sm: {theme.layout.radius_sm};
        --r-md: {theme.layout.radius_md};
        --r-lg: {theme.layout.radius_lg};
        --r-full: {theme.layout.radius_full};
        
        /* Spacing Scale */
        --s-0: 0px;
        --s-0_5: calc(var(--unit) * 0.5);
        --s-1: calc(var(--unit) * 1);
        --s-1_5: calc(var(--unit) * 1.5);
        --s-2: calc(var(--unit) * 2);
        --s-2_5: calc(var(--unit) * 2.5);
        --s-3: calc(var(--unit) * 3);
        --s-4: calc(var(--unit) * 4);
        --s-5: calc(var(--unit) * 5);
        --s-6: calc(var(--unit) * 6);
        --s-8: calc(var(--unit) * 8);
        --s-10: calc(var(--unit) * 10);
        --s-12: calc(var(--unit) * 12);
        --s-16: calc(var(--unit) * 16);
        --s-20: calc(var(--unit) * 20);
        --s-24: calc(var(--unit) * 24);
        --s-32: calc(var(--unit) * 32);
        --s-40: calc(var(--unit) * 40);
        --s-48: calc(var(--unit) * 48);
        --s-56: calc(var(--unit) * 56);
        --s-64: calc(var(--unit) * 64);
        
        /* BORDERS */
        /* BORDERS */
        --b-thin: 1px;
        --b-medium: calc(var(--b-thin) * 2);
        --b-thick: calc(var(--b-thin) * 4);
        
        /* TYPOGRAPHY */
        --font-main: {theme.layout.font_sans};
        --font-mono: {theme.layout.font_mono};
        
        /* TYPOGRAPHY SCALE */
        --text-base: var(--s-3);                  /* 12px (0.75rem) */
        --text-xs: calc(var(--text-base) * 0.85); /* ~10px */
        --text-md: calc(var(--text-base) * 1.166);/* ~14px */
        --text-lg: calc(var(--text-base) * 1.333);/* ~16px */
        --text-xl: calc(var(--text-base) * 2);    /* 24px */
        --text-2xl: calc(var(--text-xl) * 1.5);   /* 36px */
        
        /* SHADOWS (Semantic) */
        --shadow-subtle: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-card: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-float: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }}
    
    body {{
        background-color: var(--c-surface-1);
        color: var(--c-text-main);
        font-family: var(--font-main);
        font-size: var(--text-base);
        margin: 0;
    }}
    """

def load_global_styles(theme: Theme):
    """
    Injects the CSS Design System. 
    This is the ONLY place where CSS property values should live.
    """
    
    # 1. Inject Variables
    ui.add_head_html(f"<style>{generate_css_variables(theme)}</style>")
    
    # 2. Inject Semantic Classes (The Markdown-like approach)
    ui.add_head_html("""
    <style>
        /* --- ATOMS: BUTTONS --- */
        .s-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: var(--b-thin) solid transparent;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            
            /* Responsive sizes based on token units */
            padding: var(--s-2) var(--s-4);
            font-size: var(--text-md);
            border-radius: var(--r-md);
            gap: var(--s-2);
        }
        
        .s-btn:hover { transform: translateY(-1px); }
        .s-btn:active { transform: translateY(0px); }

        /* Variants */
        .s-btn--primary {
            background-color: var(--c-primary);
            color: var(--c-surface-1);
            box-shadow: var(--shadow-subtle);
        }
        .s-btn--primary:hover { filter: brightness(1.1); box-shadow: var(--shadow-card); }

        .s-btn--secondary {
            background-color: var(--c-secondary);
            color: var(--c-surface-1);
        }

        .s-btn--ghost {
            background-color: transparent;
            color: var(--c-text-subtle);
        }
        .s-btn--ghost:hover {
            background-color: var(--c-surface-2);
            color: var(--c-text-main);
        }

        /* Sizes */
        .s-btn--xs {
            padding: var(--s-1) var(--s-2);
            font-size: var(--text-xs);
            gap: var(--s-1);
        }
        .s-btn--sm {
            padding: var(--s-1_5) var(--s-3);
            font-size: var(--text-base);
        }
        .s-btn--lg {
            padding: var(--s-3) var(--s-6);
            font-size: var(--text-lg);
        }

        /* Shapes */
        .s-shape--pill { border-radius: var(--r-full); }
        .s-shape--square { aspect-ratio: 1/1; padding: var(--s-2); }

        /* --- ATOMS: CARDS --- */
        .s-card {
            background-color: var(--c-surface-2);
            border-radius: var(--r-lg);
            border: var(--b-thin) solid color-mix(in srgb, var(--c-text-main), transparent 90%);
            padding: var(--s-6); /* 1.5rem padding */
            transition: box-shadow 0.3s ease;
        }
        
        .s-card--glass {
            background-color: color-mix(in srgb, var(--c-surface-2), transparent 20%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        
        .s-card:hover {
            box-shadow: var(--shadow-card);
            border-color: color-mix(in srgb, var(--c-text-main), transparent 80%);
        }

        /* --- UTILS: TYPOGRAPHY --- */
        .s-text-h1 { font-size: var(--text-2xl); font-weight: 700; letter-spacing: -0.02em; }
        .s-text-body { font-size: var(--text-base); line-height: 1.5; color: var(--c-text-subtle); }
    </style>
    """)
