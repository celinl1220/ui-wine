from flask import Flask, render_template, session, redirect, url_for, Response, request, jsonify
import os
app = Flask(__name__)

# Set up the secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")
app.jinja_env.globals.update(enumerate=enumerate)

varietals = ["riesling", "sauvignon_blanc", "chardonnay", "pinot_noir", "cabernet_sauvignon"]
TOTAL_VARIETALS = len(varietals)

varietal_data = {
    "riesling": {
        "title": "Welcome to the Crystal Lakes of Riesling",
        "descriptions": ["Riesling is light, aromatic, and often slightly sweet.", "Think zippy acidity, juicy fruit, and floral aromas.", "It's refreshing and expressive—perfect for those who like a little personality in their glass."],
        "varietal": "Riesling",
        "varietal_url": "riesling",
        "activities": {
            1: {
                "hint": "Riesling is never heavy or brooding. Think juicy fruits, fresh blooms, and zippy citrus.",
                "hint_short": "Think juicy fruits, fesh blooms, and zippy citrus.",
            },
            2: {
                "hint": "This wine is typically pale straw to light gold.",
                "hint_short": "This wine is typically pale straw to light gold."
            },
            3: {
                "hint": "Think spicy food, light meats, and citrusy dishes!",
                "hint_short": "Riesling shines with spicy, sweet, and tangy dishes."
            }
        }
    },
    "sauvignon_blanc": {
        "title": "Welcome to the Valley of Sauvignon Blanc!",
        "descriptions": ["Sauvignon Blanc is fresh, green, and unapologetically zesty.", "Known for its high acidity and bold aromatics, this wine brings to mind citrus groves, cut grass, and cool ocean breezes.", "It's sharp, sassy, and always refreshing."],
        "varietal": "Sauvignon Blanc",
        "varietal_url": "sauvignon_blanc",
        "activities": {
            1: {
                "hint": "Picture green herbs, tropical bursts, and a splash of sharp citrus.",
                "hint_short": "Picture green herbs, tropical bursts, and a splash of sharp citrus.",
            },
            2: {
                "hint": "This wine is typically pale straw with greenish glints.",
                "hint_short": "This wine is typically pale straw with greenish glints."
            },
            3: {
                "hint": "Sauvignon Blanc is perfect with fresh, zesty, and herbaceous dishes.",
                "hint_short": "Sauvignon Blanc is perfect with fresh, zesty, and herbaceous dishes."
            }
        }
    },
    "chardonnay": {
        "title": "Welcome to the Golden Hills of Chardonnay!",
        "descriptions": ["Chardonnay is smooth, versatile, and effortlessly elegant.", "Think ripe pear, creamy vanilla, and a hint of toasted oak.", "It’s rich yet balanced—great for those who enjoy a little luxury in every sip."],
        "varietal": "Chardonnay",
        "varietal_url": "chardonnay",
        "activities": {
            1: {
                "hint": "TO UPDATE WITH CHARDONNAY",
                "hint_short": "TO UPDATE WITH CHARDONNAY",
            },
            2: {
                "hint": "This wine ranges from pale gold to rich, buttery yellow.",
                "hint_short": "This wine ranges from pale gold to rich, buttery yellow."
            },
            3: {
                "hint": "Chardonnay pairs wonderfully with rich, creamy, and buttery foods.",
                "hint_short": "Chardonnay pairs wonderfully with rich, creamy, and buttery foods."
            }
        }
    },
    "pinot_noir": {
        "title": "Welcome to the Forest of Pinot Noir!",
        "descriptions": ["Pinot Noir is delicate, earthy, and quietly complex.", "Think ripe cherry, soft spice, and subtle floral notes.", "It's graceful and layered—perfect for those who appreciate a softer kind of depth."],
        "varietal": "Pinot Noir",
        "varietal_url": "pinot_noir",
        "activities": {
            1: {
                "hint": "TO UPDATE WITH PINOT NOIR",
                "hint_short": "TO UPDATE WITH PINOT NOIR",
            },
            2: {
                "hint": "This wine is typically light ruby to translucent garnet.",
                "hint_short": "This wine is typically light ruby to translucent garnet."
            },
            3: {
                "hint": "Pinot Noir is a great match for earthy, savory, and subtly spiced dishes.",
                "hint_short": "Pinot Noir is a great match for earthy, savory, and subtly spiced dishes."
            }
        }
    },
    "cabernet_sauvignon": {
        "title": "Welcome to the Caverns of Cabernet Sauvignon!",
        "descriptions": ["Cabernet Sauvignon is bold, structured, and unapologetically full-bodied.", "Think blackcurrant, tobacco, and a whisper of cedar.", "It's powerful and intense—for those who like their wines with serious presence."],
        "varietal": "Cabernet Sauvignon",
        "varietal_url": "cabernet_sauvignon",
        "activities": {
            1: {
                "hint": "TO UPDATE WITH CABERNET",
                "hint_short": "TO UPDATE WITH CABERNET",
            },
            2: {
                "hint": "This wine is deep ruby to inky purple, often nearly opaque.",
                "hint_short": "This wine is deep ruby to inky purple, often nearly opaque."
            },
            3: {
                "hint": "Cabernet Sauvignon complements hearty, grilled, and bold-flavored meals.",
                "hint_short": "Cabernet Sauvignon complements hearty, grilled, and bold-flavored meals."
            }
        }
    }
}

activities = {
    1: {
        "name": "Drag and Drop the Notes",
        "button": "Start Tapping",
        "instructions": "Tap on the images that feel like {{ varietal_name }}. Avoid anything that doesn't match the vibe."
    },
    2: {
        "name": "Color Me",
        "button": "Start Coloring",
        "instructions": "Which color looks most like a glass of {{ varietal_name }}?"
    },
    3: {
        "name": "Right Pair, Right Swipe?",
        "button": "Start Swiping",
        "instructions": "Use your arrow keys to swipe left or right on each food item to guess whether it pairs well with {{ varietal_name }}."
    }
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
        title=data["title"], 
        descriptions=data["descriptions"],
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
        activity_instructions=activity["instructions"].replace("{{ varietal_name }}", varietal["varietal"]),
        activity_button=activity["button"],
        varietal_url=varietal["varietal_url"],
        hint=varietal_activities["hint"]
    )

@app.route("/learn/<varietal_name>/<int:activity_number>/start", methods=["POST"])
def start_activity(varietal_name, activity_number):
    varietal = varietal_data.get(varietal_name.lower())
    activity = activities.get(activity_number)
    varietal_activities = varietal["activities"][activity_number]

    if not varietal or not activity:
        return "Page not found", 404

    return render_template(
        "activity.html",
        varietal_name=varietal["varietal"],
        activity_number=activity_number,
        activity_name=activity["name"],
        varietal_url=varietal["varietal_url"],
        hint=varietal_activities["hint_short"]
    )

# When an activity is completed, update the session
@app.route("/complete_varietal/<varietal_name>", methods=["POST"])
def complete_varietal(varietal_name):
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

@app.route("/quiz", methods=["GET", "POST"])
def quiz_start():
    progress = session.get("progress", [])
    # block quiz until all varietals done
    if len(progress) < len(varietals):
        return redirect(url_for("map_view"))

    if request.method == "POST":
        # reset score
        session["quiz_score"] = 0
        return redirect(url_for("quiz_step", step=1))

    return render_template("quiz_intro.html")

@app.route("/quiz/<int:step>", methods=["GET", "POST"])
def quiz_step(step):
    total = len(quiz_questions)
    raw_q = quiz_questions.get(step)
    if not raw_q:
        return redirect(url_for("map"))
    q = quiz_questions.get(step)
    if not q:
        return redirect(url_for("map"))

    show_feedback = False
    error = None

    if request.method == "POST":
        choice = None
        try:
            choice = int(request.form.get("choice", -1))
        except:
            choice = -1

        # 1) multiple choice
        if hasattr(q, "answer"):
            if choice == q.answer:
                show_feedback = True
        # 2) imagePick
        elif q.get("type") == "imagePick":
            if 0 <= choice < len(q["images"]) and q["images"][choice]["correct"]:
                show_feedback = True
        # 3) dragAndDrop
        elif q.get("type") == "dragAndDrop":
            dropped = request.form.get("dropped_items", "")
            picked = [lbl for lbl in dropped.split(",") if lbl]
            correct = [d["label"] for d in q["draggables"] if d["correct"]]
            if set(picked) == set(correct):
                show_feedback = True
        else:
            show_feedback = True

        if not show_feedback:
            error = "Try again!"
        else:
            # tally a point
            session["quiz_score"] = session.get("quiz_score", 0) + 1

    customer_idx = ((step - 1) // 3) + 1
    group_start = (customer_idx - 1) * 3 + 1
    customer_dish = quiz_questions[group_start]["title"]

    return render_template(
        "quiz_step.html",
        step=step,
        total=total,
        q=q,
        show_feedback=show_feedback,
        error=error,
        customer_dish=customer_dish, 
    )

@app.route("/quiz_complete")
def quiz_complete():
    score = session.get("quiz_score", 0)
    total = len(quiz_questions)
    return render_template("quiz_complete.html", score=score, total=total)

@app.route("/quiz_complete/retake", methods=["POST"])
def quiz_retake():
    # clear score and go back to start
    session["quiz_score"] = 0
    return redirect(url_for("quiz_start"))

if __name__ == '__main__':
   app.run(debug = True, port=5001)
