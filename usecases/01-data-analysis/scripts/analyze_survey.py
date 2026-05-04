import csv
from collections import Counter

CSV_PATH = "../metrics/user-survey-responses.csv"

rows = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['nps_score'] = int(row['nps_score'])
        rows.append(row)

total = len(rows)
nps_scores = [r['nps_score'] for r in rows]
avg_nps = sum(nps_scores) / total
sorted_nps = sorted(nps_scores)
median_nps = sorted_nps[total // 2] if total % 2 else (sorted_nps[total // 2 - 1] + sorted_nps[total // 2]) / 2

print(f"=== ЗАГАЛЬНА СТАТИСТИКА ===")
print(f"Всього респондентів: {total}")
print(f"Середній NPS: {avg_nps:.1f}")
print(f"Медіана NPS: {median_nps:.1f}")
print()

promoters = sum(1 for s in nps_scores if s >= 9)
passives = sum(1 for s in nps_scores if 7 <= s <= 8)
detractors = sum(1 for s in nps_scores if s <= 6)
nps = ((promoters - detractors) / total) * 100

print(f"=== NPS РОЗБИВКА ===")
print(f"Промоутери (9-10): {promoters} ({promoters/total*100:.1f}%)")
print(f"Пасивні (7-8): {passives} ({passives/total*100:.1f}%)")
print(f"Детрактори (0-6): {detractors} ({detractors/total*100:.1f}%)")
print(f"NPS Score: {nps:.1f}")
print()

# Feature requests distribution
print(f"=== РОЗПОДІЛ FEATURE REQUESTS ===")
feature_counter = Counter(r['feature_request'] for r in rows)
for feature, count in feature_counter.most_common():
    pct = count / total * 100
    feature_scores = [r['nps_score'] for r in rows if r['feature_request'] == feature]
    avg = sum(feature_scores) / len(feature_scores)
    print(f"  {feature}: {count} ({pct:.1f}%) | Сер. NPS: {avg:.1f}")
print()

# NPS by feature request (sorted by avg NPS ascending)
print(f"=== NPS ПО FEATURE REQUEST (від найнижчого) ===")
feature_nps = {}
for r in rows:
    feat = r['feature_request']
    if feat not in feature_nps:
        feature_nps[feat] = []
    feature_nps[feat].append(r['nps_score'])

sorted_features = sorted(feature_nps.items(), key=lambda x: sum(x[1]) / len(x[1]))
for feat, scores in sorted_features:
    print(f"  {feat}: avg NPS={sum(scores)/len(scores):.1f}, n={len(scores)}")
print()

# Confusion themes
print(f"=== ТОП ПРОБЛЕМ ПРИ ОНБОРДИНГУ ===")
theme_keywords = {
    "Не знав що робити далі / чекліст": ["checklist", "next action", "next step", "what to do next", "guided path", "first step", "missed a step", "supposed to do"],
    "Потрібні приклади/шаблони": ["example", "prefilled", "template", "copy a typical", "blank screen", "what to enter", "hesitated"],
    "Не зрозумів як годувати": ["feeding", "portions", "daily grams", "split portions", "wet and dry", "multi-food", "too much or too little"],
    "Безпека їжі": ["dangerous", "safe food", "ingredient", "evaluate food", "can my pet eat", "refuses food", "foods are dangerous"],
    "Втрата документів / ветпаспорт": ["paper", "upload", "scan", "PDF", "vet documents", "vaccination dates", "vet reports"],
    "Екстрена допомога / клініки": ["SOS", "urgent", "panicked", "googled scary", "24/7", "clinic", "reviews"],
    "QR-код / загублення тварини": ["lost", "QR", "found pet"],
    "Спільнота": ["community", "owner experiences", "share pet moments", "other owners", "without judgment", "groups"],
    "Спільне ведення господарства": ["share access", "partner", "split responsibilities", "coordinate", "double-fed", "shared log", "did you feed"],
    "Інтеграції з девайсами": ["gadgets", "devices", "connect", "switching apps"],
}

confusion_themes = {}
for theme, keywords in theme_keywords.items():
    count = 0
    for r in rows:
        confusion = r['confusion_during_onboarding'].lower()
        if any(kw.lower() in confusion for kw in keywords):
            count += 1
    if count > 0:
        confusion_themes[theme] = count

sorted_themes = sorted(confusion_themes.items(), key=lambda x: x[1], reverse=True)
for theme, count in sorted_themes:
    pct = count / total * 100
    print(f"  {theme}: {count} ({pct:.1f}%)")
