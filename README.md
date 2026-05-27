# Data analysis and visualization project about COVID-19 in France
Authors: Martyna Pawlak and Zofia Rewak 

## Data overview

- Epidemiological data:

Download from: `https://ourworldindata.org/coronavirus#explore-our-data-on-covid-19`

The dataset contains time-series epidemiological data (specifically tracking the COVID-19 pandemic). It records daily health statistics, allowing for a direct comparison between France and the European average. The key metrics included in the dataset are the daily number of new infections, deaths, and the cumulative rate of vaccinations per 100 inhabitants.

- Economical data:

Download from: `https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv`

## Plots overview:

### *Plot 1*: Infections and deaths (Line chart)

- `plots/`

This plot illustrates the daily progression of new infections and mortality rates over the course of the pandemic. The line chart format highlights the distinct peaks of the virus, making it easy to compare the overall severity and epidemic dynamics between France and the rest of Europe.

### *Plot 2*: Global vaccination overview – Year-end status (Interactive bar chart)

- `plots/`

This chart provides a macro-level overview of the vaccination campaigns, focusing on the final cumulative status at the end of each year. By aggregating the data annually, it shows a clean comparison of the total population coverage achieved by France versus the European average.

### *Plot 3*: Detailed vaccination progress – Monthly close-up (Interactive area chart)

- `plots/`

This plot shows as a deep dive into the most critical years of the pandemic (2020–2022) on a month-to-month basis. The interactive area chart captures the real-time speed and dynamics of the vaccine rollout. It clearly highlights the transition from zero vaccines in 2020, through the exponential growth of the vaccinacions in 2021, to the stabilization phase in late 2022.

### *Plot 4*: Government Policy vs. Transmission Control (Dual-axis line chart)

- `plots/04_stringency_vs_cases.html`

This plot displays two metrics over time on a dual-axis system: the daily new COVID-19 cases (7-day smoothed) and the Oxford Government Stringency Index for France. It maps out the exact dates of government-imposed restrictions against the timeline of infection waves.

### *Plot 5*: Inferential Statistics – Impact of Pandemic Decline on Trend Predictions

- `plots/05_inference_period.html`

This plot displays the actual daily new COVID-19 cases in France alongside two polynomial regression curves. The green line shows a trend model calculated using the entire 2020–2024 dataset, while the dashed red line shows a predictive model calculated using only the data from the first period (2020–2022) and projected forward through 2024.

### *Plot 6*: Comparative Presentation Timeline – COVID-19 Trajectory & Mortality Analysis
`html/06_animated_bubbles.html`
This is an animated scatter plot that tracks the weekly progression of the pandemic across France, Poland, and Europe using a dual logarithmic scale. The horizontal axis (X) shows the total cumulative cases, the vertical axis (Y) shows the daily new cases per million, and the dynamic size of each bubble corresponds to the daily mortality rate.
