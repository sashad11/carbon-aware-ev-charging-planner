# Carbon-Aware EV Fleet Charging Planner

## What I built and who for

I created a tool to help an EV fleet manager in London identify suitable times to charge their electric vehicles.

The tool looks at two things: the cost of electricity and the expected carbon intensity of electricity throughout the day. It brings this information together and compares the available 30-minute charging periods.

Each period is given a score based on its electricity price and carbon intensity. A lower score means the time offers a better balance between keeping charging costs low and reducing carbon emissions.

The final result is a CSV file that shows the charging periods from the most suitable to the least suitable.

## The data

I used two public sources of data:

- **NESO Carbon Intensity data** – provides carbon intensity information for electricity in Great Britain. I used the forecast carbon intensity for each 30-minute period because the aim of the tool is to help plan charging in advance.

- **Octopus Energy Agile electricity prices** – provides electricity prices for 30-minute periods. I used the London electricity region because the tool is designed for a London-based fleet manager.

I chose these two sources because they both provide information in 30-minute periods. This means the electricity price and carbon forecast can be matched for the same charging window.

The original data from both sources is saved as JSON files before any changes are made to it.

## How it works

The project works in a few stages:

1. The carbon intensity and electricity price data are collected from the two public sources and saved in their original form.

2. The data is cleaned so that both sources use consistent column names and date/time formats. I also checked for missing values and duplicate time periods.

3. The cleaned data is stored in a DuckDB database. The carbon and price data are then matched using their 30-minute start and end times.

4. Only time periods that have both a carbon forecast and an electricity price are used for the final recommendations.

5. Each time period is ranked separately by electricity price and forecast carbon intensity. Lower prices and lower carbon intensity receive better ranks.

6. The two ranks are added together to create a charging score. A lower score represents a better balance between cost and carbon intensity.

7. The results are saved as a CSV file, with the best-ranked charging periods shown first.

## How to run it

1. Make sure Python is installed.

2. Install the required packages:

   `pip install -r requirements.txt`

3. Collect the carbon intensity data:

   `python "SRC/extract_carbon.py"`

4. Collect the electricity price data:

   `python "SRC/extract_prices.py"`

5. Clean, combine and analyse the data:

   `python "SRC/transform_data.py"`

6. The final ranked results can be found in:

   `Output/charging_recommendations.csv`

## What I would do next

If I developed the project further, I would:

- Allow the user to choose whether electricity cost or carbon emissions are more important to them, rather than giving both equal importance.
- Use a longer period of data to identify patterns in suitable charging times, rather than focusing on a single day.
- Make the dates easier for the user to change instead of setting them directly in the code.
- Create a simple dashboard so that a fleet manager could view the recommended charging times without opening the CSV file.
- Add more checks to make sure the tool handles situations where data is missing or unavailable.

## Where AI helped

I used AI as a learning and development assistant while building this project. As I have limited previous experience building data pipelines, I used it to help me understand the different stages of the project and to explain unfamiliar Python, SQL, DuckDB and Git concepts.

AI also helped me draft parts of the code, troubleshoot errors and think through how the two datasets could be cleaned, matched and used to create a simple charging recommendation.

I reviewed and ran the code myself throughout the project and made decisions about what to keep or change. For example, I chose to keep missing actual carbon intensity values rather than replace them, as forecast values are more relevant when planning future charging. I also chose to only include time periods with both price and carbon data in the final recommendations.

I kept the final approach relatively simple so that I could understand and explain how each part of the project works.