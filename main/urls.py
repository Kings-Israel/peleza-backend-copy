from django.urls import path


from . import views

urlpatterns = [
    path(
        "stats/",
        views.Stats.as_view(),
    ),
   
    path(
        "request/",
        views.PSMTRequestApiView.as_view(),
    ),
    path(
        "request/<request_id>/module/<module_id>/",
        views.PIDVARequestDetailView.as_view(),
    ),
    path(
        "request/<package_id>/<request_ref_number>/",
        views.PSMTRequestDetailView.as_view(),
    ),
    path(
        "requests/",
        views.PSMTRequestListApiView.as_view(),
    ),
    path(
        "test/",
        views.Test.as_view(),
    ),

    path(
        "fileUp/",
        views.simple_upload
    )
    ,
    path(
        "fileUpload/",
        views.file_upload
    ),
    path(
         "submit-help/",
        views.submit_help
    ),
    path(
        "help-items/",
        views.HelpListApiView.as_view(),
    ),
    path(
        "add-user/",
        views.add_user
    ),
    path(
         "get-add-users/",
          views.UserListAPIView.as_view(),
    ),

    # path(
    #     "test2/",
    #     views.test2
    # ),
    path(
        "list/",
        views.List
    ),
    path(
        "req/",
        views.Req
    ),
    path(
        "test_download/",
        views.download_file
    ),
    
    path("countries/", views.CountriesList.as_view(),),

    path("companies/", views.CompaniesList.as_view(),),

    path("industries/", views.IndustriesList.as_view(),),
    
] 
