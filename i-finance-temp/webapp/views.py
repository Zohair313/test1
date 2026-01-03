from django.http import JsonResponse
from .models import *


# Create your views here.
def get_all_mujtahid_representative(request):
    obligation_type_id = request.GET.get('obligation_type')
    query = MujtahidRepresentative.objects.filter(wakalatype__obligation_type=obligation_type_id)
    data = [{'id': mujtahid_repr.id, 'repr': str(mujtahid_repr)} for mujtahid_repr in query]
    return JsonResponse(data, safe=False)
