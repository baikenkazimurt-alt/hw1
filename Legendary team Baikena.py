# Базовый класс героя
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def attack_enemy(self, enemy):
        enemy.health -= self.attack
        print(f"{self.name} атаковал босса и нанес {self.attack} урона!")

# 1) Задание 1 (3 балла): Создаем класс Paladin, наследующий Hero
class Paladin(Hero):
    def __init__(self, name):
        super().__init__(name, health=150, attack=25)
        self.armor = 50

    # Уникальный метод special()
    def special(self):
        self.health += 30
        print(f"✨ {self.name} использует святую защиту! Здоровье увеличено, теперь оно: {self.health}")

# Класс Босса для боя
class Boss:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

# 2) Задание 2 (3 балла): Создаем предмет и инвентарь
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"📦 В инвентарь добавлен предмет: {item}")

# Создаем лечебное зелье
healing_potion = "Лечебное зелье (+50 HP)"

# 3) Задание 3 (2 балла): Устраиваем бой с боссом
hero = Paladin("Артур")
boss = Boss("Дракон", 200, 30)
inventory = Inventory()
inventory.add_item(healing_potion)

print(f"--- Битва начинается! Герой: {hero.name} против Босса: {boss.name} ---")
hero.special()
hero.attack_enemy(boss)
print(f"У здоровья босса осталось: {boss.health}")  