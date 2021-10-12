from django.db import models



class TrackingModel(models.Model):
    created_at                = models.DateField( auto_now=True)
    updated_at                = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True  # so we can't create an object from it but just inherit it
        ordering = ('-created_at',)