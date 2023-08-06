from raga import Dataset, TestSession, Auth
import pandas as pd
from typing import Optional, List, Dict

# Create a test DataFrame
test_df = pd.DataFrame({
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
})

# Define the Schema class
class Schema:
    def __init__(
        self,
        prediction_id: Optional[str] = None,
        timestamp_column_name: Optional[str] = None,
        feature_column_names: Optional[List[str]] = None,
        metadata_column_names: Optional[List[str]] = None,
        label_column_names: Optional[Dict[str, str]] = None,
        embedding_column_names: Optional[Dict[str, str]] = None,
    ):
        self.prediction_id = prediction_id
        self.timestamp_column_name = timestamp_column_name
        self.feature_column_names = feature_column_names
        self.metadata_column_names = metadata_column_names
        self.label_column_names = label_column_names
        self.embedding_column_names = embedding_column_names

# Create an instance of the Schema class
schema = Schema()

# Create an instance of the Auth class
auth = Auth()

# Create an instance of the TestSession class
test_experiment = TestSession(auth.token, 1, "test_experiment7")

# Create an instance of the Dataset class
test_ds = Dataset(auth.token, test_experiment.experiment_id, test_df, schema, "TestDB")

# Load labels from a file
test_ds.load_labels_from_file(
    "/Users/manabroy/localhost/observance/raga/testing_platform/testing-platform-python-client/raga/examples/coco.json",
    "coco",
    "_id",
    "label",
    "col",
    "category",
    "category_id"
)
