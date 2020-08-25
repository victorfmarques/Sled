from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user model """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """ Creates a new user """
        return get_user_model().objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    """ Serializer for user token """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validates and authenticates user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
