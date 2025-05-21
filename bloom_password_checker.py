import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        if not isinstance(size, int) or not isinstance(num_hashes, int) or size <= 0 or num_hashes <= 0:
            raise ValueError("Size and num_hashes must be positive integers.")
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item):
        item = str(item)
        hashes = []
        for i in range(self.num_hashes):
            combined = f"{item}_{i}"
            hash_digest = hashlib.sha256(combined.encode()).hexdigest()
            hash_int = int(hash_digest, 16) % self.size
            hashes.append(hash_int)
        return hashes

    def add(self, item):
        if not isinstance(item, str) or not item.strip():
            return  # ігнорувати порожні або некоректні паролі
        for hash_index in self._hashes(item):
            self.bit_array[hash_index] = 1

    def __contains__(self, item):
        if not isinstance(item, str) or not item.strip():
            return False
        return all(self.bit_array[hash_index] for hash_index in self._hashes(item))


def check_password_uniqueness(bloom_filter, new_passwords):
    if not isinstance(bloom_filter, BloomFilter) or not isinstance(new_passwords, list):
        raise ValueError("Invalid input parameters.")

    result = {}
    for password in new_passwords:
        if not isinstance(password, str) or not password.strip():
            result[password] = "некоректне значення"
            continue

        if password in bloom_filter:
            result[password] = "вже використаний"
        else:
            result[password] = "унікальний"
            bloom_filter.add(password)

    return result


# Приклад використання
if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
