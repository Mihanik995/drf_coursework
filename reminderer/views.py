from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reminderer.models import Habit
from reminderer.paginations import HabitPagination
from reminderer.permissions import IsOwner
from reminderer.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    http_method_names = ['get', 'list', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        if self.action == 'list':
            filter_query = Q()
            filter_query.add(Q(owner__in=[self.request.user]), Q.OR)
            filter_query.add(Q(is_public__in=[True]), Q.OR)

            return Habit.objects.filter(filter_query)

        return self.queryset
