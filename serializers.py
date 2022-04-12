from rest_framework import serializers
from .models import Student


#Model serializers
#Validator concept is same

#priority wise 1.validator->2.field level validator->3.object level validator

#Validator this type of validator are used if it's requred to reuse in differet fields
def start_with_r(value):
    if value[0].lower()!='r':
        raise serializers.ValidationError("Name must start with R")
    return value

class StudentSerializer(serializers.ModelSerializer):
    #To add extra properties to field
    #name=serializers.CharField(read_only=True) #This will make the name field read only it cant be updated
    #To apply validator we need to create the fields explicetly on which it's required to create
    name=serializers.CharField(validators=[start_with_r])
    class Meta:
        model=Student
        fields=['id','name','roll','city']
        #Read only can be achived in another way
        #read_only_fields=['name','roll']
        #another methode is extra_kwargs here all the extra properties can be applied in the dictionary
        extra_kwargs={'name':{'read_only':True}}
    
    #Validators: validators are called when serializerr.is_valid() is called.
    #This is field level validation 
    #Done for single field
    def validate_roll(self,value):
        if value>=200:
            raise serializers.ValidationError("No more addmisson seates are full!!!")
        return value
    
    #Object level validation
    #This is used to validate multiple fileds
    #data contain all the fields
    def validate(self,data):
        nm=data.get("name")
        ct=data.get("city")
        if nm.lower()=="rohit" and ct.lower()!="ranchi":
            raise serializers.ValidationError("city must be ranchi")
        return data

'''
#priority wise 1.validator->2.field level validator->3.object level validator

#Validator this type of validator are used if it's requred to reuse in differet fields
def start_with_r(value):
    if value[0].lower()!='r':
        raise serializers.ValidationError("Name must start with R")
    return value

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200,validators=[start_with_r])
    roll=serializers.IntegerField()
    city=serializers.CharField(max_length=100)

    def create(self,validated_data):
        return Student.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.roll = validated_data.get('roll',instance.roll)
        instance.city = validated_data.get('city',instance.city)
        instance.save()
        return instance
    
    #Validators: validators are called when serializerr.is_valid() is called.
    #This is field level validation 
    #Done for single field
    def validate_roll(self,value):
        if value>=200:
            raise serializers.ValidationError("No more addmisson seates are full!!!")
        return value
    
    #Object level validation
    #This is used to validate multiple fileds
    #data contain all the fields
    def validate(self,data):
        nm=data.get("name")
        ct=data.get("city")
        if nm.lower()=="rohit" and ct.lower()!="ranchi":
            raise serializers.ValidationError("city must be ranchi")
        return data
'''