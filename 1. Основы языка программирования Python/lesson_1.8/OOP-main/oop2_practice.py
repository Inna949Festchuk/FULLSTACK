#!/usr/bin/env python
# coding: utf-8

# # ООП-2
# 
# Булыгин Олег:  
# * [LinkedIn](linkedin.com/in/obulygin)  
# * [Мой канал в ТГ по Python](https://t.me/pythontalk_ru)

# ### Инкапсуляция
# 
# Инкапсуляция заключается в том, что данные скрыты за пределами определения объекта. Это позволяет разработчикам создавать удобный интерфейс взаимодействия и защитить данные от внешних источников.

# In[1]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.backpack = [] 
        self.hands = hands
    
    def eat(self, food):
        if self.energy < 100:
            self.energy += food
        else:
            print('Not hungry')
        
    
    def do_exercise(self, hours):
        if self.energy > 0:
            self.energy -= hours * 2
            self.power += hours * 2
        else:
            print('Too tired')
    
    def change_alias(self, new_alias):
        self.alias = new_alias

    def beat_up(self, foe):
        if not isinstance(foe, Character): 
            return
        if foe.power < self.power:
            foe.status = 'defeated'
            self.status = 'winner'
        else:
            print('Retreat!')


# In[2]:


peter = Character('Peter Parker', 80)
print(peter.backpack)
peter.do_exercise(5)


# Реализуем защищенную переменную и метод

# In[3]:


# реализуем защищенную переменную и метод
class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self._backpack = [] 
        self.hands = hands
    
    def eat(self, food):
        if self.energy < 100:
            self.energy += food
        else:
            print('Not hungry')
    
    def do_exercise(self, hours):
        if self.energy > 0:
            self.energy -= hours * 2
            self.power += hours * 2
        else:
            print('Too tired')
    
    def _change_alias(self, new_alias):
        self.alias = new_alias
    
    def beat_up(self, foe):
        if not isinstance(foe, Character): 
            return
        if foe.power < self.power:
            foe.status = 'defeated'
            self.status = 'winner'
        else:
            print('Retreat!')
            
    

peter = Character('Peter Parker', 80)
peter._change_alias('Spider-Man')
print(peter.alias)
print(peter._backpack)


# На самом деле, технические для интерпретатора это не имеет никакого значения. Это просто соглашение, согласно которому, такие атрибуты и методы не стоит использовать за рамками класса и дочерних классов.

# Двойное подчеркивание в начале имени атрибута/метода дает большую защиту: атрибут становится недоступным по этому имени вне самого класса.

# In[4]:


# реализуем приватную переменную и метод

class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.__backpack = [] 
        self.hands = hands
    
    def eat(self, food):
        if self.energy < 100:
            self.energy += food
        else:
            print('Not hungry')
        
    
    def do_exercise(self, hours):
        if self.energy > 0:
            self.energy -= hours * 2
            self.power += hours * 2
        else:
            print('Too tired')
    
    def __change_alias(self, new_alias):
        self.alias = new_alias

    def beat_up(self, foe):
        if not isinstance(foe, Character): 
            return
        if foe.power < self.power:
            foe.status = 'defeated'
            self.status = 'winner'
        else:
            print('Retreat!')

peter = Character('Peter Parker', 80)
peter.__change_alias('Spider-Man')
print(peter.__backpack)


# Но и это можно обойти при помощи прямого указания класса.

# In[5]:


peter = Character('Peter Parker', 80)
peter._Character__change_alias('Spider-Man')
print(peter.alias)
print(peter._Character__backpack)


# Таким образом, реализация инкапсуляции в Python носит формальный характер и работает только на уровне соглашения.
# 
# 
# 

# ### Наследование

# In[6]:


# и сразу реализуем множественное наследование!

class Character:
    name = ''
    power = 0
    energy = 100
    hands = 2

class Spider:
    power = 0
    energy = 50
    hands = 8
    
    def webshoot(self):
        print('Pew-Pew!')

        
class SpiderMan(Character, Spider):
    pass


peter_parker = SpiderMan()
print(peter_parker.name)
print(peter_parker.power)
print(peter_parker.energy)
print(peter_parker.hands)
peter_parker.webshoot()


# Линеаризация способ представления дерева (графа, дерева) в линейную модель (плоскую структуру, список) для определения порядка наследования.

# In[7]:


print(SpiderMan.mro())


# In[12]:


class Character:
    # перенесем все в init
     def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands
    

class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
        
    
    def webshoot(self):
        print('Pew-Pew!')

        
    
class SpiderMan(Character, Spider):
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20

              
        
peter_parker = SpiderMan('Peter Parker', 80)
print(peter_parker.energy)
print(peter_parker.power)
print(peter_parker.hands)
peter_parker.turn_spider_sense()
print(peter_parker.energy)
print(peter_parker.power)


# ### Полиморфизм
# 
# Полиморфизм позволяет методам с одинаковыми именами реализовывать разную функциональность для разных классов (в т.ч. дочерних).

# In[13]:


# добавим в наши родительские классы новые методы

class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Changing position')

        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Changing position')

        
    
class SpiderMan(Character, Spider):
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20

peter_parker = SpiderMan('Peter Parker', 80)
peter_parker.move()


# In[ ]:





# In[14]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')

        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')

        
    
class SpiderMan(Character, Spider):
    
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
    
    def move(self):
        self.webshoot()
        print('Moving on 3 square')

        
peter_parker = SpiderMan('Peter Parker', 80)
peter_parker.move()


# А теперь хотим создам инвентарь нашему игровому персонажу

# In[15]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')

        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')

        
    
class SpiderMan(Character, Spider):
    # такой вариант допустимый, но зачем нам перезаписывать инициализацию,
    # которая полностью совпадает с родителем?
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands
        self.backpack = []
    
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20

    def move(self):
        self.webshoot()
        print('Moving on 3 square')

        
peter_parker = SpiderMan('Peter Parker', 80)
print(peter_parker.backpack)


# Функция super() можно получить доступ к унаследованным методам, которые были перезаписаны в дочернем классе.

# In[16]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')

class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')   
    
class SpiderMan(Character, Spider):
    # мы полностью наследуем от родителя инициализацию и добавляем новый атрибут для экземпляра
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20

    def move(self):
        self.webshoot()
        print('Moving on 3 square')


peter_parker = SpiderMan('Peter Parker', 80)
print(peter_parker.backpack)
print(peter_parker.power)
print(peter_parker.energy)
print(peter_parker.hands)


# In[17]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')

        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')   
    
    
class SpiderMan(Character, Spider):
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
 
    # наш персонаж не может пользоваться паутиной, если ее нет! попробуем исправить
    # где ошибка?
    def webshoot(self):
        if 'web' in self.backpack:
            self.webshoot() 
        else:
            print('No web!')

    def move(self):
        self.webshoot()
        print('Moving on 3 square')



peter_parker = SpiderMan('Peter Parker', 80)
peter_parker.webshoot()


# In[18]:


peter_parker.backpack.append('web')
peter_parker.webshoot()


# In[19]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')

        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')   
    
    
class SpiderMan(Character, Spider):
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
    
    # исправляем
    def webshoot(self):
        if 'web' in self.backpack:
            super().webshoot() 
        else:
            print('No web!')

    def move(self):
        self.webshoot()
        print('Moving on 3 square')

        
peter_parker = SpiderMan('Peter Parker', 80)
peter_parker.webshoot()
peter_parker.backpack.append('web')
peter_parker.webshoot()


# Можем ли наследовать что-то не от родителя по mro, а от другого родителя?

# In[20]:


# добавим родительским классам атаку и проверим, как будет наследоваться

class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')
    
    def attack(self, foe):
        foe.health -= 10
        
        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self, foe):
        self.webshoot()
        print('Moving on 1 square')   
        
    def attack(self, foe):
        foe.status = 'stunned'
    
    
class SpiderMan(Character, Spider):
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
    
    def webshoot(self):
        if 'web' in self.backpack:
            super().webshoot() 
        else:
            print('No web!')

    def move(self):
        self.webshoot()
        print('Moving on 3 square')
        


        
peter_parker = SpiderMan('Peter Parker', 80)
enemy = Character('Some Enemy', 10)
enemy.health = 100

peter_parker.attack(enemy)

print(enemy.health)
print(enemy.status)


# In[32]:


# сделаем у дочернего класса свою атаку

class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')
    
    def attack(self, foe):
        foe.health -= 10
        
        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')   
        
    def attack(self, foe):
        foe.status = 'stunned'
    
    
class SpiderMan(Character, Spider):
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
    
    def webshoot(self):
        if 'web' in self.backpack:
            super().webshoot() 
        else:
            print('No web!')

    def move(self):
        self.webshoot()
        print('Moving on 3 square')
        
    # делаем классу свою атаку   
    def attack(self, foe):
        super().attack(foe)
        Spider.attack(self, foe)
        

peter_parker = SpiderMan('Peter Parker', 80)
enemy = Character('Some Enemy', 10)
enemy.health = 100
peter_parker.attack(enemy)

print(enemy.health)
print(enemy.status)


# Магические методы – это общий термин, относящийся к "специальным" методам классов, для которых нет единого определения, поскольку их применение разнообразно. 

# И мы также можем перегрузить эти магические методы

# In[38]:


class Character:
    def __init__(self, name, power, energy=100, hands=2):
        self.name = name
        self.power = power
        self.energy = energy
        self.hands = hands

    def move(self):
        print('Moving on 2 squares')
    
    def attack(self, foe):
        foe.health -= 10
        
        
class Spider:
    def __init__(self, power, energy=50, hands=8):
        self.power = power
        self.energy = energy
        self.hands = hands
    
    def webshoot(self):
        print('Pew-Pew!')
    
    def move(self):
        self.webshoot()
        print('Moving on 1 square')   
        
    def attack(self, foe):
        foe.status = 'stunned'
    
    
class SpiderMan(Character, Spider):
    def __init__(self, name, power):
        super().__init__(name, power)
        self.backpack = []
        
    def turn_spider_sense(self):
        self.energy -= 10
        self.power += 20
    
    def webshoot(self):
        if 'web' in self.backpack:
            super().webshoot() 
        else:
            print('No web!')

    def move(self):
        self.webshoot()
        print('Moving on 3 square')
        
    def attack(self, foe):
        super().attack(foe)
        Spider.attack(self, foe)
        
#     добавим возможность сравнения персонажей 
    def __lt__(self, other):
        if not isinstance(other, Character):
            print('Not a Character!')
            return
        return self.power < other.power
    
    def __str__(self):
        res = f'Сила персонажа = {self.power}'
        return res
    
    
peter_parker = SpiderMan('Peter Parker', 80)
miles_morales = SpiderMan('Miles Morales', 85)

# print(peter_parker < miles_morales)
# и даже "больше" будет работать!
# print(peter_parker > miles_morales)
# print(peter_parker.__lt__(miles_morales))

print(peter_parker)
print(miles_morales)


# In[ ]:




