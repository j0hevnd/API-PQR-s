from django.core.validators import RegexValidator
from django.forms import ValidationError

from rest_framework import serializers, pagination

from apps.pqrs.models import Pqrs


class PqrsSerializer(serializers.ModelSerializer):
    """ Serializador para los PQR's de la base de datos """

    def validate(self, attrs):
        """ Valida campos 'movil_phone, phone, dni'  por medio de expresiones regulares """
        
        errors = {}
        try:
            regex = RegexValidator(r'^\+([\d]{2,3}[\s]{1})[\d]{10}$')
            regex(attrs['movil_phone'])
        except ValidationError:
            errors['movil_phone'] = 'Número no válido, debe ser: +indicativo número, ejmp: +57 3002001000'
            
        try:
            regex = RegexValidator(r'^([\d]{3})[\d]{7}$')
            regex(attrs['phone'])
        except ValidationError as e:
            errors['phone'] = 'Número no válido, debe ser: indicativo_ciudad número, ejmp: 6042436221'

        try:
            regex = RegexValidator(r'^[\d]{8,11}$')
            regex(attrs['dni'])
        except ValidationError as e:
            errors['dni'] = 'Número de documento no válido.'
        
        # Si encuentra algún error retorna estos
        if len(errors) >= 1:
            raise serializers.ValidationError(errors)
        return attrs
    
    class Meta:
        model = Pqrs
        fields = ('id', 'dni', 'type_dni', 'name', 'lastname', 'email', 
                  'phone', 'movil_phone', 'ticket_type', 'title', 'description')
        

class PqrsSerializerDelete(serializers.ModelSerializer):
    """ Serializador usado para la parte de eliminar varios PQR's """
    
    class Meta:
        model = Pqrs
        fields = ('id', 'title')
        
class PqrsPagination(pagination.PageNumberPagination):
    page_size = 3
    max_page_size = 20