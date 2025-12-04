# app.py
import os
import uuid

from flask import Flask, render_template, request
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from crime_api import get_hate_crime_trends, get_state_choices


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    states = get_state_choices()  # dynamic list for dropdown

    if request.method == "POST":
        state = request.form.get("state", "MA")
        graph_type = request.form.get("graph_type", "state_trend")

        # Read year inputs as strings first
        start_year_str = request.form.get("start_year", "").strip()
        end_year_str = request.form.get("end_year", "").strip()

        error = None
        start_year = end_year = None

        # Check empty inputs
        if not start_year_str or not end_year_str:
            error = "Please enter both a start year and an end year."
        else:
            try:
                start_year = int(start_year_str)
                end_year = int(end_year_str)

                # Rule 1: years must differ
                if start_year == end_year:
                    error = "Start year and end year must be different."

                # Rule 2: end year must be greater
                elif end_year < start_year:
                    error = "End year cannot be earlier than the start year."

            except ValueError:
                error = "Years must be whole numbers, e.g., 2005."

        # Return form + error message
        if error:
            return render_template(
                "index.html",
                states=states,
                error=error,
                form_values={
                    "state": state,
                    "start_year": start_year_str,
                    "end_year": end_year_str,
                    "graph_type": graph_type,
                },
            )


        # ---- normal happy path: call the API & draw the graph ----
        data = get_hate_crime_trends(state, start_year, end_year)
        years = [int(y) for y in data["years"]]
        state_rates = data["state_rates"]
        us_rates = data["us_rates"]
        state_label = data["state_label"]

        # build plot etc. (your existing plotting code here)
        fig, ax = plt.subplots(figsize=(9, 4))
        if graph_type == "state_vs_us":
            ax.plot(years, state_rates, marker="o", label=state_label)
            ax.plot(years, us_rates, marker="o", label="United States")
            title = f"Hate crime rate: {state_label} vs United States"
        else:
            ax.plot(years, state_rates, marker="o", label=state_label)
            title = f"Hate crime rate over time: {state_label}"

        ax.set_xlabel("Year")
        ax.set_ylabel("Incidents per 100,000 people")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend()

        os.makedirs("static", exist_ok=True)
        plot_filename = f"plot_{uuid.uuid4().hex}.png"
        plot_path = os.path.join("static", plot_filename)
        fig.tight_layout()
        fig.savefig(plot_path)
        plt.close(fig)

        max_rate = max(state_rates)
        min_rate = min(state_rates)
        max_year = years[state_rates.index(max_rate)]
        min_year = years[state_rates.index(min_rate)]
        if state_rates[0] != 0:
            change_pct = (state_rates[-1] - state_rates[0]) / state_rates[0] * 100
        else:
            change_pct = 0.0

        summary = {
            "state": state_label,
            "start_year": years[0],
            "end_year": years[-1],
            "max_year": max_year,
            "max_rate": round(max_rate, 2),
            "min_year": min_year,
            "min_rate": round(min_rate, 2),
            "change_pct": round(change_pct, 1),
        }

        return render_template(
            "results.html",
            plot_filename=plot_filename,
            summary=summary,
            graph_type=graph_type,
        )

    return render_template(
        "index.html",
        states=states,
        error=None,
        form_values=None,
    )


if __name__ == "__main__":
    app.run(debug=True)