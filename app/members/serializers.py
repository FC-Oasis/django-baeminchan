import re

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from members.models import Phone

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        label='비밀번호',
        min_length=8,
        help_text='8자 이상 입력',)
    email = serializers.EmailField(
        required=True,
        label='이메일',
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

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

    def validate(self, data):
        phone = data.get('contact_phone')
        if not re.match('\d{3}[-]\d{4}[-]\d{4}$', phone):
            raise serializers.ValidationError('올바른 전화번호 형식이 아닙니다')
        else:
            return data

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data,
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class PasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    check_new_password = serializers.CharField(
        write_only=True,
        min_length=8,
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
    email = serializers.EmailField(max_length=500, write_only=True,)

    class Meta:
        model = User
        fields = ('email',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get(
            'email', instance.email
            )
        instance.save()
        return instance

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError('이미 사용중인 이메일입니다')
        return data


class ContactPhoneChangeSerializer(serializers.ModelSerializer):
    contact_phone = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ('contact_phone',)

    def validate(self, data):
        new_phone = data.get('contact_phone')
        if not re.match('\d{3}[-]\d{4}[-]\d{4}$', new_phone):
            raise serializers.ValidationError('올바른 전화번호 형식이 아닙니다')
        else:
            return data

    def update(self, instance, validated_data):
        instance.contact_phone = validated_data.get('contact_phone')
        instance.save()
        return instance


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

    def validate(self, data):
        new_phone = data.get('contact_phone')

        if not re.match('\d{3}[-]\d{4}[-]\d{4}$', new_phone):
            raise serializers.ValidationError('올바른 전화번호 형식이 아닙니다')
        else:
            return data


class PhoneAuthSerializer(PhoneSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

    def validate(self, data):
        super().validate(data)
        created_at = Phone.objects.get(contact_phone=data.get('contact_phone')).created_at
        now = timezone.now()

        if created_at + timezone.timedelta(minutes=5) <= now:
            raise serializers.ValidationError('인증 가능 시간이 지났습니다.')
        else:
            return data
