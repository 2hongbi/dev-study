from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')

    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png')
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)   # auto_now_add : 객체가 추가될 때 자동으로 값을 설정
    updated = models.DateTimeField(auto_now=True)   # auto_now : 객체가 수정될 때마다 자동으로 값을 설정

    class Meta:
        ordering = ['-updated']     # 해당 모델의 객체들을 어떤 기준으로 정렬할 것인지 설정하는 옵션. 내림차순 정렬

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        # get_absolute_url : 객체의 상세 피이지의 주소를 반환하는 메서드, 상세 화면의 패턴 이름 : photo:photo_detail
        return reverse('photo:photo_detail', args=[str(self.id)])