import datetime
import logging
from datetime import datetime
from multiprocessing import Process

import dotenv
import uvicorn
from decouple import config
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from urllib.parse import urlparse
import requests
import os
import shutil
import datetime
import tempfile
from distutils.dir_util import copy_tree


dotenv.load_dotenv('.env')

from rpamaker.utils import call_robot, call_command
from rpamaker.orquestador import OrquestadorAPI

logging.basicConfig(level=logging.INFO)

api_keys = [
    config('RPAMAKER_TOKEN')
]  # This is encrypted in the database
RPAMAKER_HOST = config('RPAMAKER_HOST', "0.0.0.0")
RPAMAKER_PORT = int(config('RPAMAKER_PORT', 8001))

print(config('RPAMAKER_TOKEN'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


def start_workspace_api():
    app = FastAPI()

    @app.get("/", dependencies=[Depends(api_key_auth)])
    def test_endpoint():
        return JSONResponse(content={'status': 'ok'}, status_code=200)
    
    @app.post("/deploy/", dependencies=[Depends(api_key_auth)])
    async def deploy(request: Request):
        json_body = {}
        try:
            json_body = await request.json()
        except Exception as err:
            logging.error(err)
        
        _url = json_body['url']
        _branch = json_body['branch']
        _deployment_id = json_body['deployment_id']
        _, owner, repo = urlparse(_url).path.split("/")

        if "Token" in request.headers.get("X-GitHub-Token"):
            _orquestador_api = OrquestadorAPI()
            _git_token = request.headers.get("X-GitHub-Token").split()[1]
            _headers = {
                    "Content-Type": "application/json",
                    'Authorization': f"Bearer {_git_token}",
                    'X-GitHub-Api-Version': "2022-11-28"
                }
            _zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{_branch}"
            
            result = requests.get(_zip_url, headers=_headers, timeout=15)
            if result.status_code != 200:
                logging.error("Error in downloading the zip file")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error in downloading the zip file"
                )            
                        
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            extract_dir = os.path.join(tempfile.gettempdir(), now)
            archive_file = os.path.join(extract_dir, f"build_{_deployment_id}.zip")
            os.makedirs(extract_dir)
                        
            with open(archive_file, "wb") as file_pointer:
                file_pointer.write(result.content)  
                logging.info("extracting zip file '%s' to '%s'", archive_file, extract_dir)                   
            shutil.unpack_archive(archive_file, extract_dir, "zip") 
            os.remove(archive_file)    
            from_dir =  os.path.join(os.path.join(extract_dir, os.listdir(extract_dir)[0]),"base")  
            to_dir =  os.path.join(os.getcwd(), "base")
            
            if not os.path.isdir(extract_dir):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error in structure robot"
                )                         
            
            copy_tree(from_dir, to_dir)              
            response=_orquestador_api.deploy(deployment_id=_deployment_id, status="SUCCESS", message="Deployed successfully")              
            if response.status_code == 200:
                return JSONResponse(content={'status': 'ok'}, status_code=200)                
            else:
                return JSONResponse({'error': response.text}, status_code=400)                
        else:            
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )        


    @app.post("/execute-command/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
    async def execute_command(request: Request, t_id, w_id):
        json_body = {}
        try:
            json_body = await request.json()
        except Exception as err:
            logging.error(err)

        _type = json_body['_type'] = 'python'
        _command = json_body['_command']
        _config = json_body['_meta']
        _console_flag = json_body['_console_flag']

        if _type == 'python':
            _command = f'python -c "{_command}"'

        start_command(_command, t_id)

        return 200

    @app.post("/run/{keyword}/{t_id}/{w_id}/", dependencies=[Depends(api_key_auth)])
    async def run_robot(request: Request, keyword, t_id, w_id):
        logging.debug(f'{datetime.now()}')
        console_flag = request.headers.get('console_flag') == 'True'

        json_body = {}
        try:
            json_body = await request.json()
        except Exception as err:
            logging.error(err)

        variables = []
        for k, v in json_body.items():
            variables.append('--variable')
            variables.append(f'{k}:{v}')

        variables.extend([
            '--variable', f'id_t:{t_id}',
            '--variable', f'id_p:{w_id}',
            '--variable', f'console_flag:{console_flag}',
        ])

        start_process(keyword, variables, t_id)

        return 200

    def start_process(keyword, variables, t_id):
        p = Process(target=call_robot, args=(keyword, variables, t_id))
        p.start()
        logging.info(f"Process {p} started")

    def start_command(command, t_id):
        p = Process(target=call_command, args=(command, t_id))
        p.start()
        logging.info(f"Process {p} started")

    logging.info('About to start worksapce')
    uvicorn.run(app, host=RPAMAKER_HOST, port=RPAMAKER_PORT)


if __name__ == '__main__':
    start_workspace_api()
