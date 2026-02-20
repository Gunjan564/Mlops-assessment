# MLOps Task Submission

## 1. Setup Instructions
[cite_start]To install the required dependencies, run the following command [cite: 146-148]:
`pip install -r requirements.txt`

## 2. Local Execution Instructions
[cite_start]To run the pipeline locally, execute the following command [cite: 149-153]:
`python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log`

## 3. Docker Instructions
[cite_start]To build the Docker image, run [cite: 154-156]:
`docker build -t mlops-task .`

[cite_start]To run the container, execute [cite: 157-158]:
`docker run --rm mlops-task`

## 4. Expected Output
[cite_start]Upon successful execution, the container will output and generate a `metrics.json` file with the following structure[cite: 159]:
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4989,
    "latency_ms": 29,
    "seed": 42,
    "status": "success"
}

## 5. Dependencies
[cite_start]The following standard Python packages are required[cite: 160]:
- pandas
- numpy
- PyYAML

*Note regarding data.csv: The dataset link provided in the original Google Document was not an active hyperlink. To demonstrate the pipeline's end-to-end functionality, error handling, and Docker containerization, a synthetic `data.csv` file was generated containing the exact requested OHLCV columns and 10,000 rows.*