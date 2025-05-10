from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import whois
import subprocess
import dns.resolver
from core.infrastructure.scanners.dns_scan import DNSScanner
from core.infrastructure.scanners.google_dorks import perform_google_search
from core.infrastructure.scanners.whois_scan import WhoisScanner
from core.infrastructure.scanners.nmap_scan import NmapScanner
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleDorkSearchView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "No query provided"}, status=400)

        api_key = os.getenv("API_KEY")
        search_engine_id = os.getenv("SEARCH_ENGINE_ID")

        if not api_key or not search_engine_id:
            return Response({"error": "Missing API_KEY or SEARCH_ENGINE_ID"}, status=500)

        results = perform_google_search(api_key, search_engine_id, query)
        return Response({"results": results})

# WHOIS
class WhoisScanView(APIView):
    def post(self, request):
        domain = request.data.get("domain")
        if not domain:
            return Response({"error": "No domain provided"}, status=400)

        scanner = WhoisScanner(domain)
        data = scanner.run_scan()
        return Response(data)

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


class NmapScanView(APIView):
    def post(self, request):
        target = request.data.get("target")
        if not target:
            return Response({"error": "No target provided"}, status=400)

        scanner = NmapScanner(target)
        data = scanner.run_scan()
        return Response(data)



class DNSScanView(APIView):
    def post(self, request):
        domain = request.data.get("domain")
        if not domain:
            return Response({"error": "No domain provided"}, status=400)
        scanner = DNSScanner(domain)
        data = scanner.run_scan()
        return Response(data)