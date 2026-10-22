from django.http import JsonResponse

coins = 0
inventory = [5, 5, 5]


def inventory_list(request):
    return JsonResponse(inventory, safe=False)