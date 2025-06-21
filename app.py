# STEP 1: Upload the CSV file to Colab
from google.colab import files
import pandas as pd

# Upload manually through file selector
uploaded = files.upload()

# Load the uploaded file
import io
df = pd.read_csv(io.BytesIO(uploaded['road_traffic_injuries_sample.csv']))

# Preview the first few rows
df.head()
