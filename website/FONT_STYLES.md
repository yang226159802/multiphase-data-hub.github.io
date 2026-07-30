 # Font & Style Reference
 
 Last updated: 2026-07-30
 Branch: ui_optimization
 
 ## Navigation Bar
 
 | Element | Property | Value |
 |---|---|---|
 | Logo (.brand) | font-size | 28px |
 | Logo (.brand) | font-weight | 780 |
 | Logo (.brand) | color | var(--accent-dark) = #084a43 |
 | Nav links (.nav-links a) | font-size | 24px |
 | Nav links | color | var(--ink) = #16201d |
 | Nav links hover | text-decoration | underline |
 | Nav links hover | text-underline-offset | 4px |
 | Nav bar (.site-nav) | background | #fff |
 | Nav bar (.site-nav) | position | fixed; top: 0; z-index: 100 |
 | Nav bar (.site-nav) | border-bottom | 1px solid var(--line) |
 
 ## Page Titles (h1)
 
 | Element | Property | Value |
 |---|---|---|
 | h1 | font-size | clamp(14px, 2.3vw, 27px) |
 | h1 | line-height | 0.98 |
 | h1 | letter-spacing | 0 |
 
 ## Body Text
 
 | Element | Property | Value |
 |---|---|---|
 | body | font-family | Inter, ui-sans-serif, system-ui, sans-serif |
 | body | color | var(--ink) = #16201d |
 | body | background | var(--bg) = #f6f7f4 |
 | body | padding-top | 52px (for fixed nav) |
 
 ## Footer
 
 | Element | Property | Value |
 |---|---|---|
 | .footer | background | #1a1a1a |
 | .footer | color | rgba(255, 255, 255, 0.72) |
 | .footer | font-size | 14px |
 | .footer a | color | rgba(255, 255, 255, 0.88) |
 | .footer a:hover | color | #fff |
 | .footer a:hover | text-decoration | underline |
 
 ## Color Palette
 
 | Variable | Value | Usage |
 |---|---|---|
 | --bg | #f6f7f4 | Page background |
 | --ink | #16201d | Primary text |
 | --muted | #5f6b64 | Secondary text |
 | --line | #d9dfd9 | Borders |
 | --panel | #ffffff | Cards |
 | --soft | #e9efeb | Soft backgrounds |
 | --accent | #0d6f62 | Links, buttons |
 | --accent-dark | #084a43 | Nav logo, headers |
 | --rust | #ad4a34 | Alerts |
 | --amber | #d4a236 | Highlights |
