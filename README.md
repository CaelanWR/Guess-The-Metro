# Guess the Metro 🏙️

An interactive Streamlit game where players identify U.S. metropolitan areas using workforce data clues.

## About

**Guess the Metro** challenges players to identify a mystery U.S. metropolitan area using economic and workforce data hints. Players start with 50 points and 5 guesses, with each incorrect guess revealing a new hint and costing 10 points.

### Features

- 🎯 5 metropolitan areas to discover: Memphis, Charlotte, Washington DC, Pittsburgh, and Houston
- 📊 Interactive data visualizations using real workforce metrics
- 🏆 Score tracking and performance comparison
- 🎨 Modern, responsive UI with smooth animations

### Hints Include:

1. **Industry Breakdown** - Treemap of employment by sector and subsector
2. **Salary Ranges** - Salary distributions across major industries
3. **Employment Growth** - Historical employment trends
4. **Metro Comparison** - Percentile rankings vs other U.S. metros
5. **Top Employers** - Largest employers by education level

## Running Locally

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/guess-the-metro.git
cd guess-the-metro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
guess-the-metro/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── city-data-chart.png        # Logo image
├── game_data/                 # Data files for each metro
│   ├── memphis/
│   │   ├── industry.csv
│   │   ├── salary.csv
│   │   ├── noncollege_employers.csv
│   │   ├── college_employers.csv
│   │   ├── time_series.csv
│   │   ├── education.csv
│   │   └── growth.csv
│   ├── charlotte/
│   ├── dc/
│   ├── pittsburgh/
│   └── houston/
└── README.md
```

## Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set main file path to `app.py`
7. Click "Deploy"

## Data Sources

The game uses simulated workforce data based on real labor market patterns. Data includes:
- Employment by industry sector and subsector
- Salary ranges and distributions
- Employment growth trends
- Top employers by education requirement
- Metro-level comparative statistics

## Technologies Used

- **Streamlit** - Web app framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Python** - Backend logic

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Contact

For questions or feedback, please open an issue on GitHub.
