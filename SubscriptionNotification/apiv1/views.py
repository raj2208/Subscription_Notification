from django.shortcuts import render
from django.http import HttpResponse
from apiv1.models import Subscription,SubscriptionLog,NotifierPipeline,users
from rest_framework.decorators import api_view
from apiv1.serializers import SubscriptionLogSerializer, SubscriptionSerializer, NotifierPipelineSerializer,SubscriptionSerializerInput,userSerializer,userSerializerInput,NotifierPipelineSerializerInput,SubscriptionLogSerializerInput
from rest_framework.response import Response
from django.contrib.auth.models import User
from .pipeline_send import send
import threading
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
def index(request):
    return HttpResponse("Please Refer The Endpoint Docs to Hit the Endpoints")


@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def allsubscriptions(request):
    if request.method=='GET':
        subs=Subscription.objects.all()
        subsSerializer=SubscriptionSerializer(subs,many=True)
        return Response(subsSerializer.data)

    elif request.method=='POST':
        subsSerializerInput= SubscriptionSerializerInput(data=request.data)
        if subsSerializerInput.is_valid():
            subsSerializerInput.save()
            return Response(subsSerializerInput.data)
        return Response(subsSerializerInput.errors)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def allusers(request):
    if request.method=='GET':
        myusers=users.objects.all()
        serializedUsers=userSerializer(myusers,many=True)
        return Response(serializedUsers.data)
    elif request.method=='POST':
        savingUser=userSerializerInput(data=request.data)
        if savingUser.is_valid():
            savingUser.save()
            return Response(savingUser.data)
        return Response(savingUser.errors)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def specificSubscription(request,sid):
    if request.method=='GET':
        try:
            sub=Subscription.objects.get(id=int(sid))
            serializer=SubscriptionSerializer(sub)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='PUT':
        try:
            sub=Subscription.objects.get(id=int(sid))
            serializer=SubscriptionSerializerInput(sub,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='DELETE':
        try:
            sub=Subscription.objects.get(id=int(sid))
            sub.delete()
        except Exception as e:
            return Response({"Error":str(e)})
    



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def specificUser(request,uid):
    if request.method=='GET':
        try:
            sub=users.objects.get(id=int(uid))
            serializer=userSerializer(sub)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='PUT':
        try:
            myuser=users.objects.get(id=int(uid))
            serializer=userSerializerInput(myuser,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='DELETE':
        try:
            myuser=users.objects.get(id=int(uid))
            myuser.delete()
            return Response({"DELETED":"True"})
        except Exception as e:
            return Response({"Error":str(e)})


    
        
        

    



@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def subscriptionUsers(request,sid):
    if request.method=='GET':
        try:
            sub=Subscription.objects.get(id=int(sid))
            allsubs=SubscriptionLog.objects.filter(subscription=sub)
            serializer=SubscriptionLogSerializer(allsubs,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'Error':str(e)})

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def subscriptionUserView(request,sid,uid):
    if request.method=='GET':
        try:
            sub=Subscription.objects.get(id=sid)
            user=users.objects.get(id=uid)  
            slog=SubscriptionLog.objects.get(subscription=sub,user=user)
            serializer=SubscriptionLogSerializer(slog)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='PUT':
        try:
            sub=Subscription.objects.get(id=sid)
            myuser=users.objects.get(id=uid)  
            slog=SubscriptionLog.objects.get(subscription=sub,user=myuser)
            if "user" in request.data and request.data['user']==myuser.id:
                serializer=SubscriptionLogSerializerInput(slog,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            else:
                return Response({"Error":"Ambigious user please enter user else check the user"})
        except:
            return Response({"Error":str(e)})
                
    elif request.method=='DELETE':
        try:
            sub=Subscription.objects.get(id=sid)
            myuser=users.objects.get(id=uid)  
            slog=SubscriptionLog.objects.get(subscription=sub,user=myuser)
            slog.delete()
            return Response({"DELETED":"True"})
        except Exception as e:
            return Response({"Error":str(e)})
            


    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def userSubscriptions(request,uid):
    if request.method=='GET':
        try:
            myuser=users.objects.get(id=int(uid))
            subs=SubscriptionLog.objects.filter(user=myuser)
            serializer=SubscriptionLogSerializer(subs,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    
    elif request.method=='POST':
        try:
            postdata=request.data
            print(postdata)
            verifyuser=users.objects.get(id=int(postdata["user"]))
            myuser=users.objects.get(id=int(uid))
            print(myuser)
            print(verifyuser)
            if myuser==verifyuser:
                serializer=SubscriptionLogSerializerInput(data=postdata)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            else:
                return Response({"Error":"User not matching"})
        except Exception as e:
            return Response({"Error":str(e)})
    
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def userSubscriptionview(request,uid,slid):
    if request.method=='GET':
        try:
            sluser=users.objects.get(id=uid)
            subslog=SubscriptionLog.objects.get(id=slid,user=sluser)
            serializer=SubscriptionLogSerializer(subslog)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"Error":str(e)})
        
    elif request.method=='PUT':
        try:
            sluser=users.objects.get(id=uid)
            subslog=SubscriptionLog.objects.get(id=slid,user=sluser)
            if request.data['user'] == sluser.id:
                serializer=SubscriptionLogSerializerInput(subslog,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            else:
                return Response({"Error":"Ambigous users"})
        except Exception as e:
            return Response({"Error":str(e)})
    
    elif request.method=='DELETE':
        try:
            sluser=users.objects.get(id=uid)
            subslog=SubscriptionLog.objects.get(id=slid,user=sluser)
            subslog.delete()
            return Response({"DELETED":"True"})
        except Exception as e:
            return Response({"Error":str(e)})

    


@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def getPipeLine(request):
    if request.method=='GET':
        try:
            allNotifs=NotifierPipeline.objects.filter(issent=False)
            serialzer=NotifierPipelineSerializer(allNotifs,many=True)
            return Response(serialzer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    elif request.method=='POST':
        try:
            notif=NotifierPipelineSerializerInput(data=request.data)
            if notif.is_valid():
                notif.save()
                return Response(notif.data)
            return Response(notif.errors)
        except Exception as e:
            return Response({"Error":str(e)})


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def getspecificPipeline(request,pid):
    if request.method=='GET':
        try:
            notif=NotifierPipeline.objects.filter(id=int(pid),issent=False)
            print(notif)
            serializer=NotifierPipelineSerializer(notif,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error":str(e)})
    
    elif request.method=='PUT':
        try:
            notif=NotifierPipeline.objects.get(id=int(pid))
            serializer=NotifierPipelineSerializerInput(notif,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error)
        except Exception as e:
            return Response({"Error":str(e)})
        
    elif request.method=='DELETE':
        try:
            notif=NotifierPipeline.objects.filter(id=int(pid),issent=False)
            notif.delete()
            return Response({"Deleted":"True"})
        except Exception as e:
            return Response({"Error":str(e)})


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def sendNotification(request,pid):
    try:
        notif=NotifierPipeline.objects.get(id=int(pid),issent=False)
        sub=Subscription.objects.get(id=notif.subscription.id)

        userstosend=SubscriptionLog.objects.filter(subscription=sub,sub_type=notif.subtype,ispaid=True)
        emails=[]
        for objs in userstosend:
            emails.append(objs.user.emailid)
        print(emails)
        if len(emails)<2:
            send1_thread=threading.Thread(target=send,args=(emails,notif.name,notif.subscriptionfeed))
            print(emails)
            send1_thread.start()
            send1_thread.join()
        else:
            emails1 = emails[:len(emails)//2]  
            send1_thread=threading.Thread(target=send,args=(emails1,notif.name,notif.subscriptionfeed))
            send1_thread.start()
            emails2 = emails[len(emails)//2:] 
            send2_thread=threading.Thread(target=send,args=(emails2,notif.name,notif.subscriptionfeed))
            send2_thread.start()
            send1_thread.join()
            send2_thread.join()
        
        print("sent")
        notif.issent=True
        notif.save()
        return Response({"Sent":"Yes"})
    except Exception as e:
        return Response({"Error":str(e)})



@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, ])
def getSentNotifs(request,pid):
    if request.method=='GET':
        try:
            notif=NotifierPipeline.objects.get(id=int(pid),issent=True)
            serializer=NotifierPipelineSerializer(notif)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Error": str(e)})
    

    


        






        
