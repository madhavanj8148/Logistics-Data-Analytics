"""
Logistics Data Analytics - Step 6: Data Normalization and Feature Scaling
Author: Paladugula Madhavan
Institution: Vellore Institute of Technology, Andhra Pradesh
Role: Logistics Data Analyst Intern
Track: Week 2 - Data Collection, Cleaning & Preprocessing
Module: src/normalization.py
"""

import os
import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Import preceding pipeline modules
try:
    from data_collection import find_raw_dataset, load_and_verify_dataset
    from data_cleaning import clean_strings_and_categories
except ImportError:
    from src.data_collection import find_raw_dataset, load_and_verify_dataset
    from src.data_cleaning import clean_strings_and_categories

TARGET_SCALING_COLS = ['distance_km', 'package_weight_kg', 'expected_time_hours', 'delivery_cost']

EXCLUDED_COLUMNS_RATIONALE = {
    'delivery_id': (
        "Primary Identifier / Key",
        "Unique record identifier. Numerical scaling would destroy relational integrity and unique shipment reference semantics."
    ),
    'delayed': (
        "Supervised Target Variable",
        "Binary classification target ('yes' / 'no'). Scaling the dependent variable alongside features causes data leakage and model contamination."
    ),
    'delivery_status': (
        "Post-Event Categorical State",
        "Nominal operational lifecycle label ('delivered', 'delayed', 'failed'). Not continuous; constitutes post-event leakage if scaled as predictor."
    ),
    'delivery_rating': (
        "Discrete Ordinal Metric",
        "Customer satisfaction Likert scale [1 to 5 integer stars]. Continuous feature scaling distorts discrete ordinal distances."
    )
}

def apply_minmax_scaling(df, columns=None):
    """
    Applies Min-Max Scaling:
        X_scaled = (X - X_min) / (X_max - X_min)
    Transforms selected features into the bounded interval [0, 1].
    Preserves all other unscaled columns intact.
    """
    if columns is None:
        columns = TARGET_SCALING_COLS
        
    df_scaled = df.copy()
    scaler = MinMaxScaler()
    df_scaled[columns] = scaler.fit_transform(df[columns])
    
    metrics = {}
    for col in columns:
        orig = df[col]
        trans = df_scaled[col]
        metrics[col] = {
            'Original Min': float(orig.min()),
            'Original Max': float(orig.max()),
            'Original Mean': float(orig.mean()),
            'Original Std': float(orig.std()),
            'Scaled Min': float(trans.min()),
            'Scaled Max': float(trans.max()),
            'Scaled Mean': float(trans.mean()),
            'Scaled Std': float(trans.std())
        }
        
    return df_scaled, scaler, metrics

def apply_standard_scaling(df, columns=None):
    """
    Applies Z-Score Standardization:
        Z = (X - mu) / sigma
    Transforms selected continuous features to approximately zero mean and unit standard deviation.
    Note: StandardScaler rescales the features but does NOT transform data into a normal distribution;
    the original distribution's shape, skewness, and kurtosis are preserved.
    Preserves all other unscaled columns intact.
    """
    if columns is None:
        columns = TARGET_SCALING_COLS
        
    df_standard = df.copy()
    scaler = StandardScaler()
    df_standard[columns] = scaler.fit_transform(df[columns])
    
    metrics = {}
    for col in columns:
        orig = df[col]
        trans = df_standard[col]
        metrics[col] = {
            'Original Min': float(orig.min()),
            'Original Max': float(orig.max()),
            'Original Mean': float(orig.mean()),
            'Original Std': float(orig.std()),
            'Standardized Min': float(trans.min()),
            'Standardized Max': float(trans.max()),
            'Standardized Mean': float(trans.mean()),
            'Standardized Std': float(trans.std())
        }
        
    return df_standard, scaler, metrics

def build_normalization_comparison_table(df_orig, df_minmax, df_standard, columns=None):
    """
    Constructs a comprehensive, academic comparison matrix detailing:
    Original vs. Min-Max Scaled vs. Standardized metrics across:
    Min, Max, Mean, Std Dev, Skewness, and Excess Kurtosis.
    Also documents the exclusion rationale for unscaled attributes.
    """
    if columns is None:
        columns = TARGET_SCALING_COLS
        
    comparison_rows = []
    
    for col in columns:
        s_orig = df_orig[col]
        s_mm = df_minmax[col]
        s_std = df_standard[col]
        
        comparison_rows.append({
            'Feature': col,
            'Transformation': 'Original Raw',
            'Min': round(float(s_orig.min()), 4),
            'Max': round(float(s_orig.max()), 4),
            'Mean': round(float(s_orig.mean()), 4),
            'Std Dev': round(float(s_orig.std()), 4),
            'Skewness': round(float(s_orig.skew()), 4),
            'Excess Kurtosis': round(float(s_orig.kurtosis()), 4),
            'Mathematical Domain': f"[{s_orig.min():.2f}, {s_orig.max():.2f}]",
            'Logistics Interpretation': "Physical engineering units (km, kg, hrs, INR)"
        })
        
        comparison_rows.append({
            'Feature': col,
            'Transformation': 'Min-Max Scaled',
            'Min': round(float(s_mm.min()), 4),
            'Max': round(float(s_mm.max()), 4),
            'Mean': round(float(s_mm.mean()), 4),
            'Std Dev': round(float(s_mm.std()), 4),
            'Skewness': round(float(s_mm.skew()), 4),
            'Excess Kurtosis': round(float(s_mm.kurtosis()), 4),
            'Mathematical Domain': "[0.0000, 1.0000]",
            'Logistics Interpretation': "Normalized relative operational intensity (0% to 100%)"
        })
        
        comparison_rows.append({
            'Feature': col,
            'Transformation': 'Standardized (Z-Score)',
            'Min': round(float(s_std.min()), 4),
            'Max': round(float(s_std.max()), 4),
            'Mean': round(float(s_std.mean()), 6),
            'Std Dev': round(float(s_std.std()), 4),
            'Skewness': round(float(s_std.skew()), 4),
            'Excess Kurtosis': round(float(s_std.kurtosis()), 4),
            'Mathematical Domain': f"[{s_std.min():.2f}, {s_std.max():.2f}]",
            'Logistics Interpretation': "Standard deviation deviations from network fleet average"
        })
        
    return pd.DataFrame(comparison_rows)

def generate_normalization_visualizations(df_orig, df_minmax, df_standard, output_path, columns=None):
    """
    Generates a high-resolution (300 DPI) 4x3 multi-panel diagnostic dashboard:
    - Column 1: Original feature distribution (KDE + Histogram) in physical units.
    - Column 2: Min-Max scaled distribution bounded strictly within [0, 1].
    - Column 3: Standardized distribution with zero mean and unit variance.
    """
    if columns is None:
        columns = TARGET_SCALING_COLS
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    fig, axes = plt.subplots(4, 3, figsize=(18, 16))
    
    titles_units = {
        'distance_km': ('Transit Distance', 'km', '#2980B9'),
        'package_weight_kg': ('Package Weight', 'kg', '#27AE60'),
        'expected_time_hours': ('Expected Duration', 'hours', '#E67E22'),
        'delivery_cost': ('Delivery Tariff', 'INR', '#8E44AD')
    }
    
    for row_idx, col in enumerate(columns):
        name, unit, color = titles_units[col]
        
        # 1. Original Distribution
        ax_orig = axes[row_idx, 0]
        sns.histplot(df_orig[col], kde=True, ax=ax_orig, color=color, bins=35, edgecolor='black', alpha=0.6)
        mean_o = df_orig[col].mean()
        std_o = df_orig[col].std()
        ax_orig.axvline(mean_o, color='#C0392B', linestyle='-', linewidth=2, label=f'Mean: {mean_o:.1f}')
        ax_orig.set_title(f'{name} – Original (Raw)\n[Domain: {df_orig[col].min():.1f} to {df_orig[col].max():.1f} {unit}]', fontsize=11, fontweight='bold')
        ax_orig.set_xlabel(f'{name} ({unit})', fontsize=10, fontweight='bold')
        ax_orig.set_ylabel('Shipment Frequency', fontsize=10)
        ax_orig.legend(loc='upper right', fontsize=8, frameon=True)
        
        # 2. Min-Max Scaled Distribution
        ax_mm = axes[row_idx, 1]
        sns.histplot(df_minmax[col], kde=True, ax=ax_mm, color='#16A085', bins=35, edgecolor='black', alpha=0.6)
        mean_m = df_minmax[col].mean()
        ax_mm.axvline(mean_m, color='#C0392B', linestyle='-', linewidth=2, label=f'Mean: {mean_m:.3f}')
        ax_mm.set_title(f'{name} – Min-Max Scaled\n[Bounded Interval: [0.0, 1.0]]', fontsize=11, fontweight='bold')
        ax_mm.set_xlabel(f'{name} (Normalized [0, 1])', fontsize=10, fontweight='bold')
        ax_mm.set_ylabel('Shipment Frequency', fontsize=10)
        ax_mm.set_xlim(-0.05, 1.05)
        ax_mm.legend(loc='upper right', fontsize=8, frameon=True)
        
        # 3. Standardized (Z-Score) Distribution
        ax_std = axes[row_idx, 2]
        sns.histplot(df_standard[col], kde=True, ax=ax_std, color='#8E44AD', bins=35, edgecolor='black', alpha=0.6)
        mean_s = df_standard[col].mean()
        std_s = df_standard[col].std()
        ax_std.axvline(0.0, color='#C0392B', linestyle='-', linewidth=2, label='Mean: 0.00')
        ax_std.axvline(-1.0, color='#2980B9', linestyle='--', linewidth=1.5, label='-1 StdDev')
        ax_std.axvline(1.0, color='#2980B9', linestyle='--', linewidth=1.5, label='+1 StdDev')
        ax_std.set_title(f'{name} – Standardized (Z-Score)\n[Mean = 0.0, StdDev = 1.0]', fontsize=11, fontweight='bold')
        ax_std.set_xlabel(f'{name} (Z-Score)', fontsize=10, fontweight='bold')
        ax_std.set_ylabel('Shipment Frequency', fontsize=10)
        ax_std.legend(loc='upper right', fontsize=8, frameon=True)
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Normalization comparison visualization saved to: {output_path}")

def run_normalization_pipeline():
    """
    Orchestrates the entire Step 6 Data Normalization and Feature Scaling workflow:
    1. Loads verified dataset from dataset/raw/.
    2. Cleans strings and categorical naming.
    3. Executes Min-Max scaling for target numerical features.
    4. Executes Z-score standardization for target numerical features.
    5. Validates scaling integrity (bounds, mean, standard deviation, NaN counts).
    6. Builds comparison table and exports CSVs.
    7. Generates 300 DPI multi-panel visualization.
    """
    print("=" * 70)
    print("LOGISTICS DATA ANALYTICS: WEEK 2 - STEP 6 DATA NORMALIZATION & SCALING")
    print("=" * 70)
    
    raw_file = find_raw_dataset()
    df_raw = load_and_verify_dataset(raw_file)
    df_clean = clean_strings_and_categories(df_raw)
    
    # 1. Feature Selection & Exclusion Review
    print("\n[Phase 2: Feature Selection & Scaling Scope]")
    print(f"Features Selected for Scaling: {TARGET_SCALING_COLS}")
    print("\nExcluded Features Rationale:")
    for col, (role, reason) in EXCLUDED_COLUMNS_RATIONALE.items():
        print(f"  - {col} [{role}]: {reason}")
        
    # 2. Min-Max Scaling
    print("\n[Phase 3: Min-Max Scaling [0, 1]]")
    df_minmax, scaler_mm, mm_metrics = apply_minmax_scaling(df_clean)
    for col, m in mm_metrics.items():
        print(f"  * {col:19s}: Orig [{m['Original Min']:7.2f}, {m['Original Max']:7.2f}] -> Scaled [{m['Scaled Min']:4.2f}, {m['Scaled Max']:4.2f}] | Scaled Mean: {m['Scaled Mean']:.4f}")
        
    # 3. Standardization
    print("\n[Phase 4: Z-Score Standardization (N(0, 1))]")
    df_standard, scaler_std, std_metrics = apply_standard_scaling(df_clean)
    for col, m in std_metrics.items():
        print(f"  * {col:19s}: Orig Mean: {m['Original Mean']:7.2f}, Std: {m['Original Std']:6.2f} -> Std Mean: {m['Standardized Mean']:8.1e}, StdDev: {m['Standardized Std']:.4f}")
        
    # 4. Phase 5 & 7: Comparison Table & File Exports
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    tables_dir = os.path.join(project_root, 'reports', 'tables')
    charts_dir = os.path.join(project_root, 'reports', 'charts')
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    # Comparison CSV
    df_comparison = build_normalization_comparison_table(df_clean, df_minmax, df_standard)
    comp_csv_path = os.path.join(tables_dir, 'normalization_comparison.csv')
    df_comparison.to_csv(comp_csv_path, index=False)
    print(f"\nNormalization comparison table exported to: {comp_csv_path}")
    
    # Scaled Datasets
    mm_csv_path = os.path.join(tables_dir, 'minmax_scaled_dataset.csv')
    std_csv_path = os.path.join(tables_dir, 'standardized_dataset.csv')
    df_minmax.to_csv(mm_csv_path, index=False)
    df_standard.to_csv(std_csv_path, index=False)
    print(f"Min-Max scaled dataset exported to: {mm_csv_path}")
    print(f"Standardized dataset exported to: {std_csv_path}")
    
    # 5. Phase 6: Visualization
    chart_path = os.path.join(charts_dir, 'normalization_comparison.png')
    generate_normalization_visualizations(df_clean, df_minmax, df_standard, chart_path)
    
    # 6. Phase 9: Validation
    print("\n[Phase 9: Integrity & Mathematical Validation]")
    for col in TARGET_SCALING_COLS:
        # Min-Max checks
        assert abs(df_minmax[col].min() - 0.0) < 1e-7, f"Min-Max minimum violated for {col}"
        assert abs(df_minmax[col].max() - 1.0) < 1e-7, f"Min-Max maximum violated for {col}"
        assert df_minmax[col].isnull().sum() == 0, f"NaNs detected in Min-Max scaled {col}"
        
        # Standard checks
        assert abs(df_standard[col].mean()) < 1e-10, f"Standardized mean non-zero for {col}"
        assert abs(df_standard[col].std() - 1.0) < 1e-3, f"Standardized std non-unit for {col}"
        assert df_standard[col].isnull().sum() == 0, f"NaNs detected in standardized {col}"
        
    # Unscaled feature preservation
    for col in EXCLUDED_COLUMNS_RATIONALE.keys():
        if col in df_clean.columns:
            assert (df_minmax[col] == df_clean[col]).all(), f"Excluded column {col} altered in Min-Max!"
            assert (df_standard[col] == df_clean[col]).all(), f"Excluded column {col} altered in Standardized!"
            
    assert len(df_minmax) == 25000 and len(df_standard) == 25000, "Row count altered!"
    assert df_minmax.shape[1] == 15 and df_standard.shape[1] == 15, "Column count altered!"
    print("Validation Succeeded: All scaling transforms conform to mathematical specifications with 100% preservation of unscaled attributes.")
    
    return df_minmax, df_standard, df_comparison

if __name__ == '__main__':
    run_normalization_pipeline()

