# Simple Analysis System: COVID-19 Country Data Analyzer

## What is the Simple Analysis System?

The Simple Analysis System is a lightweight Flask-based web application that provides quick insights into COVID-19 data by country. It processes historical case data to generate key statistics like total cases, total deaths, and peak infection days for any country in the dataset.

## How It Works

1. **Data Processing**: The system reads COVID-19 data from a CSV file (`covid_data.csv`) containing daily case reports
2. **Analysis Engine**: When a user submits a country name:
   - Filters the dataset for that country
   - Calculates total cases and deaths
   - Identifies the peak infection day
3. **Optional Storage**: Can store results in an SQLite database for future reference (using APSW)
4. **Web Interface**: Presents results in a simple, user-friendly format

## Key Features

- Fast country-specific COVID-19 analysis
- Minimal dependencies (Flask, pandas, and optionally APSW)
- Clean web interface with instant results
- Optional data persistence

## Example Usage

1. **github installation and directory**
```bash
apt-get update -y && apt-get upgrade -y
apt-get install python git
git clone https://github.com/Elang-elang/SASTPython.git 
```

2. **Prepare your data**:
   - Create a `covid_data.csv` file with columns: `date, country, cases, deaths`
   - Sample data format:
     ```
     2020-01-22,China,548,17
     2020-03-01,Italy,1701,41
     ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the web interface** at `http://localhost:5000`

5. **Enter a country name** (e.g., "Italy") and view results:
   - Total Cases
   - Total Deaths
   - Peak Infection Day

## Technical Implementation

The core functionality is implemented in `app.py` which:
- Uses Flask for web interface
- Leverages pandas for data analysis
- Optionally stores results using APSW/SQLite

```python
# Core analysis function
def analyze_data(country_name):
    country_data = df[df['country'].str.lower() == country_name.lower()]
    summary = {
        'total_cases': int(country_data['cases'].sum()),
        'total_deaths': int(country_data['deaths'].sum()),
        'peak_day': str(country_data.loc[country_data['cases'].idxmax()]['date'].date())
    }
    return summary
```

## Requirements

- Python 3.x
- Flask
- pandas
- APSW (optional for database storage)

Install requirements with:
```bash
pip install flask pandas apsw
```

## Future Enhancements

- Add visualization of case trends
- Support for date-range filtering
- Comparative analysis between countries
- Automated data updates from public sources
