from django.http import HttpResponse, JsonResponse


coins = 0
inventory = [5, 5, 5]


def inventory_list(request):
    return JsonResponse(inventory, safe=False)


def inventory_item(request, item_id):
    if item_id >= len(inventory):
        return HttpResponse(status=404)
    return JsonResponse(inventory[item_id], safe=False)