from django.contrib import admin
from django.urls import path,include
from apiv1 import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.index),
    path('subscriptions/',views.allsubscriptions),
    path('users/',views.allusers),
    path('subscription/<sid>',views.specificSubscription),
    path('user/<uid>',views.specificUser),
    path('subscription/<sid>/users/',views.subscriptionUsers),
    path('subscription/<sid>/user/<uid>',views.subscriptionUserView),
    path('user/<uid>/subscriptions/',views.userSubscriptions),
    path('user/<uid>/subscription/<slid>/',views.userSubscriptionview),
    path('pipeline/',views.getPipeLine),
    path('pipeline/<pid>',views.getspecificPipeline),
    path('sentnotifs/<pid>',views.getSentNotifs),
    path('send/<pid>',views.sendNotification),
    
]
