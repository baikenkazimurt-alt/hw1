import time
from functools import wraps

# --- 1. Фильтр редких предметов ---
# Создаем класс Item для удобства
class Item:
    def __init__(self, name, rarity, power):
        self.name = name
        self.rarity = rarity  # common, rare, legendary и т.д.
        self.power = power

    def __repr__(self):
        return f"Item({self.name}, {self.rarity}, power={self.power})"

# Создаем минимум 8 предметов
items = [
    Item("Деревянный меч", "common", 10),
    Item("Ржавый щит", "common", 5),
    Item("Зелье здоровья", "common", 15),
    Item("Кожаная куртка", "common", 8),
    Item("Огненный посох", "rare", 50),
    Item("Эльфийский лук", "rare", 45),
    Item("Меч Тысячи Истин", "legendary", 100),
    Item("Амулет Дракона", "legendary", 90)
]

print("--- 1. Редкие и легендарные предметы ---")
# Используем filter() и lambda для поиска редких и легендарных предметов
rare_items = list(filter(lambda x: x.rarity in ["rare", "legendary"], items))
for item in rare_items:
    print(item)


# --- 2. Рейтинг лучших предметов ---
print("\n--- 2. Топ-5 предметов по силе ---")
# Сортируем по силе (power) от большего к меньшему и берем первые 5
top_5_items = sorted(items, key=lambda x: x.power, reverse=True)[:5]
# С помощью list comprehension получаем список их названий
top_5_names = [item.name for item in top_5_items]
print("Названия топ-5 предметов:", top_5_names)


# --- 3. Генератор лута ---
print("\n--- 3. Генератор лута (yield) ---")
def loot_generator():
    loot_pool = [
        ("Золотая монета", "common", 1),
        ("Кристалл маны", "rare", 30),
        ("Шлем берсерка", "rare", 60),
        ("Кольцо всевластия", "legendary", 150),
        ("Трава исцеления", "common", 5)
    ]
    # Бесконечный цикл с yield выдает случайные предметы по одному
    while True:
        import random
        yield random.choice(loot_pool)

# Выводим первые 10 результатов работы генератора
gen = loot_generator()
for i in range(10):
    print(f"Лут #{i+1}: {next(gen)}")


# --- 4. Декоратор логирования и Бонус (таймер) ---
print("\n--- 4 и Бонус: Декораторы @log_action и @timer ---")

# Бонусный декоратор для измерения времени
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        print(f"[TIMER] Функция '{func.__name__}' выполнилась за {execution_time:.4f} мс")
        return result
    return wrapper

# Обязательный декоратор логирования
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Срабатывает действие: вызван метод '{func.__name__}'")
        return func(*args, **kwargs)
    return wrapper

# Применяем оба декоратора к функции атаки
@timer
@log_action
def attack(target_name):
    print(f"Герой наносит мощный удар по противнику: {target_name}!")

# Проверяем работу функции
attack("Гоблин-разбойник")