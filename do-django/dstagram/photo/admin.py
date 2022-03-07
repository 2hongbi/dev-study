from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created', 'updated']   # list_display : 목록에 보일 필드 설정
    raw_id_fields = ['author']      # raw_id_fields : 검색 기능을 사용해 선택할 수 있음
    list_filter = ['created', 'updated', 'author']  # list_filter : 필터 기능을 사용할 필드 선택
    search_fields = ['text', 'created']     # search_fields : 검색 기능을 통해 검색할 필드 선택
    ordering = ['updated', '-created']      # ordering : 모델의 기본 정렬값이 아닌 관리자 사이트에서 기본으로 사용할 정렬값 설정


admin.site.register(Photo, PhotoAdmin)
