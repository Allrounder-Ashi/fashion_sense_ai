
import sys

# ---------------- PART 1: KNOWLEDGE BASE ------------------
STYLES = ["Casual", "Streetwear", "Formal", "Minimal", "Ethnic", "Sporty"]
OCCASIONS = ["College", "Office", "Party", "Wedding/Festive", "Date", "Casual Outing", "Gym/Sports"]
WEATHERS = ["Summer", "Monsoon", "Winter", "Spring/Autumn"]
TYPES = ["Western", "Ethnic", "Fusion"]
FITS = ["Relaxed", "Regular", "Slim"]
ACCESSORIES = ["Minimal", "Moderate", "Statement"]
AGES = ["18-25", "26-35", "36-45", "46+"]

# How dressy is each occasion? (1 = very casual ... 5 = very formal)
FORMALITY = {"College": 2, "Office": 4, "Party": 3, "Wedding/Festive": 5,
             "Date": 3, "Casual Outing": 1, "Gym/Sports": 1}
# How warm should clothes be? (1 = very light ... 10 = very heavy)
WARMTH = {"Summer": 2, "Monsoon": 4, "Winter": 8, "Spring/Autumn": 5}

# How close are two styles? (1.0 = same). Pairs not listed count as 0.0
STYLE_CLOSE = {("Casual", "Streetwear"): 0.7, ("Casual", "Minimal"): 0.7,
    ("Casual", "Sporty"): 0.5, ("Casual", "Formal"): 0.3, ("Casual", "Ethnic"): 0.3,
    ("Streetwear", "Sporty"): 0.7, ("Streetwear", "Minimal"): 0.5,
    ("Streetwear", "Formal"): 0.1, ("Streetwear", "Ethnic"): 0.2,
    ("Formal", "Minimal"): 0.7, ("Formal", "Ethnic"): 0.4,
    ("Minimal", "Sporty"): 0.4, ("Minimal", "Ethnic"): 0.3}

def style_match(a, b):
    if a == b:
        return 1.0
    return STYLE_CLOSE.get((a, b), STYLE_CLOSE.get((b, a), 0.0))

# Outfit = name, style, type, fit, formality, warmth, colours, accessories, trend, items, rain_friendly
OUTFIT_DATA = [
 ("Casual Chic", "Casual", "Western", "Relaxed", 2, 2, ["white", "blue"], "Minimal", 0.8,
  [("white oversized shirt", 500), ("blue straight-fit jeans", 800), ("white sneakers", 700)]),
 ("Minimal Streetwear", "Streetwear", "Western", "Relaxed", 1, 2, ["black", "white", "grey"], "Moderate", 0.9,
  [("graphic t-shirt", 400), ("relaxed-fit trousers", 800), ("sneakers", 700), ("crossbody bag", 400)]),
 ("Summer Kurta Look", "Ethnic", "Ethnic", "Relaxed", 3, 2, ["white", "beige", "blue"], "Minimal", 0.5,
  [("cotton kurta", 700), ("linen pants", 700), ("kolhapuri sandals", 500)]),
 ("Smart Formal", "Formal", "Western", "Regular", 5, 4, ["blue", "black", "grey"], "Minimal", 0.3,
  [("light-blue formal shirt", 800), ("tailored trousers", 1200), ("leather shoes", 1500)]),
 ("Sporty Comfort", "Sporty", "Western", "Relaxed", 1, 3, ["black", "blue", "grey"], "Moderate", 0.7,
  [("dry-fit t-shirt", 500), ("track pants", 600), ("running shoes", 1200), ("cap", 200)]),
 ("Cozy Layers", "Casual", "Western", "Relaxed", 2, 8, ["black", "grey", "blue"], "Minimal", 0.7,
  [("hoodie", 900), ("straight-fit jeans", 800), ("sneakers", 700), ("beanie", 200)]),
 ("Winter Formal", "Formal", "Western", "Slim", 5, 8, ["black", "grey", "navy"], "Minimal", 0.3,
  [("blazer", 2500), ("formal shirt", 800), ("formal trousers", 1200), ("leather shoes", 1500)]),
 ("Festive Ethnic", "Ethnic", "Ethnic", "Regular", 5, 5, ["maroon", "gold", "cream"], "Statement", 0.4,
  [("silk kurta", 2500), ("churidar", 800), ("mojari shoes", 900)]),
 ("Monsoon Ready", "Casual", "Western", "Relaxed", 2, 4, ["olive", "black", "blue"], "Minimal", 0.6,
  [("quick-dry t-shirt", 400), ("cargo shorts", 600), ("waterproof sneakers", 1200), ("rain jacket", 800)], True),
]
KEYS = ["name", "style", "type", "fit", "formality", "warmth", "colours",
        "accessories", "trend", "items", "rain_friendly"]
OUTFITS = [dict(zip(KEYS, row)) for row in OUTFIT_DATA]   # tuple -> easy dictionary

# ---------------- PART 2: USER INPUT ----------------------
def ask_choice(question, options):
    print("\n" + question)
    for number, option in enumerate(options, 1):
        print(f"  {number}. {option}")
    while True:
        answer = input("Enter choice: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        print(f"  Please type a number from 1 to {len(options)}")

def ask_budget():
    while True:
        digits = "".join(c for c in input("\nBudget for the whole outfit in Rs.: ") if c.isdigit())
        if digits and int(digits) > 0:
            return int(digits)
        print("  Please enter a number greater than 0.")

def ask_list(question):
    text = input("\n" + question + "\n> ")
    return [x.strip().lower() for x in text.split(",") if x.strip()]

def get_user_details():
    user = {}
    user["age"] = ask_choice("Age group:", AGES)
    user["style"] = ask_choice("Preferred style:", STYLES)
    user["occasion"] = ask_choice("Occasion:", OCCASIONS)
    user["weather"] = ask_choice("Weather / season:", WEATHERS)
    user["colours"] = ask_list("Favourite colours (example: black, white, blue):")
    user["type"] = ask_choice("Outfit preference:", TYPES)
    user["fit"] = ask_choice("Fit preference:", FITS)
    user["budget"] = ask_budget()
    user["accessories"] = ask_choice("Accessories preference:", ACCESSORIES)
    user["owned"] = ask_list("Clothes you ALREADY own (example: sneakers, jeans) or press Enter:")
    return user

DEMO_USER = {"age": "18-25", "style": "Casual", "occasion": "College", "weather": "Summer",
             "colours": ["black", "white", "blue"], "type": "Western", "fit": "Relaxed",
             "budget": 2000, "accessories": "Minimal", "owned": ["sneakers"]}

def user_owns(item_name, owned):
    return any(word in item_name.lower() for word in owned)

# ---------------- PART 3: IF-THEN RULES -------------------
# IF (something is true) THEN (outfit is good / bad).
# Each rule has a CF number: positive = good idea, negative = bad idea.
def check_rules(u, o):
    fired = []
    def fire(rule_id, meaning, cf):
        fired.append((rule_id, meaning, cf))
    occ, wea, warm, formal = u["occasion"], u["weather"], o["warmth"], o["formality"]
    formal_day = occ in ("Office", "Wedding/Festive")
    low_budget = u["budget"] <= 1500
    if occ == "College" and wea == "Summer" and warm <= 3:
        fire("R1", "College in summer -> prefer light, breathable clothes", 0.6)
    if formal_day and formal >= 4: fire("R2", "Office / wedding -> prefer smart outfits", 0.7)
    if formal_day and formal <= 2: fire("R3", "Office / wedding -> avoid very casual outfits", -0.8)
    if occ == "Gym/Sports" and o["style"] != "Sporty": fire("R4", "Gym -> avoid non-sporty outfits", -0.7)
    if u["fit"] == o["fit"]: fire("R5", "Outfit fit matches the fit you like", 0.5)
    if {u["fit"], o["fit"]} == {"Relaxed", "Slim"}: fire("R6", "Relaxed and slim fits clash", -0.6)
    if wea == "Winter" and warm >= 7: fire("R7", "Winter -> prefer warm layers", 0.6)
    if wea == "Winter" and warm <= 4: fire("R8", "Winter -> avoid light clothing", -0.8)
    if wea == "Summer" and warm >= 6: fire("R9", "Summer -> avoid heavy clothing", -0.8)
    if wea == "Monsoon" and o.get("rain_friendly"): fire("R10", "Monsoon -> prefer rain-friendly outfits", 0.6)
    if low_budget and o["cost"] > u["budget"]: fire("R11", "Low budget and outfit costs too much", -0.7)
    if low_budget and o["owned_count"] >= 2: fire("R12", "Low budget -> prefer clothes you already own", 0.5)
    if u["type"] == o["type"]: fire("R13", "Outfit type matches your choice", 0.5)
    if u["type"] != o["type"] and "Fusion" not in (u["type"], o["type"]):
        fire("R14", "Outfit type is different from your choice", -0.5)
    if u["accessories"] == "Minimal" and o["accessories"] == "Statement":
        fire("R15", "You like minimal accessories -> avoid statement pieces", -0.4)
    if u["age"] == "18-25" and o["trend"] >= 0.7: fire("R16", "Age 18-25 -> prefer trendy outfits", 0.3)
    return fired

# ---------------- PART 4: CERTAINTY FACTOR ----------------
# Many rules can fire for one outfit. We mix their CF numbers into
# ONE number using the formula of the MYCIN expert system.
def mix_cf(a, b):
    if a >= 0 and b >= 0:                  # both say good -> belief grows
        return a + b * (1 - a)
    if a < 0 and b < 0:                    # both say bad -> doubt grows
        return a + b * (1 + a)
    return (a + b) / (1 - min(abs(a), abs(b)))   # they pull against each other

# ---------------- PART 5: FUZZY LOGIC ---------------------
# Not just YES / NO, but "how much?" from 0 (no match) to 1 (perfect).
def closeness(value, ideal, spread):
    return max(0, 1 - abs(value - ideal) / spread)

def budget_score(cost, budget):
    if cost <= budget:
        return 1.0
    return max(0, 1 - (cost - budget) / (budget * 0.3))

def colour_score(user_colours, outfit_colours):
    if not user_colours:
        return 0.5                         # user did not say -> neutral
    matches = sum(1 for c in user_colours if c in outfit_colours)
    return min(1.0, matches / min(2, len(user_colours)))

def fuzzy_word(degree):
    if degree >= 0.8: return "excellent"
    if degree >= 0.5: return "good"
    if degree >= 0.25: return "partial"
    return "poor"

# ---------------- INFERENCE ENGINE ------------------------
# Uses the facts + rules to work out numbers for every outfit.
def analyse_all_outfits(u):
    results = []
    for original in OUTFITS:
        o = dict(original)                 # copy, so the original stays safe
        o["cost"] = sum(p for n, p in o["items"] if not user_owns(n, u["owned"]))
        o["owned_count"] = sum(1 for n, p in o["items"] if user_owns(n, u["owned"]))
        o["fired"] = check_rules(u, o)     # IF-THEN rules
        o["cf"] = 0.0
        for rule_id, meaning, cf in o["fired"]:
            o["cf"] = mix_cf(o["cf"], cf)
        o["style_fit"] = style_match(u["style"], o["style"])      # fuzzy scores
        o["occasion_fit"] = closeness(o["formality"], FORMALITY[u["occasion"]], 2.5)
        o["weather_fit"] = closeness(o["warmth"], WARMTH[u["weather"]], 4.0)
        o["colour_fit"] = colour_score(u["colours"], o["colours"])
        o["budget_fit"] = budget_score(o["cost"], u["budget"])
        o["score"] = make_score(o)
        results.append(o)
    return results

# ---------------- PART 6: HEURISTIC SCORE -----------------
# A smart rule of thumb: add up small scores, important ones weigh more.
def make_score(o):
    rules_part = (o["cf"] + 1) / 2         # change -1..1 into 0..1
    total = (0.20 * o["style_fit"] + 0.20 * o["occasion_fit"] + 0.15 * o["weather_fit"]
             + 0.15 * o["colour_fit"] + 0.15 * o["budget_fit"] + 0.15 * rules_part)
    return round(total * 100)

def pick_best(results, u, how_many=3):
    good = [o for o in results if o["cf"] > -0.5 and o["budget_fit"] > 0]
    rejected = len(results) - len(good)
    if good:
        good.sort(key=lambda o: o["score"], reverse=True)
        return good[:how_many], rejected, True
    # Nothing suitable (e.g. tiny budget): show the closest outfits,
    # losing points for being over budget.
    results.sort(key=lambda o: o["score"] - 20 * max(0, o["cost"] - u["budget"]) / u["budget"],
                 reverse=True)
    return results[:how_many], rejected, False

# ---------------- PART 7: EXPLAINABLE AI ------------------
# Explain WHY an outfit was chosen.
def explain(o, u):
    reasons, cautions = [], []
    for rule_id, meaning, cf in o["fired"]:
        line = f"{meaning} (rule {rule_id}, CF {cf:+.2f})"
        (reasons if cf > 0 else cautions).append(line)
    for label, key in [(f"Style match with '{u['style']}'", "style_fit"),
                       (f"Right for the {u['occasion']} occasion", "occasion_fit"),
                       (f"Comfort in {u['weather']} weather", "weather_fit"),
                       ("Matches your favourite colours", "colour_fit")]:
        reasons.append(f"{label}: {fuzzy_word(o[key])} ({o[key]:.2f})")
    if o["cost"] <= u["budget"]:
        reasons.append(f"Within budget: you spend Rs. {o['cost']} (budget Rs. {u['budget']})")
    else:
        cautions.append(f"Over your budget by Rs. {o['cost'] - u['budget']}")
    return reasons, cautions

# ---------------- PART 8: PERSONAL TIPS -------------------
ACC_TIPS = {"Minimal": "Keep it simple: a watch or a thin band is enough.",
            "Moderate": "Add one or two pieces: a watch plus a bag or cap.",
            "Statement": "Go bold: statement jewellery or sunglasses."}
WEATHER_TIPS = {"Summer": "Choose cotton or linen and carry sunglasses.",
                "Monsoon": "Carry an umbrella and avoid light-coloured bottoms.",
                "Winter": "Layer up with a jacket or scarf.",
                "Spring/Autumn": "Carry a light layer for cooler evenings."}

def make_tips(o, u):
    tips = []
    missing = [c for c in u["colours"] if c not in o["colours"]]
    if missing:
        tips.append(f"Colour twist: try the main top in {missing[0]}.")
    tips += [ACC_TIPS[u["accessories"]], WEATHER_TIPS[u["weather"]]]
    have = [(n, p) for n, p in o["items"] if user_owns(n, u["owned"])]
    need = [(n, p) for n, p in o["items"] if not user_owns(n, u["owned"])]
    if have:
        tips.append("You already own: " + ", ".join(n for n, p in have)
                    + f" (saves Rs. {sum(p for n, p in have)}).")
    if need:
        tips.append("You need to buy: " + ", ".join(f"{n} (Rs. {p})" for n, p in need))
    return tips

# ---------------- PART 9: MAIN ----------------------------
def heading(title, subtitle=""):
    print("\n" + "=" * 40 + "\n" + title.center(40))
    if subtitle:
        print(subtitle.center(40))
    print("=" * 40)

def show_everything(u, top, rejected, found_good):
    heading("FASHION PROFILE CREATED SUCCESSFULLY")
    print(f"\nAge: {u['age']} | Style: {u['style']} | Occasion: {u['occasion']} | Weather: {u['weather']}")
    print(f"Type: {u['type']} | Fit: {u['fit']} | Budget: Rs. {u['budget']} | Accessories: {u['accessories']}")
    print("Colours:", ", ".join(u["colours"]) or "no preference")
    print("Already owned:", ", ".join(u["owned"]) or "none")
    heading("AI OUTFIT RECOMMENDATIONS")
    print(f"The AI rejected {rejected} unsuitable outfit(s).")
    if not found_good:
        print("Note: nothing matched all your needs well, so these are the closest.")
    for rank, o in enumerate(top, 1):
        reasons, cautions = explain(o, u)
        print(f"\n{rank}. {o['name'].upper()}")
        print(f"Compatibility Score: {o['score']}/100  (rule certainty {o['cf']:+.2f})\n\nOutfit:")
        for name, price in o["items"]:
            print(f"- {name} - Rs. {price}" + (" (owned)" if user_owns(name, u["owned"]) else ""))
        print("\nWhy recommended:")
        print("\n".join("- " + line for line in reasons))
        if cautions:
            print("\nThings to think about:")
            print("\n".join("- " + line for line in cautions))
    heading("PERSONALIZED STYLE ANALYSIS")
    print(f"Your best match: {top[0]['name']} ({top[0]['score']}/100)\n")
    print("\n".join("- " + tip for tip in make_tips(top[0], u)))
    print("\nAnalysis completed successfully!")

def main():
    heading("STYLESENSE AI", "Your Personal Fashion Advisor")
    if "--demo" in sys.argv:
        user = dict(DEMO_USER)
        print("(demo mode: using a ready-made sample user)")
    else:
        user = get_user_details()                         # step 1: ask
    results = analyse_all_outfits(user)                   # step 2: think
    top, rejected, found_good = pick_best(results, user)  # step 3: choose
    show_everything(user, top, rejected, found_good)      # step 4: explain

if __name__ == "__main__":
    main()