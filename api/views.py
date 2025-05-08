from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import whois
import subprocess
import dns.resolver
from core.infrastructure.scanners.dns_scan import DNSScanner


# DORKS
def google_dorks(request):
    dorks = [
        'inurl:"admin/login"',
        'intitle:"index of"',
        'filetype:sql "password"',
        'site:.cl ext:sql'
    ]
    return JsonResponse({"dorks": dorks})


# WHOIS
def whois_lookup(request):
    try:
        domain = request.GET.get("domain", "")
        info = whois.whois(domain)
        return JsonResponse({
            "domain_name": info.domain_name,
            "registrar": info.registrar,
            "creation_date": str(info.creation_date),
            "expiration_date": str(info.expiration_date),
            "name_servers": info.name_servers,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# DNS
def dns_lookup(request):
    try:
        domain = request.GET.get("domain", "")
        result = {}
        for record_type in ["A", "AAAA", "MX", "NS", "TXT"]:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                result[record_type] = [str(r) for r in answers]
            except:
                result[record_type] = []
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# NMAP
def nmap_scan(request):
    target = request.GET.get("target", "")
    if not target:
        return JsonResponse({"error": "No target provided"}, status=400)

    try:
        result = subprocess.run(["nmap", "-T4", "-F", target], capture_output=True, text=True)
        return JsonResponse({"scan": result.stdout})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# DNS SCAN CLASS 
class DNSScanView(APIView):
    def get(self, request):
        domain = request.query_params.get("domain")
        if not domain:
            return Response({"error": "No domain provided"}, status=400)
        scanner = DNSScanner(domain)
        data = scanner.run_scan()
        return Response(data)
