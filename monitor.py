import psutil
import datetime

def get_system_metrics():
    # Fetch CPU, Memory, and Disk Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    metrics = {
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'cpu_usage': cpu_usage,
        'memory_used': memory.used,
        'memory_total': memory.total,
        'disk_used': disk.used,
        'disk_total': disk.total
    }
    return metrics

if __name__ == "__main__":
    metrics = get_system_metrics()
    print(metrics)
