

# 1. The Big Idea

Crime News/Data detection  

Main idea is to use real-time incident-level crime data to help people understand the safety risks in their local area. Important crime and safety signals are often scattered across police logs, public dashboards, and news sites. A typical resident might have a hard time to manually track these sources, and risk patterns are often missed. Since they have different times and locations. This will hopefully result in a clear snapshot of what is happening around them.

My MVP:
- Make authenticated API requests to CrimeoMeter using x-api-key.
- Pull all crime incidents for a chosen neighborhood (based on lat/lon + radius).
Categorize crimes into:
-   Property
-   Violent
-   Drug-related
-   incident date/time
-   crime type (e.g., Motor Vehicle Theft)
-   offense category (Property, Person, Society)
-   detailed narrative
-   lat/long coordinates

Stretch Goals:
- Develop a Neighborhood Risk Score (0–100 scale) based on incident type, frequency, and severity.
- Add visualizations (bar charts, line charts, or maps).
- Build a small web interface (Flask or Streamlit) to display live risk summaries.
- Detect crime spikes (e.g., “vehicle thefts up 30% this week”) and flag anomalies.

# 2. Learning Objectives:
- Gain proficiency working with real APIs (authentication, parameters, rate limits).
- Handle structured JSON data and convert it into usable forms for analysis.
- Be more familiar with Python libraries

# 3. Implementation Plan
Step 1: API familiarity (Test the API usage)
Learning how to use the data:
Ex.
("incident_offense": "Motor Vehicle Theft",
"incident_offense_crime_against": "Property",
"incident_latitude": 41.9751781,
"incident_longitude": -87.6499609,
"incident_date": "2024-01-12T21:00:00Z")

Step 2 — Data Cleaning & Storage
- Convert timestamps to understandable format
- Save normalized data

Step 3 — Crime Categorization:
Property crime
Violent crime
Drug/overdose-related crime
Other crimes

Step 4 - Weekly Summary Generation Through:
- Graphs 
- Charts 
- number of a certain crime 
- this type of crime went up 10%

# 4. Project Schedule 
Week 1: Experiment with a certain Neighborhood and test API
Week 2: Clean the data and store the data
Week 3-4: Start generating the graphs and visualizations and maybe show the results on a website using flask

# 5. Collaboration:
- I will be working by myself

# 6. Risks and Limitations:
- Unfamiliarity with new API
- How to make use of the Latitude and Longitude 
- Hard to vizualize the data 

# 7. Additional Course Content:
- Python analysis tools (Pandas, datetime)
- Maybe Matplotlib, Plotly

