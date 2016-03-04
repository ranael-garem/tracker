from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )
    password = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message="This email has already been registered",
                            )]
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get(
            'username', instance.username)

        instance.save()

        password = validated_data.get('password', None)

        if password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance
