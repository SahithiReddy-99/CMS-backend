
from rest_framework import serializers
from app.models import User, Flat, Bill, Reciept, Roles, Block, Visitors,Reviews

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class FlatOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'mobileNo', 'email', 'occupation']


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = [ 'name', 'description']


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


# class EmployeesSerializer(serializers.ModelSerializer):
#     # roleId = RolesSerializer(read_only=True)
#
#     class Meta:
#         model = Employees
#         fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    flatId = FlatSerializer(read_only=True, many=True)

    class Meta:
        model = Visitors
        fields = "__all__"


class EmployeeServicesSerializer(serializers.ModelSerializer):
    employeeId = User()
    flatId = FlatSerializer(read_only=True, many=True)

class ReviewSerializer(serializers.ModelSerializer):
    userId=User()

    class Meta:
        model = Reviews
        fields = "__all__"