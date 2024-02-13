from rest_framework import serializers
from apiv1.models import Subscription,SubscriptionLog,NotifierPipeline,users

class SubscriptionSerializer(serializers.ModelSerializer):
    class  Meta:
        model=Subscription
        fields="__all__"

class SubscriptionSerializerInput(serializers.ModelSerializer):
    class  Meta:
        model=Subscription
        fields= (
            'name',
            'category',
            'description',
            'price'
        )

class SubscriptionLogSerializer(serializers.ModelSerializer):
    class  Meta:
        model=SubscriptionLog
        fields="__all__"
class SubscriptionLogSerializerInput(serializers.ModelSerializer):
    class  Meta:
        model=SubscriptionLog
        fields=('user','subscription','sub_type','ispaid')


class NotifierPipelineSerializer(serializers.ModelSerializer):
    class  Meta:
        model=NotifierPipeline
        fields="__all__"   

class NotifierPipelineSerializerInput(serializers.ModelSerializer):
    class  Meta:
        model=NotifierPipeline
        fields=('name','subscription','subtype','subscriptionfeed','issent')  


class userSerializer(serializers.ModelSerializer):
    class  Meta:
        model=users
        fields="__all__"  

class userSerializerInput(serializers.ModelSerializer):
    class  Meta:
        model=users
        fields=('name','emailid','phoneno','isSU') 

