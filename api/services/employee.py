from api.models.employee import Employee


class EmployeeService:
    @staticmethod
    def create(validated_data: dict):
        return Employee.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

    @staticmethod
    def get(pk: int) -> Employee:
        return Employee.objects.get(pk=pk)

    @staticmethod
    def exists(pk: int) -> bool:
        return Employee.objects.filter(pk=pk).exists()
