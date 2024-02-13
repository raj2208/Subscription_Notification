from django.contrib import admin
from apiv1.models import Subscription,NotifierPipeline,SubscriptionLog,users


admin.site.register(Subscription)
admin.site.register(SubscriptionLog)
admin.site.register(NotifierPipeline)
admin.site.register(users)