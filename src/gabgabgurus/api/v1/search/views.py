# from django.contrib.auth import get_user_model
# from drf_spectacular.utils import extend_schema
# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
#
# from gabgabgurus.api.v1.search.serializers import (
#     InterlocutorListQueryParamsSerializer,
#     InterlocutorListSerializer,
# )
# from gabgabgurus.apps.users.selectors import (
#     get_interlocutors,
#     annotate_user_queryset_with_relations,
#     get_top_members,
# )
# from gabgabgurus.common.utils.api import get_validated_data
#
# User = get_user_model()
#
#
# @extend_schema(parameters=[InterlocutorListQueryParamsSerializer])
# class InterlocutorListView(ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = User.objects.all()
#     serializer_class = InterlocutorListSerializer
#     filterset_fields = ("first_name", "last_name", "email")
#
#     def get_queryset(self):
#         query_param_serializer = InterlocutorListQueryParamsSerializer
#         validated_data = get_validated_data(
#             query_param_serializer,
#             self.request.query_params,
#             raise_exception=False,
#         )
#
#         qs = get_interlocutors(
#             speaks=validated_data.get("speaks"),
#             learning=validated_data.get("learning"),
#             countries=validated_data.get("countries"),
#             hobbies=validated_data.get("hobbies"),
#             lookup_field="name",
#         )
#
#         return qs
#
#
# class TopMembersView(ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = User.objects.all()
#     serializer_class = InterlocutorListSerializer
#     pagination_class = None
#
#     def get_queryset(self):
#         qs = get_top_members()
#         qs = annotate_user_queryset_with_relations(qs)
#         return qs
