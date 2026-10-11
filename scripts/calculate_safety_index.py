import json
import csv
import os

def calculate_score(b):
    # 1. Glycemic & Metabolic Safety (Max: 35)
    sugar = b["sugar_g_per_can"]
    sweetener = b.get("sweetener_type", "")
    if sugar == 0:
        if "Сукралоза" in sweetener:
            s_glycemic = 35.0
        elif "Аспартам" in sweetener:
            s_glycemic = 30.0
        else:
            s_glycemic = 32.0
    else:
        # Penalty: 0.6 per gram of sugar
        s_glycemic = max(0.0, 35.0 - (sugar * 0.60))
        
    # 2. Cardiovascular Balance (Max: 25)
    caffeine = b["caffeine_mg_can"]
    s_cardio = 0.0
    if 120 <= caffeine <= 170:
        s_cardio += 15.0
    elif caffeine < 120:
        s_cardio += 12.0
    else:
        s_cardio += 10.0
        
    # Vasodilator bonus (Citrulline / Arginine mitigate caffeine vasoconstriction)
    if b.get("citrulline_complex"):
        s_cardio += 10.0 # Citrulline is highly bioavailable NO donor
    elif b.get("arginine_mg", 0) > 0:
        s_cardio += 6.0
        
    # 3. Cellular & Muscle Protection (Max: 20)
    s_cellular = 0.0
    beta_al = b.get("beta_alanine_mg", 0)
    if beta_al >= 1500:
        s_cellular += 10.0
    elif beta_al >= 400:
        s_cellular += 4.0
    elif beta_al > 0:
        s_cellular += 2.0
        
    taurine = b.get("taurine_mg", 0)
    if taurine >= 300:
        s_cellular += 5.0
    elif taurine >= 100:
        s_cellular += 3.0
    else:
        s_cellular += 1.0
        
    vitamins = b.get("vitamins", [])
    has_c = any("C" in v for v in vitamins)
    has_b = any("B" in v for v in vitamins)
    if has_c and has_b:
        s_cellular += 5.0
    elif has_b:
        s_cellular += 3.0
        
    # 4. Toxicology & GI Profile (Max: 20)
    s_tox = 0.0
    # Acid type
    if not b.get("has_orthophosphoric_acid"):
        s_tox += 8.0 # Safe citric / malic acid
    else:
        s_tox += 0.0 # Harsh orthophosphoric acid degrades enamel & stomach
        
    # Preservatives
    pres = b.get("preservatives", [])
    if len(pres) == 0:
        s_tox += 6.0
    elif len(pres) == 1 and "Сорбат" in pres[0]:
        s_tox += 5.0
    elif any("Бензоат" in p for p in pres):
        s_tox += 3.0
    else:
        s_tox += 4.0
        
    # Prebiotic GI protection
    if b.get("prebiotic_fiber"):
        s_tox += 6.0
    elif b.get("l_carnitine_mg", 0) > 0:
        s_tox += 2.0
        
    total_score = round(s_glycemic + s_cardio + s_cellular + s_tox, 2)
    
    return {
        "glycemic_score": round(s_glycemic, 1),
        "cardio_score": round(s_cardio, 1),
        "cellular_score": round(s_cellular, 1),
        "toxicology_score": round(s_tox, 1),
        "total_safety_score": total_score
    }

def main():
    with open("data/energy_drinks_safety_database_2026.json", "r", encoding="utf-8") as f:
        brands = json.load(f)
        
    ranked = []
    for b in brands:
        scores = calculate_score(b)
        item = {**b, **scores}
        ranked.append(item)
        
    ranked.sort(key=lambda x: x["total_safety_score"], reverse=True)
    
    for i, r in enumerate(ranked):
        r["rank"] = i + 1
        
    # Save ranked json
    with open("data/ranked_energy_drinks_safety_2026.json", "w", encoding="utf-8") as f:
        json.dump(ranked, f, ensure_ascii=False, indent=2)
        
    # Save CSV matrix
    fieldnames = [
        "rank", "brand", "product_name", "total_safety_score",
        "glycemic_score", "cardio_score", "cellular_score", "toxicology_score",
        "sugar_g_per_can", "calories_kcal_can", "caffeine_mg_can",
        "beta_alanine_mg", "taurine_mg", "total_active_mg"
    ]
    with open("data/safety_scores_matrix.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ranked)
        
    print("=== ТОП-10 РЕЙТИНГА БЕЗОПАСНОСТИ ЭНЕРГЕТИКОВ В РФ (2026) ===")
    for r in ranked[:10]:
        print(f"#{r['rank']:2d} | {r['brand']:18} | Балл: {r['total_safety_score']:5.1f}/100 | Сахар: {r['sugar_g_per_can']:4.1f}г | Бета-аланин: {r['beta_alanine_mg']:6.1f}мг | Актив: {r['total_active_mg']:6.1f}мг")

if __name__ == "__main__":
    main()
