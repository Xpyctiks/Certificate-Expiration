# Certificate-Expiration  

Python script to check certificate expiration for any domain.Self-signature or invalid domain(s) don't matter.  

Returns integer codes for easy evaulate in any monitoring system:  
0 - means everything is ok. The certificate has more than 3 days before expiration  
1 - means the certificate has less then 3 days before its expiration  
2 - means the certificate is expired  
255 - means any other error  

# Zabbix template  

I have included an example of Zabbix 7.x template for this script.  
Just substitute inside the template script path "/opt/zabbix/scripts/Certificate-Expiration/certificate-expiration.py" to your path before import the template into Zabbix.  
Use Macro {$DOMAIN} to set a domain you need when creating a host for certificate monitoring.  