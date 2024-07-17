from django.test import TestCase
from .models import Animal


class AnimalTest(TestCase):
    def setUp(self):
        Animal.objects.create(name="Lion", sound="Roar")
        Animal.objects.create(name="Cat", sound="Meow")

    def test_animals_can_speak(self):
        lion = Animal.objects.get(name='Lion')
        cat = Animal.objects.get(name='Cat')

        self.assertEquals(lion.speak(), "The Lion says 'Roar'")
        self.assertEquals(cat.speak(), "The Cat says 'Meow'")

