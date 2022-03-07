from django.db import models
from django.urls import reverse


class Bookmark(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField('Site URL')

    def __str__(self):
        # 객체를 출력할 때 나타날 값
        return "이름 : " + self.site_name + ", 주소 : " + self.url

    def get_absolute_url(self):
        # 수정이 완료된 후 이동할 페이지는 뷰에 success_url이 설정되어 있거나 모델에 get_absolute_url이라는 메서드를 통해 결정
        return reverse('detail', args=[str(self.id)])