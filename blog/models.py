from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

# Create your models here.
# یک کلاس برای هر مقاله که حاوی متن  عنوانه نویسنده تاریخ ایجاد
#وتاربیخ آخرین ویرایش است


class Category(models.Model):
    
    
    title = models.CharField(max_length=100)
    
    def __str__(self):
        
        return self.title    
    #یک مدل برای کامنت ها 
    #def __str__ هنگام راخوانی نام تابع عنوان را برمی گرداند
 
 
    
class Maqale(models.Model):
    
    title = models.CharField(max_length=255)
    #title
    matn = models.TextField()
    #متن مقاله
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "maqalat"
    )
    thumbnail = models.ImageField(
    upload_to="maqale_thumbnails/",
    blank=True,
    null=True
    )
    #thumbnail برای عکس تامنیل است 
    #ForeignKey نوعی رابطه یک به چند ایجاد می کند یعنی هر نویسنده چند مقاله ممکن است داشته باشد
    #هر نویسنده یک مقاله دارد که  نوسنده نوعی عضو در وبلاگ است 
    
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name = "maqalat"
    )
    #برای دسته بندی ههر مقاله 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #تاریخ ایجاد و تاریخ آپدیت
   
    #عنوان نویسنده بیان می شود نویسندممبر است ولی هر ممبری نویسنده نیست!
    #هر نویسنهده چنیدن مقاله دارد ولی هر مقاله یک نویسنده دارد
    def __str__(self):
        
        return self.title
    
class Comment(models.Model):

    maqale = models.ForeignKey(
        Maqale,
        on_delete = models.CASCADE,
        related_name = "comments"
    )
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name = "comments"
    )
    parent = models.ForeignKey(
        "self",
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = "children",
   )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,)
    is_edited = models.BooleanField(default=False)
    class Meta:
        ordering =[
            "created_at",
        ]
#مدلی برای کامنت ها که یک فرد می تواند چنذد کامنت بذارد و هر مقاله می تواند چند کامنت داشته باشد 
    def __str__(self):
        
        return f"{self.author.username} - {self.maqale.title}"

    @property
    def is_parent(self):
        
        return self.parent is None
    
    def get_absolute_url(self):
        return reverse(
            "blog:detail",
            kwargs={
                "slug": self.maqale.slug,
            },
        )
    
class Like(models.Model):
    
    maqale = models.ForeignKey(
        Maqale,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "likes"
    ) 
    class Meta:
        
        constraints = [
        models.UniqueConstraint(
            fields=["user", "maqale"],
            name="unique_user_like"
        )
    ]
        
    def __str__(self):
        
        return f"{self.user.username} likes {self.maqale.title}"
#مدلی برای لایک ها
# هر فرد می تواند چند مقاله را لایک کند 
# هر مقاله گزینه لایک کردن دارد هر فرد می تواند فقط یک بار یک مقاله را لایک کند 
#این ویژگی با class meta  تعریف شده است 
  

    