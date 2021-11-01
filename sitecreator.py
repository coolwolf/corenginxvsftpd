import os
import os.path
from os import path
import re

def display_title_bar():
    print("\t***********************************************************")
    print("\t*** .netCore + Nginx + VsFtpd Site Creator by @coolwolf***")
    print("\t***********************************************************")
    print("\tPress q for exit...")

display_title_bar()

WebFolder='/var/www/'
NginxSaFolder='/etc/nginx/sites-available/'
NginxSeFolder='/etc/nginx/sites-enabled/'
NginxLogFolder='/var/log/nginx/'
DotNetBin='/usr/bin/dotnet'
VsFtpUserListFolder='/etc/vsftpd.user_list'
DomainName = ''
DmnUserName=''
UserPassword=''
CoreUrl=''
DllName=''
IncludeWWW=False

def is_tool(name):
    from shutil import which
    return which(name) is not None

def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def Controls():
    if not path.exists(WebFolder):
        print("\n"+WebFolder+" folder does not exists")
        return False
    if not path.exists(NginxSaFolder):
        print("\n"+NginxSaFolder+" folder does not exists")
        return False
    if not path.exists(NginxSeFolder):
        print("\n"+NginxSeFolder+" folder does not exists")
        return False
    if not path.exists(DotNetBin):
        print("\n"+DotNetBin+" does not exists")
        return False
    if not path.exists(NginxLogFolder):
        print("\n"+NginxLogFolder+" folder does not exists")
        return False
    if not path.exists(VsFtpUserListFolder):
        print("\n"+VsFtpUserListFolder+" folder does not exists")
        return False
    if not is_tool('certbot'):
        print("\ncertbot is not installed")
        return False

def GetDomainName():
    isValid=False
    global DomainName
    while not isValid:
        print("\nEnter domain name without www prefix.")
        DomainName = input("Ex: mydomain.com, sub.mydomain.com :")
        if DomainName=='q':
            exit()
        if DomainName.startswith('http'):
            print("\nDomain Name Should not start with HTTP.")
            continue
        if DomainName.startswith('www.'):
            print("\nDomain Name Should not start with www.")
            continue
        if not is_valid_hostname(DomainName):
            print("\nEntered domain name is not valid.")
            continue
        isValid=True

def WwwIncluded():
    global IncludeWWW
    answer = input("Inlcude www prefix for domain ? [y/n]:")
    if answer=='y':
        IncludeWWW=True

def AskUserName():
    global DmnUserName
    DmnUserName=DomainName[1:DomainName.index(".")]
    answer = input("User Name for domain ? ["+DmnUserName+"]:")
    if answer!="":
        DmnUserName=answer

def AskPassword():
    isValid=False
    global UserPassword
    while not isValid:
        UserPassword = input("Enter password for user "+DmnUserName+" :")
        if len(UserPassword)<8:
            print("\nMin. 8 characters required.")
        else:
            isValid=True

def AskCoreUrl():
    isValid=False
    global CoreUrl
    while not isValid:
        print("\nEnter .netCore app url.")
        CoreUrl = input("Ex: http://localhost:5000 :")
        if CoreUrl=='q':
            exit()
        if not CoreUrl.startswith('http://'):
            print("\nEntered URL name is not valid.")
        else:
            isValid=True

def AskDllName():
    isValid=False
    global DllName
    while not isValid:
        print("\nEnter .netCore app DLL name.")
        DllName = input("Ex: myapp.dll :")
        if DllName=='q':
            exit()
        if len(DllName)<5:
            print("\nEntered DLL name is not valid.")
        else:
            isValid=True
        if ".dll" not in DllName:
            print("\nString must end with .dll.")
            isValid=False
        else:
            isValid=True

def CreateFolders():
    print("\nCreate folder:"+WebFolder+DmnUserName)
    os.mkdir(WebFolder+DmnUserName,0o755)
    print("\nCreate folder:"+WebFolder+DmnUserName+"/html")
    os.mkdir(WebFolder+DmnUserName+"/html",0o755)
    print("\nCreate folder:"+WebFolder+DmnUserName+"/logs")
    os.mkdir(WebFolder+DmnUserName+"/logs",0o755)
    print("\nCreate folder:"+WebFolder+DmnUserName+"/data")
    os.mkdir(WebFolder+DmnUserName+"/data",0o755)

def CreateUser():
    print("\nRun command: useradd -p "+UserPassword+" "+DmnUserName+" -d "+WebFolder+DmnUserName)
    os.system("useradd -p "+UserPassword+" "+DmnUserName+" -d "+WebFolder+DmnUserName)
    print("\nRun command: chown -R "+DmnUserName+":"+DmnUserName+ " "+WebFolder+DmnUserName)
    os.system("chown -R "+DmnUserName+":"+DmnUserName+ " "+WebFolder+DmnUserName)
    print("\nRun command: chmod -R 755 "+WebFolder+DmnUserName)
    os.system("chmod -R 755 "+WebFolder+DmnUserName)

def CreateNginxSite():
    wwwsub=''
    if IncludeWWW:
        wwwsub=' www.'+DomainName
    SiteStr='server {\n'\
        'listen 80;\n'\
        'server_name '+DomainName+wwwsub+';\n'\
        'return 301 https://$server_name$request_uri;\n'\
    '}\n'\
    'server {\n'\
        'listen 443 ssl;\n'\
        'server_name '+DomainName+wwwsub+';\n'\
        'ssl_session_cache  builtin:1000  shared:SSL:10m;\n'\
        'ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;\n'\
        'ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;\n'\
        'ssl_prefer_server_ciphers on;\n'\
        '\n'\
        'gzip  on;\n'\
        'gzip_http_version 1.1;\n'\
        'gzip_vary on;\n'\
        'gzip_comp_level 6;\n'\
        'gzip_proxied any;\n'\
        'gzip_types text/plain text/css application/json application/javascript application/x-javascript text/javascript text/xml application/xml application/rss+xml application/atom+xml application/rdf+xml;\n'\
        'gzip_buffers 16 8k;\n'\
        'gzip_disable “MSIE [1-6].(?!.*SV1)”;\n'\
        '\n'\
        'access_log '+WebFolder+DmnUserName+'/logs/access.log;\n'\
        'location / {\n'\
            'proxy_pass '+CoreUrl+';\n'\
            'proxy_http_version 1.1;\n'\
            'proxy_set_header   Upgrade $http_upgrade;\n'\
            'proxy_set_header   Connection keep-alive;\n'\
            'proxy_set_header   Host $host;\n'\
            'proxy_cache_bypass $http_upgrade;\n'\
            'proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;\n'\
            'proxy_set_header   X-Forwarded-Proto $scheme;\n'\
        '}\n'\
        'ssl_certificate /etc/ssl/certs/testCert.crt;\n'\
        'ssl_certificate_key /etc/ssl/certs/testCert.key;\n'\
    '}\n'
    print("\nCreatefile: "+NginxSaFolder+DmnUserName)
    f=open(NginxSaFolder+DmnUserName,"w+")
    f.write(SiteStr)
    f.close()
    print("\nCreate Link: ln -s "+NginxSaFolder+DmnUserName +" "+NginxSeFolder+DmnUserName)
    os.system("ln -s "+NginxSaFolder+DmnUserName +" "+NginxSeFolder+DmnUserName)

def CreateKestrel():
    KestrelStr='[Unit]\n'\
        'Description='+DomainName+' .netCore App\n'\
        '[Service]\n'\
        'WorkingDirectory='+WebFolder+DmnUserName+'/html\n'\
        'ExecStart='+DotNetBin+' '+WebFolder+DmnUserName+'/html/'+DllName+'\n'\
        'Restart=always\n'\
        'RestartSec=10\n'\
        'KillSignal=SIGINT\n'\
        'SyslogIdentifier='+DllName+'\n'\
        'User='+DmnUserName+'\n'\
        'Environment=ASPNETCORE_ENVIRONMENT=Production\n'\
        'Environment=DOTNET_PRINT_TELEMETRY_MESSAGE=false\n'\
        '\n'\
        '[Install]\n'\
        'WantedBy=multi-user.target\n'
    print("\nCreate Kestrel: /etc/systemd/system/kestrel-"+DmnUserName+".service")
    f=open("/etc/systemd/system/kestrel-"+DmnUserName+".service","w+")
    f.write(KestrelStr)
    f.close()
    print("\nEnable Service: systemctl enable kestrel-"+DmnUserName+".service")
    os.system("systemctl enable kestrel-"+DmnUserName+".service")

def CreateFtpUser():
    print("\n Append Ftp User: echo '"+DmnUserName+"' >> "+VsFtpUserListFolder)
    os.system("echo '"+DmnUserName+"' >> "+VsFtpUserListFolder)

def CreateLetsEncryptCert():
    answer = input("Create LetsEncrypt Certificate ? [y/n]:")
    if answer=='y':
        wwwsub=''
        if IncludeWWW:
            wwwsub=' -d www.'+DomainName
        print("\nCreate Letsencrypt Certificate: certbot --nginx -d "+DomainName+wwwsub)
        os.system("certbot --nginx -d "+DomainName+wwwsub)

GetDomainName()
WwwIncluded()
AskPassword()
AskCoreUrl()
AskDllName()
CreateFolders()
CreateUser()
CreateNginxSite()
CreateKestrel()
CreateFtpUser()
CreateLetsEncryptCert()