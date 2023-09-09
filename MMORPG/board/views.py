from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from .forms import AdForm, ResponseForm, ResponseFilter
from .models import Ad, Response
from django.contrib import messages


# Create your views here.
class AdListView(ListView):
    model = Ad
    template_name = 'ad_list.html'
    context_object_name = 'ads'
    queryset = Ad.objects.order_by('-created_at')
    paginate_by = 9


class AdDetailView(DetailView):
    template_name = 'ad_detail.html'
    queryset = Ad.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = context['ad']

        # Проверяем, есть ли у пользователя уже отклик на это объявление
        user_has_response = ad.response_set.filter(responseUser=self.request.user).exists()

        context['user_has_response'] = user_has_response
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ad_create.html'
    form_class = AdForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('board:ad_detail', kwargs={'pk': self.object.pk})


class AdDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'ad_delete.html'
    queryset = Ad.objects.all()
    success_url = reverse_lazy('home')


class AdUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'ad_create.html'
    form_class = AdForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)


def respond_to_ad(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    user = request.user
    if ad.author == user:
        messages.error(request, "Вы не можете оставить отзыв на свою собственную статью.")
        return redirect('board:ad_detail', ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.responseAd = ad
            response.responseUser = request.user
            response.save()
            send_email_notification(response)
            return redirect('board:ad_detail', ad_id)
    else:
        form = ResponseForm()

    return render(request, 'response_form.html', {'form': form, 'ad': ad})


class PersonRoomView(TemplateView):
    template_name = 'cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        responses = Response.objects.filter(responseAd__author=user)
        context['responses'] = responses

        # Используйте ResponseFilter для фильтрации откликов
        response_filter = ResponseFilter(self.request.GET, queryset=responses)
        context['response_filter'] = response_filter

        return context


def accept_response(request, response_id):
    user = request.user

    # Получаем отклик по его ID или возвращаем 404, если отклик не существует
    response = get_object_or_404(Response, id=response_id)

    # Проверяем, что пользователь, пытающийся принять отклик, является автором объявления
    if user == response.responseAd.author:
        response.is_accepted = True
        response.save()
        send_acceptance_email(response)
        messages.success(request, "Отклик успешно принят.")
    else:
        messages.error(request, "Вы не можете принять свой собственный отклик.")
    # После обработки принятия отклика перенаправляем пользователя обратно на страницу откликов
    return redirect('cabinet')


def delete_response(request, response_id):
    user = request.user

    # Получаем отклик по его ID или возвращаем 404, если отклик не существует
    response = get_object_or_404(Response, id=response_id)

    # Проверяем, что пользователь, пытающийся удалить отклик, является автором объявления
    if user == response.responseAd.author:
        response.delete()
        messages.success(request, "Отклик успешно удален.")
    else:
        messages.error(request, "Вы не можете удалить отклик, который не является вашим.")

    # После удаления отклика перенаправляем пользователя обратно на страницу откликов
    return redirect('cabinet')


def send_email_notification(response):
    subject = 'Новый отклик на ваше объявление'
    message = f'Получен новый отклик на ваше объявление "{response.responseAd.title}".'
    from_email = settings.DEFAULT_FROM_EMAIL  # Адрес, с которого будет отправлено уведомление
    recipient_list = [response.responseAd.author.email]  # Адрес получателя (в данном случае, автор объявления)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def send_acceptance_email(response):
    subject = 'Ваш отклик принят'
    message = f'Ваш отклик на объявление "{response.responseAd.title}" был принят.'
    from_email = settings.DEFAULT_FROM_EMAIL  # Адрес, с которого будет отправлено уведомление
    recipient_list = [response.responseUser.email]  # Адрес получателя (в данном случае, автор отклика)
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
