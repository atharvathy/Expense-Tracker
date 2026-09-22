import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_simple_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    DARK_BLUE = RGBColor(30, 58, 138)
    SLATE = RGBColor(71, 85, 105)
    MUTED = RGBColor(100, 116, 139)
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)
    GREEN = RGBColor(16, 185, 129)

    def set_bg(slide, color=LIGHT_BG):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, subtitle_text="EXPENSE TRACKER APPLICATION"):
        # Category Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = subtitle_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide with Division, Specialization & Students
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1, NAVY)

    # Decorative Accent Bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(4.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Title & Subtitle Text Box
    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(11.0), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "Expense Tracker Application"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = WHITE

    p1 = tf.add_paragraph()
    p1.text = "Personal Finance Management System"
    p1.font.size = Pt(20)
    p1.font.color.rgb = RGBColor(148, 163, 184)
    p1.space_before = Pt(8)

    # Division & Specialization Badge
    p2 = tf.add_paragraph()
    p2.text = "Division: F  |  Specialization: FSW (Full Stack Web)"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = BLUE
    p2.space_before = Pt(16)

    # Team Members Card
    team_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.9), Inches(11.0), Inches(2.3))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    team_card.line.color.rgb = RGBColor(51, 65, 85)

    tf_team = team_card.text_frame
    tf_team.word_wrap = True
    tf_team.margin_left = Inches(0.3)
    tf_team.margin_top = Inches(0.2)

    p_th = tf_team.paragraphs[0]
    p_th.text = "👥 PRESENTED BY (TEAM MEMBERS)"
    p_th.font.size = Pt(12)
    p_th.font.bold = True
    p_th.font.color.rgb = GREEN

    members = [
        ("Patel Jagrutiben Takhatsinh", "2505112110020"),
        ("Prajapati Riya Maheshbhai", "2505112110025"),
        ("Sonar Mahi Umakat", "2505112110035")
    ]

    for name, student_id in members:
        p_m = tf_team.add_paragraph()
        p_m.text = f"•  {name}   —   (ID: {student_id})"
        p_m.font.size = Pt(14)
        p_m.font.bold = True
        p_m.font.color.rgb = WHITE
        p_m.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 2: Project Overview
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_bg(slide2)
    add_header(slide2, "1. Project Overview")

    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card1.fill.solid()
    card1.fill.fore_color.rgb = WHITE
    card1.line.color.rgb = RGBColor(226, 232, 240)
    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.3)
    tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "📌 Introduction"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    bullets1 = [
        "The Expense Tracker is a complete personal finance solution built to help users manage their money effectively.",
        "It provides real-time tracking of incomes and expenses with category-wise budget limits.",
        "Designed to work smoothly both as a Web Application and as a Terminal Command-Line Tool (CLI).",
        "Operates completely locally to ensure maximum data privacy and fast response times."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0))
    card2.fill.solid()
    card2.fill.fore_color.rgb = WHITE
    card2.line.color.rgb = RGBColor(226, 232, 240)
    tf2 = card2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "🎯 Main Objectives"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE

    bullets2 = [
        "Simplify Expense Tracking: Easily record transactions with dates, categories, payment methods, and notes.",
        "Budget Monitoring: Set spending caps for food, rent, entertainment, and utilities to avoid overspending.",
        "Visual Analytics: View clear interactive charts for category breakdowns and monthly income vs expense trends.",
        "Data Export & Import: Easily export financial reports in CSV and JSON formats."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 3: Core Features
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_bg(slide3)
    add_header(slide3, "2. Key Features")

    features = [
        ("💵 Financial Summary", "Calculates Total Income, Total Expenses, Net Balance, and Savings Rate automatically."),
        ("📈 Plotly Interactive Charts", "Provides interactive Donut and Bar charts for deep insights into spending habits."),
        ("🎯 Category Budgets", "Set monthly spending limits for each category with visual progress indicators."),
        ("🔍 Smart Search & Filters", "Instantly filter transactions by type, category, or title keyword search."),
        ("📂 CSV & JSON Export", "Export and import your transaction records anytime for backup or reporting."),
        ("💻 Terminal CLI Support", "Perform all financial actions directly from your terminal using simple commands.")
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
        tf_c.margin_left = Inches(0.25)
        tf_c.margin_top = Inches(0.25)

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
    # SLIDE 4: Technology Stack
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_bg(slide4)
    add_header(slide4, "3. Technology Stack")

    tech_cols = [
        ("🐍 Backend", BLUE, [
            "Python 3",
            "Flask Web Framework",
            "REST API Endpoints",
            "Plotly Python Engine"
        ]),
        ("🗄️ Database", GREEN, [
            "SQLite3 Database Engine",
            "expenses.db File Storage",
            "transactions Table",
            "budgets Constraints Table"
        ]),
        ("🌐 Frontend", DARK_BLUE, [
            "HTML5 Markup",
            "Vanilla CSS3 Design System",
            "JavaScript (ES6 Fetch API)",
            "Plotly.js Interactive Charts"
        ])
    ]

    for idx, (title, color, items) in enumerate(tech_cols):
        x = Inches(0.8 + idx * 3.9)
        y = Inches(1.6)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(226, 232, 240)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.3)
        tf_c.margin_top = Inches(0.3)

        p = tf_c.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p = tf_c.add_paragraph()
            p.text = "• " + it
            p.font.size = Pt(13)
            p.font.color.rgb = SLATE
            p.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 5: How It Works & Data Architecture
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_bg(slide5)
    add_header(slide5, "4. How It Works (System Architecture)")

    flow_steps = [
        ("1. User Action", "User submits transaction or applies filters in the Web interface or CLI."),
        ("2. Flask Controller", "app.py processes the HTTP request and calls tracker.py business methods."),
        ("3. SQLite Storage", "database.py executes SQL queries to store or retrieve financial data."),
        ("4. Plotly Processing", "Python generates Plotly visual data objects for charts."),
        ("5. Real-Time Update", "JavaScript receives JSON and updates the UI instantly without page reload.")
    ]

    for idx, (step_title, step_desc) in enumerate(flow_steps):
        y = Inches(1.6 + idx * 1.0)
        
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
    # SLIDE 6: User Interface Pages
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_bg(slide6)
    add_header(slide6, "5. User Interface Structure")

    card_l = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = WHITE
    card_l.line.color.rgb = RGBColor(226, 232, 240)
    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_top = Inches(0.3)

    p = tf_l.paragraphs[0]
    p.text = "📊 Page 1: Dashboard View"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    b_l = [
        "Summary Cards: Shows Total Income, Total Expenses, Net Balance, and Savings Rate.",
        "Interactive Charts: Displays Expense by Category Donut Chart and Monthly Trends Bar Chart.",
        "Budget Limits: Shows monthly spending progress bars and over-budget status per category."
    ]
    for b in b_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    card_r = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = WHITE
    card_r.line.color.rgb = RGBColor(226, 232, 240)
    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.3)

    p = tf_r.paragraphs[0]
    p.text = "📋 Page 2: Transactions View"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = BLUE

    b_r = [
        "Transaction Table: Lists all records with Date, Title, Category, Payment Method, Type, and Amount.",
        "Search & Filters: Filter by type (Expense/Income), category, or keyword search.",
        "Action Buttons: Add new transactions, edit existing entries, delete records, and export CSV/JSON data."
    ]
    for b in b_r:
        p = tf_r.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = SLATE
        p.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 7: How To Run
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_bg(slide7)
    add_header(slide7, "6. How to Run the Application")

    card_run = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    card_run.fill.solid()
    card_run.fill.fore_color.rgb = NAVY
    card_run.line.fill.background()
    tf_run = card_run.text_frame
    tf_run.word_wrap = True
    tf_run.margin_left = Inches(0.4)
    tf_run.margin_top = Inches(0.4)

    p = tf_run.paragraphs[0]
    p.text = "💻 Running the Application"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE

    commands_list = [
        ("# Step 1: Install Python dependencies", "pip install -r requirements.txt"),
        ("# Step 2: Start the Web Dashboard server on http://127.0.0.1:5000", "python main.py"),
        ("# Step 3: Add transaction using Terminal CLI", "python main.py cli add --title \"Grocery\" --amount 125.50 --category \"Food & Dining\" --type Expense"),
        ("# Step 4: Display financial summary in Terminal", "python main.py cli summary"),
        ("# Step 5: Export data to CSV file", "python main.py cli export --format csv --output my_expenses.csv")
    ]

    for comment, cmd in commands_list:
        p = tf_run.add_paragraph()
        p.text = comment
        p.font.size = Pt(11)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

        p2 = tf_run.add_paragraph()
        p2.text = "$ " + cmd
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(52, 211, 153)

    # -------------------------------------------------------------
    # SLIDE 8: Conclusion & Team Details
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_bg(slide8, NAVY)

    t_box8 = slide8.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0))
    tf8 = t_box8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf8.add_paragraph()
    p.text = "Expense Tracker Application  |  Division: F  |  Specialization: FSW"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(8)

    p = tf8.add_paragraph()
    p.text = "Presented by Team Members:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_before = Pt(20)

    for name, student_id in members:
        p_m = tf8.add_paragraph()
        p_m.text = f"•  {name}  (ID: {student_id})"
        p_m.font.size = Pt(15)
        p_m.font.color.rgb = RGBColor(226, 232, 240)
        p_m.space_before = Pt(6)

    output_file = "ExpenseTracker_Presentation_Simple.pptx"
    prs.save(output_file)
    print(f"Simple presentation with team details created: {output_file}")

if __name__ == '__main__':
    create_simple_deck()
