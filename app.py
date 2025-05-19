from flask import Flask, render_template_string, request
import pandas as pd
import apsw  # Opsional: jika tidak ada, gunakan sqlite3 atau abaikan

app = Flask(__name__)

# Baca data COVID dari CSV
df = pd.read_csv('covid_data.csv', parse_dates=['date'])

# Fungsi analisis sederhana
def analyze_data(country_name):
    country_data = df[df['country'].str.lower() == country_name.lower()]
    if country_data.empty:
        return None
    summary = {
        'total_cases': int(country_data['cases'].sum()),
        'total_deaths': int(country_data['deaths'].sum()),
        'peak_day': str(country_data.loc[country_data['cases'].idxmax()]['date'].date())
    }
    return summary

# Simpan ke database SQLite (opsional dengan APSW)
def save_to_db(country, summary):
    try:
        conn = apsw.Connection("covid_analysis.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                country TEXT,
                total_cases INTEGER,
                total_deaths INTEGER,
                peak_day TEXT
            )
        """)
        cursor.execute("INSERT INTO analysis VALUES (?, ?, ?, ?)", 
                       (country, summary['total_cases'], summary['total_deaths'], summary['peak_day']))
    except Exception as e:
        print("APSW error:", e)

# Flask route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        country = request.form['country']
        result = analyze_data(country)
        if result:
            try:
                save_to_db(country, result)
            except:
                pass  # abaikan jika APSW tidak tersedia
    return render_template_string('''
        <h1>COVID-19 Country Analysis</h1>
        <form method="post">
            Country: <input name="country" required>
            <button type="submit">Analyze</button>
        </form>
        {% if result %}
            <h2>Result for {{request.form['country']}}</h2>
            <p>Total Cases: {{result.total_cases}}</p>
            <p>Total Deaths: {{result.total_deaths}}</p>
            <p>Peak Day: {{result.peak_day}}</p>
        {% elif request.method == 'POST' %}
            <p>No data found for that country.</p>
        {% endif %}
    ''', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
