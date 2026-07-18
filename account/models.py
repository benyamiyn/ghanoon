from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    
    
    prof_image = models.ImageField(
        
        upload_to = "/profiles",
        blank = True,
        null = True
    )
    
    bio = models.TextField(blank=True)
   
    birth_date= models.DateField(null=True,blank=True)
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        
        return self.user.username
    
#پروفایل حاوی نام نام خانوادگی تاریخ تولد پسوورد یوزرنیم عکس پروفایل . ایمیل است
#همچنین بیوگرافی 
#پیش فرض جنگو تعلاریف مربوط به ایمیل نام نام خانوادگی یوزرنیم پس ورد . ایمیل را تعریف کرده است 