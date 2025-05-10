from django.urls import path
from .views import GoogleDorkSearchView, WhoisScanView, dns_lookup, NmapScanView, DNSScanView

urlpatterns = [
    path('dorks/', GoogleDorkSearchView.as_view(), name='google_dork_search'),
    path('whois/', WhoisScanView.as_view(), name='whois_scan'),
    path('dns/', dns_lookup, name='dns_lookup'),
    path("nmap/", NmapScanView.as_view(), name="nmap_scan"),
    path('scan-dns/', DNSScanView.as_view(), name='scan_dns'),
]
