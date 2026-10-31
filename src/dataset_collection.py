"""
Compatibility layer for dataset_collection.py.
Preserves existing references while delegating all functionality to src/data_collection.py.
Author: Paladugula Madhavan
"""

from data_collection import (
    find_raw_dataset,
    load_and_verify_dataset,
    generate_dataset_overview,
    generate_data_dictionary,
    document_simulation_methodology,
    main
)

if __name__ == '__main__':
    main()
