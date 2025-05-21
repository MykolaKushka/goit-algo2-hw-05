import time
from datasketch import HyperLogLog
import pandas as pd

def load_ips_from_file(filepath):
    ips = []
    with open(filepath, 'r') as f:
        for line in f:
            ip = line.strip()
            if ip.count('.') == 3:
                ips.append(ip)
    return ips

def count_unique_exact(ips):
    start = time.time()
    result = len(set(ips))
    end = time.time()
    return result, round(end - start, 4)

def count_unique_hll(ips, p=14):
    hll = HyperLogLog(p=p)
    start = time.time()
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    end = time.time()
    return round(hll.count()), round(end - start, 4)

def check_ip_counting(filepath):
    print("Завантаження IP-адрес...")
    ips = load_ips_from_file(filepath)

    print("Підрахунок унікальних IP (точний)...")
    exact_count, exact_time = count_unique_exact(ips)

    print("Підрахунок унікальних IP (HyperLogLog)...")
    hll_count, hll_time = count_unique_hll(ips)

    df = pd.DataFrame({
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact_count, hll_count],
        "Час виконання (сек.)": [exact_time, hll_time]
    })

    print("\nРезультати порівняння:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    check_ip_counting("lms-stage-access.log")
