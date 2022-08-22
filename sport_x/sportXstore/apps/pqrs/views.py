from django.db import connection

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
)

from apps.pqrs.models import Pqrs
from apps.pqrs.serializers import PqrsSerializer, PqrsSerializerDelete, PqrsPagination


class PqrsListApiView(ListAPIView):
    """ Lista todas las PQR's """
    serializer_class = PqrsSerializer
    pagination_class = PqrsPagination
    queryset = Pqrs.objects.filter(status=True)
    
    
class PqrsCreateApiView(CreateAPIView):
    """ Crear PQR's """
    
    serializer_class = PqrsSerializer
    
    def create(self, request, *args, **kwargs) -> Response:
        """ Intercepta el método POST, para devolver una repuesta personalizada
            Return:
                Respuesta tipo Json, mensaje de correcto o devuelve los datos inválidos
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'message_success': 'PQR´s cargado correctamente.'}, status=status.HTTP_201_CREATED)
    

class PqrsDetailApiView(RetrieveAPIView):
    """ Recupera una PQR de la base de datos """
    
    serializer_class = PqrsSerializer
    queryset = Pqrs.objects.filter(status=True)
    

class PqrsRetrieveUpdateApiView(RetrieveUpdateAPIView):
    """ Recupera una PQR de la base de datos y permite actualizarla """
    
    serializer_class = PqrsSerializer
    queryset = Pqrs.objects.filter(status=True)
    
    def put(self, request, *args, **kwargs) -> Response:
        """ Interceptamos el método PUT/POST para devolver una repuesta personalizada
            Return:
                Respuesta tipo Json, con datos correctos o invalidos
        """
        
        instance = self.get_object()
        instance.dni = request.data['dni']
        instance.type_dni = request.data['type_dni']
        instance.name = request.data['name']
        instance.lastname = request.data['lastname']
        instance.email = request.data['email']
        instance.phone = request.data['phone']
        instance.movil_phone = request.data['movil_phone']
        instance.ticket_type = request.data['ticket_type']
        instance.title = request.data['title']
        instance.description = request.data['description']
        
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'message_success': 'PQR editado correctamente'}, status=status.HTTP_200_OK)
        

class PqrsDeleteApiView(DestroyAPIView):
    """ Elimina solo una PQR """
    
    queryset = Pqrs.objects.filter(status=True)
     
    def delete(self, request, pk=None, *args, **kwargs) -> Response:
        pqrs = self.queryset.filter(id = pk).first()
        if pqrs:
           pqrs.status = False
           pqrs.save()
           return Response({'message_success': 'PQR eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'message_error': 'PQR no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
    

class PqrsDeleteSeveralApiView(APIView):
    """ Elimina una o más PQR's de la base de datos """
    
    def sql_delete_several_items(self, ids) -> bool:
        """ 
        Funcion para SQL personalizado con el fin de borrar 
        varios datos al tiempo.
        
        Args:
            ids (list): lista con diccionarios los ids a borrar
            
        Returns:
            bool 
        """
        array_ids = []
        for items in ids:
            for key, value in items.items():  
                array_ids.append(value)
                
        msg_error = None
        try:
            for pk in array_ids:
                Pqrs.objects.get(id=pk, status=1)
            
            with connection.cursor() as cursor:
                for pk in array_ids:
                    try:
                        row = cursor.execute("UPDATE %s SET status=0 WHERE id = %s and status=1" % (Pqrs._meta.db_table, pk))
                        if row.rowcount < 1: raise AttributeError("El PQR con id %s no existe" % (pk,))
                        
                    except AttributeError as e: msg_error = "Error causado por...", e
                        
        except Pqrs.DoesNotExist as e: msg_error = "Alguno de los/el id's pasados no existe."
        
        if msg_error: 
            return False, msg_error
        return (True,)
    
    def get(self, request) -> Response:
        """ Obtiene las PQR's disponibles para eliminar """
        
        queryset = Pqrs.objects.filter(status=True)
        pqrs_serializer = PqrsSerializerDelete(queryset, many=True)
        if pqrs_serializer.data:
            return Response(pqrs_serializer.data, status= status.HTTP_200_OK)
        return Response({"message_info": "No hay PQR's disponibles para borrar"}, status=status.HTTP_204_NO_CONTENT)
        
    def delete(self, request, *args, **kwargs) -> Response:
        """ Elimina las PQR's correspondientes """
        print(request.data)
        data = self.sql_delete_several_items(request.data)
        if data[0]:
            return Response({'message_success': 'PQR´s eliminados correctamente.'}, status=status.HTTP_200_OK)
        return Response({"message_error": f"Ha ocurrido un error por... {data[1]}"}, status=status.HTTP_400_BAD_REQUEST)
