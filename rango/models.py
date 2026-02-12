from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-')
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def get_absolute_url(self):
        return reverse('rango:show_category', kwargs={'category_name_slug': self.slug})
    
    # BOOK CHAPTER 10 EXACT:
    def likes_button(self):
        return f'<button type="button" class="btn btn-primary" name="category_id" value="{self.id}">Like Category</button>'
    
    likes_button.allow_tags = True
    likes_button.short_description = 'Like'

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
