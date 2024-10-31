from django.db import models
from shop.models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SiteSlider(models.Model):
    image = models.ImageField(upload_to='sliders', verbose_name='عکس')
    url = models.URLField(max_length = 200, verbose_name = 'ادرس اسلایدر')
    is_active = models.BooleanField(default= True, verbose_name= 'فعال / غیر فعال')
    
    class Meta:
        verbose_name = 'اسلایدر سایت'
        verbose_name_plural = 'اسلایدر'
    
    def __str__(self) :
        return self.url
    
def validate_video_file(value):
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    if not any([value.name.endswith(ext) for ext in valid_extensions]):
        raise ValidationError(_('فقط فایل‌های ویدیویی با پسوندهای %(valid_extensions)s مجاز هستند.'),
                              params={'valid_extensions': ', '.join(valid_extensions)})    

class Story(models.Model):
    thumbnail = models.ImageField(upload_to='story_thumbnails', verbose_name='تامبنیل')
    title = models.CharField(max_length = 200, verbose_name = 'عنوان')
    video = models.FileField(upload_to='stories', verbose_name='ویدیو', validators=[validate_video_file])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', null=True, blank=True)
    is_active = models.BooleanField(default= True, verbose_name= 'فعال / غیر فعال')
    
    class Meta:
        verbose_name = 'استوری'
        verbose_name_plural = 'استوری ها'
    
    def __str__(self) :
        return self.title
    
class SiteBanner(models.Model):
    image = models.ImageField(upload_to='banners', verbose_name='عکس')
    url = models.URLField(max_length = 200, verbose_name = 'ادرس اسلایدر')
    is_active = models.BooleanField(default= True, verbose_name= 'فعال / غیر فعال')
    
    class Meta:
        verbose_name = 'بنر سایت'
        verbose_name_plural = 'بنر'
    
    def __str__(self) :
        return self.url