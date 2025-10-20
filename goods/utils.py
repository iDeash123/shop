import keyword
import re
from goods.models import Products
from django.db.models import Q


def q_search(querry):

    if querry.isdigit() and len(querry) <= 5:
        return Products.objects.filter(id=int(querry))

    keywords = [word for word in querry.split() if len(word) > 2]

    q_objects = Q()

    for token in keywords:
        if token in keywords:
            q_objects |= Q(description__icontains=token)
            q_objects |= Q(name__icontains=token)

    return Products.objects.filter(q_objects)
