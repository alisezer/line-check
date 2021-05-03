from lc.config import PORT, WORKERS, THREADS

# Binding Port
bind = f":{PORT}"

# Timeout if worker has been silent
timeout = 5

# Number of workers to boot
workers = WORKERS

# Number of threads within each worker
threads = THREADS