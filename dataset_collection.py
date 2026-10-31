"""
Root-level entry point delegating to src.data_collection.
Maintains CLI execution capability from root without duplicating code.
Author: Paladugula Madhavan
"""

import sys
import os

# Ensure src/ is on sys.path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

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
