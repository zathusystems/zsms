from schooladminstration.models import Institution
from subscription.models import Feature
from system_admin.models import SystemFeature
from teacher.models import Instructor

def global_data(request):
    ins=SystemFeature.objects.all()[0:5]
    return {'featuress': ins, }
   