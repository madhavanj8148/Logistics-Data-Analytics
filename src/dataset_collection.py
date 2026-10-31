"""
Logistics Data Analytics - Step 1: Dataset Collection and Verification
Author: Paladugula Madhavan
Institution: Vellore Institute of Technology, Andhra Pradesh
Role: Logistics Data Analyst Intern
Track: Week 2 - Data Collection, Cleaning & Preprocessing
"""

import os
import glob
import pandas as pd
import numpy as np

def find_raw_dataset(base_dir=None):
    """
    Search for and verify the original logistics Excel dataset.
    Ensures the original dataset is never modified or overwritten.
    """
    if base_dir is None:
        # Determine base directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    candidates = [
        os.path.join(base_dir, 'dataset', 'raw', 'Delivery Logistics Dataset (India \u2013 Multi-Partner).xlsx'),
        os.path.join(base_dir, 'dataset', 'raw', 'Delivery Logistics Dataset (India - Multi-Partner).xlsx'),
        os.path.join(base_dir, '..', 'dataset', 'raw', 'Delivery Logistics Dataset (India \u2013 Multi-Partner).xlsx'),
        os.path.join(base_dir, '..', 'dataset', 'raw', 'Delivery Logistics Dataset (India - Multi-Partner).xlsx'),
        os.path.join(base_dir, '..', 'File', 'Delivery Logistics Dataset (India \u2013 Multi-Partner).xlsx'),
        os.path.join(base_dir, '..', 'DATA', 'Delivery Logistics Dataset (India \u2013 Multi-Partner).xlsx'),
    ]
    
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
            
    # Pattern search
    patterns = [
        os.path.join(base_dir, 'dataset', 'raw', '*.xlsx'),
        os.path.join(base_dir, '..', 'dataset', 'raw', '*.xlsx'),
        os.path.join(base_dir, '..', 'File', '*.xlsx'),
        os.path.join(base_dir, '..', 'DATA', '*.xlsx'),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            for m in matches:
                if 'Delivery Logistics' in m or 'Multi-Partner' in m:
                    return m
                    
    raise FileNotFoundError("CRITICAL ERROR: Original logistics dataset could not be located in dataset/raw/. Please upload the original dataset.")

def load_and_verify_dataset(file_path):
    """
    Loads the original dataset into a Pandas DataFrame without modifying raw data.
    Verifies dimensions, columns, and data integrity.
    """
    print("=" * 70)
    print("LOGISTICS DATA ANALYTICS: DATASET COLLECTION & VERIFICATION")
    print("=" * 70)
    print(f"Loading raw dataset from: {file_path}")
    
    df = pd.read_excel(file_path)
    
    expected_rows = 25000
    expected_cols = 15
    actual_rows, actual_cols = df.shape
    
    print(f"\n[Verification] Actual Dimensions: {actual_rows:,} rows, {actual_cols} columns")
    assert actual_rows == expected_rows, f"Row count mismatch! Expected {expected_rows}, got {actual_rows}"
    assert actual_cols == expected_cols, f"Column count mismatch! Expected {expected_cols}, got {actual_cols}"
    print("[Verification Passed] Exact dimensions (25,000 x 15) confirmed!")
    
    expected_columns = [
        'delivery_id', 'delivery_partner', 'package_type', 'vehicle_type', 'delivery_mode',
        'region', 'weather_condition', 'distance_km', 'package_weight_kg', 'expected_time_hours',
        'delayed', 'delivery_status', 'delivery_rating', 'delivery_cost', 'traffic_Level'
    ]
    
    missing_cols = set(expected_columns) - set(df.columns)
    assert len(missing_cols) == 0, f"Missing columns detected: {missing_cols}"
    print("[Verification Passed] All 15 required domain columns are present!")
    
    return df

def generate_dataset_overview(df, file_path, output_paths):
    """
    Generates a comprehensive dataset overview table and exports to CSV.
    """
    delayed_counts = df['delayed'].value_counts()
    file_size_bytes = os.path.getsize(file_path)
    
    overview_data = [
        {"Attribute": "Project Title", "Value": "Logistics Performance Analysis and Delivery Delay Prediction"},
        {"Attribute": "Dataset File Name", "Value": os.path.basename(file_path)},
        {"Attribute": "File Size (KB)", "Value": f"{file_size_bytes / 1024:.2f} KB"},
        {"Attribute": "Domain / Industry", "Value": "Supply Chain Logistics & Transportation Operations"},
        {"Attribute": "Geographic Scope", "Value": "India (Multi-Regional: North, South, East, West, Central)"},
        {"Attribute": "Total Record Count (Rows)", "Value": f"{df.shape[0]:,}"},
        {"Attribute": "Total Feature Count (Columns)", "Value": str(df.shape[1])},
        {"Attribute": "Total Missing Values (Cells)", "Value": str(df.isnull().sum().sum())},
        {"Attribute": "Exact Duplicate Rows", "Value": str(df.duplicated().sum())},
        {"Attribute": "Unique Delivery IDs", "Value": f"{df['delivery_id'].nunique():,}"},
        {"Attribute": "Repeated Delivery IDs", "Value": f"{df['delivery_id'].duplicated().sum()} (Requires Week 2 investigation)"},
        {"Attribute": "Total Logistics Partners", "Value": f"{df['delivery_partner'].nunique()} ({', '.join(df['delivery_partner'].unique()[:5])}...)"},
        {"Attribute": "Total Vehicle Types", "Value": f"{df['vehicle_type'].nunique()} ({', '.join(df['vehicle_type'].unique())})"},
        {"Attribute": "Total Delivery Modes", "Value": f"{df['delivery_mode'].nunique()} ({', '.join(df['delivery_mode'].unique())})"},
        {"Attribute": "Total Package Categories", "Value": f"{df['package_type'].nunique()} ({', '.join(df['package_type'].unique()[:5])}...)"},
        {"Attribute": "Weather Condition Categories", "Value": f"{df['weather_condition'].nunique()} ({', '.join(df['weather_condition'].unique())})"},
        {"Attribute": "Traffic Levels", "Value": f"{df['traffic_Level'].nunique()} ({', '.join(df['traffic_Level'].unique())})"},
        {"Attribute": "Target Variable", "Value": "delayed (Binary: yes / no)"},
        {"Attribute": "Target Distribution (No Delays)", "Value": f"{delayed_counts.get('no', 0):,} ({delayed_counts.get('no', 0)/len(df)*100:.2f}%)"},
        {"Attribute": "Target Distribution (Delays)", "Value": f"{delayed_counts.get('yes', 0):,} ({delayed_counts.get('yes', 0)/len(df)*100:.2f}%)"},
        {"Attribute": "Distance Range (km)", "Value": f"{df['distance_km'].min():.1f} km to {df['distance_km'].max():.1f} km (Mean: {df['distance_km'].mean():.2f} km)"},
        {"Attribute": "Package Weight Range (kg)", "Value": f"{df['package_weight_kg'].min():.2f} kg to {df['package_weight_kg'].max():.2f} kg (Mean: {df['package_weight_kg'].mean():.2f} kg)"},
        {"Attribute": "Expected Transit Time Range", "Value": f"{df['expected_time_hours'].min():.2f} hrs to {df['expected_time_hours'].max():.2f} hrs (Mean: {df['expected_time_hours'].mean():.2f} hrs)"},
        {"Attribute": "Delivery Cost Range (INR)", "Value": f"INR {df['delivery_cost'].min():.2f} to INR {df['delivery_cost'].max():.2f} (Mean: INR {df['delivery_cost'].mean():.2f})"},
        {"Attribute": "Customer Rating Range", "Value": f"{df['delivery_rating'].min()} to {df['delivery_rating'].max()} (Mean: {df['delivery_rating'].mean():.2f} / 5.0)"}
    ]
    
    overview_df = pd.DataFrame(overview_data)
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        overview_df.to_csv(p, index=False)
        print(f"Dataset overview saved to: {p}")
        
    return overview_df

def generate_data_dictionary(df, output_paths):
    """
    Generates a formal data dictionary detailing column names, data types,
    domain definitions, ranges, and operational roles.
    """
    dictionary_entries = [
        {
            "Column Name": "delivery_id",
            "Data Type": "float64",
            "Non-Null Count": df['delivery_id'].count(),
            "Null Count": df['delivery_id'].isnull().sum(),
            "Unique Count": df['delivery_id'].nunique(),
            "Range / Categories": f"Min: {df['delivery_id'].min():.2f}, Max: {df['delivery_id'].max():.2f}",
            "Business Definition": "Unique operational identifier assigned to each shipment transaction.",
            "Operational Role": "Primary Identifier (Exclude from predictive ML feature sets)"
        },
        {
            "Column Name": "delivery_partner",
            "Data Type": "object (string)",
            "Non-Null Count": df['delivery_partner'].count(),
            "Null Count": df['delivery_partner'].isnull().sum(),
            "Unique Count": df['delivery_partner'].nunique(),
            "Range / Categories": ", ".join(df['delivery_partner'].unique()),
            "Business Definition": "Third-party logistics carrier managing the parcel dispatch and fulfillment.",
            "Operational Role": "Categorical Feature (Benchmark partner operational SLA)"
        },
        {
            "Column Name": "package_type",
            "Data Type": "object (string)",
            "Non-Null Count": df['package_type'].count(),
            "Null Count": df['package_type'].isnull().sum(),
            "Unique Count": df['package_type'].nunique(),
            "Range / Categories": ", ".join(df['package_type'].unique()),
            "Business Definition": "Product commodity classification of the delivered merchandise.",
            "Operational Role": "Categorical Feature (Evaluate handling constraints and latency)"
        },
        {
            "Column Name": "vehicle_type",
            "Data Type": "object (string)",
            "Non-Null Count": df['vehicle_type'].count(),
            "Null Count": df['vehicle_type'].isnull().sum(),
            "Unique Count": df['vehicle_type'].nunique(),
            "Range / Categories": ", ".join(df['vehicle_type'].unique()),
            "Business Definition": "Fleet modality utilized for the delivery route (bike, van, truck, EV).",
            "Operational Role": "Categorical Feature (Fleet assignment and capacity modeling)"
        },
        {
            "Column Name": "delivery_mode",
            "Data Type": "object (string)",
            "Non-Null Count": df['delivery_mode'].count(),
            "Null Count": df['delivery_mode'].isnull().sum(),
            "Unique Count": df['delivery_mode'].nunique(),
            "Range / Categories": ", ".join(df['delivery_mode'].unique()),
            "Business Definition": "Service tier SLA requested by customer (same day, express, two day, standard).",
            "Operational Role": "Categorical Feature (SLA benchmark and prioritization)"
        },
        {
            "Column Name": "region",
            "Data Type": "object (string)",
            "Non-Null Count": df['region'].count(),
            "Null Count": df['region'].isnull().sum(),
            "Unique Count": df['region'].nunique(),
            "Range / Categories": ", ".join(df['region'].unique()),
            "Business Definition": "Geographical territory in India where the fulfillment took place.",
            "Operational Role": "Categorical Feature (Regional logistics disparity analysis)"
        },
        {
            "Column Name": "weather_condition",
            "Data Type": "object (string)",
            "Non-Null Count": df['weather_condition'].count(),
            "Null Count": df['weather_condition'].isnull().sum(),
            "Unique Count": df['weather_condition'].nunique(),
            "Range / Categories": ", ".join(df['weather_condition'].unique()),
            "Business Definition": "Ambient weather condition recorded during the shipment route.",
            "Operational Role": "Categorical Feature (Environmental vulnerability modeling)"
        },
        {
            "Column Name": "distance_km",
            "Data Type": "float64",
            "Non-Null Count": df['distance_km'].count(),
            "Null Count": df['distance_km'].isnull().sum(),
            "Unique Count": df['distance_km'].nunique(),
            "Range / Categories": f"Min: {df['distance_km'].min():.1f} km, Max: {df['distance_km'].max():.1f} km, Mean: {df['distance_km'].mean():.2f} km",
            "Business Definition": "Total road distance in kilometers between fulfillment center and customer address.",
            "Operational Role": "Numerical Feature (Primary route distance metric)"
        },
        {
            "Column Name": "package_weight_kg",
            "Data Type": "float64",
            "Non-Null Count": df['package_weight_kg'].count(),
            "Null Count": df['package_weight_kg'].isnull().sum(),
            "Unique Count": df['package_weight_kg'].nunique(),
            "Range / Categories": f"Min: {df['package_weight_kg'].min():.2f} kg, Max: {df['package_weight_kg'].max():.2f} kg, Mean: {df['package_weight_kg'].mean():.2f} kg",
            "Business Definition": "Physical gross weight of the package in kilograms.",
            "Operational Role": "Numerical Feature (Vehicle payload and handling factor)"
        },
        {
            "Column Name": "expected_time_hours",
            "Data Type": "float64",
            "Non-Null Count": df['expected_time_hours'].count(),
            "Null Count": df['expected_time_hours'].isnull().sum(),
            "Unique Count": df['expected_time_hours'].nunique(),
            "Range / Categories": f"Min: {df['expected_time_hours'].min():.2f} hrs, Max: {df['expected_time_hours'].max():.2f} hrs, Mean: {df['expected_time_hours'].mean():.2f} hrs",
            "Business Definition": "Estimated planned delivery duration in hours communicated to the customer.",
            "Operational Role": "Numerical Feature (Planned transit baseline; not actual duration)"
        },
        {
            "Column Name": "delayed",
            "Data Type": "object (string)",
            "Non-Null Count": df['delayed'].count(),
            "Null Count": df['delayed'].isnull().sum(),
            "Unique Count": df['delayed'].nunique(),
            "Range / Categories": "no: 18,331 (73.32%), yes: 6,669 (26.68%)",
            "Business Definition": "Ground-truth binary delay indicator provided in the shipment ledger.",
            "Operational Role": "Target Variable (Supervised classification objective)"
        },
        {
            "Column Name": "delivery_status",
            "Data Type": "object (string)",
            "Non-Null Count": df['delivery_status'].count(),
            "Null Count": df['delivery_status'].isnull().sum(),
            "Unique Count": df['delivery_status'].nunique(),
            "Range / Categories": ", ".join(df['delivery_status'].unique()),
            "Business Definition": "Final recorded delivery outcome (delivered, delayed, failed).",
            "Operational Role": "Target Leakage Candidate (MUST be excluded from features at dispatch time)"
        },
        {
            "Column Name": "delivery_rating",
            "Data Type": "int64",
            "Non-Null Count": df['delivery_rating'].count(),
            "Null Count": df['delivery_rating'].isnull().sum(),
            "Unique Count": df['delivery_rating'].nunique(),
            "Range / Categories": f"Min: {df['delivery_rating'].min()}, Max: {df['delivery_rating'].max()}, Mean: {df['delivery_rating'].mean():.2f}",
            "Business Definition": "Customer post-delivery satisfaction score recorded on a discrete 1 to 5 scale.",
            "Operational Role": "Evaluation KPI / Customer Experience Metric"
        },
        {
            "Column Name": "delivery_cost",
            "Data Type": "float64",
            "Non-Null Count": df['delivery_cost'].count(),
            "Null Count": df['delivery_cost'].isnull().sum(),
            "Unique Count": df['delivery_cost'].nunique(),
            "Range / Categories": f"Min: INR {df['delivery_cost'].min():.2f}, Max: INR {df['delivery_cost'].max():.2f}, Mean: INR {df['delivery_cost'].mean():.2f}",
            "Business Definition": "Total operational cost charged or incurred for the delivery trip in INR.",
            "Operational Role": "Numerical Feature / Financial KPI"
        },
        {
            "Column Name": "traffic_Level",
            "Data Type": "object (string)",
            "Non-Null Count": df['traffic_Level'].count(),
            "Null Count": df['traffic_Level'].isnull().sum(),
            "Unique Count": df['traffic_Level'].nunique(),
            "Range / Categories": ", ".join(df['traffic_Level'].unique()),
            "Business Definition": "Road congestion condition observed along the primary route segment.",
            "Operational Role": "Categorical Feature (Dynamic urban bottleneck indicator)"
        }
    ]
    
    dict_df = pd.DataFrame(dictionary_entries)
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        dict_df.to_csv(p, index=False)
        print(f"Data dictionary saved to: {p}")
        
    return dict_df

def document_simulation_methodology():
    """
    Returns the formal documentation of the data collection simulation methodology.
    """
    methodology_text = (
        "DATA COLLECTION SIMULATION METHODOLOGY:\n"
        "1. Context: In modern multi-carrier e-commerce fulfillment networks, operational shipment records\n"
        "   are aggregated from heterogeneous enterprise systems including Warehouse Management Systems (WMS),\n"
        "   Transport Management Systems (TMS), 3PL Carrier Webhooks/REST APIs, and On-board Vehicle Telemetry.\n"
        "2. Ingestion Flow: When an order is packed and dispatched, a unique `delivery_id` is generated along with\n"
        "   planned attributes (distance_km, package_weight_kg, expected_time_hours, vehicle_type, delivery_mode).\n"
        "3. Environmental Integration: Route-segment weather conditions and traffic congestion telemetry are appended\n"
        "   from external meteorological and mapping service APIs.\n"
        "4. Completion Logging: Upon delivery confirmation, final attributes (delayed, delivery_status, delivery_rating,\n"
        "   delivery_cost) are committed to the transaction database.\n"
        "5. Simulation Dataset Integrity: The working dataset consists of 25,000 empirical records reflecting multi-carrier\n"
        "   logistics performance in India, preserved in its original unedited format inside `dataset/raw/`."
    )
    return methodology_text

if __name__ == '__main__':
    raw_file = find_raw_dataset()
    df = load_and_verify_dataset(raw_file)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    
    overview_paths = [
        os.path.join(project_root, 'reports', 'tables', 'dataset_overview.csv'),
        os.path.join(project_root, 'dataset_overview.csv')
    ]
    generate_dataset_overview(df, raw_file, overview_paths)
    
    dict_paths = [
        os.path.join(project_root, 'reports', 'tables', 'data_dictionary.csv'),
        os.path.join(project_root, 'data_dictionary.csv')
    ]
    generate_data_dictionary(df, dict_paths)
    
    print("\n" + document_simulation_methodology())
    print("\nDataset collection and verification completed successfully!")

