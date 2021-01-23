from rest_framework import mixins, viewsets


class CreateAndListAndDeleteViewSet(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    pass
