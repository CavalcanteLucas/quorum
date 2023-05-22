from pathlib import Path
import pandas as pd
import os
import logging


PROVIDED_DATA_PATH = Path("provided_data")
DELIVERABLE_DATA_PATH = Path("deliverable_data")


def load_csv_file(
    filename: str,
    data_path: Path = PROVIDED_DATA_PATH,
) -> pd.DataFrame:
    """Load data from csv file."""
    csv_path = os.path.join(data_path, filename)
    return pd.read_csv(csv_path)


def save_csv_file(
    result_df: pd.DataFrame,
    filename: str,
    data_path: Path = DELIVERABLE_DATA_PATH,
) -> None:
    """Save data to csv file."""
    target_path = os.path.join(data_path, filename)
    result_df.to_csv(target_path, index=False)
    logging.info(f" [x] CSV saved in {target_path}")
