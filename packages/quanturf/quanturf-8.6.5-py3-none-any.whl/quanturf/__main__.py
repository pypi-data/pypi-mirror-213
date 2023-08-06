import os
import typer
import requests
import maskpass
import json
import site
import os

app=typer.Typer()

@app.command()
def deploy():   
    AUTH_URL="https://quanturf.com/api/auth/"
    URL="https://quanturf.com/api/files/"

    path=os.getcwd()
    dir_list = os.listdir(path)
    files=[]
    for file in dir_list:
        if file != '__pycache__' and file != 'assets':
            files.append(('file',open(path+'/'+str(file),"rb")))
    
    print("Enter your Quanturf username and password...")
    username=input("Enter Username: ")
    password=maskpass.askpass(mask="*")
    user_auth={'username':username,'password':password}
    user_auth=json.dumps(user_auth)
    headers = {'Content-type': 'application/json'}
    auth_request=requests.post(url=AUTH_URL,data=user_auth,headers=headers)
    auth_response=auth_request.json()
    print(auth_response['message'])

    if auth_response['message'] == 'Authentication Successful!':
        file_upload_request=requests.post(url=URL,files=files)
        file_upload_response=file_upload_request.json()
        print(file_upload_response['message'])

@app.command()
def jupyterlab():
    print("Running Jupyter platform!")
    out = site.getsitepackages()

    if len(out) == 1:
        str_out = out
        str_out = ' '.join(str_out)
        env_dir = os.path.normpath(os.path.join(str_out, "quanturf"))
        os.environ['JUPYTER_APP_LAUNCHER_PATH'] = env_dir

        filename = os.path.join(str_out, "quanturf","jupyter_notebook_config.py")
        filename2 = filename.replace(os.sep, '/')
        print("filename2: ", filename2)
        os.system("jupyter lab --config=" + filename2)

    if len(out) >= 2:
        str_out = out[1]
        env_dir = os.path.normpath(os.path.join(str_out, "quanturf"))
        os.environ['JUPYTER_APP_LAUNCHER_PATH'] = env_dir

        filename = os.path.join(str_out, "quanturf","jupyter_notebook_config.py")
        filename2 = filename.replace(os.sep, '/')
        os.system("jupyter lab --config=" + filename2)


if __name__ == "__main__":
    app()
