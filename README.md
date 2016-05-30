
# veeamrestapi

Python wrapper for some of the methods of Veeam REST API (more info on API here: https://helpcenter.veeam.com/backup/rest/overview.html )
Before first usage create file config.ini in app directory with the following content (specify settings of Veeam Enterprise manager accordingly):


**[bem_settings]**  
username = domain\username  
password = your_pass  
address = ip:port  
