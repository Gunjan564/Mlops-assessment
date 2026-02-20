import pandas as pd
import numpy as np
import yaml
import json
import argparse
import logging
import sys
import time

def main():
    # 1. Start execution timer
    start_time_ns = time.time_ns()

    # 2. Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    # 3. Setup Logging
    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Job started")

    # function to handle errors
    def handle_error(msg, ver="unknown"):
        logging.error(msg)
        with open(args.output, 'w') as f:
            json.dump({"version": ver, "status": "error", "error_message": msg}, f, indent=4)
        sys.exit(1)

    # 4. Load Config
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
        seed = config.get('seed')
        window = config.get('window')
        version = config.get('version', 'unknown')
        if seed is None or window is None:
            handle_error("Invalid config structure", version)
            
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")
        np.random.seed(seed)
    except Exception:
        handle_error("Missing or invalid config file")

    # 5. Load Data
    try:
        df = pd.read_csv(args.input)
        if df.empty:
            handle_error("Empty input file", version)
        if 'close' not in df.columns:
            handle_error("Missing required 'close' column", version)
        logging.info(f"Data loaded: {len(df)} rows")
    except FileNotFoundError:
        handle_error("Missing input file", version)
    except Exception:
        handle_error("Invalid CSV format", version)

    # 6. Processing: Rolling Mean & Signals
    try:
        rolling_mean = df['close'].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")
        
        signals = np.where(df['close'] > rolling_mean, 1, 0)
        logging.info("Signals generated")
        
        signal_rate = float(np.mean(signals))
        rows_processed = len(df)
        logging.info(f"Metrics: signal_rate={signal_rate:.4f}, rows_processed={rows_processed}")
    except Exception as e:
        handle_error(f"Processing error: {str(e)}", version)

    # 7. Metrics Output
    latency_ms = (time.time_ns() - start_time_ns) // 1_000_000
    
    metrics = {
        "version": version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    try:
        with open(args.output, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(json.dumps(metrics, indent=4))
        logging.info(f"Job completed successfully in {latency_ms}ms")
        sys.exit(0)
    except Exception as e:
        handle_error(f"Failed to write output: {str(e)}", version)

if __name__ == "__main__":
    main()