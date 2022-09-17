from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
<<<<<<< HEAD
    pass
=======
    pass
>>>>>>> cca0c517d865d14422d3af979c2de2cc09d0daef
