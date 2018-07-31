from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'email',
            'fullname',
            'address',
            'contact_phone',
            'birthday',
        )

