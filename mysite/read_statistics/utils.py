import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
def read_statistics_once_read(request,obj):  
    ct = ContentType.objects.get_for_model(obj)
    key='%s_%s_read' % (ct.model,obj.pk)
    if not request.COOKIES.get(key): 
        #总阅读+
        readnum,created=ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)    
        readnum.read_num+=1
        readnum.save() 
        #当天阅读+
        date=timezone.now().date()
        readDetail,created=ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk,date=date)    
        readDetail.read_num+=1
        readDetail.save()    
    return key    
def get_days_read_data(content_type):
    today=timezone.now().date()
    dates=[]
    read_nums=[]
    for i in range(7,0,-1):
        date=today-datetime.timedelta(days=i)
        # dates.append(date.strftime('%m/%d'))
        read_details=ReadDetail.objects.filter(content_type=content_type,date=date)
        result=read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums 
        
        

