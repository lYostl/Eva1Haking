from django.urls import path
from api import views

urlpatterns = [
    path('dorks/', views.GoogleDorksView.as_view(), name='google_dorks'),
    path('whois/', views.WhoisLookupView.as_view(), name='whois_lookup'),
    path('dns/', views.DNSLookupView.as_view(), name='dns_lookup'),
    path('nmap/', views.NmapScanView.as_view(), name='nmap_scan'),
]
