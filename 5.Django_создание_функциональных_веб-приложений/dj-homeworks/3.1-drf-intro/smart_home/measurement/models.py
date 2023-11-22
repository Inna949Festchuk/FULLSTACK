from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Measurement(models.Model):
    # У одного датчика много измерений
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
