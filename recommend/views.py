from django.shortcuts import render
from .inference import recommend, als_get_recs, popularity_get_recs, hybrid_get_recs, u2idx, i2idx, train_user_items, global_pop_rank    
from rest_framework.response import Response
from rest_framework.decorators import api_view

#test_user= 10   
#print("Hybrid:", recommend(test_user, method="hybrid", K=10))


@api_view(["GET"])
def recommendation(request):
    data=request.data 
    id=data.get("id")
    output=recommend(id, method="hybrid", K=10)
    return Response({"products":output})

@api_view(["GET"])
def recommend_by_id(request,id):
    output=recommend(id, method="hybrid", K=10)
    return Response({"products":output})
