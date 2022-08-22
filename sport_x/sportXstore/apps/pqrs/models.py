from django.db import models

# Create your models here.

class Pqrs(models.Model):
    TYPE_DOC = (
        ('CC', 'cedula ciudadania'),
        ('TI', 'targeta de identidad'),
        ('CE', 'cedula de extranjeria')
    )
    
    TICKET_TYPE = (
        ('DP', 'derecho de peticion'),
        ('FL', 'felicitacion'),
        ('PT', 'peticion'),
        ('QJ', 'queja'),
        ('RC', 'reclamo'),
        ('SG', 'sugerencia'),
    )
    
    dni  = models.IntegerField(
        "Número de documento", 
        blank=False, 
        null=False
    )
    
    type_dni = models.CharField(
        "Tipo de documento", 
        max_length=2, 
        choices=TYPE_DOC, 
        blank=False, 
        null=False
    )
    
    name = models.CharField(
        "Nombre", 
        max_length=70, 
        blank=False, 
        null=False
    )
    
    lastname = models.CharField(
        "Apellidos", 
        max_length=120, 
        blank=False, 
        null=False
    )
    
    email = models.EmailField("Correo electrónico")
    
    phone = models.IntegerField(
        "Número fijo",
    )
    
    movil_phone = models.CharField(
        "Número celular",
        max_length=14,
        blank=True,
        null=True
    )
    
    ticket_type = models.CharField(
        "Tipo de ticket",
        max_length=2,
        choices=TICKET_TYPE,
        blank=False,
        null=False
    )
    
    title = models.CharField(
        "Título", 
        max_length=255,  
        blank=False, 
        null=False
    )
    
    description = models.TextField(
        "Descripción", 
        blank=False, 
        null=False
    )
    
    status = models.BooleanField(
        "Estado", 
        default=1
    )
    
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "PQRS"
        verbose_name_plural = "PQRS"
    
    def __str__(self) -> str:
        return self.title
    