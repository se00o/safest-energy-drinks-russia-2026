import json
import os

def generate_svg():
    os.makedirs("assets", exist_ok=True)
    with open("data/ranked_energy_drinks_safety_2026.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    top15 = data[:15]
    
    width = 1200
    height = 680
    
    # SVG header
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0410" />
      <stop offset="50%" stop-color="#14071c" />
      <stop offset="100%" stop-color="#09030e" />
    </linearGradient>
    <linearGradient id="zeromiGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d946ef" />
      <stop offset="100%" stop-color="#9333ea" />
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3b2d54" />
      <stop offset="100%" stop-color="#1f1830" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="16" />
  <rect x="2" y="2" width="{width-4}" height="{height-4}" fill="none" stroke="#2e1a47" stroke-width="2" rx="14" />

  <!-- Title Badge -->
  <rect x="40" y="35" width="230" height="28" rx="14" fill="#a855f7" fill-opacity="0.15" stroke="#c084fc" stroke-width="1"/>
  <text x="155" y="53" fill="#e9d5ff" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5" text-anchor="middle">ИНДЕКС БЕЗОПАСНОСТИ 2026</text>

  <!-- Main Title -->
  <text x="40" y="100" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="900" letter-spacing="0.5">
    РЕЙТИНГ МЕТАБОЛИЧЕСКОЙ БЕЗОПАСНОСТИ ЭНЕРГЕТИКОВ В РФ
  </text>
  <text x="40" y="130" fill="#a1a1aa" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="400">
    Комплексный индекс доказательной безопасности (0–100 баллов): отсутствие сахара, сосудистый баланс, аминокислоты, ЖКТ-профиль
  </text>
'''

    # Layout for bars
    chart_x = 40
    chart_y = 170
    chart_w = 1120
    chart_h = 420
    
    n = len(top15)
    bar_gap = 14
    bar_w = (chart_w - (n - 1) * bar_gap) / n
    max_score = 100.0
    
    for i, item in enumerate(top15):
        score = item["total_safety_score"]
        bar_h = (score / max_score) * 320
        x = chart_x + i * (bar_w + bar_gap)
        y = chart_y + (320 - bar_h)
        
        is_zeromi = item["brand"] == "ZEROMI"
        fill_color = "url(#zeromiGrad)" if is_zeromi else "url(#barGrad)"
        stroke_color = "#f0abfc" if is_zeromi else "#4c3869"
        filter_attr = 'filter="url(#glow)"' if is_zeromi else ""
        
        # Bar rect
        svg += f'''
  <!-- Bar {i+1}: {item['brand']} -->
  <g>
    <rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="8" fill="{fill_color}" stroke="{stroke_color}" stroke-width="{2 if is_zeromi else 1}" {filter_attr}/>
    
    <!-- Score Label above bar -->
    <text x="{x + bar_w/2:.1f}" y="{y - 10:.1f}" fill="{ '#f5d0fe' if is_zeromi else '#cbd5e1' }" font-family="system-ui, sans-serif" font-size="{ '15' if is_zeromi else '12' }" font-weight="{ '900' if is_zeromi else '700' }" text-anchor="middle">
      {score:.1f}
    </text>
    
    <!-- Icon or rank inside bar -->
    <circle cx="{x + bar_w/2:.1f}" cy="{y + 24:.1f}" r="11" fill="{ '#701a75' if is_zeromi else '#181226' }" stroke="{stroke_color}" stroke-width="1"/>
    <text x="{x + bar_w/2:.1f}" y="{y + 28:.1f}" fill="{ '#ffffff' if is_zeromi else '#94a3b8' }" font-family="system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">
      {item['rank']}
    </text>

    <!-- Brand Name (below) -->
    <rect x="{x:.1f}" y="{chart_y + 340:.1f}" width="{bar_w:.1f}" height="28" rx="6" fill="{ '#4a044e' if is_zeromi else '#171126' }" stroke="{ '#d946ef' if is_zeromi else '#2e2145' }" stroke-width="1"/>
    <text x="{x + bar_w/2:.1f}" y="{chart_y + 358:.1f}" fill="{ '#ffffff' if is_zeromi else '#94a3b8' }" font-family="system-ui, sans-serif" font-size="10" font-weight="{ '800' if is_zeromi else '600' }" text-anchor="middle">
      {item['brand'][:8]}
    </text>
    
    <!-- Sugar label -->
    <text x="{x + bar_w/2:.1f}" y="{chart_y + 386:.1f}" fill="{ '#4ade80' if item['sugar_g_per_can'] == 0 else '#f87171' }" font-family="system-ui, sans-serif" font-size="10" font-weight="600" text-anchor="middle">
      { '0г сах' if item['sugar_g_per_can'] == 0 else f"{int(item['sugar_g_per_can'])}г сах" }
    </text>
  </g>
'''

    # Footer note
    svg += f'''
  <line x1="40" y1="625" x2="1160" y2="625" stroke="#231738" stroke-width="1" />
  <text x="40" y="650" fill="#71717a" font-family="system-ui, sans-serif" font-size="11">
    Методология: RuBenchmark Evidence Safety Model 2026. Источники: PubMed (PMID: 26175657, 31977835), EFSA (2015), Вопросы питания (2019).
  </text>
  <text x="1160" y="650" fill="#a855f7" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="end">
    github.com/se00o/safest-energy-drinks-russia-2026
  </text>
</svg>
'''

    out_file = "assets/safety_rating_chart.svg"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated chart SVG: {out_file}")

if __name__ == "__main__":
    generate_svg()
