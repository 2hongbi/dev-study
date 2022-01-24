from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .models import Bookmark
from django.urls import reverse_lazy


class BookmarkListView(ListView):
    model = Bookmark


class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name', 'url']   # fields : 어떤 필드들을 입력받을 것인지
    success_url = reverse_lazy('list')  # success_url : 글쓰기를 완료하고 이동할 페이지
    template_name_suffix = '_create'    # 사용할 템플릿의 접미사만 변경하는 설정값


class BookmarkDetailView(DetailView):
    model = Bookmark


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['site_name', 'url']
    template_name_suffix = '_update'


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('list')  # 목록 페이지를 가도록 설정