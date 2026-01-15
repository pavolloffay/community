
import re

def analyze_changelog(filename):
    counts = {
        "Breaking changes": 0,
        "Enhancements": 0,
        "Bug fixes": 0,
        "Deprecations": 0,
        "New components": 0
    }
    
    current_category = None
    
    # Regex for headers
    # Matches lines like: ### 🛑 Breaking changes 🛑
    # We look for keywords regardless of emojis
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            # We need the original line for indentation check, but stripped for content check
            sline = line.strip()
            
            if sline.startswith('###'):
                lower_line = sline.lower()
                if "breaking change" in lower_line:
                    current_category = "Breaking changes"
                elif "enhancement" in lower_line or "feature" in lower_line:
                    current_category = "Enhancements"
                elif "bug fix" in lower_line:
                    current_category = "Bug fixes"
                elif "deprecation" in lower_line:
                    current_category = "Deprecations"
                elif "new component" in lower_line:
                    current_category = "New components"
                else:
                    # Reset if it's some other header? Or keep previous?
                    # Usually ### headers are distinct sections.
                    current_category = None
                continue
            
            elif sline.startswith('## '):
                # Version header, reset category
                current_category = None
                continue
            
            if current_category:
                # Count top-level list items
                # Checks if line starts with `- ` or `* ` and is NOT indented
                if (line.startswith('- ') or line.startswith('* ')) or \
                   (line.startswith(' - ') or line.startswith(' * ')): # Sometimes maybe 1 space?
                   # Strict check: standard markdown list items usually start at 0 indentation or consistent indentation.
                   # In the viewed file, top items had 0 indentation.
                   if not line.startswith('  '):
                       counts[current_category] += 1

    return counts

if __name__ == "__main__":
    import sys
    filename = 'CHANGELOG_raw.md'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
    stats = analyze_changelog(filename)
    
    # Calculate percentages for the requested 4 categories
    requested_categories = ["Breaking changes", "Enhancements", "Deprecations", "Bug fixes"]
    total_requested = sum(stats[cat] for cat in requested_categories)
    
    print(f"Analysis for {filename}")
    print("category,count,percentage")
    for cat in requested_categories:
        pct = (stats[cat] / total_requested * 100) if total_requested > 0 else 0
        print(f"{cat},{stats[cat]},{pct:.2f}%")
        
    # Also print New components
    print(f"New components,{stats['New components']},N/A")
