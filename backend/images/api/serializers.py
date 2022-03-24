from images.models import UploadedImage
from rest_framework import serializers


class UploadedImageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UploadedImage
        fields = '__all__'
