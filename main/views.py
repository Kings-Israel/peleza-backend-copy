from main.models.company import (
    BusinessCompanyReg,
    CompanyOfficialDetails,
    Encumbrance,
    ShareCapital,
    Shares,
    
)
from main.models.help import FormData, HelpSubject, HelpMessage, HelpResponse

from authentication.models import PelClient, ClientCompany
from main.models.permissions import Permissions
from main.models.user_has_permission import UserHasPermission
from rest_framework.serializers import Serializer
from rest_framework import response
from main.api_requests import HelperFunctions, RequestHandler
from main.serializers.company import BusinessCompanyRegSerializer
from main.serializers.psmt import (
    PIDVARequestDetailSerializer,
    PSMTRequestDetailSerializer,
    PSMTRequestSerializer,
    RequestSerializer,
)
from django.core.exceptions import ObjectDoesNotExist

from main.serializers.user import UserSerializer
from main.serializers.help import HelpSerializer, HelpSubjectSerializer, HelpMessageSerializer, HelpResponseSerializer
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http.response import JsonResponse
from rest_framework.status import HTTP_201_CREATED
import string, random
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from .worker_threads import MailerThread
from django.http import FileResponse, JsonResponse

# Excel Upload and Save to Db
# from .resources import PSMTRequestResource
from django.shortcuts import render
from .models import PSMTRequest , PelPsmtRequestModules
from tablib import Dataset
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from . import custom_query
from . import reports
from . import rabbit_queue
from authentication import models
from django.core import serializers
import hashlib
# Create your views here.
packages_id = settings.ALL_API_PACKAGES
helper = HelperFunctions()
queue_publisher = rabbit_queue.QueuePublisher()
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils import timezone


@csrf_exempt
def submit_help(request):
    if request.method == 'POST':
        # Access form data from the request.POST dictionary
        user_id = request.POST.get('userId', None)
        subject = request.POST.get('subject', '')
        image = request.POST.get('image')
        message = request.POST.get('message', '')
        help_id = request.POST.get('help_id', '')

        # Return a JSON response indicating the success or failure of the form submission
        user = PelClient.objects.get(client_id=user_id)
        if help_id is None or help_id is '':
            new_subject = HelpSubject.objects.create(
                user = user,
                subject = subject
            )
            HelpMessage.objects.create(
                subject = new_subject,
                message = message
            )
        else:
            subject = HelpSubject.objects.get(id=help_id)
            HelpMessage.objects.create(
                subject = subject,
                message = message
            )
        
        return JsonResponse({'message': 'Form submitted'})
    else:
        # Handle GET requests to the submit-form URL
        return JsonResponse({'message': 'Form not submitted!'})

class HelpListApiView(ListAPIView):
    serializer_class = HelpSerializer

    def get_queryset(self):
        user = self.request.user
        return FormData.objects.filter(user_id=user.client_id).order_by('-id')

class HelpSubjectApiView(ListAPIView):
    serializer_class = HelpSubjectSerializer

    def get_queryset(self):
        return HelpSubject.objects.filter(user=self.request.user).order_by('-created_at')
    
class HelpSubjectDetailView(RetrieveAPIView):
    serializer_class = HelpSubjectSerializer

    def get_object(self):
        help_id = self.kwargs.get("help_id", 0)

        obj = get_object_or_404(
            HelpSubject,
            id=help_id,
        )

        for response in obj.responses.filter(read_at=None):
            response.read_at = timezone.now
            response.save()

        self.check_object_permissions(self.request, obj)
        return obj
    
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        # Access form data from the request.POST dictionary
        first_name = request.POST.get('firstName','')
        last_name = request.POST.get('lastName','')
        email = request.POST.get('email','')
        phone_number = request.POST.get('phoneNumber','')
        city = request.POST.get('city', '')
        address = request.POST.get('address')
        postal_code = request.POST.get('postalCode')
        added_by_id = request.POST.get('added_by_id')
        company_id = request.POST.get('company', '')
        title = request.POST.get('title', '')
        
        try:
           added_by = PelClient.objects.get(client_id=int(added_by_id))
        except (ValueError, PelClient.DoesNotExist):
           return JsonResponse({'message': 'Invalid added_by'})

        try:
            client_parent_company = ClientCompany.objects.get(company_name=company_id)
        except (ValueError, ClientCompany.DoesNotExist):
            return JsonResponse({'message': 'Invalid company'})
        
        password = get_random_string(length=10)
        
        client = PelClient(
            client_company_id=client_parent_company.company_code,
            client_first_name=first_name,
            client_last_name=last_name,
            client_login_username= email,
            client_mobile_number=phone_number,
            client_postal_address=address,
            client_postal_code=postal_code,
            added_by=added_by,
            client_city=city,
            client_parent_company=client_parent_company,
            client_password=hashlib.md5(password.encode()).hexdigest(),
            title = title
        )
        client.save()
        

        # Extract the selected permissions data
        permissions_data = {
            'create requests': int(request.POST.get('create_request', 0)),
            'view requests': int(request.POST.get('view_request', 0)),
            'create users': int(request.POST.get('add_user', 0)),
            'view users': int(request.POST.get('view_user', 0)),
            'create batch requests': int(request.POST.get('create_batch_request', 0)),
            'view batch requests': int(request.POST.get('view_batch_request', 0)),
        }

        # Save user permissions in UserHasPermission model
        for permission, value in permissions_data.items():
            if value:
                permission_obj = Permissions.objects.get(permission=permission)
                user_permission = UserHasPermission(
                    permission_id=permission_obj.id,
                    user_id=client.client_id
                )
                user_permission.save()

        context = {
            "client_login_id": client_parent_company.company_code,
            "username": email,
            "password": password
        }

        subject = "PELEZA ACCOUNT CREATED"
        to = email
        html_content = render_to_string("newUser.html", context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # response = send_mail(
        #     "PELEZA ACCOUNT CREATED",
        #     text_content,
        #     "peleza@international.com",
        #     [email, ],
        #     fail_silently=False,
        # )

        # print(response)

        # Return a JSON response indicating the success or failure of the form submission
        return JsonResponse({'message': 'User added'})
    else:
        # Handle GET requests to the submit-form URL
        return JsonResponse({'message': 'Invalid request method'})



    

@csrf_exempt
@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def file_upload(request):
    user=json.loads(request.data.get('user'))
    #print(user)
    package_querry ="SELECT pel_client_package.client_id,pel_client_package.package_name,pel_client_package.package_id,pel_client_package.`status`FROM pel_client_package where client_id = '" + str(user["cl_id"]) + "' and status = '11';"
    package_data = custom_query.custom_sql(package_querry)
    #print(package_data)
    dataset = Dataset()
    bulk_request = request.FILES['myfile']
    imported_data = dataset.load(bulk_request.read(), format='xlsx')
    for data in imported_data:
            module_querry = ('SELECT pel_client_package.client_id,'
                    'pel_client_package.package_name,'
                    'pel_client_package.package_id,'
                    'pel_packages_module.module_name,'
                    'pel_packages_module.module_id,'
                    'pel_packages_module.`status`,'
                    'pel_packages_module.modulepackage_id,'
                    'pel_module.module_code, '
                    'pel_module.module_cost, '
                    'pel_packages_module.package_id '
                    'FROM '
                    'pel_client_package '
                    'INNER JOIN pel_packages_module ON pel_packages_module.package_id = pel_client_package.package_id '
                    'INNER JOIN pel_module ON pel_module.module_id = pel_packages_module.module_id '
                    'WHERE '
                    'pel_client_package.client_id = '+ str(user["cl_id"]) +' AND '
                    'pel_packages_module.`status` = "11" AND pel_module.module_code= "'+ data[4] + '"')
            #print(module_querry)   
            module_data = custom_query.custom_sql(module_querry) 
            #print(module_data)
            request_ref_num=uuid.uuid4()
            #print(module_data)     
            value = PSMTRequest(
                client_number=data[0],
                company_name=data[1],
                registration_number=data[2],
                dataset_citizenship=data[3],
                request_plan=data[4],
                bg_dataset_name=data[1],
                user_name=user["username"],
                client_name=user["company_id"],
                request_type="company",
                client_login_id=user["company_id"],
                request_credit_charged=module_data[0][8],
                client_id=user["cl_id"],
                request_package=package_data[0][2],
                request_ref_number=request_ref_num ,
                status="00",
                file_tracker= request_ref_num,
                package_id=module_data[0][9],
                #module_id=module_data[0][4]
            )
            value.save()
            #print(value)
            ReqMod = PelPsmtRequestModules(
                request_ref_number=request_ref_num,
                client_id = user["cl_id"],
                package_id = module_data[0][2],
                package_name = module_data[0][1],
                module_name = module_data[0][3],
                request_type = "company",
                module_id = module_data[0][4],
                request_id=request_ref_num,
          
            )
            ReqMod.save()
            #print(value)


    rep ={
     "receive":"request processed successfully"
    }        
    return JsonResponse(data=rep, status=HTTP_201_CREATED)


@csrf_exempt
def simple_upload(request):
    if request.method == 'POST':
        print(request)
        # request_resource = PSMTRequestResource()
        dataset = Dataset()
        bulk_request = request.FILES['myfile']

        imported_data = dataset.load(bulk_request.read(), format='xlsx')
        #print(imported_data)
        for data in imported_data:
            #print(data[0])
            value = PSMTRequest(
                client_number=data[0],
                company_name=data[1],
                registration_number=data[2],
                dataset_citizenship=data[3],
                request_plan=data[4],
                bg_dataset_name=data[1],
                user_name="demo@peleza.com",
                client_name="Demo Account",
                request_type="company",
                client_login_id="NCBA",
                request_credit_charged="1",
                client_id="325",
                # packages_id="40"

            )
            value.save()

        # result = request_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    request_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'input.html')


class PSMTRequestApiView(CreateAPIView):
    serializer_class = RequestSerializer

    def generate_ref_number(self,):
        letters = string.ascii_uppercase
        timestamp = datetime.now()
        output = "%s%s-%s" % (
            "".join(random.choices(letters, k=3)),
            timestamp.strftime("%f"),
            "".join(random.choices(letters, k=3)),
        )
        return output

    def post(self, request, *args, **kwargs):
        instance = self.validate_request()
        request_ref_number = self.generate_ref_number()

        request_thread = RequestHandler(request, request_ref_number)
        request_thread.start()

        data = {
            **instance.validated_data,
            "request_ref_number": request_ref_number,
            "status": "00",
            "percentage": 0.00,
        }

        return Response(data, status=HTTP_201_CREATED)

    def validate_request(self):
        serializer = self.get_serializer(data=self.request.data)
        dataset_name = self.request.data.get("dataset_name", None)
        errors = {}

        if not serializer.is_valid():
            errors = {**serializer.errors}

        if not dataset_name:
            errors["dataset_name"] = ["This field cannot be null!"]

        if errors:
            raise ValidationError(errors)

        return serializer


class PSMTRequestListApiView(ListAPIView):
    serializer_class = PSMTRequestSerializer
    queryset = serializer_class.Meta.model.objects

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("modules")
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        company = self.request.user.client_parent_company

        extra = {}
        if status == "completed":
            extra["status"] = 11
        elif status == "in_progress":
            extra["status__in"] = ["33", "44"]
        elif status == "new":
            extra["status"] = "00"

        if q == "all":
            queryset = queryset.filter(
                client_login_id=company.company_code if company else "_As_MMM", **extra
            )
        elif q == "recent":
            queryset = queryset.filter(
                client_login_id=company.company_code if company else "_As_MMM",
                client_id=self.request.user.pk,
                **extra
            )[:12]
        else:
            queryset = queryset.filter(
                client_login_id=company.company_code if company else "_As_MMM",
                client_id=self.request.user.pk,
                **extra
            )

        queryset: QuerySet = queryset

        return queryset


class PSMTRequestDetailView(RetrieveAPIView):
    serializer_class = PSMTRequestDetailSerializer

    def get_object(self):
        user=self.request.user
        package_id = self.kwargs.get("package_id", 0)
        request_ref_number = self.kwargs.get("request_ref_number", 0)

        obj = get_object_or_404(
            PSMTRequest,
            package_id=package_id,
            request_ref_number=request_ref_number,
        )

        self.check_object_permissions(self.request, obj)
        return obj


class PIDVARequestDetailView(RetrieveUpdateAPIView):
    serializer_class = PIDVARequestDetailSerializer
    authentication_classes = []

    def get_object(self):
        request_id = self.kwargs.get("request_id", 0)

        obj = get_object_or_404(
            PSMTRequest,
            request_id=request_id,
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
   
        self.psmt_req: PSMTRequest = self.get_object()
        try:
            self.business = self.psmt_req.business
        except:
            self.business = None

        instance: PSMTRequest = self.get_object()

        if instance.status == 11 or instance.status == "11":
            # raise LockedException()
            pass

        serializer: Serializer = self.get_serializer(
            instance,
            data={**self.request.data},
        )

        serializer.is_valid()

        edited = self.review_info()
        self.registration_info()

        self.psmt_req = instance = instance if not edited else self.get_object()

        if self.business:
            self.partners_info()
            self.encumbrance_info()
            self.share_capital_info()
            self.officials_info()

        _response = self.get_serializer(instance=instance).data

        # queue data 
        #print(self.kwargs.get("request_id", 0))

        if edited:
           print(" === Record has been reviewed so it should send to queue===")
           queue_publisher.sendToqueue(self.kwargs.get("request_id", 0))
        #print(" === Data response===")
        #print(_response)
        #print(" === Data response===")
        return response.Response(data=_response)

    def review_info(self):
        review = self.request.data.get("review", None)
        negative = self.request.data.get("negative", False)
        instance = self.psmt_req

        # check this later
        if not review:
            return True
        
        status = review.get("status", None)
        comments = review.get("comments", None)
        negative = review.get("negative", None)

        if status == "55" or status == 55:
         # if status invalid just save status and commentsand return true
           instance.status = status
           instance.comments = comments
           instance.save()
           return True
        
        if not review or negative or not self.business:
            return False
        # SEND MAIL IF APPROVED instead of mail add to queue
        #if status == "11" or status == 11:
            #mailer = MailerThread()
            #mailer.instance = instance
            #mailer.start()
            #
            #instance.status = "11"
        instance.status = status

        if negative and instance.business:
            instance.business.delete()
            instance.business = None

        if comments:
            instance.comments = comments

        instance.save()

        return True

    def officials_info(self):
        officials = self.request.data.pop("officials", None)
        official = self.request.data.pop("official", None)
        delete = self.request.data.pop("delete", False)
        pk = official.pop("pk", None) if official else None

        if not officials and not official:
            return

        elif officials:
            for _official in officials:
                pk = _official.pop("pk", None)
                if pk:
                    CompanyOfficialDetails.objects.filter(pk=pk).update(**_official)
                elif _official.get("name", "") != "":
                    CompanyOfficialDetails.objects.create(
                        **_official, business=self.business
                    )
        elif official and delete and pk:
            instance = CompanyOfficialDetails(pk=pk)
            instance.delete()

    def encumbrance_info(self):
        encumbrance = self.request.data.pop("encumbrance", None)
        if not encumbrance:
            return
        delete = self.request.data.pop("delete", False)
        pk = encumbrance.pop("pk", None)

        instance = Encumbrance(**encumbrance, pk=pk)
        instance.business = self.business

        if delete and pk:
            instance.delete()
        elif pk:
            instance.save(force_update=True)

        elif not delete:
            instance.save()

    def share_capital_info(self):
        share_capital = self.request.data.pop("share_capital", None)
        if not share_capital:
            return

        delete = self.request.data.pop("delete", False)
        pk = share_capital.pop("pk", None)

        instance = ShareCapital(**share_capital, pk=pk)
        instance.business = self.business

        if pk and delete:
            instance.delete()
        elif pk:
            instance.save(force_update=True)
        elif not delete:
            instance.business = self.business
            instance.save()

    def partners_info(self):
        partner = self.request.data.pop("partner", None)

        if not partner:
            return

        delete = self.request.data.pop("delete", False)
        pk = partner.pop("pk", None)

        instance = Shares(**partner, pk=pk)
        instance.business = self.business

        if pk and delete:
            instance.delete()
        elif pk:
            instance.save(force_update=True)
        elif not delete:
            instance.save()

    # def share_
    def registration_info(
            self,
    ):
        data = self.request.data.pop("registration", None)
        if not data:
            return

        pk = data.get("pk", None)
        pk = self.business.pk if self.business else pk

        # pop registration data first
        business_name = data.pop("business_name", "")
        type = data.pop("type", "")
        registration_date = data.pop("registration_date", "")
        email = data.pop("email", "")
        phone_number = data.pop("phone_number", "")
        branches = data.pop("branches", "")
        physical_address = data.pop("physical_address", "")
        postal_address = data.pop("postal_address", "")
        kra_pin = data.pop("kra_pin", "")
        member_count = data.pop("member_count", "")
        objective = data.pop("objective", "")
        request_ref_number = self.psmt_req
        registration_number = data.pop("registration_number", "")

        # pop other data

        instance = BusinessCompanyReg(
            pk=pk,
            business_name=business_name,
            type=type,
            registration_date=registration_date,
            email=email,
            phone_number=phone_number,
            branches=branches,
            physical_address=physical_address,
            postal_address=postal_address,
            kra_pin=kra_pin,
            member_count=member_count,
            objective=objective,
            request_ref_number=request_ref_number,
            registration_number=registration_number,
        )
        if pk:
            instance.save(force_update=True)
        else:
            instance.save()

        return instance


class Stats(ListAPIView):
    def get(self, request, *args, **kwargs):
        company = request.user.client_parent_company
        credits = company.company_credit if company else 0
        packages_id.append(52)
        extra_query = {"company_name": company.company_name}
        new = PSMTRequest.objects.filter(status="00", **extra_query).count()
        final = PSMTRequest.objects.filter(status="11", **extra_query).count()
        invalid = PSMTRequest.objects.filter(status="55", **extra_query).count()
        in_progress = PSMTRequest.objects.filter(Q(status="44") | Q(status="33"), **extra_query).order_by("-request_id").count()

        _recent_requests = PSMTRequest.objects.filter(**extra_query)[:100].select_related("business")
        recent_requests = PSMTRequestSerializer(_recent_requests, many=True)

        data = {
            "credits": credits,
            "new": new,
            "final": final,
            "in_progress": in_progress,
            "interim": 0,
            "invalid": invalid,
            "recent": recent_requests.data,
        }

        return response.Response(data=data)


class Test(ListAPIView):
    serializer_class = BusinessCompanyRegSerializer
    queryset = serializer_class.Meta.model.objects.all()




@csrf_exempt
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def download_file(response):

    user=response.user
    company_id=getattr(user,'company_id')
    module_code = response.query_params.get('module_code')
    date_from = response.query_params.get('date_from')
    date_to = response.query_params.get('date_to')
    status = response.query_params.get('status')

    module_code=module_code.upper()

    ngo=['NGO','SACCO','TR','CBO','SOCIETIES','TRUSTS','SOC']
    bness=['CLG','CO','BN','ICO','LLP','NCBA','COOPERATIVE']
     
    querry_data=custom_query.request_querry(status,module_code,date_from,date_to,company_id)
    if module_code in ngo:
        rpt = reports.ngo_report(company_id,querry_data,module_code)
    elif module_code in bness: 
        rpt = reports.company_report(company_id,querry_data,module_code)
    else :
        rpt = reports.unknown_report(company_id,querry_data,module_code) 

    response = FileResponse(open(rpt, 'rb'))
    return response    


@csrf_exempt
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def List(request):  
    user = request.user
    company_id = user.client_parent_company.company_code
    
    module_code = request.query_params.get('module_code')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    status = request.query_params.get('status')
    module_data = custom_query.request_querry(status,module_code,date_from,date_to,company_id)
    return JsonResponse(data=module_data, safe=False)

class CountriesList(ListAPIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        countries_query = "SELECT * FROM pel_countries ORDER BY country_name ASC"

        countries = custom_query.custom_sql(countries_query)

        return response.Response(countries)
    
class CompaniesList(ListAPIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        companies = models.ClientCompany.objects.all()

        return response.Response(serializers.serialize('json', companies))
    
class IndustriesList(ListAPIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        industries_query = "SELECT * FROM pel_industries ORDER BY industry_name DESC"

        industries = custom_query.custom_sql(industries_query)

        return response.Response(industries)
    
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        client_id = user.client_parent_company
        return PelClient.objects.filter(client_parent_company=client_id).order_by('client_id')
