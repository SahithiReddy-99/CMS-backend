from rest_framework import serializers
from app.models import User, Flat, Bill, Reciept, Roles, Employees, Visitors


class FlatOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'mobileNo', 'email', 'username']


# class BlockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Block
#         fields = ['id', 'name', 'description']


class FlatSerializer(serializers.ModelSerializer):
    ownerId = FlatOwnerSerializer(read_only=True)
    # blockId = BlockSerializer(read_only=True)

    class Meta:
        model = Flat
        fields = ['id', 'name', 'description', 'type', 'address', 'ownerId']


class BillSerializer(serializers.ModelSerializer):
    ownerId = FlatOwnerSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = "__all__"


class RecieptSerializer(serializers.ModelSerializer):
    billId = BillSerializer(read_only=True)

    class Meta:
        model = Reciept
        fields = "__all__"


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"


class EmployeesSerializer(serializers.ModelSerializer):
    # roleId = RolesSerializer(read_only=True)

    class Meta:
        model = Employees
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    flatId = FlatSerializer(read_only=True, many=True)

    class Meta:
        model = Visitors
        fields = "__all__"


class EmployeeServicesSerializer(serializers.ModelSerializer):
    employeeId = EmployeesSerializer(read_only=True, many=True)
    flatId = FlatSerializer(read_only=True, many=True)
