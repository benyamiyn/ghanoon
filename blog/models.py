from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
# یک کلاس برای هر مقاله که حاوی متن  عنوانه نویسنده تاریخ ایجاد
#وتاربیخ آخرین ویرایش است
class Maqale(models.Model):
    title = models.CharField(max_length=255)
    #title
    matn = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    #عنوان نویسنده بیان می شود نویسندممبر است ولی هر ممبری نویسنده نیست!
    #هر نویسنهده چنیدن مقاله دارد ولی هر مقاله یک نویسنده دارد
    
class Comment(models.Model):
    
    maqale = models.ForeignKey(
        Maqale,
        on_delete = models.CASCADE,
        relatd_name = "comment"
    )
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.username} - {self.maqale.title}"
    
    