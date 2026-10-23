from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
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
    if item_id < 1 or item_id > len(inventory):
        response = HttpResponse(status=404)
        response["X-Coins"] = str(coins)
        return response

    index = item_id - 1

    if request.method == "GET":
        return JsonResponse(inventory[index], safe=False)

    elif request.method == "PUT":
        if inventory[index] == 0:
            response = HttpResponse(status=404)
            response["X-Coins"] = str(coins)
            return response

        if coins < PRICE:
            response = HttpResponse(status=403)
            response["X-Coins"] = str(coins)
            return response

        change = coins - PRICE
        coins = 0
        inventory[index] -= 1
        response = JsonResponse({"quantity": 1})
        response["X-Coins"] = str(change)
        response["X-Inventory-Remaining"] = str(inventory[index])
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


def machine_page(request):
    return render(request, "machine/index.html", {"coins": coins})
