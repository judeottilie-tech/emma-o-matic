from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


coins = 0
inventory = [5, 5, 5]
PRICE = 2


@csrf_exempt
def inventory_list(request):
    if request.method != "GET":
        return HttpResponse(status=405)
    return JsonResponse(inventory, safe=False)


@csrf_exempt
def inventory_item(request, item_id):
    global coins
    if item_id >= len(inventory):
        response = HttpResponse(status=404)
        response["X-Coins"] = str(coins)
        return response

    if request.method == "GET":
        return JsonResponse(inventory[item_id], safe=False)

    elif request.method == "PUT":
        if inventory[item_id] == 0:
            response = HttpResponse(status=404)
            response["X-Coins"] = str(coins)
            return response

        if coins < PRICE:
            response = HttpResponse(status=403)
            response["X-Coins"] = str(coins)
            return response

        change = coins - PRICE
        coins = 0
        inventory[item_id] -= 1
        response = JsonResponse({"quantity": 1})
        response["X-Coins"] = str(change)
        response["X-Inventory-Remaining"] = str(inventory[item_id])
        return response

    return HttpResponse(status=405)


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
