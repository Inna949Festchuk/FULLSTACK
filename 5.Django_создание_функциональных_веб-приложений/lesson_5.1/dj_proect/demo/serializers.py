from .models import Weaponts
from rest_framework import serializers

# В сериалайзер передаются все объекты модели,
# которые мы хотим преобразовать в байт-код (поток) - СЕРИАЛИЗОВАТЬ
# без указания max_lenght и прочих параметров полей

# Сериализация представляет собой процесс преобразования 
# состояния объекта в форму, пригодную для сохранения или передачи.

# Десериализация (deserialization) — это процесс создания структуры данных 
# из битовой последовательности путем перевода этой последовательности 
# в объекты и их упорядочивания (структуризации).

# class WeaponSerializer(serializers.Serializer):
#     power = serializers.IntegerField()
#     rerity = serializers.CharField()

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weaponts # Указываем модель из models.py 
        fields = ['id', 'power', 'rerity'] # Указываем поля модели которые мы хотим отобразить
        # 'id' указываем при применении класса RetrieveAPIView