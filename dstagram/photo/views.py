from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Photo


def photo_list(request):
    # 함수형 뷰는 기본 매개변수로 request 설정
    photos = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos':photos})


class PhotoUploadView(CreateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html'     # 실제 사용할 템플릿 설정

    def form_valid(self, form):     # 업로드를 끝낸 후 이동할 페이지를 호출하기 위해 사용하는 메서드
        form.instance.author_id = self.request.user.id      # 작성자는 현재 로그인 한 사용자로 설정
        if form.is_valid():     # 입력된 값 검증
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'


class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'
