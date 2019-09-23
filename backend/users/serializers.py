from rest_framework import serializers
from users.models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        fields = ('user', 'address', 'state', 'postal_code')


class UserSerializer(serializers.ModelSerializer):
    # companies = CompaySerializer(many=True, read_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        profile = instance.profile

        profile.address = profile_data.get('address', profile.address)
        profile.state = profile_data.get('state', profile.state)
        profile.postal_code = profile_data.get('postal_code', profile.postal_code)
        profile.save()

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance
