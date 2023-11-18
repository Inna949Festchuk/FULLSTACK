from .models import Weaponts
from rest_framework import serializers

# В сериалайзер передаются все параметры модели
# которые мы хотим преобразовать в примитивы json
# без указания max_lenght и прочих параметров полей

# class WeaponSerializer(serializers.Serializer):
#     power = serializers.IntegerField()
#     rerity = serializers.CharField()

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weaponts # Указываем модель из models.py 
        fields = ['id', 'power', 'rerity'] # Указываем поля модели которые мы хотим отобразить
        # 'id' указываем при применении класса RetrieveAPIView