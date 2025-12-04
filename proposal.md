

# 1. The Big Idea

My project is a full Flask web application called Hate Crime Trends Explorer. It allows users to:
- Select a U.S. state
- Enter a start year and end year
- Choose a graph type (state trend vs. state vs. U.S.)
- View a summary of hate-crime trends over time

The application pulls real data from the FBI Crime Data Explorer API, processes it, and presents it through a clean, user-friendly interface. The purpose of this project is to pull data from the FBI's data source to create meaningful graphs about public safety and historical changes in hate-crime activity from each state.

My MVP:
A functioning Flask web application to pull all crime incidents for a chosen state
- Graph 
- Pulls data from FBI reports 
- Has a start and end year 
- Add real U.S. national averages to “State vs U.S.” charts

Stretch Goals:
- Develop a Risk Score (0–100 scale) based on incident type, frequency, and severity.
- Add visualizations (bar charts, line charts, or maps).
- 
- Detect crime spikes and flag anomalies.

# 2. Learning Objectives:
- Gain proficiency working with real APIs (authentication, parameters, rate limits).
- Handle structured JSON data and convert it into usable forms for analysis.
- Be more familiar with Python libraries

# 3. Implementation Plan
Step 1: 1. Construct Correct CRIME API URLs from FBI data

The FBI API requires:
- A state abbreviation
- A date format (MM-YYYY)
- A type parameter (counts)
- A functioning API key 

Step 2 — Data Processing 
Extract Single-Year Incidents
- The FBI API returns each year as a list inside "results".
- Missing or malformed data becomes None
- Only the correct fields are pulled: "data_year" and "value"

Step 3 — Web Application Layer app.py
- Use GET to Load:
    - A list of states
    - And Renders index.html 

- Use POST to: 
    - Pull values from the form
    - Validates input (state, years, graph type)
    - Calls backend functions if everything is valid
    - Redirects user to results view with a generated plot

Step 4 Account for Validation
- Required fields are present:
    - If either start or end year is empty then return error
- Logical constraints:
    - Start year ≠ end year
    - End year has to be greater than start year

Step 5 Summary Statistics Computation
- Maximum yearly ratew
- Minimum yearly rate
- Percent change (start → end)
- First and last year in the dataset
- Overall trend direction


# 4. Project Schedule 
- Week 1: Experiment with a certain State and test API
- Week 2: Clean the data and store the data
- Week 3-4: Start generating the graphs and visualizations and show the results on a website using flask

# 5. Collaboration:
- I will be working by myself

# 6. Risks and Limitations:
- Unfamiliarity with new API
- The FBI Crime Data Explorer API responds very slowly
- Temporarily go offline for maintenance

Because this project fully depends on the API, any downtime or irregular response format affects the app’s ability to fetch accurate results, which can cause the graph to:

- Fail to generate if required data is missing
- Some states may show gaps in data from missing records

# 7. Additional Course Content:
- Python analysis tools (Pandas, datetime)
- Maybe Matplotlib, Plotly
- Make the UI look more user friendly using bootstrap

