from ckeditor.fields import RichTextField
from django.db import models
# Create your models here.
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Tittle')
    text = RichTextField(verbose_name='Text')

    published_at = models.DateTimeField(verbose_name='Publish date')
    image = models.ImageField(null=True, blank=True, verbose_name='Image', )
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ("-published_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


        # TODO:
        #<< articles should be related to products
        #also check media dir for article pictures and if they are in git repository
