## Simplify creation of Folder, Site, User, Ftp User, Kestrel Service and LetsEncrypt for .Net Core using NginX over debian

This simple Python script helps to automate first steps to run .net core application on debian linux.

**Before running script, assume you have installed following apps:**
1. Nginx
2. CertBot
3. Python3
4. VsFtp
5. .Net Core Framework


**How to use the script:**
1. Save script anywhere in your filesystem. For example: */opt/sitecreator.py*
2. Run *python3 /opt/sitecreator.py* from debian shell
3. Enter domain name without http and www prefix. Example: mydomain.com or sub.mydomain.com
4. Answer the question if www prefix for domain will be used or not. If yes, Nginx site name with www prefix will be added. Also certificate for www prefix will bre created.
5. Enter the password for ftp user
6. Enter the url which your .net core app will be run. Example: http://localhost:5000. If you want to change this url, you have to change it also in your appsettings.json file. Like "Urls": "http://localhost:5100",
7. Enter your .Net Core DLL file name. For example: myapp.dll

That is all. Now script will be create following folders:
*/var/www/[DomainName]*
*/var/www/[DomainName]/html*
*/var/www/[DomainName]/logs*
*/var/www/[DomainName]/data*

After creating folders, a user named [DomainName] will be created with given password on step 5.
After creation of user the ownership of folder */var/www/[DomainName]* will be changed to user [DomainName] recursively.
Also, folder umasks will be changed to 755

A host file named [DomainName] will be added to */etc/nginx/sites/available/*. Then adds a symbolic link from */etc/nginx/sites-available/[DomainName]* to */etc/nginx/sites-enabled/[DomainName]*

Now a Kestrel service will be add to /etc/systemd/system and then will be enabled.

After appending user named [DomainName] to **/etc/vsftpd.user_list**, Script will as to create LetsEncrypt certificate.
If you answer [y] certificate for [DomainName] will be created and applied to nginx host file.

**Note: i am not good in python. this script is created just for ease and not forgot steps to run a .net core app.**
