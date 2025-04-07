from django.db import models


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    prep_time = models.IntegerField()  # in minutes
    cook_time = models.IntegerField()  # in minutes
    servings = models.IntegerField()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=20, help_text="e.g., grams, cups, etc.")
    recipe = models.ForeignKey(
        Recipe, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.quantity} of {self.name} for {self.recipe.title}"


class IngredientPrice(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    store = models.ForeignKey(
        "Store", related_name="ingredient_prices", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("ingredient", "date")
        ordering = ["-date"]
        verbose_name = "Ingredient Price"
        verbose_name_plural = "Ingredient Prices"

    def __str__(self):
        return f"{self.price_per_unit} for {self.ingredient.name} on {self.date}"


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Meal