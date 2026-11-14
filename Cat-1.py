class Cat:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.hunger = 50  # сытость от 0 до 100
        self.energy = 50  # энергия от 0 до 100

    def meow(self):
        print(f"{self.name} говорит: Мяу! 🐾")

    def eat(self, food):
        self.hunger += 20
        print(f"{self.name} кушает {food}. Сытость теперь: {self.hunger}")

    def sleep(self):
        self.energy += 30
        print(f"{self.name} спит и набирается сил. Энергия: {self.energy}")

# Создаем котика по имени Барсик
my_cat = Cat("Барсик", "Шотландский вислоухий")
my_cat.meow()
my_cat.eat("корм")
my_cat.sleep()