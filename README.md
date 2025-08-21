# Natural Disaster Visualisation

## Objective
- To visualise cleaned data loaded into SQL Pagilla database from ETL pipeline

Visit Part 1 of Natural Disaster Project at https://github.com/ha282/natural-disasters/tree/main.

## Setup
1. Create virtual environment
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\\Scripts\\activate  # Windows
   ```

2. Install required packages: 
   ```bash
   pip install -r requirements.txt
   ```

3. Run Streamlit \
To run the script:
    ```bash
    streamlit run home.py
    ```