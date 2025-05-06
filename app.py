from flask import Flask, render_template, session, redirect, url_for, Response, request, jsonify
from markupsafe import Markup
import re
import os
app = Flask(__name__)

# Set up the secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")
app.jinja_env.globals.update(enumerate=enumerate)

varietals = ["riesling", "sauvignon_blanc", "chardonnay", "pinot_noir", "cabernet_sauvignon"]
TOTAL_VARIETALS = len(varietals)

def format_bold_text(text):
    # Convert **bold** to <strong>bold</strong>
    def boldify(s):
        return Markup(re.sub(r"\*\*(.*?)\*\*", r"<strong class='highlighted-text'>\1</strong>", s))

    if isinstance(text, list):
        return [boldify(item) for item in text]
    else:
        return boldify(text)

varietal_data = {
    "riesling": {
        "location": "Crystal Lakes of Riesling",
        "title": "Welcome to the **Crystal Lakes of Riesling**",
        "descriptions": ["Riesling is **light**, **aromatic**, and often **slightly sweet**.", "Think **zippy acidity**, **juicy fruit**, and **floral aromas**.", "It's refreshing and expressive—perfect for those who like a little personality in their glass."],
        "varietal": "Riesling",
        "varietal_url": "riesling",
        "activities": {
            1: {
                "hint": "Riesling is **never heavy or brooding**. Think **juicy fruits**, **fresh blooms**, and **zippy citrus**.",
                "hint_short": "Think **juicy fruits**, **fresh blooms**, and **zippy citrus**.",
                "note_options": ["lemon", "lime", "mushroom", "pineapple", "grass", "cedar", "apricot", "vanilla"],
                "correct_notes": ["lemon", "lime", "pineapple", "apricot"],
            },
            2: {
                "hint": "This wine is typically **pale straw to light gold**.",
                "hint_short": "This wine is typically **pale straw to light gold**.",
                "color_options": ["#F9F6D2", "#FAE1DC", "#ffbf6b", "#d42c48"],
                "correct_index": 0
            },
            3: {
                "hint": "Think **spicy food**, **light meats**, and **citrusy dishes**!",
                "hint_short": "Riesling shines with **spicy**, **sweet**, and **tangy dishes**."
            }
        }
    },
    "sauvignon_blanc": {
        "location": "Valley of Sauvignon Blanc",
        "title": "Welcome to the **Valley of Sauvignon Blanc**",
        "descriptions": ["Sauvignon Blanc is fresh, green, and unapologetically zesty.", "Known for its high acidity and bold aromatics, this wine brings to mind citrus groves, cut grass, and cool ocean breezes.", "It's sharp, sassy, and always refreshing."],
        "varietal": "Sauvignon Blanc",
        "varietal_url": "sauvignon_blanc",
        "descriptions": ["Sauvignon Blanc is **fresh**, **green**, and unapologetically **zesty**.", "Known for its **high acidity** and **bold aromatics**, this wine brings to mind **citrus groves**, **cut grass**, and cool **ocean breezes**.", "It's **sharp**, **sassy**, and **always refreshing**."],
        "activities": {
            1: {
                "hint": "Known for its **high acidity** and **bold aromatics**, this wine brings to mind **citrus** groves, cut **grass**, and cool **ocean breezes**. Picture **green herbs**, **tropical** bursts, and a splash of **sharp citrus**.",
                "hint_short": "Picture **green herbs**, **tropical bursts**, and a splash of **sharp citrus**.",
                "note_options": ["grapefruit", "passionfruit", "leather", "apricot", "grass", "blackberry", "gooseberry", "vanilla"],
                "correct_notes": ["grapefruit", "passionfruit", "gooseberry", "grass"],
            },
            2: {
                "hint": "This wine is typically **pale straw with greenish glints**.",
                "hint_short": "This wine is typically **pale straw with greenish glints**.",
                "color_options": ["#FFE3B3", "#e3747f", "#F4FCD9", "#ffbf6b"],
                "correct_index": 2
            },
            3: {
                "hint": "Sauvignon Blanc is perfect with **fresh**, **zesty**, and **herbaceous** dishes.",
                "hint_short": "Sauvignon Blanc is perfect with **fresh**, **zesty**, and **herbaceous** dishes."
            }
        }
    },
    "chardonnay": {
        "location": "Golden Hills of Chardonnay",
        "title": "Welcome to the **Golden Hills of Chardonnay**",
        "descriptions": ["Chardonnay is **smooth**, **versatile**, and effortlessly **elegant**.", "Think ripe **pear**, creamy **vanilla**, and a hint of **toasted oak**.", "It's **rich yet balanced**—great for those who enjoy a little luxury in every sip."],
        "varietal": "Chardonnay",
        "varietal_url": "chardonnay",
        "activities": {
            1: {
                "hint": "Think ripe pear, creamy vanilla, and a hint of toasted oak.",
                "hint_short": "Think ripe pear, creamy vanilla, and a hint of toasted oak.",
                "note_options": ["green_apple", "butter", "bell_pepper", "pineapple", "licorice", "toasted_almond", "black_pepper", "vanilla"],
                "correct_notes": ["green_apple", "butter", "toasted_almond", "vanilla"],
            },
            2: {
                "hint": "This wine ranges from **pale gold to rich, buttery yellow**.",
                "hint_short": "This wine ranges from **pale gold to rich, buttery yellow**.",
                "color_options": ["#F4FCD9", "#e3747f", "#C9D4A5", "#E3DB94"],
                "correct_index": 3,
            },
            3: {
                "hint": "Chardonnay pairs wonderfully with **rich**, **creamy**, and **buttery** foods.",
                "hint_short": "Chardonnay pairs wonderfully with **rich**, **creamy**, and **buttery** foods."
            }
        }
    },
    "pinot_noir": {
        "location": "Forest of Pinot Noir",
        "title": "Welcome to the **Forest of Pinot Noir**",
        "descriptions": ["Pinot Noir is **delicate**, **earthy**, and quietly **complex**.", "Think ripe **cherry**, **soft spice**, and subtle **floral** notes.", "It's graceful and layered—perfect for those who appreciate a softer kind of depth."],
        "varietal": "Pinot Noir",
        "varietal_url": "pinot_noir",
        "activities": {
            1: {
                "hint": "Pinot Noir is **delicate**, **earthy**, and quietly **complex**. Think **soft spice** and subtle **floral** notes.",
                "hint_short": "Think **soft spice** and subtle **floral** notes.",
                "note_options": ["cherry", "vanilla", "raspberry", "mushroom", "butter", "blackberry", "clove", "cinnamon"],
                "correct_notes": ["cherry", "clove", "raspberry", "mushroom"],
            },
            2: {
                "hint": "This wine is typically **light ruby to translucent garnet**.",
                "hint_short": "This wine is typically **light ruby to translucent garnet**.",
                "color_options": ["#E3DB94", "#d49299", "#A42C2C", "#781F1F"],
                "correct_index": 2
            },
            3: {
                "hint": "Pinot Noir is a great match for **earthy**, **savory**, and subtly **spiced** dishes.",
                "hint_short": "Pinot Noir is a great match for **earthy**, **savory**, and subtly **spiced** dishes."
            }
        }
    },
    "cabernet_sauvignon": {
        "location": "Caverns of Cabernet Sauvignon",
        "title": "Welcome to the **Caverns of Cabernet Sauvignon**",
        "descriptions": ["Cabernet Sauvignon is **bold**, **structured**, and unapologetically **full-bodied**.", "Think **blackcurrant**, **tobacco**, and a whisper of **cedar**.", "It's powerful and intense—for those who like their wines with serious presence."],
        "varietal": "Cabernet Sauvignon",
        "varietal_url": "cabernet_sauvignon",
        "activities": {
            1: {
                "hint": "Cabernet Sauvignon is **bold**, **structured**, and unapologetically **full-bodied**. Think **dark berries**, **dried leaves**, and a touch of **wood** and **smoke**.",
                "hint_short": "Think **dark berries**, **dried leaves**, and the **fireplace**.",
                "note_options": ["tobacco", "butter", "peach", "black_currant", "cedar", "vanilla", "grass", "blackberry"],
                "correct_notes": ["black_currant", "blackberry", "tobacco", "cedar"],
            },
            2: {
                "hint": "This wine is **deep ruby to inky purple**, often nearly opaque.",
                "hint_short": "This wine is **deep ruby to inky purple**, often nearly opaque.",
                "color_options": ["#F4FCD9", "#d49299", "#4B0F1C", "#9F1D35"],
                "correct_index": 2
            },
            3: {
                "hint": "Cabernet Sauvignon complements **hearty**, **grilled**, and **bold-flavored** meals.",
                "hint_short": "Cabernet Sauvignon complements **hearty**, **grilled**, and **bold-flavored** meals."
            }
        }
    }
}

activities = {
    1: {
        "name": "Drag and Drop the Notes",
        "button": "Start Dragging & Dropping",
        "instructions": "**Drag and drop** the notes that feel like {{ varietal_name }} to the wine glass. Avoid anything that doesn't match the vibe."
    },
    2: {
        "name": "Color the Correct Glass",
        "button": "Start Coloring",
        "instructions": "Which color looks most like a glass of {{ varietal_name }}?"
    },
    3: {
        "name": "Right Pair, Right Swipe?",
        "button": "Start Swiping",
        "instructions": "Use your arrow keys to swipe left or right on each food item to guess whether it pairs well with {{ varietal_name }}."
    }
}

activity3 = {
    "riesling": [{
            "image": "apple_tart.png",
            "correct_answer": "good",
            "explanation": "The crisp sweetness of Riesling complements the fruitiness of the tart."
        }, {
            "image": "steak.png",
            "correct_answer": "meh",
            "explanation": "The tannins in steak can clash with the sweetness and acidity of Riesling."
        }, {
            "image": "blue_cheese.png",
            "correct_answer": "meh",
            "explanation": "The bold, tangy flavors of blue cheese can overwhelm the more subtle qualities of Riesling."
        }, {
            "image": "thai_curry.png",
            "correct_answer": "good",
            "explanation": "Riesling's sweetness balances the heat and spiciness of the curry."
        }, {
            "image": "brie_cheese.png",
            "correct_answer": "good",
            "explanation": "Riesling's acidity cuts through the richness of the cheese, enhancing the flavor."
        }, {
            "image": "pickles.png",
            "correct_answer": "meh",
            "explanation": "The acidity of pickles may overpower the delicate flavors of Riesling."
    }], "sauvignon_blanc": [{
        "image": "tomato_pasta.png",
        "correct_answer": "meh",
        "explanation": "Tomato-heavy sauces like marinara clash with the acidity of Sauvignon Blanc."
    }, {
        "image": "goat_cheese.png",
        "correct_answer": "good",
        "explanation": "The tangy, creamy goat cheese pairs perfectly with the crisp acidity of Sauvignon Blanc."
    }, {
        "image": "dark_chocolate.png",
        "correct_answer": "meh",
        "explanation": "The bitterness of dark chocolate doesn't complement Sauvignon Blanc's acidity and grassy flavors."
    }, {
        "image": "green_vegetables.png",
        "correct_answer": "good",
        "explanation": "The wine's bright acidity complements the earthy flavors of green vegetables like grilled asparagus."
    }, {
        "image": "lemon_herb_chicken.png",
        "correct_answer": "good",
        "explanation": "The citrus notes in the wine enhance the lemony flavors of the chicken."
    }, {
        "image": "cream_pasta.png",
        "correct_answer": "meh",
        "explanation": "The richness of cream pasta dishes can overwhelm the freshness of Sauvignon Blanc."
    }], "chardonnay": [{
        "image": "grilled_salmon.png",
        "correct_answer": "good",
        "explanation": "The wine’s creamy texture and moderate acidity complement the rich flavor of grilled salmon."
    }, {
        "image": "pickles.png",
        "correct_answer": "meh",
        "explanation": "The sharp acidity of pickles clashes with Chardonnay's rounder, buttery profile."
    }, {
        "image": "lobster_butter.png",
        "correct_answer": "good",
        "explanation": "Buttery lobster highlights the full-bodied richness of Chardonnay beautifully."
    }, {
        "image": "blue_cheese.png",
        "correct_answer": "meh",
        "explanation": "Strong blue cheese overpowers the subtler flavors of Chardonnay."
    }, {
        "image": "cream_pasta.png",
        "correct_answer": "good",
        "explanation": "Cream sauces like creamy alfredo sauce pair well with Chardonnay's texture and mild oak influence."
    }, {
        "image": "spicy_mexican_food.png",
        "correct_answer": "meh",
        "explanation": "Spicy Mexican food can amplify the alcohol and overshadow Chardonnay's balance."
    }], "pinot_noir": [{
        "image": "grilled_salmon.png",
        "correct_answer": "good",
        "explanation": "Pinot Noir's light body and fruitiness work well with the richness of salmon."
    }, {
        "image": "spicy_mexican_food.png",
        "correct_answer": "meh",
        "explanation": "Spicy foods can overwhelm Pinot Noir's delicate flavor profile."
    }, {
        "image": "roast_chicken.png",
        "correct_answer": "good",
        "explanation": "Pinot Noir's earthiness and acidity match the savory notes in roasted chicken."
    }, {
        "image": "sushi.png",
        "correct_answer": "meh",
        "explanation": "The light, delicate flavor of sushi doesn't stand up to the complexity of Pinot Noir."
    }, {
        "image": "mushroom_risotto.png",
        "correct_answer": "good",
        "explanation": "Earthy mushrooms bring out Pinot Noir's subtle, savory depth."
    }, {
        "image": "thai_curry.png",
        "correct_answer": "meh",
        "explanation": "The intense spice of Thai curry clashes with Pinot Noir's gentle structure."
    }
    ], "cabernet_sauvignon": [{
        "image": "shrimp_scampi.png",
        "correct_answer": "meh",
        "explanation": "Shrimp scampi’s delicate flavors are overwhelmed by the bold intensity of Cabernet."
    }, {
        "image": "ribeye_steak.png",
        "correct_answer": "good",
        "explanation": "Cabernet's tannins are perfect for cutting through the fat of a juicy ribeye steak."
    }, {
        "image": "salad.png",
        "correct_answer": "meh",
        "explanation": "Light, acidic salads don't offer enough substance for Cabernet's intensity."
    }, {
        "image": "cheddar_cheese.png",
        "correct_answer": "good",
        "explanation": "Cheddar cheese's sharpness and texture pair well with the bold tannins of Cabernet."
    }, {
        "image": "grilled_lamb_chops.png",
        "correct_answer": "good",
        "explanation": "The richness of grilled lamb chops is a great match for the structure and depth of Cabernet."
    }, {
        "image": "soft_cheese.png",
        "correct_answer": "meh",
        "explanation": "The creamy, mild nature of soft cheese doesn’t stand up to the bold intensity of Cabernet."
    }]
}

activity3 = {
    "riesling": [{
            "image": "apple_tart.png",
            "correct_answer": "good",
            "explanation": "The crisp sweetness of Riesling complements the fruitiness of the tart."
        }, {
            "image": "steak.png",
            "correct_answer": "meh",
            "explanation": "The tannins in steak can clash with the sweetness and acidity of Riesling."
        }, {
            "image": "blue_cheese.png",
            "correct_answer": "meh",
            "explanation": "The bold, tangy flavors of blue cheese can overwhelm the more subtle qualities of Riesling."
        }, {
            "image": "thai_curry.png",
            "correct_answer": "good",
            "explanation": "Riesling's sweetness balances the heat and spiciness of the curry."
        }, {
            "image": "brie_cheese.png",
            "correct_answer": "good",
            "explanation": "Riesling's acidity cuts through the richness of the cheese, enhancing the flavor."
        }, {
            "image": "pickles.png",
            "correct_answer": "meh",
            "explanation": "The acidity of pickles may overpower the delicate flavors of Riesling."
    }], "sauvignon_blanc": [{
        "image": "tomato_pasta.png",
        "correct_answer": "meh",
        "explanation": "Tomato-heavy sauces like marinara clash with the acidity of Sauvignon Blanc."
    }, {
        "image": "goat_cheese.png",
        "correct_answer": "good",
        "explanation": "The tangy, creamy goat cheese pairs perfectly with the crisp acidity of Sauvignon Blanc."
    }, {
        "image": "dark_chocolate.png",
        "correct_answer": "meh",
        "explanation": "The bitterness of dark chocolate doesn't complement Sauvignon Blanc's acidity and grassy flavors."
    }, {
        "image": "green_vegetables.png",
        "correct_answer": "good",
        "explanation": "The wine's bright acidity complements the earthy flavors of green vegetables like grilled asparagus."
    }, {
        "image": "lemon_herb_chicken.png",
        "correct_answer": "good",
        "explanation": "The citrus notes in the wine enhance the lemony flavors of the chicken."
    }, {
        "image": "cream_pasta.png",
        "correct_answer": "meh",
        "explanation": "The richness of cream pasta dishes can overwhelm the freshness of Sauvignon Blanc."
    }], "chardonnay": [{
        "image": "grilled_salmon.png",
        "correct_answer": "good",
        "explanation": "The wine’s creamy texture and moderate acidity complement the rich flavor of grilled salmon."
    }, {
        "image": "pickles.png",
        "correct_answer": "meh",
        "explanation": "The sharp acidity of pickles clashes with Chardonnay's rounder, buttery profile."
    }, {
        "image": "lobster_butter.png",
        "correct_answer": "good",
        "explanation": "Buttery lobster highlights the full-bodied richness of Chardonnay beautifully."
    }, {
        "image": "blue_cheese.png",
        "correct_answer": "meh",
        "explanation": "Strong blue cheese overpowers the subtler flavors of Chardonnay."
    }, {
        "image": "cream_pasta.png",
        "correct_answer": "good",
        "explanation": "Cream sauces like creamy alfredo sauce pair well with Chardonnay's texture and mild oak influence."
    }, {
        "image": "spicy_mexican_food.png",
        "correct_answer": "meh",
        "explanation": "Spicy Mexican food can amplify the alcohol and overshadow Chardonnay's balance."
    }], "pinot_noir": [{
        "image": "grilled_salmon.png",
        "correct_answer": "good",
        "explanation": "Pinot Noir's light body and fruitiness work well with the richness of salmon."
    }, {
        "image": "spicy_mexican_food.png",
        "correct_answer": "meh",
        "explanation": "Spicy foods can overwhelm Pinot Noir's delicate flavor profile."
    }, {
        "image": "roast_chicken.png",
        "correct_answer": "good",
        "explanation": "Pinot Noir's earthiness and acidity match the savory notes in roasted chicken."
    }, {
        "image": "sushi.png",
        "correct_answer": "meh",
        "explanation": "The light, delicate flavor of sushi doesn't stand up to the complexity of Pinot Noir."
    }, {
        "image": "mushroom_risotto.png",
        "correct_answer": "good",
        "explanation": "Earthy mushrooms bring out Pinot Noir's subtle, savory depth."
    }, {
        "image": "thai_curry.png",
        "correct_answer": "meh",
        "explanation": "The intense spice of Thai curry clashes with Pinot Noir's gentle structure."
    }
    ], "cabernet_sauvignon": [{
        "image": "shrimp_scampi.png",
        "correct_answer": "meh",
        "explanation": "Shrimp scampi’s delicate flavors are overwhelmed by the bold intensity of Cabernet."
    }, {
        "image": "ribeye_steak.png",
        "correct_answer": "good",
        "explanation": "Cabernet's tannins are perfect for cutting through the fat of a juicy ribeye steak."
    }, {
        "image": "salad.png",
        "correct_answer": "meh",
        "explanation": "Light, acidic salads don't offer enough substance for Cabernet's intensity."
    }, {
        "image": "cheddar_cheese.png",
        "correct_answer": "good",
        "explanation": "Cheddar cheese's sharpness and texture pair well with the bold tannins of Cabernet."
    }, {
        "image": "grilled_lamb_chops.png",
        "correct_answer": "good",
        "explanation": "The richness of grilled lamb chops is a great match for the structure and depth of Cabernet."
    }, {
        "image": "soft_cheese.png",
        "correct_answer": "meh",
        "explanation": "The creamy, mild nature of soft cheese doesn’t stand up to the bold intensity of Cabernet."
    }]
}


quiz_questions = {
    1: {
        "title": "Spicy Thai Curry",
        "prompt": 'Pairing Request: "I need something to pair with my spicy Thai curry."',
        "choices": ["Chardonnay","Cabernet Sauvignon","Riesling","Sauvignon Blanc","Pinot Noir"],
        "answer": 2,
        "explanation": "due to its slight sweetness and refreshing acidity."
    },
    2: {
        "title": "Pick Your Riesling",
        "prompt": "Choose the glass that matches the Riesling you picked earlier.",
        "type": "imagePick",
        "images": [
            {"src": "glass1.png", "correct": True},
            {"src": "glass2.png", "correct": False},
            {"src": "glass3.png", "correct": False},
            {"src": "glass4.png", "correct": False},
        ]
    },
    3: {
        "title": "Description Request",
        "prompt": "Can you tell me what to expect from the Riesling with my curry?",
        "type": "dragAndDrop",
        "draggables": [
            {"label": "lime",      "image": "notes/lime.png",      "correct": True},
            {"label": "lemon",     "image": "notes/lemon.png",     "correct": True},
            {"label": "mushroom",  "image": "notes/mushroom.png",  "correct": False},
            {"label": "pineapple", "image": "notes/pineapple.png", "correct": True},
            {"label": "grass",     "image": "notes/grass.png",     "correct": False},
            {"label": "cedar",     "image": "notes/cedar.png",     "correct": False},
            {"label": "apricot",   "image": "notes/apricot.png",   "correct": True},
            {"label": "vanilla",   "image": "notes/vanilla.png",   "correct": False},
        ],
        "max_attempts": 4
    },
    4: {
        "title": "Creamy Chicken Alfredo",
        "prompt": 'Pairing Request: "I\'m having a creamy chicken Alfredo pasta tonight. What should I drink?"',
        "choices": ["Chardonnay","Cabernet Sauvignon","Riesling","Sauvignon Blanc","Pinot Noir"],
        "answer": 0,
        "explanation": "Its buttery, oaky flavor complements the creaminess of the dish."
    },
    5: {
        "title": "Pick Your Chardonnay",
        "prompt": "Choose the glass that matches the Chardonnay you picked earlier.",
        "type": "imagePick",
        "images": [
            {"src": "glass5.png", "correct": False},
            {"src": "glass6.png", "correct": False},
            {"src": "glass7.png", "correct": False},
            {"src": "glass8.png", "correct": True},
        ],
    },
    6: {
        "title": "Description Request",
        "prompt": '"What are the flavors like in the Chardonnay?"',
        "type": "dragAndDrop",
        "draggables": [
            {"label": "green apple",  "image": "notes/green_apple.png",  "correct": True},
            {"label": "butter",       "image": "notes/butter.png",       "correct": True},
            {"label": "bell pepper",  "image": "notes/bell_pepper.png",  "correct": False},
            {"label": "pineapple",    "image": "notes/pineapple.png",    "correct": True},
            {"label": "licorice",     "image": "notes/licorice.png",     "correct": False},
            {"label": "toasted almond","image":"notes/toasted_almond.png","correct": True},
            {"label": "black pepper", "image": "notes/black_pepper.png", "correct": False},
            {"label": "vanilla",      "image": "notes/vanilla.png",      "correct": False},
        ],
        "max_attempts": 4
    },
    7: {
        "title": "Fresh Oysters",
        "prompt": 'Pairing Request: "I have fresh oysters. What wine would you recommend?"',
        "choices": ["Chardonnay", "Cabernet Sauvignon", "Riesling", "Sauvignon Blanc", "Pinot Noir"],
        "answer": 3,
        "explanation": "Sauvignon Blanc’s crisp acidity and citrus notes are ideal for oysters."
    },
    8: {
        "title": "Pick Your Sauvignon Blanc",
        "prompt": "Choose the glass that matches the Sauvignon Blanc you picked earlier.",
        "type": "imagePick",
        "images": [
            {"src": "glass5.png", "correct": False},
            {"src": "glass6.png", "correct": True},
            {"src": "glass7.png", "correct": False},
            {"src": "glass8.png", "correct": False},
        ]
    },
    9: {
        "title": "Description Request",
        "prompt": 'Description Request: "Tell me more about this Sauvignon Blanc."',
        "type": "dragAndDrop",
        "draggables": [
            {"label": "grapefruit",   "image": "notes/grapefruit.png",   "correct": True},
            {"label": "gooseberry",   "image": "notes/gooseberry.png",   "correct": True},
            {"label": "leather",      "image": "notes/leather.png",      "correct": False},
            {"label": "fig",          "image": "notes/fig.png",          "correct": False},
            {"label": "blackberry",   "image": "notes/blackberry.png",   "correct": False},
            {"label": "vanilla",      "image": "notes/vanilla.png",      "correct": False},
            {"label": "grass",        "image": "notes/grass.png",        "correct": True},
            {"label": "passionfruit", "image": "notes/passionfruit.png", "correct": True},
        ],
        "max_attempts": 4
    },
        10: {
        "title": "Hearty Steak",
        "prompt": 'Pairing Request: "I’m about to enjoy a steak. What wine should I get?"',
        "choices": ["Chardonnay","Cabernet Sauvignon","Riesling","Sauvignon Blanc","Pinot Noir"],
        "answer": 1,  # Cabernet Sauvignon
        "explanation": "Its bold flavors of dark berries and tannins complement the richness of steak."
    },
    11: {
        "title": "Pick Your Cabernet Sauvignon",
        "prompt": "Choose the glass that matches the Cabernet Sauvignon you picked earlier.",
        "type": "imagePick",
        "images": [
            {"src": "glass2.png",  "correct": False},
            {"src": "glass5.png", "correct": True},
            {"src": "glass3.png", "correct": False},
            {"src": "glass8.png", "correct": False},
        ]
    },
    12: {
        "title": "Description Request",
        "prompt": 'Description Request: "What’s the Cabernet Sauvignon like?"',
        "type": "dragAndDrop",
        "draggables": [
            {"label": "lime",           "image": "notes/lime.png",         "correct": False},
            {"label": "blackberry",     "image": "notes/blackberry.png",   "correct": True},
            {"label": "melon",          "image": "notes/melon.png",        "correct": False},
            {"label": "peach",          "image": "notes/peach.png",        "correct": False},
            {"label": "rosewater",      "image": "notes/rosewater.png",    "correct": False},
            {"label": "cedar",          "image": "notes/cedar.png",        "correct": True},
            {"label": "blackcurrant",   "image": "notes/blackcurrant.png", "correct": True},
            {"label": "tobacco",        "image": "notes/tobacco.png",      "correct": True},
        ],
        "max_attempts": 4
    },
    13: {
        "type": "multipleChoice",
        "title": "Grilled Salmon",
        "prompt": "I’m having grilled salmon for dinner. Which wine would be the best choice to go with it?",
        "choices": [
            "Chardonnay",
            "Cabernet Sauvignon",
            "Riesling",
            "Sauvignon Blanc",
            "Pinot Noir"
        ],
        "answer": 4,  # Pinot Noir
        "explanation": "Its light-to-medium body and subtle flavors of red berries and earthiness complement the rich but delicate taste of grilled salmon."
    },

    14: {
        "type": "imagePick",
        "title": "Grilled Salmon",
        "prompt": "Choose the glass that matches the Pinot Noir you picked earlier.",
        "images": [
            { "src": "glass1.png", "correct": False },
            { "src": "glass2.png", "correct": False },
            { "src": "glass3.png", "correct": True  },  # this one is the Pinot Noir
            { "src": "glass4.png", "correct": False }
        ]
    },

    15: {
        "type": "dragAndDrop",
        "title": "Grilled Salmon",
        "prompt": "What can I expect from the Pinot Noir?",
        "max_attempts": 4,
        "draggables": [
            { "label": "mint",       "image": "notes/mint.png",       "correct": False },
            { "label": "raspberry",  "image": "notes/raspberry.png",  "correct": True  },
            { "label": "mushroom",   "image": "notes/mushroom.png",   "correct": True  },
            { "label": "mango",      "image": "notes/mango.png",      "correct": False },
            { "label": "clove",      "image": "notes/clove.png",      "correct": True },
            { "label": "coconut",    "image": "notes/coconut.png",    "correct": False },
            { "label": "cherry",     "image": "notes/cherry.png",     "correct": True  },
            { "label": "blueberry",  "image": "notes/blueberry.png",  "correct": False  }
        ]
    }
}

# 1) Secret key for sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")

# 2) Home screen
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

# 2) Map screen
@app.route("/map", methods=["GET","POST"])
def map():
    progress = session.get("progress", [])
    all_completed = set(progress) >= set(varietals)
    return render_template(
        "map.html", 
        progress=progress, 
        varietals=varietals, 
        varietal_data=varietal_data, 
        all_completed=all_completed
    )

# 3) Wine varietal introduction page (dynamic)
@app.route("/introduction/<varietal_name>", methods=["POST"])
def varietal_intro(varietal_name):
    # Get the wine info
    data = varietal_data.get(varietal_name.lower())

    if not data:
        return "Varietal not found", 404

    return render_template(
        "varietal_intro.html", 
        title=format_bold_text(data["title"]), 
        descriptions=format_bold_text(data["descriptions"]),
        varietal=data["varietal"],
        varietal_url=data["varietal_url"]
    )

@app.route("/learn/<varietal_name>/<int:activity_number>", methods=["GET", "POST"])
def activity_intro(varietal_name, activity_number):
    varietal = varietal_data.get(varietal_name.lower())
    activity = activities.get(activity_number)
    varietal_activities = varietal["activities"][activity_number]

    if not varietal or not activity:
        return "Page not found", 404

    return render_template(
        "activity_intro.html",
        varietal_name=varietal["varietal"],
        activity_number=activity_number,
        activity_name=activity["name"],
        activity_instructions=format_bold_text(activity["instructions"].replace("{{ varietal_name }}", varietal["varietal"])),
        activity_button=activity["button"],
        varietal_url=varietal["varietal_url"],
        hint=format_bold_text(varietal_activities["hint"])
    )

@app.route("/learn/<varietal_name>/<int:activity_number>/start", methods=["POST"])
def start_activity(varietal_name, activity_number):
    varietal = varietal_data.get(varietal_name.lower())
    activity = activities.get(activity_number)
    varietal_activities = varietal["activities"][activity_number]

    if not varietal or not activity:
        return "Page not found", 404

    # Add this part only for activity 3 (pairings)
    current_food = None
    if activity_number == 3:
        foods = activity3.get(varietal_name.lower(), [])
        if foods:
            session["food_index"] = 0
            current_food = foods[0]

    # Add this part only for activity 3 (pairings)
    current_food = None
    if activity_number == 3:
        foods = activity3.get(varietal_name.lower(), [])
        if foods:
            session["food_index"] = 0
            current_food = foods[0]

    return render_template(
        "activity.html",
        varietal_name=varietal["varietal"],
        activity_number=activity_number,
        activity_name=activity["name"],
        varietal_url=varietal["varietal_url"],
        hint=format_bold_text(varietal_activities["hint_short"]),
        current_food=current_food, # only for activity 3, 
        note_options=varietal_activities.get("note_options", []),
        correct_notes=varietal_activities.get("correct_notes", []),
        color_options=varietal_activities.get("color_options", []),
        correct_index=varietal_activities.get("correct_index", 0),
    )



# When an activity is completed, update the session
@app.route("/complete_varietal/<varietal_name>", methods=["POST"])
def complete_varietal(varietal_name):
    varietal = varietal_data.get(varietal_name.lower())
    varietal = varietal_data.get(varietal_name.lower())
    if varietal_name not in varietals:
        return "Varietal not found", 404

    # Get (or init) the list of completed varietals
    progress = session.get("progress", [])

    if varietal_name not in progress:
        progress.append(varietal_name)
        session["progress"] = progress

    # back to the map overview
    return render_template("activity_complete.html", varietal_name=varietal["varietal"], varietal_url=varietal["varietal_url"])

@app.route("/next_food/<varietal_name>", methods=["GET", "POST"])
def next_food(varietal_name):
    varietal = varietal_data.get(varietal_name.lower())
    if varietal_name not in activity3:
        return jsonify({"error": "Invalid varietal"}), 400

    # Initialize index if not in session
    if "food_index" not in session:
        session["food_index"] = 0
    else:
        session["food_index"] += 1

    foods = activity3[varietal_name]
    index = session["food_index"]

    if index >= len(foods):
        return jsonify({
            "done": True
        })

    food = foods[index]
    return jsonify({
        "image": food["image"],
        "explanation": food["explanation"],
        "correct_answer": food["correct_answer"]
    })
    return render_template("activity_complete.html", varietal_name=varietal["varietal"], varietal_url=varietal["varietal_url"])

@app.route("/quiz", methods=["GET", "POST"])
def quiz_start():
    progress = session.get("progress", [])
    if len(progress) < len(varietals):
        return redirect(url_for("map"))
    if request.method == "POST":
        session["quiz_score"] = 0
        session["quiz_attempts"] = {}
        return redirect(url_for("quiz_step", step=1))
    return render_template("quiz_intro.html")

@app.route("/quiz/<int:step>", methods=["GET", "POST"])
def quiz_step(step):
    total = len(quiz_questions)
    q = quiz_questions.get(step)
    # when step > 15, go to complete
    if not q:
        return redirect(url_for("quiz_complete"))

    # track attempts
    attempts = session.setdefault("quiz_attempts", {})
    this_try = attempts.get(str(step), 0)

    show_feedback = False
    error = None

    if request.method == "POST":
        this_try += 1
        attempts[str(step)] = this_try
        session["quiz_attempts"] = attempts

        # correctness logic
        correct = False
        if "answer" in q:
            correct = (int(request.form.get("choice", -1)) == q["answer"])
        elif q.get("type") == "imagePick":
            choice = int(request.form.get("choice", -1))
            correct = (0 <= choice < len(q["images"]) and q["images"][choice]["correct"])
        elif q.get("type") == "dragAndDrop":
            dropped = request.form.get("dropped_items", "")
            picked = [lbl for lbl in dropped.split(",") if lbl]
            correct_set = {d["label"] for d in q["draggables"] if d["correct"]}
            correct = (set(picked) == correct_set)
        else:
            correct = True

        if not correct:
            error = "Try again!"
        else:
            show_feedback = True
            # only on first correct attempt
            if this_try == 1:
                session["quiz_score"] = session.get("quiz_score", 0) + 1

    customer_idx = ((step - 1) // 3) + 1
    group_start = (customer_idx - 1) * 3 + 1
    customer_dish = quiz_questions[group_start]["title"]

    return render_template("quiz_step.html",
                           step=step,
                           total=total,
                           q=q,
                           show_feedback=show_feedback,
                           error=error,
                           customer_dish=customer_dish)

@app.route("/quiz_complete")
def quiz_complete():
    score = session.get("quiz_score", 0)
    total = len(quiz_questions)
    return render_template("quiz_complete.html", score=score, total=total)

@app.route("/quiz_complete/retake", methods=["POST"])
def quiz_retake():
    session["quiz_score"] = 0
    session["quiz_attempts"] = {}
    return redirect(url_for("quiz_start"))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

