class Theme:
    BG = "#0B0B0D"        # near-black
    TEXT_HI = "#F5F5F7"
    TEXT_LO = "#B4BBC7"
    ACCENT = "#7CD4FD"
    GLOW = "#87CEFA"

    # ultralight cards (subtle on mirror)
    CARD_BG = "rgba(18, 20, 24, 0.55)"
    CARD_RADIUS = 20

    @staticmethod
    def base_stylesheet():
        return f"""
        QWidget {{
            background-color: {Theme.BG};
            color: {Theme.TEXT_HI};
            font-family: 'Inter', 'Roboto', 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
            letter-spacing: 0.2px;
        }}
        QLabel#title {{ font-weight: 500; color: {Theme.TEXT_HI}; }}
        QLabel#subtitle {{ font-weight: 400; color: {Theme.TEXT_LO}; }}
        QLabel#accent {{ color: {Theme.ACCENT}; }}

        /* Minimal cards */
        .card {{
            background-color: {Theme.CARD_BG};
            border-radius: {Theme.CARD_RADIUS}px;
            border: 1px solid rgba(124, 212, 253, 0.08);
        }}

        /* Hairline divider */
        QFrame#line {{
            background: rgba(255,255,255,0.08);
            min-height: 1px;
            max-height: 1px;
            border: none;
        }}
        """
