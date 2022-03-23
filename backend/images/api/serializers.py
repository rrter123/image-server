from images.models import UploadedImage
from rest_framework import serializers

class UploadedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedImage
        fields = '__all__'
