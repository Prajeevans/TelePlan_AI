# TelePlan AI - Telecom Network Planner & RF Propagation Simulator

TelePlan AI is an interactive, data-driven network planning and RF (Radio Frequency) propagation simulation tool. It is designed to assist telecom engineers and data scientists in simulating signal strengths, planning cellular tower deployments, analyzing network coverage, and building machine learning models for signal quality prediction.

The application combines traditional empirical propagation models with interactive web GIS visualizations (Streamlit + Folium) and synthetic dataset generation pipelines.

---

## 🚀 Key Features

* **Interactive Multi-Page Streamlit Dashboard**: Easily place base stations (towers) on a map, adjust transmitter/receiver settings, and run network simulations dynamically.
* **RF Propagation Modeling**:
  * **Free Space Path Loss (FSPL)**: Theoretical line-of-sight propagation modeling.
  * **Okumura-Hata Model**: Empirical path loss prediction for frequencies between $150\text{ MHz}$ and $1500\text{ MHz}$, optimized for Urban, Suburban, and Rural environment categories.
* **Comprehensive Link Budget Calculator**: Simulates signal attenuation and gains, accounting for:
  * Transmitter power and antenna gain.
  * Cable, connector, and miscellaneous hardware losses.
  * Environmental factors (rain attenuation, shadow fading).
  * Receiver antenna specifications.
* **Geospatial Visualizations**:
  * Base station location tagging.
  * Signal intensity heatmaps based on predicted RSRP (Reference Signal Received Power).
  * **Best-Server Network Map**: Boundary plotting showing which base station provides the strongest signal at any given coordinate.
  * Coverage grid point classifications (Excellent, Good, Fair, Poor).
* **Telecom Data Simulator**: Simulates high-fidelity datasets including user distributions, weather effects, traffic load, base station configurations, and terrain/building density.
* **Machine Learning Pipelines**: Pre-configured notebooks and scripts for exploratory data analysis (EDA), data synthesis, and ML-based path loss or RSRP prediction models.

---

## 📂 Project Structure

```directory
TelePlan-AI/
├── app.py                   # Main entry point for the Streamlit dashboard
├── requirements.txt         # Project dependencies (Streamlit, Folium, Numpy, Pandas, etc.)
├── models/                  # Core scientific & RF modeling engines
│   ├── config.py            # Global default radio, antenna, and environmental configurations
│   ├── propagation.py       # Base classes and implementations of FSPL & Okumura-Hata models
│   ├── link_budget.py       # Link budget calculations (Tx power, gains, losses -> Rx power)
│   ├── coverage.py          # CoverageEngine to generate prediction matrices around towers
│   ├── coverage_grid.py     # Grid generation and RSRP computations for geographic areas
│   ├── network.py           # NetworkPlanner class for best-server and cell-boundary analysis
│   ├── path_loss.py         # Baseline FSPL and Log-Distance path loss functions
│   ├── rsrp.py              # RSRPEngine for power-to-RSRP conversion and quality classification
│   └── signal.py            # High-level signal calculator wrappers
├── simulator/               # Synthetic telecom dataset generator components
│   ├── dataset_builder.py   # Main simulation loop compiling weather, traffic, user, and tower data
│   ├── tower_generator.py   # Synthesizer for base station coordinates and parameters
│   ├── user_generator.py    # Synthesizer for subscriber/user coordinates
│   ├── environment_generator.py # Synthesizer for terrain types, shadowing, and densities
│   ├── weather_generator.py # Weather-related attenuation loss modeler
│   └── traffic_generator.py # Network congestion and user traffic simulator
├── ml/                      # Machine learning training datasets and scripts
│   ├── dataset_generator.py # Fast dataset generator for training RSRP prediction models
│   └── saved_models/        # Storage directory for trained serialized ML models
├── notebooks/               # Jupyter notebooks for analysis and development
│   ├── 01_Data_Exploration.ipynb # Initial telecom dataset exploration
│   ├── 02_Telecom_EDA.ipynb      # Detailed exploratory data analysis
│   ├── 04_Model_Training.ipynb   # Scikit-learn model training pipeline
├── utils/                   # Shared auxiliary helper scripts
│   ├── calculations.py      # GPS coordinate math (Haversine formula)
│   ├── map_utils.py         # Folium map drawing (markers, heatmaps, circles)
│   └── signal_classifier.py # Categorizes received power signals to quality levels (colors/labels)
└── pages/                   # Multi-page Streamlit dashboards (placeholders for expansion)
    ├── Dashboard.py
    ├── Coverage_Map.py
    ├── Analytics.py
    ├── Tower_Manager.py
    └── AI_Optimizer.py
```

---

## 📊 Scientific & Mathematical Background

### 1. Free Space Path Loss (FSPL)
Used as the basic line-of-sight propagation equation:
$$\text{FSPL (dB)} = 32.44 + 20\log_{10}(d) + 20\log_{10}(f)$$
Where:
* $d$ = distance in kilometers ($\text{km}$)
* $f$ = frequency in Megahertz ($\text{MHz}$)

### 2. Okumura-Hata Model
Predicts path loss in urban, suburban, and rural environments:
$$L_{50}\text{ (urban) (dB)} = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d)$$
Where:
* $f$ = frequency ($150\text{ MHz} \le f \le 1500\text{ MHz}$)
* $h_b$ = base station antenna height in meters ($30\text{ m} \le h_b \le 200\text{ m}$)
* $h_m$ = mobile antenna height in meters ($1\text{ m} \le h_m \le 10\text{ m}$)
* $d$ = link distance in kilometers ($\text{km}$)
* $a(h_m)$ = mobile antenna height correction factor:
  $$a(h_m) = (1.1\log_{10}(f) - 0.7)h_m - (1.56\log_{10}(f) - 0.8)$$
* Adjustments are applied to $L_{50}$ for suburban and rural settings depending on the selected environment.

### 3. Received Power & Link Budget
$$\text{Rx Power (dBm)} = \text{Tx Power (dBm)} + \text{Tx Gain (dBi)} + \text{Rx Gain (dBi)} - \text{Total Losses (dB)}$$
Where:
$$\text{Total Losses (dB)} = \text{Path Loss} + \text{Tx Cable Loss} + \text{Tx Connector Loss} + \text{Shadow Fading} + \text{Rain Attenuation} + \text{Misc Losses} + \text{Rx Cable Loss}$$

---

## 🛠️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd TelePlan-AI
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Ensure you have all the required libraries installed. You can install them by running:
   ```bash
   pip install streamlit folium streamlit-folium numpy pandas scikit-learn matplotlib jinja2
   ```

---

## 💻 How to Run the App

1. Make sure your virtual environment is active.
2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to the local address provided (usually `http://localhost:8501`).

---

## 📈 Running the Simulator & ML Pipeline

### Generate Telecom Datasets
To run the high-fidelity simulator and generate a synthetic telecom dataset for training ML models:
```bash
python simulator/dataset_builder.py
```
This script runs a simulation across 100,000 samples and generates `data/telecom_dataset.csv`.

To generate the faster, lightweight RSRP dataset:
```bash
python ml/dataset_generator.py
```
This generates `data/rsrp_dataset.csv`.
