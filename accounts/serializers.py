from rest_framework import serializers
from django.contrib.auth import get_user_model

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        field = [
            "username",
            "password"
        ]
        extra_kwargs = {
            "password" : {"write_only" : True}
        }

    def create(self, validated_data):
        user = get_user_model()(
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 올바르지 않습니다.")
        return value
    
    def validate(self, attrs):
        new_password1 = attrs.get("new_password1")
        new_password2 = attrs.get("new_password2")
        if new_password1 != new_password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        
        user = self.context['request'].user
        if user.check_password(new_password1):
            raise serializers.ValidationError("기존 비밀번호와 동일합니다.")
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user