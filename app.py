from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("india_tourism.csv")

@app.route("/", methods=["GET","POST"])
def home():
    plan = ""
    if request.method=="POST":
        state = request.form["state"].lower()
        days = int(request.form["days"])
        budget = int(request.form["budget"])

        data = df[df["State"].str.lower() == state]

        per_day = 3
        total = days * per_day
        selected = data.head(total)

        day = 1
        count = 0

        plan = f"Travel Plan for {state.title()} ({days} Days)\n\n"

        for i,row in selected.iterrows():
            if count % per_day == 0:
                plan += f"\nDay {day}\n"
                day+=1
            plan += f"""📍 {row['Name']} ({row['City']})
⭐ Rating: {row['Google review rating']}
⏰ Time: {row['time needed to visit in hrs']} hrs
💰 Entry Fee: ₹{row['Entrance Fee in INR']}
🕒 Best Time: {row['Best Time to visit']}
📸 camera allow: {row['DSLR Allowed']}

"""
            count+=1

        plan += f"\nEstimated Budget: ₹{budget}"

    return render_template("chat.html", plan=plan)

app.run(debug=True)