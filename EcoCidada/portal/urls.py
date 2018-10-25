from django.conf.urls import include, url

from portal import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home', views.home, name='home'),
    url(r'^divmidias', views.midias, name='midias'),
    url(r'^midias/alfakit', views.send_alfakit, name='send_alfakit'),
    url(r'^midias/data_collector', views.send_collector, name='send_collector'),
    url(r'^data', views.send_file, name='send_file'),
]
