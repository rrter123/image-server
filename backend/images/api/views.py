
from rest_framework import viewsets
from images.models import UploadedImage
from images.api.serializers import UploadedImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedImageSerializer
    queryset = UploadedImage.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)
