from hashlib import md5
from rest_framework import generics, serializers, response, exceptions
from .serializers import AuthSerializer, UserSerializer
from .models import PelClient
import base64
from . import querry
from main.models.user_has_permission import UserHasPermission
# Create your views here.


class Login(generics.CreateAPIView):
    serializer_class = AuthSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        self.validate_request()
        user = PelClient.login(**request.data)

        if not user:
            raise exceptions.AuthenticationFailed()
        company_querry ="SELECT company_logo ,company_industry FROM peleza_db_local.pel_client_co where company_code='"+str(user.client_company_id)+"'"
        permissions_query = "SELECT permission_id FROM peleza_db_local.main_userhaspermission WHERE user_id='"+str(user.client_id)+"'"
        client_co = querry.custom_sql(company_querry)
        user_permissions = querry.custom_sql(permissions_query)
        selected_permissions = []
        for permission in user_permissions:
            permission_query = "SELECT permission FROM peleza_db_local.main_permissions WHERE id='"+str(permission[0])+"'"
            permission_query_run = querry.custom_sql(permission_query)
            for permission_name in permission_query_run:
                selected_permissions.append(permission_name[0])
            
        data = {
            "access": user.token,
            "username": user.client_login_username,
            "cl_id": user.client_id ,
            "company_id": user.client_company_id,
            "first_name": user.client_first_name,
            "company_logo": client_co[0][0],
            "company_industry": client_co[0][1]
            if user.client_first_name
            else user.client_login_username,
            "full_name": (
                "%s %s" % (user.client_first_name, user.client_last_name)
            ).title(),
            "permissions": selected_permissions
        }

        return response.Response({**data})

    def validate_request(self):
        instance = self.get_serializer(data=self.request.data)
        if not instance.is_valid():
            raise serializers.ValidationError(instance.errors)

class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = PelClient.objects.all()

    def get_object(self):
        return PelClient.objects.get(client_id=self.request.user.pk)

    def put(self, request, *args, **kwargs):
        password = request.data.get("password", None)
        profile = request.data.get("profile", None)

        try:
            user: PelClient = self.get_object()
            if password:
                password = md5(
                    base64.b64decode(str(password).encode("ascii"))
                ).hexdigest()
                user.client_password = password

            if profile:
                user.client_postal_address = profile.get(
                    "client_postal_address", user.client_postal_address
                )
                user.client_postal_code = profile.get(
                    "client_postal_code", user.client_postal_code
                )
                user.client_city = profile.get("client_city", user.client_city)

            if profile or password:
                user.save()
        except Exception as e:
            print(e)
        finally:
            return response.Response(self.get_serializer(instance=user).data)

class Register(generics.CreateAPIView):
    serializer_class = AuthSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = PelClient.register(**request.data)

        if not user:
            raise exceptions.AuthenticationFailed()
        
        permissions_query = "SELECT id FROM peleza_db_local.main_permissions"
        user_permissions = querry.custom_sql(permissions_query)
        for permission in user_permissions:
            user_permission = UserHasPermission(
                permission_id=permission[0],
                user_id=user.client_id
            )
            user_permission.save()
        # company_querry ="SELECT company_logo ,company_industry FROM peleza.pel_client_co where company_code='"+user.client_company_id +"'"
        company_querry ="SELECT company_logo ,company_industry FROM peleza_db_local.pel_client_co where company_code='"+str(user.client_company_id)+"'"
        permissions_query = "SELECT permission_id FROM peleza_db_local.main_userhaspermission WHERE user_id='"+str(user.client_id)+"'"
        client_co = querry.custom_sql(company_querry)
        user_permissions = querry.custom_sql(permissions_query)
        selected_permissions = []
        for permission in user_permissions:
            permission_query = "SELECT permission FROM peleza_db_local.main_permissions WHERE id='"+str(permission[0])+"'"
            permission_query_run = querry.custom_sql(permission_query)
            for permission_name in permission_query_run:
                selected_permissions.append(permission_name[0])

        data = {
            "access": user.token,
            "username": user.client_login_username,
            "cl_id": user.client_id ,
            "company_id": user.client_company_id,
            "company_id": user.client_company_id,
            "first_name": user.client_first_name,
            "company_logo": client_co[0][0],
            "company_industry": client_co[0][1]
            if user.client_first_name
            else user.client_login_username,
            "full_name": (
                "%s %s" % (user.client_first_name, user.client_last_name)
            ).title(),
            "permissions": selected_permissions
        }

        return response.Response({**data})
