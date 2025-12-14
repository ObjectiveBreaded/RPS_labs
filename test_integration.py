import mysql.connector
import random
import time

# ================== НАСТРОЙКИ ТЕСТОВОЙ БД ==================
TEST_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Rom2132412",
    "database": "lab3_test_db"
}

# ================== СОЕДИНЕНИЕ С БД ==================
def get_db():
    return mysql.connector.connect(**TEST_DB_CONFIG)

# ================== ИНИЦИАЛИЗАЦИЯ ТАБЛИЦ ==================
def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS arrays (
        id INT AUTO_INCREMENT PRIMARY KEY,
        original TEXT,
        sorted TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    con.commit()
    cur.close()
    con.close()

# ================== ГЕНЕРАЦИЯ СЛУЧАЙНОГО МАССИВА ==================
def random_array(size=10, min_val=0, max_val=100):
    return [random.randint(min_val, max_val) for _ in range(size)]

# ================== TREE SORT ==================
def tree_sort(arr):
    if len(arr) <= 1:
        return arr
    root = arr[0]
    left = [x for x in arr[1:] if x < root]
    right = [x for x in arr[1:] if x >= root]
    return tree_sort(left) + [root] + tree_sort(right)

# ================== ТЕСТ 1: ДОБАВЛЕНИЕ МАССИВОВ ==================
def test_insert(num_arrays):
    con = get_db()
    cur = con.cursor()
    start = time.time()
    try:
        for _ in range(num_arrays):
            arr = random_array()
            sorted_arr = tree_sort(arr)
            cur.execute(
                "INSERT INTO arrays (original, sorted) VALUES (%s, %s)",
                (",".join(map(str, arr)), ",".join(map(str, sorted_arr)))
            )
        con.commit()
        success = True
    except Exception as e:
        print("Ошибка вставки:", e)
        success = False
    elapsed = round(time.time() - start, 3)
    cur.close()
    con.close()
    print(f"Добавление {num_arrays} массивов: {'Успешно' if success else 'Не успешно'}, Время: {elapsed} сек")

# ================== ТЕСТ 2: ВЫГРУЗКА И СОРТИРОВКА ==================
def test_select_and_sort(num_select=100):
    con = get_db()
    cur = con.cursor()
    start_total = time.time()
    try:
        cur.execute("SELECT original FROM arrays")
        all_rows = cur.fetchall()
        if len(all_rows) < num_select:
            print("В базе меньше массивов, чем требуется для теста")
            num_select = len(all_rows)
        total_sort_time = 0
        for arr_str in random.sample(all_rows, num_select):
            arr = list(map(int, arr_str[0].split(',')))
            t0 = time.time()
            tree_sort(arr)
            total_sort_time += time.time() - t0
        success = True
    except Exception as e:
        print("Ошибка выборки/сортировки:", e)
        success = False
        total_sort_time = 0
    elapsed_total = round(time.time() - start_total, 3)
    avg_time_ms = round(total_sort_time/num_select*1000, 3) if num_select else 0
    cur.close()
    con.close()
    print(f"Выборка и сортировка {num_select} массивов: {'Успешно' if success else 'Не успешно'}, "
          f"Общее время: {elapsed_total} сек, Среднее на 1 массив: {avg_time_ms} мс")

# ================== ТЕСТ 3: ОЧИСТКА БАЗЫ ==================
def test_clear():
    con = get_db()
    cur = con.cursor()
    start = time.time()
    try:
        cur.execute("DELETE FROM arrays")
        con.commit()
        success = True
    except Exception as e:
        print("Ошибка очистки:", e)
        success = False
    elapsed = round(time.time() - start, 3)
    cur.close()
    con.close()
    print(f"Очистка базы: {'Успешно' if success else 'Не успешно'}, Время: {elapsed} сек")

# ================== ЗАПУСК ВСЕХ ТЕСТОВ ==================
if __name__ == "__main__":
    init_db()
    for count in [100, 1000, 10000]:
        test_insert(count)
        test_select_and_sort(100)
        test_clear()
