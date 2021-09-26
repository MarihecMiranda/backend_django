from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from pensum.models import Programa

# Create your models here.
class Trabajador(models.Model):
    """Modelo Trabajador"""
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    foto = models.ImageField(
        upload_to='pictures/%y/%m/%d',
        default='pictures/default.jpg',
        max_length=255
    )
    programa_id = models.ForeignKey(Programa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Trabajador"""
        db_table = 'trabajador'

class Rol(models.Model):
    """Modelo Rol de usuario"""
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Rol"""
        db_table = 'Rol'

class Usuario(AbstractUser):
    """ Modelo Usuario """
    username = None
    email = models.EmailField(('Correo electronico'), unique=True)
    USERNAME_FIELD = 'email'
    first_name = None
    last_name = None
    is_staff = None
    is_superuser = None
    persona = models.OneToOneField(Trabajador, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['persona', 'tipo_usuario']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicioneles del modelo Usuario"""
        db_table = 'Usuario'