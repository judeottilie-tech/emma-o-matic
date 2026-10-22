from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


coins = 0
inventory = [5, 5, 5]


def inventory_list(request):
    return JsonResponse(inventory, safe=False)


def inventory_item(request, item_id):
    if item_id >= len(inventory):
        return HttpResponse(status=404)
    return JsonResponse(inventory[item_id], safe=False)


@csrf_exempt
def handle_coins(request):
    global coins
    if request.method == "PUT":
        coins += 1
        response = HttpResponse(status=204)
        response["X-Coins"] = str(coins)
        return response
    elif request.method == "DELETE":
        returned = coins
        coins = 0
        response = HttpResponse(status=204)
        response["X-Coins"] = str(returned)
        return response
    return HttpResponse(status=405)
