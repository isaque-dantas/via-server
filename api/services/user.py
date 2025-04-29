from api.models.user import User


class UserService:
    @staticmethod
    def create(validated_data: dict):
        return User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
