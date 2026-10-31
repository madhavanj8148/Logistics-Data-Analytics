# Logistics Data Analytics – End-to-End Analytics & Prediction System
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Domain](https://img.shields.io/badge/Domain-Supply%20Chain%20%26%20Logistics-orange.svg)]()
[![Repository](https://img.shields.io/badge/GitHub-Logistics--Data--Analytics-blueviolet.svg)](https://github.com/madhavanj8148/Logistics-Data-Analytics.git)

---

## 1. Project Title & Overview
**Logistics Performance Analysis and Delivery Delay Prediction: An End-to-End Analytical Study of Multi-Partner Supply Chain Operations in India**

* **Author:** Paladugula Madhavan
* **Institution:** Vellore Institute of Technology, Andhra Pradesh
* **Email:** madhavanpaladugula2311@gmail.com
* **Role:** Logistics Data Analyst Intern
* **Repository:** `https://github.com/madhavanj8148/Logistics-Data-Analytics.git`

This project delivers an enterprise-grade, end-to-end data analytics and predictive modeling system evaluating third-party logistics (3PL) delivery operations across India. Analyzing 25,000 multi-partner transactional records, the project quantifies delivery delays, models cost structures, evaluates the impact of weather and traffic congestion, and builds machine learning models to forecast shipment delays before transit begins.

---

## 2. Project Objectives
1. **Analyze Delivery Performance:** Benchmark delivery reliability, on-time rates, and latency across 9 major logistics carriers in India.
2. **Identify Delay Drivers:** Diagnose root causes of shipment delays across traffic tiers, regional topographies, and weather conditions.
3. **Analyze Transportation Costs:** Assess delivery expenditure by distance, package weight, vehicle modality, and service tiers.
4. **Evaluate Carrier Operations:** Compare delivery partners (Delhivery, Blue Dart, DHL, FedEx, Shadowfax, Xpressbees, Ekart, Ecom Express, Amazon Logistics) on cost, SLA compliance, and customer satisfaction.
5. **Mitigate Target Leakage:** Engineer preprocessing and classification workflows that strictly exclude post-event attributes (`delivery_status`) to ensure real-world utility at dispatch time.
6. **Deploy Machine Learning Models:** Implement interpretable baselines (Logistic Regression) and non-linear ensembles (Random Forest) for delay prediction.
7. **Generate Actionable Intelligence:** Formulate evidence-based recommendations for dynamic dispatch buffering, partner contract renegotiation, and fleet assignment.

---

## 3. Project Architecture & Folder Structure

```text
Logistics-Data-Analytics/
│
├── dataset/
│   ├── raw/
│   │   └── Delivery Logistics Dataset (India – Multi-Partner).xlsx  # 25,000 records × 15 features
│   └── processed/                # Destination for cleaned, outlier-treated & normalized data
│
├── notebooks/                    # Jupyter notebooks for interactive analysis & modeling
│   ├── Week1_Strategic_Planning.ipynb
│   └── Week2_Data_Preprocessing.ipynb
│
├── src/                          # Modular production Python pipeline scripts
│   ├── data_collection.py        # Dataset metadata and ingestion specifications
│   ├── data_exploration.py       # Automated dataset profiling & exploratory summaries
│   ├── data_cleaning.py          # Whitespace stripping, type casting & duplicate handling
│   ├── missing_values.py         # Missing value diagnostics & statistical imputation
│   ├── outlier_detection.py      # Statistical outlier detection (IQR, Z-Score) & capping
│   ├── normalization.py          # Feature scaling (Min-Max & StandardScaler)
│   └── preprocessing_pipeline.py # End-to-end unified ETL and transformation pipeline
│
├── reports/                      # Visual and tabular analytical outputs
│   ├── charts/                   # High-resolution figures and correlation heatmaps
│   ├── tables/                   # KPI scorecards, partner rankings & data dictionary
│   └── outputs/                  # Execution logs, metrics & model evaluation summaries
│
├── documentation/                # Formal academic & managerial DOCX reports
│   ├── Week1_Strategic_Planning_Report.docx
│   ├── Week2_Data_Preprocessing_Report.docx
│   └── Combined_Project_Report.docx
│
├── requirements.txt              # Environment dependencies
├── README.md                     # Project documentation & guidelines
└── .gitignore                    # Version control exclusion rules
```

---

## 4. Dataset Description
* **Domain:** Logistics, Freight Transportation & E-commerce Supply Chain
* **Geographical Coverage:** India (West, Central, East, North, South regions)
* **Sample Size:** 25,000 transactional delivery records
* **Feature Count:** 15 columns
* **File Format:** Microsoft Excel (`.xlsx`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `delivery_id` | Float / ID | Unique identifier for each shipment record |
| `delivery_partner` | String | Third-party carrier partner (e.g., Delhivery, FedEx, DHL) |
| `package_type` | String | Product category (e.g., Electronics, Cosmetics, Clothing) |
| `vehicle_type` | String | Transportation modality (Bike, EV Van, Van, Truck) |
| `delivery_mode` | String | Service tier (Same Day, Express, Two Day, Standard) |
| `region` | String | Operational territory (North, South, East, West, Central) |
| `weather_condition` | String | Environmental condition (Clear, Rainy, Foggy, Cold, Stormy) |
| `distance_km` | Float | Total transit distance in kilometers (3.6 km to 297.1 km) |
| `package_weight_kg`| Float | Parcel physical weight in kilograms (0.5 kg to 50.0 kg) |
| `expected_time_hours`| Float | Planned SLA delivery duration in hours |
| `delayed` | String | Target label indicating whether shipment was delayed (`yes`/`no`) |
| `delivery_status` | String | Final operational status (`delivered`, `delayed`, `failed`) |
| `delivery_rating` | Integer | Customer satisfaction rating (1 to 5 scale) |
| `delivery_cost` | Float | Total transportation cost in Indian Rupees (INR) |
| `traffic_Level` | String | Recorded road traffic congestion (Low, Medium, High) |

---

## 5. Technology Stack

* **Language:** Python 3.11+ / 3.14
* **Data Processing & Analytics:** `pandas`, `numpy`
* **Data Visualization:** `matplotlib`, `seaborn`
* **Machine Learning & Pipeline Modeling:** `scikit-learn`
* **File Handling & Excel Automation:** `openpyxl`
* **Document Generation:** `python-docx`
* **Version Control:** Git & GitHub

---

## 6. Installation & Execution Instructions

### Prerequisites
Ensure Python 3.10+ and Git are installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/madhavanj8148/Logistics-Data-Analytics.git
cd Logistics-Data-Analytics
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Analytics
* **Interactive Notebooks:** Launch Jupyter Lab or VS Code and open `notebooks/Week1_Strategic_Planning.ipynb` or `notebooks/Week2_Data_Preprocessing.ipynb`.
* **Automated Python Pipeline:** Run modular scripts from `src/` to execute data cleaning, outlier capping, and feature normalization.

---

## 7. Project Progress & Roadmap

| Stage / Phase | Scope Description | Status |
| :--- | :--- | :---: |
| **Setup & Repo Init** | Directory structure, `.gitignore`, `requirements.txt`, README | **COMPLETED** |
| **Week 1 – Phase 1** | Project Introduction, Problem Statement, Scope & Significance | **COMPLETED** |
| **Week 1 – Phase 2** | Project Objectives Definition & KPI Mathematical Formulas | **COMPLETED** |
| **Week 1 – Phase 3** | Dataset Selection, Quality Profiling & Metadata Verification | **COMPLETED** |
| **Week 1 – Phase 4** | Key Performance Indicators (KPI) Calculations & Benchmark | **COMPLETED** |
| **Week 1 – Phase 5** | Technical & Environment Requirements Specification | **COMPLETED** |
| **Week 1 – Phase 6** | Project Timeline & Milestone Mapping | **COMPLETED** |
| **Week 1 Report** | Word Document Generation (`Week1_Strategic_Planning_Report.docx`) | **COMPLETED** |
| **Week 2 – Phase 7** | Data Collection Simulation & Data Dictionary | **COMPLETED** |
| **Week 2 – Phase 8** | Exploratory Data Profiling & Diagnostic Metrics | **COMPLETED** |
| **Week 2 – Phase 9** | Data Sanitation, Type Coercion & Duplicate Handling | **COMPLETED** |
| **Week 2 – Phase 10** | Missing Value Diagnostics & Statistical Imputation | **COMPLETED** |
| **Week 2 – Phase 11** | Statistical Outlier Detection (IQR / Z-Score) & Treatment | **COMPLETED** |
| **Week 2 – Phase 12** | Feature Scaling (Min-Max Scaling & Standardization) | **COMPLETED** |
| **Week 2 – Phase 13** | Reusable Automated Preprocessing Pipeline (`src/`) | **COMPLETED** |
| **Week 2 – Phase 14** | Final Data Quality Scorecard, Business Rules & Leakage Audit | **COMPLETED** |
| **Week 2 Report** | Word Document Generation (`Week2_Final_Complete_Report.docx`) | **COMPLETED** |
| **Week 2 Audit** | Master QA & Verification Report (`Week2_Complete_Project_Audit_Report.docx`) | **COMPLETED** |
| **Week 2 Readiness**| Final Data Readiness Report (`Week2_Final_Data_Readiness_Report.docx`) | **COMPLETED** |
| **Final Delivery** | Combined Academic & Industry Documentation (`Combined_Project_Report.docx`) | Upcoming |

---

## 8. Documentation Links & Deliverables
* **Week 1 Strategic Planning Document:** `documentation/Week1_Strategic_Planning_Report.docx`
* **Week 2 Dataset Collection Report:** `documentation/Week2_Dataset_Collection_Report.docx`
* **Week 2 Data Cleaning Report:** `documentation/Week2_Data_Cleaning_Report.docx`
* **Week 2 Missing Value Analysis Report:** `documentation/Week2_Missing_Value_Analysis_Report.docx`
* **Week 2 Outlier Detection Report:** `documentation/Week2_Outlier_Detection_Report.docx`
* **Week 2 Data Normalization Report:** `documentation/Week2_Data_Normalization_Report.docx`
* **Week 2 Complete Preprocessing Pipeline Report:** `documentation/Week2_Complete_Preprocessing_Pipeline_Report.docx`
* **Week 2 Master Submission Report:** `documentation/Week2_Final_Submission_Report.docx`
* **Week 2 Requirement Mapping Matrix:** `documentation/Week2_Assignment_Requirement_Mapping.csv`
* **Week 2 Final Report Generation Summary:** `documentation/Week2_Final_Report_Generation_Summary.md`
* **Week 2 Final Data Readiness Report:** `documentation/Week2_Final_Data_Readiness_Report.docx`
* **Week 2 Master Audit Report:** `documentation/Week2_Complete_Project_Audit_Report.docx`
* **Week 2 Final Technical Correction Log:** `documentation/Week2_Final_Correction_Log.docx`
* **Week 2 Final Complete Report:** `documentation/Week2_Final_Complete_Report.docx`
* **Final Consolidated Project Report:** `documentation/Combined_Project_Report.docx`
* **Cleaned & Processed Dataset:** `dataset/processed/`
* **Quality Scorecards & Validation Tables:** `reports/tables/`
* **Charts & Visualizations:** `reports/charts/`

---

## 9. Future Enhancements
* Integration of real-time GPS telematic feeds for live ETA re-calibration.
* Development of interactive Streamlit / PowerBI operational control towers.
* Deployment of containerized FastAPI inference endpoints for dynamic dispatch risk scoring.
