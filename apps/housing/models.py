from django.db.models import Model, CharField, DecimalField, ForeignKey, CASCADE, DateTimeField, ImageField
from django.conf import settings

class City(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Property(Model):
    title = CharField(max_length=255)

    price = DecimalField(max_digits=10, decimal_places=2)

    city = ForeignKey(City, on_delete=CASCADE, related_name='properties')
    category = ForeignKey(Category, on_delete=CASCADE, related_name='properties')

    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    created_at = DateTimeField(auto_now_add=True)

class PropertyImage(Model):
    property = ForeignKey(Property, on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='properties/')

class Favourite(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    property = ForeignKey(Property, on_delete=CASCADE)

    class Meta:
        unique_together = ('user', 'property')



