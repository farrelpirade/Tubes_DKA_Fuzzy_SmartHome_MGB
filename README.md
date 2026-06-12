# Smart Home Energy Efficiency Evaluator

> A smart home energy efficiency evaluation system using a Hybrid approach: Sugeno Fuzzy Logic (Knowledge-Driven) & Random Forest (Data-Driven). Built entirely from scratch without fuzzy libraries and wrapped in an interactive Glassmorphism-style web interface.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)

---

## Project Description

This project evaluates energy efficiency metrics using two algorithmic approaches:

1. **Knowledge-Driven (Sugeno Fuzzy Logic):** Built from scratch (without built-in fuzzy libraries) using 25 knowledge base rules to translate environmental sensor values (Temperature and Humidity) into an efficiency index.
2. **Data-Driven (Hybrid Machine Learning):** Utilizes the **Random Forest Regressor** algorithm to correct and optimize the output from the Fuzzy system, proven to significantly reduce the _Mean Absolute Error_ (MAE) on the test data.

Data sourced from the **[Appliances Energy Prediction Data Set](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction)** (UCI Machine Learning Repository).

## Key Features

- **Standalone Fuzzy Algorithm:** Fuzzification, Inference Engine (MIN/MAX), and Defuzzification (Sugeno) are built entirely using basic Python functions.
- **Hybrid Machine Learning:** Integration of the Fuzzy output as an _expert knowledge feature_ into the Random Forest model.
- **Interactive Dashboard:** A modern web interface using Streamlit with a Glassmorphism design (transparent cards) and a Cyberpunk/Neon Dark Mode color palette.
- **Real-time Prediction:** Instant comparison of parameters and evaluation results (Fuzzy vs. Hybrid) updated dynamically via slider manipulation.

## How to Run Locally

**1. Clone the Repository**

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

**2. Install Dependencies**
Ensure you have Python installed, then run:

```bash
pip install streamlit pandas scikit-learn joblib
```

**3. Run the Streamlit App**

```bash
python -m streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`.

## Repository Structure

- `app.py` — Main Streamlit web app script and Fuzzy Logic functions.
- `model_hybrid.pkl` — Trained Random Forest model (exported from the Colab notebook).
- `Tubes_DKA_Fuzzy_SmartHome.ipynb` — Google Colab containing data exploration, model training, membership function visualizations, and comparative performance analysis.

## Development Team

| Name                 | Student ID (NIM) |
| :------------------- | :--------------- |
| Farrel Malik Pirade  | 103012400068     |
| Ghifari Nurwafi Yoga | 103012400020     |
| Sava Arsya Syandana  | 103012400043     |
