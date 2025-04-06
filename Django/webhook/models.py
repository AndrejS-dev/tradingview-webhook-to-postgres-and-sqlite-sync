from django.db import models

# Create your models here.

# 1 HOUR
class BTCUSD_1H(models.Model):
    time = models.DateTimeField()  # Store full date and time
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

class ETHUSD_1H(models.Model):
    time = models.DateTimeField() 
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

class SOLUSD_1H(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

class XRPUSD_1H(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=4)
    high = models.DecimalField(max_digits=15, decimal_places=4)
    low = models.DecimalField(max_digits=15, decimal_places=4)
    close = models.DecimalField(max_digits=15, decimal_places=4)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

class BNBUSD_1H(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

class SUIUSD_1H(models.Model):
    time = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=4)
    high = models.DecimalField(max_digits=15, decimal_places=4)
    low = models.DecimalField(max_digits=15, decimal_places=4)
    close = models.DecimalField(max_digits=15, decimal_places=4)
    volume = models.DecimalField(max_digits=15, decimal_places=2)

# If you need more assets, copy the class and rename it and ensure that the max_digits and decimal_places are suitable for the asset you want

# If you need more timeframes, copy the class and change the last part with timeframe 
# (if you are using the same assets but on different timeframe, there is no need to change the number precision)