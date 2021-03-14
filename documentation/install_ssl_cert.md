# Install SSL certificate

## Install self-signed SSL certificate on front-end

### Instructions for installation on Windows while using WSL
1. Open Windows PowerShell as an administrator (search for Widnows PowerShell, right click and run as administrator) and install [choco](https://chocolatey.org/install):
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

2. Install mkcert inside the Windows PowerShell
```
choco install mkcert
```

3. Cd into a direcotry you like (I choose Desktop) and create a direcotry to store your certificates:
```
cd C:\Users\YOUR_USER\Desktop
mkdir cert
cd cert
```

4. Issue the certificates:
```
mkcert -key-file ./key.pem -cert-file ./cert.pem "localhost"


#### output should look like this:
Created a new certificate valid for the following names 📜 - "localhost"

The certificate is .....
```

5. You are done with the PowerShell. Open WSL and cd into `MHMelectric/front-end/user_management` and do the following commands:
```
mkdir .cert
cp /mnt/c/Users/YOUR_USER/Desktop/cert/* ./.cert
```

6. Make sure that inside the `package.json` file the starting script looks like that:
```
"scripts": {
    "start": "HTTPS=true SSL_CRT_FILE=./.cert/cert.pem SSL_KEY_FILE=./.cert/key.pem react-scripts start",
    ...
}
```

