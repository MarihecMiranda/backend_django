# pylint: skip-file
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from .models import Trabajador, Usuario, Rol


class CustomRegisterSerializer(RegisterSerializer):
    """Custom register serializer"""
    user_types = (
        (1, "administrador"),
        (2, "gestor"),
    )
    username = None
    email = serializers.EmailField(required=True)
    password1 = None
    password2 = None

    nombre = serializers.CharField(required=True, write_only=True)
    apellido = serializers.CharField(required=True, write_only=True)
    direccion = serializers.CharField(required=True, write_only=True)
    telefono = serializers.CharField(required=True, write_only=True)
    rol = serializers.ChoiceField(required=True, choices=user_types, initial=user_types[0])
    foto = serializers.ImageField(required=False, write_only=True, default='pictures/default.jpg')

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        return data

    def get_cleaned_data(self):
        name = str(self.validated_data.get('nombre', ''))
        last_name = str(self.validated_data.get('apellido', ''))
        password = Usuario.objects.generate_password(name, last_name)

        return {
            'password1': password,
            'email': self.validated_data.get('email', ''),
            'nombre': self.validated_data.get('nombre', ''),
            'apellido': self.validated_data.get('apellido', ''),
            'direccion': self.validated_data.get('direccion', ''),
            'telefono': self.validated_data.get('telefono', ''),
            'rol': self.validated_data.get('rol', ''),
            'foto': self.validated_data.get('foto', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        trabajador = Trabajador(
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
            direccion=self.cleaned_data["direccion"],
            telefono=self.cleaned_data["telefono"],
            foto=self.cleaned_data["foto"]
        )
        trabajador.save()
        rol_id = self.cleaned_data["rol"]
        user.trabajador = trabajador
        user.rol_id = rol_id
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        self.custom_signup(request, user)
        return user


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'email_template_name': 'password_reset_email.html',
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class TrabajadorSerializer(serializers.ModelSerializer):
    """Trabajador serilizer"""

    class Meta:
        model = Trabajador
        fields = ('nombre', 'apellido', 'direccion', 'telefono', 'foto')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'nombre',)
        read_only_fields = ('id', 'nombre',)


class UsuarioSerializerAuthenticated(serializers.ModelSerializer):
    """shows the details from the authenticated user"""
    trabajador = TrabajadorSerializer()
    rol = RolSerializer(required=False)

    class Meta:  # pylint: disable=too-few-public-methods
        model = Usuario
        fields = ('email', 'trabajador', 'rol')

    def update(self, instance, validated_data):
        """overwrited update method for handle nested representations"""
        trabajador_data = validated_data.pop('trabajador')

        trabajador = instance.trabajador

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        trabajador.nombre = trabajador_data.get('nombre', trabajador.nombre)
        trabajador.apellido = trabajador_data.get('apellido', trabajador.apellido)
        trabajador.direccion = trabajador_data.get('direccion', trabajador.direccion)
        trabajador.telefono = trabajador_data.get('telefono', trabajador.telefono)
        trabajador.foto = trabajador_data.get('foto', trabajador.foto)
        trabajador.save()

        return instance


class UsuarioSerializer(serializers.ModelSerializer):
    user_types = (
        (1, "administrador"),
        (2, "gestor"),
    )
    trabajador = TrabajadorSerializer()
    rol_write = serializers.ChoiceField(choices=user_types, write_only=True)
    rol = RolSerializer(required=False)

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'is_active', 'trabajador', 'rol_write', 'rol')

    def update(self, instance, validated_data):
        """overwrited update method for handle nested representations"""
        trabajador_data = validated_data.pop('trabajador')
        trabajador = instance.trabajador

        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.rol_id = validated_data.get('rol_write', instance.rol_id)
        instance.save()

        trabajador.nombre = trabajador_data.get('nombre', trabajador.nombre)
        trabajador.apellido = trabajador_data.get('apellido', trabajador.apellido)
        trabajador.direccion = trabajador_data.get('direccion', trabajador.direccion)
        trabajador.telefono = trabajador_data.get('telefono', trabajador.telefono)
        trabajador.foto = trabajador_data.get('foto', trabajador.foto)
        trabajador.save()

        return instance

