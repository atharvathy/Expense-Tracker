import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette - Apple Minimalist Theme
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    SLATE = RGBColor(71, 85, 105)
    MUTED = RGBColor(148, 163, 184)
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)
    CARD_BG = RGBColor(241, 245, 249)
    GREEN = RGBColor(5, 150, 105)
    ROSE = RGBColor(225, 29, 72)

    def set_bg(slide, color=LIGHT_BG):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="EXPENSE TRACKER PROJECT"):
        # Category Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide1, NAVY)

    # Accent decorative box
    shape = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.2), Inches(0.15), Inches(2.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE
    shape.line.fill.background()

    # Title text
    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11.0), Inches(3.0))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "Personal Finance & Expense Tracker"
    p0.font.size = Pt(38)
    p0.font.bold = True
    p0.font.color.rgb = WHITE

    p1 = tf.add_paragraph()
    p1.text = "A Full-Featured Python Web Dashboard & CLI Application"
    p1.font.size = Pt(20)
    p1.font.color.rgb = RGBColor(148, 163, 184)
    p1.space_before = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Tech Stack: Python 3 | Flask | SQLite3 | Plotly | Apple Minimalist UI"
    p2.font.size = Pt(13)
    p2.font.color.rgb = BLUE
    p2.space_before = Pt(30)

    # -------------------------------------------------------------
    # SLIDE 2: Project Overview & Problem Statement
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide2)
    add_header(slide2, "1. Executive Overview & Problem Statement")

    # Left Card - The Challenge
    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card1.fill.solid()
    card1.fill.fore_color.rgb = WHITE
    card1.line.color.rgb = RGBColor(226, 232, 240)
    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.3)
    tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "⚠️ The Challenge"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ROSE

    bullets1 = [
        "Managing daily expenses without clear visual analytics leads to budget overspending.",
        "Existing solutions are bloated, require cloud accounts, or lack real-time privacy control.",
        "Power users need quick terminal command access alongside a graphical web interface.",
        "Need for automated budget alerts and instant data import/export."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(10)

    # Right Card - The Solution
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0))
    card2.fill.solid()
    card2.fill.fore_color.rgb = WHITE
    card2.line.color.rgb = RGBColor(226, 232, 240)
    tf2 = card2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "💡 The ExpenseTracker Solution"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN

    bullets2 = [
        "Zero-Setup Local Application: Runs locally with zero database configuration (SQLite3).",
        "Dual-Interface Mode: Modern Web Dashboard + Command-Line Interface (CLI).",
        "Interactive Plotly Analytics: Real-time category pie breakdown & monthly income vs expense trends.",
        "Budget Limits & Progress: Track monthly caps with visual alert badges and remaining balance calculations."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: Key Features & Capabilities
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide3)
    add_header(slide3, "2. Key Features & Functionality")

    features = [
        ("📊 Financial Dashboard", "Calculates Total Income, Total Expenses, Net Balance, and Savings Rate dynamically."),
        ("📈 Plotly Interactive Visuals", "Donut chart for expense categories and grouped bar chart for monthly financial trends."),
        ("🎯 Category Budgeting", "Set monthly spending caps per category with real-time progress bars and over-budget warnings."),
        ("📂 Import & Export", "One-click CSV & JSON export and bulk import for seamless data backups and portability."),
        ("💻 Full CLI Utility", "Execute transactions, budget caps, and analytical summaries directly from your terminal."),
        ("📱 Apple Minimalist UI", "Two-page clean layout (Dashboard vs Transactions) with smooth animations and responsive controls.")
    ]

    for idx, (title, desc) in enumerate(features):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 3.9)
        y = Inches(1.6 + row * 2.5)

        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(226, 232, 240)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.2)
        tf_c.margin_top = Inches(0.2)

        p = tf_c.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf_c.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 4: Technical Architecture & Tech Stack
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide4)
    add_header(slide4, "3. Technical Architecture & Tech Stack")

    cols = [
        ("🐍 Backend", BLUE, [
            "Python 3.8+ Core",
            "Flask Microframework (WSGI)",
            "REST API Routing (/api/*)",
            "Plotly Python Engine"
        ]),
        ("🗄️ Database", GREEN, [
            "SQLite3 Embedded Engine",
            "expenses.db Persistence",
            "transactions Table Schema",
            "budgets Constraints & Seeding"
        ]),
        ("🌐 Frontend", ROSE, [
            "HTML5 & Vanilla CSS3",
            "Apple Light Theme Design System",
            "JavaScript ES6 (Fetch API)",
            "Plotly.js Interactive Canvas"
        ])
    ]

    for idx, (title, color, items) in enumerate(cols):
        x = Inches(0.8 + idx * 3.9)
        y = Inches(1.6)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(226, 232, 240)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.25)
        tf_c.margin_top = Inches(0.25)

        p = tf_c.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p = tf_c.add_paragraph()
            p.text = "✔ " + it
            p.font.size = Pt(13)
            p.font.color.rgb = SLATE
            p.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 5: How It Works & Data Flow
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide5)
    add_header(slide5, "4. End-to-End System Data Flow")

    steps = [
        ("1. User Request", "User submits transaction via Web Modal or CLI command"),
        ("2. Flask API Handler", "app.py captures JSON payload & invokes ExpenseTracker business logic"),
        ("3. SQLite Operations", "tracker.py executes parameterised SQL queries against expenses.db"),
        ("4. Analytics Calculation", "Python computes net metrics & generates Plotly chart JSON payloads"),
        ("5. Dynamic UI Update", "Fetch API updates summary stats, budget bars, and Plotly charts without reload")
    ]

    for idx, (step_title, step_desc) in enumerate(steps):
        y = Inches(1.6 + idx * 1.0)
        
        # Step Number Badge
        badge = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(2.6), Inches(0.8))
        badge.fill.solid()
        badge.fill.fore_color.rgb = BLUE
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        p = tf_b.paragraphs[0]
        p.text = step_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        # Step Detail Box
        box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.6), y, Inches(8.9), Inches(0.8))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = RGBColor(226, 232, 240)
        tf_box = box.text_frame
        tf_box.word_wrap = True
        tf_box.margin_left = Inches(0.2)
        p = tf_box.paragraphs[0]
        p.text = step_desc
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE

    # -------------------------------------------------------------
    # SLIDE 6: UI & User Experience Highlights
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide6)
    add_header(slide6, "5. User Interface & Experience Design")

    card_left = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = WHITE
    card_left.line.color.rgb = RGBColor(226, 232, 240)
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_top = Inches(0.3)

    p = tf_l.paragraphs[0]
    p.text = "📱 Two-Page Navigation Architecture"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    bullets_l = [
        "Page 1: Analytics Dashboard (Summary metrics, Plotly donut & trend charts, budget limit bars).",
        "Page 2: Transactions Manager (Dedicated full-width table, real-time search, filters).",
        "Instant Tab Switching: Clean transition between views without page reloads."
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    card_right = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0))
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = WHITE
    card_right.line.color.rgb = RGBColor(226, 232, 240)
    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.3)

    p = tf_r.paragraphs[0]
    p.text = "🎨 Apple Minimalist Design System"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = BLUE

    bullets_r = [
        "Clean Light Theme: Off-white background (#f8fafc) with white cards & 1px borders.",
        "Color-Coded Badges: Mint Green (Income), Coral Rose (Expense), Electric Blue (Balance), Indigo (Savings).",
        "Micro-Animations: Button hover lifts, glowing input focus rings, slide-up modal overlays."
    ]
    for b in bullets_r:
        p = tf_r.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 7: How To Run & Terminal CLI Usage
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide7)
    add_header(slide7, "6. Execution & Command Line Interface")

    # Command Box Left
    card_cmd = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    card_cmd.fill.solid()
    card_cmd.fill.fore_color.rgb = NAVY
    card_cmd.line.fill.background()
    tf_cmd = card_cmd.text_frame
    tf_cmd.word_wrap = True
    tf_cmd.margin_left = Inches(0.4)
    tf_cmd.margin_top = Inches(0.4)

    p = tf_cmd.paragraphs[0]
    p.text = "💻 Terminal Commands Quick-Reference"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE

    cmds = [
        ("# 1. Install dependencies", "pip install -r requirements.txt"),
        ("# 2. Launch Web Dashboard on http://127.0.0.1:5000", "python main.py"),
        ("# 3. Add transaction via CLI", "python main.py cli add --title \"Grocery\" --amount 125.50 --category \"Food & Dining\" --type Expense"),
        ("# 4. View financial summary in terminal", "python main.py cli summary"),
        ("# 5. Export data to CSV file", "python main.py cli export --format csv --output my_expenses.csv")
    ]
    for comment, cmd in cmds:
        p = tf_cmd.add_paragraph()
        p.text = comment
        p.font.size = Pt(11)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

        p2 = tf_cmd.add_paragraph()
        p2.text = "$ " + cmd
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(52, 211, 153)

    # -------------------------------------------------------------
    # SLIDE 8: Summary & Conclusion
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_bg(slide8, NAVY)

    t_box8 = slide8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.0))
    tf8 = t_box8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf8.add_paragraph()
    p.text = "Expense Tracker Application in Python"
    p.font.size = Pt(22)
    p.font.color.rgb = BLUE
    p.space_before = Pt(10)

    p = tf8.add_paragraph()
    p.text = "• Full-featured Web Dashboard + CLI interface\n• Interactive Plotly visual analytics & SQLite persistence\n• Ready for deployment & personal finance management"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(20)

    # Save presentation
    output_filename = "ExpenseTracker_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation successfully created: {output_filename}")

if __name__ == '__main__':
    create_deck()
