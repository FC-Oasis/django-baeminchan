from django.contrib.auth import get_user_model
from rest_framework import serializers, generics
from rest_framework.response import Response

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     label='비밀번호')

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'email',
            'fullname',
            'jibun_address',
            'road_address',
            'contact_phone',
            'birthday',
        )

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True,
    )
    check_new_password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'new_password',
            'check_new_password',
        )

    def validate(self, data):
        if data.get('new_password') != data.get('check_new_password'):
            raise serializers.ValidationError('비밀번호가 맞지 않습니다')
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance


class EmailChangeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=500,)

    class Meta:
        model = User
        fields = ('email',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get(
            'email', instance.email
            )
        instance.save()
        return instance


class ContactPhoneChangeSerializer(serializers.ModelSerializer):
    contact_phone = serializers.CharField(max_length=500,)

    class Meta:
        model = User
        fields = ('contact_phone',)

    def update(self, instance, validated_data):
        instance.contact_phone = validated_data.get(
            'contact_phone', instance.contact_emial
        )
        instance.save()
        return instance

