from django.urls import path
from .views import google_dorks, whois_lookup, dns_lookup, nmap_scan, DNSScanView

urlpatterns = [
    path('dorks/', google_dorks, name='google_dorks'),
    path('whois/', whois_lookup, name='whois_lookup'),
    path('dns/', dns_lookup, name='dns_lookup'),
    path('nmap/', nmap_scan, name='nmap_scan'),
    path('scan-dns/', DNSScanView.as_view(), name='scan_dns'),
]
