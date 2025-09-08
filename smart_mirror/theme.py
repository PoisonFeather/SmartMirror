class Theme:
    BG = "#0B0B0D"        # near-black
    BG_DIM = "#0F1115"    # slightly lighter for cards
    TEXT_HI = "#F5F5F7"   # high emphasis text
    TEXT_LO = "#B4BBC7"   # low emphasis text
    ACCENT = "#7CD4FD"    # soft cyan accent
    GLOW = "#87CEFA"      # glow color for subtle text shadow

    @staticmethod
    def base_stylesheet():
        return f"""
        QWidget {{
            background-color: {Theme.BG};
            color: {Theme.TEXT_HI};
            font-family: 'Inter', 'Roboto', 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
            letter-spacing: 0.2px;
        }}
        QLabel#title {{
            font-weight: 500;
            color: {Theme.TEXT_HI};
        }}
        QLabel#subtitle {{
            font-weight: 400;
            color: {Theme.TEXT_LO};
        }}
        QLabel#accent {{
            color: {Theme.ACCENT};
        }}
        .card {{
            background-color: {Theme.BG_DIM};
            border-radius: 20px;
        }}
        """
