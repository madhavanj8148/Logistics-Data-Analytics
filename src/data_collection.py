"""
Alias module for dataset_collection.py to maintain directory architecture alignment.
"""
from dataset_collection import (
    find_raw_dataset,
    load_and_verify_dataset,
    generate_dataset_overview,
    generate_data_dictionary,
    document_simulation_methodology
)

if __name__ == '__main__':
    raw_file = find_raw_dataset()
    df = load_and_verify_dataset(raw_file)
    print("data_collection.py alias verified successfully.")
