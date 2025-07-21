import datetime
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Define survey structure with maximum possible scores
CATEGORIES = {
    '1A': (2, 30, 0.35),  # (weight, num_questions, bonus_fraction)
    '1B': (3, 12, 0.30),
    '2A': (5, 21, 0.25),
    '2B': (8, 23, 0.20),
    '3A': (13, 22, 0.15),
    '3B': (21, 10, 0.10),
    '3C': (34, 14, 0.02),    
    '4A': (55, 22, 0),
    '4B': (89, 19, 0),
    '5A': (144, 20, 0),
    '5B': (233, 17, 0)
}

CB_ORANGE = '#E69F00'
CB_BLUE = '#0072B2'
CB_PURPLE = '#CC79A7' # Or try '#009E73' (green) for another option

def calculate_max_possible_score(weight, num_questions, bonus_fraction):
    """Calculate maximum possible score for a section"""
    base_max = weight * num_questions
    bonus_max = bonus_fraction * base_max if bonus_fraction > 0 else 0
    return base_max + bonus_max

def calculate_polygon_area(normalized_scores):
    """Calculate the area of the polygon formed by the radar chart using shoelace formula"""
    n = len(normalized_scores)
    
    # Create angles for each vertex
    angles = [2 * math.pi * i / n for i in range(n)]
    
    # Convert polar coordinates to cartesian
    x_coords = [r * math.cos(angle) for r, angle in zip(normalized_scores, angles)]
    y_coords = [r * math.sin(angle) for r, angle in zip(normalized_scores, angles)]
    
    # Apply shoelace formula
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += x_coords[i] * y_coords[j]
        area -= x_coords[j] * y_coords[i]
    
    area = abs(area) / 2.0
    return area

def calculate_max_possible_area(num_sections):
    """Calculate the maximum possible area for a regular polygon with n sides and radius 1"""
    # For a regular n-sided polygon with radius 1, the area is:
    # A = (n/2) * sin(2π/n)
    return (num_sections / 2.0) * math.sin(2 * math.pi / num_sections)

def normalize_section_scores(section_scores, categories):
    """Normalize each section score to 0-1 range"""
    normalized_scores = []
    labels = []
    
    for i, (cat, (weight, num, bonus_frac)) in enumerate(categories.items()):
        raw_score = section_scores[i]
        max_possible = calculate_max_possible_score(weight, num, bonus_frac)
        
        # Min-Max normalization to [0,1]
        normalized = raw_score / max_possible if max_possible > 0 else 0
        normalized_scores.append(normalized)
        labels.append(cat)
    
    return normalized_scores, labels

def compute_section_scores_normalized(yes_counts, categories):
    """Compute raw scores then normalize them"""
    section_scores = []
    labels = []
    
    for cat, (weight, num, bonus_frac) in categories.items():
        yes = yes_counts.get(cat, 0)
        subtotal = weight * yes
        
        # Check for bonus
        if bonus_frac > 0 and yes >= (2/3 * num):
            bonus = bonus_frac * (weight * num)
        else:
            bonus = 0
        
        section_score = subtotal + bonus
        section_scores.append(section_score)
        labels.append(cat)
    
    # Normalize the scores
    normalized_scores, labels = normalize_section_scores(section_scores, categories)
    
    return normalized_scores, labels, section_scores

def display_normalized_radar(normalized_scores, labels, raw_scores, polygon_area, area_percentage, user_name):
    """Display radar chart with normalized scores and area information"""
    n = len(normalized_scores)
    angles = [2 * math.pi * i / n for i in range(n)]
    angles.append(angles[0])  # Close the circle
    
    values = normalized_scores + [normalized_scores[0]]
    
    fig, ax = plt.subplots(figsize=(10,8), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color=CB_ORANGE, alpha=0.4)
    ax.plot(angles, values, color=CB_ORANGE, linewidth=2)



    # --- Add blue polygon for levels ---
    # Define which sections belong to each level
    level_sections = [
        ['1A', '1B'],
        ['2A', '2B'],
        ['3A', '3B', '3C'],
        ['4A', '4B'],
        ['5A', '5B']
    ]
    # Calculate average normalized score for each level
    score_by_label = dict(zip(labels, normalized_scores))
    level_avgs = [sum(score_by_label[sec] for sec in group)/len(group) for group in level_sections]

    # Calculate blue polygon area and percentage
    polygon_area_blue = calculate_polygon_area(level_avgs)
    max_possible_area_blue = calculate_max_possible_area(len(level_avgs))
    area_percentage_blue = (polygon_area_blue / max_possible_area_blue) * 100

    # Prepare angles for levels (evenly spaced)
    n_levels = len(level_avgs)
    level_angles = [2 * math.pi * i / n_levels for i in range(n_levels)]
    level_angles.append(level_angles[0])
    level_values = level_avgs + [level_avgs[0]]
    # Plot blue polygon
    ax.fill(level_angles, level_values, color=CB_BLUE, alpha=0.3, label='Level Averages')
    ax.plot(level_angles, level_values, color=CB_BLUE, linewidth=2)

    # --- End blue polygon addition ---


  

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)  # Set consistent scale

    today = datetime.date.today().strftime("%d-%m-%Y")
    ax.set_title(f"{user_name}\n Date d-m-y: {today}\n Normalized Antisemitic Risk Assessment\n(Each axis: 0=No Risk, 1=Maximum Risk)\n Red Polygon Area: {polygon_area:.3f} sq units ({area_percentage:.3f}% of max)")
    
    # Add grid lines for better readability
    ax.grid(True)
    ax.set_yticks([0.1, 0.2,0.3, 0.4, 0.5, 0.6,0.7, 0.8,0.9, 1.0])
    ax.set_yticklabels(['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

    # Remove the default yticklabels
    ax.set_yticklabels([])

    # Custom staggered ytick labels
    yticks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    yticklabels = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
    for i, (ytick, label) in enumerate(zip(yticks, yticklabels)):
        # Alternate the angle for offset (e.g., -10 and +10 degrees)
        angle = -5 if i % 2 == 0 else -10
        ax.text(
            math.radians(angle), ytick, label,
            ha='center', va='center', fontsize=8, color='black'
        )

    # --- Add info box under the figure ---

    max_possible_score = sum(
        calculate_max_possible_score(weight, num_questions, bonus_frac)
        for weight, num_questions, bonus_frac in CATEGORIES.values()
    )
    total_yes = sum(yes_counts.values())
    total_questions = sum(num_questions for _, num_questions, _ in CATEGORIES.values())

    positive_percentages = {
    cat: f"{yes_counts[cat]}/{num_questions} ({round(yes_counts[cat]/num_questions*100, 3)}%)"
    for cat, (_, num_questions, _) in CATEGORIES.items()
    }

    max_before_3C = sum(
        calculate_max_possible_score(*CATEGORIES[cat])
        for cat in ['1A', '1B', '2A', '2B', '3A', '3B']
    )

    info = (
        f"Detailed evaluation (Orange):\n"
        f"Normalized scores of sections: {dict(zip(labels, [f'{round(s*100, 3)}%' for s in normalized_scores]))}\n"        f"Red Polygon area: {polygon_area:.4f} square units\n"
        f"Detailed Risk Exposure(Orange): {area_percentage:.3f}% of maximum possible\n"
        f"Raw total score and max score: {sum(raw_scores):.3f} / {max_possible_score:.3f}\n\n"
        f"Positive answers of total: {total_yes} / {total_questions}\n"
        f"Positive answers per section: {positive_percentages}\n\n"
        f"Pyramid Levels (blue):\n "
        f"Normalized scores of Levels (blue): { {k: f'{round(v, 3)}%' for k, v in levels_score.items()} }\n"        #f"Normalized scores of Levels (blue): {levels_score}\n"
        f"General Risk Exposure(blue): {area_percentage_blue:.3f}% of maximum possible\n"

        f"max severe score before 3C: {max_before_3C}\n"
    )

      # --- Add purple polygon for max risk ---
    # max_before_3C = sum(
    #     calculate_max_possible_score(*CATEGORIES[cat])

   


    score_by_label = dict(zip(labels, normalized_scores))
    raw_by_label = dict(zip(labels, raw_scores))

    # Correct trigger logic: use raw scores
    trigger1 = (raw_by_label['3C'] + raw_by_label['4A']) >= max_before_3C
    trigger2 = any(
        raw_by_label[cat] >= max_before_3C
        for cat in ['4A', '4B', '5A', '5B']
    )

    purple_max = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    purple_max.append(purple_max[0])
    purple_area_max = calculate_polygon_area(purple_max)

    if trigger1 or trigger2:
        purple_values = [0, 0, 0, 0, 0, 0]  # 1A, 1B, 2A, 2B, 3A, 3B
        for cat in ['3C', '4A', '4B', '5A', '5B']:
            purple_values.append(score_by_label[cat])
        purple_values.append(purple_values[0])
        purple_angles = [2 * math.pi * i / len(labels) for i in range(len(labels))]
        purple_angles.append(purple_angles[0])
        ax.fill(purple_angles, purple_values, color=CB_PURPLE, alpha=0.4, label='High Risk Tier')
        ax.plot(purple_angles, purple_values, color=CB_PURPLE, linewidth=2)

        # Calculate purple area and percentage
        purple_area = calculate_polygon_area(purple_values)
        purple_area_pct = (purple_area / purple_area_max) * 100 if purple_area_max > 0 else 0

        info += (
            f"\nHigh Risk Tier (purple):\n"
            f"Polygon area: {purple_area:.4f} sq units\n"
            f"Risk Exposure (purple): {purple_area_pct:.2f}% of max possible for this tier\n"
        )
 
    # --- End purple polygon addition ---

    plt.figtext(0.5, 0.025, info, wrap=True, horizontalalignment='center', fontsize=10, bbox={'facecolor':'white', 'alpha':0.7, 'pad':5})
    # --- End info box addition ---
    
    plt.subplots_adjust(bottom=0.5)  # Increase bottom margin for info box
    plt.tight_layout(rect=[0, 0.22, 1, 1])  # Leave space at the bottom

     # --- Prepare PDF output ---
    safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(" ", "_")
    pdf_filename = f"spiderweb_report_{safe_name}.pdf"

    # Save radar chart (with info box) as first page
    fig.set_size_inches(8.27, 11.69)  # A4 size in inches (width, height)
    plt.subplots_adjust(bottom=0.5)
    plt.tight_layout(rect=[0, 0.22, 1, 1])

    # --- Pie chart of raw scores ---
    fig_pie, ax_pie = plt.subplots(figsize=(8.27, 6))
    wedges, texts, autotexts = ax_pie.pie(
        raw_scores,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*sum(raw_scores))})",
        startangle=90,
        colors=plt.cm.tab20.colors
    )

    # Set smaller font for pie chart percentages
    for autotext in autotexts:
        autotext.set_fontsize(9)  # or any size you prefer


    ax_pie.set_title(f"Raw Score Distribution per Section\n{user_name} ({datetime.date.today().strftime('%d-%m-%Y')})")
    plt.tight_layout()

    # --- Save both figures to the same PDF ---
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig)      # Save radar chart (with info box)
        pdf.savefig(fig_pie)  # Save pie chart

    plt.close(fig)
    plt.close(fig_pie)

     # Save as A4 PDF
    #fig.set_size_inches(8.27, 11.69)  # A4 size in inches (width, height)
   # plt.savefig("spiderweb_report.pdf", format="pdf", bbox_inches="tight")

    # Optionally, still show the plot interactively
    plt.show()
    
    return sum(normalized_scores) / len(normalized_scores)  # Average normalized score

def get_yes_counts_from_user(categories):
    print("Enter the number of 'yes' answers for each section (max shown):")
    yes_counts = {}
    for cat, (_, num_questions, _) in categories.items():
        while True:
            try:
                value = int(input(f"{cat} (max {num_questions}): "))
                if 0 <= value <= num_questions:
                    yes_counts[cat] = value
                    break
                else:
                    print(f"Please enter a value between 0 and {num_questions}.")
            except ValueError:
                print("Please enter a valid integer.")
    return yes_counts

if __name__ == "__main__":

    user_name = input("Please enter your name: ").strip()



      # Show max questions per section
    print("Max number of questions per section:")
    for cat, (_, num_questions, _) in CATEGORIES.items():
        print(f"{cat}: {num_questions}")

    # Get user input
    yes_counts = get_yes_counts_from_user(CATEGORIES)



    # Example usage
    #yes_counts = {
    #    '1A': 0, '1B': 0, '2A': 0, '2B': 0, '3A': 0,
    #    '3B': 0, '3C': 0, '4A': 0, '4B': 0, '5A': 0, '5B': 17
    #}

    normalized_scores, labels, raw_scores = compute_section_scores_normalized(yes_counts, CATEGORIES)

    # Calculate polygon area
    polygon_area = calculate_polygon_area(normalized_scores)
    max_possible_area = calculate_max_possible_area(len(normalized_scores))
    area_percentage = (polygon_area / max_possible_area) * 100

    # Map section labels to their raw scores for easy lookup
    score_by_label = dict(zip(labels, normalized_scores))

    levels_score = {
        '1': (score_by_label['1A'] + score_by_label['1B'])*50,
        '2': (score_by_label['2A'] + score_by_label['2B'])*50,
        '3': (score_by_label['3A'] + score_by_label['3B'] + score_by_label['3C'])*(100/3),
        '4': (score_by_label['4A'] + score_by_label['4B'])*50,
        '5': (score_by_label['5A'] + score_by_label['5B'])* 50
    }

    avg_normalized_score = display_normalized_radar(normalized_scores, labels, raw_scores, polygon_area, area_percentage, user_name)

