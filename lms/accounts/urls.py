from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.dashboard),
    url(r'^dashboard/$',views.dashboard,name="dashboard"),
    url(r'^register/$', views.CreateEmployeeView.as_view(), name='register'),
    url(r'^update_profile/$', views.update_profile, name='update'),
    url(r'^update_leave/(?P<pk>[-\w]+)/$', views.update_leave, name='update-leave'),
    url(r'^application/$', views.CreateLeaveView.as_view(), name='application'),
    url(r'^history/$', views.LeaveListView.as_view(), name='history'),
    url(r'^history/(?P<pk>[-\w]+)/$', views.LeaveDetailView.as_view(), name='leave-detail'),
    url(r'^email_verification/(?P<email_token>[^/]+)/', views.email_verification),
    url(r'^chat/$', views.process),
    ]