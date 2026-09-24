backend-1  | INFO:     Started reloader process [1] using WatchFiles                                                                            
frontend-1  |                                                                                                                                   
frontend-1  | > agentscout-frontend@1.0.0 dev
frontend-1  | > vite --host                                                                                                                     
frontend-1  |                                                                                                                                   
frontend-1  |                                                                                                                                   
frontend-1  |   VITE v5.4.21  ready in 205 ms
frontend-1  |                                                                                                                                   
frontend-1  |   ➜  Local:   http://localhost:5173/                                                                                              
frontend-1  |   ➜  Network: http://172.20.0.4:5173/                                                                                             
backend-1   | Process SpawnProcess-1:                                                                                                           
backend-1   | Traceback (most recent call last):
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 419, in import_email_validator
backend-1   |     import email_validator                                                                                                        
backend-1   | ModuleNotFoundError: No module named 'email_validator'                                                                            
backend-1   | 
backend-1   | The above exception was the direct cause of the following exception:                                                              
backend-1   |                                                                                                                                   
backend-1   | Traceback (most recent call last):                                                                                                
backend-1   |   File "/usr/local/lib/python3.11/multiprocessing/process.py", line 314, in _bootstrap                                            
backend-1   |     self.run()                                                                                                                    
backend-1   |   File "/usr/local/lib/python3.11/multiprocessing/process.py", line 108, in run                                                   
backend-1   |     self._target(*self._args, **self._kwargs)                                                                                     
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started                           
backend-1   |     target(sockets=sockets)
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 65, in run                                               
backend-1   |     return asyncio.run(self.serve(sockets=sockets))                                                                               
backend-1   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                               
backend-1   |   File "/usr/local/lib/python3.11/asyncio/runners.py", line 190, in run                                                           
backend-1   |     return runner.run(main)                                                                                                       
backend-1   |            ^^^^^^^^^^^^^^^^                                                                                                       
backend-1   |   File "/usr/local/lib/python3.11/asyncio/runners.py", line 118, in run                                                           
backend-1   |     return self._loop.run_until_complete(task)                                                                                    
backend-1   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend-1   |   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete                                                       
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 69, in serve                                             
backend-1   |     await self._serve(sockets)                                                                                                    
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 76, in _serve                                            
backend-1   |     config.load()                                                                                                                 
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 434, in load                                             
backend-1   |     self.loaded_app = import_from_string(self.app)                                                                                
backend-1   |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                
backend-1   |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
backend-1   |     module = importlib.import_module(module_str)                                                                                  
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                  
backend-1   |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module                                              
backend-1   |     return _bootstrap._gcd_import(name[level:], package, level)                                                                   
backend-1   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                   
backend-1   |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import                                                                 
backend-1   |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load                                                              
backend-1   |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked                                                     
backend-1   |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
backend-1   |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module                                                         
backend-1   |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed                                                    
backend-1   |   File "/app/app/main.py", line 11, in <module>                                                                                   
backend-1   |     from app.api.auth import router as auth_router                                                                                
backend-1   |   File "/app/app/api/auth.py", line 13, in <module>
backend-1   |     from app.schemas.schemas import UserCreate, UserResponse, Token                                                               
backend-1   |   File "/app/app/schemas/schemas.py", line 7, in <module>                                                                         
backend-1   |     class UserCreate(BaseModel):                                                                                                  
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_model_construction.py", line 224, in __new__                  
backend-1   |     complete_model_class(                                                                                                         
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_model_construction.py", line 577, in complete_model_class
backend-1   |     schema = cls.__get_pydantic_core_schema__(cls, handler)                                                                       
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                       
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 671, in __get_pydantic_core_schema__                      
backend-1   |     return handler(source)                                                                                                        
backend-1   |            ^^^^^^^^^^^^^^^                                                                                                        
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__            
backend-1   |     schema = self._handler(source_type)                                                                                           
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 655, in generate_schema             
backend-1   |     schema = self._generate_schema_inner(obj)                                                                                     
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                     
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 924, in _generate_schema_inner      
backend-1   |     return self._model_schema(obj)                                                                                                
backend-1   |            ^^^^^^^^^^^^^^^^^^^^^^^
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 739, in _model_schema               
backend-1   |     {k: self._generate_md_field_schema(k, v, decorators) for k, v in fields.items()},                                             
backend-1   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                              
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 739, in <dictcomp>                  
backend-1   |     {k: self._generate_md_field_schema(k, v, decorators) for k, v in fields.items()},                                             
backend-1   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                          
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 1115, in _generate_md_field_schema  
backend-1   |     common_field = self._common_field_schema(name, field_info, decorators)                                                        
backend-1   |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 1308, in _common_field_schema       
backend-1   |     schema = self._apply_annotations(                                                                                             
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^                                                                                             
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 2107, in _apply_annotations         
backend-1   |     schema = get_inner_schema(source_type)                                                                                        
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                        
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__            
backend-1   |     schema = self._handler(source_type)
backend-1   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                           
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 2086, in inner_handler              
backend-1   |     from_property = self._generate_schema_from_property(obj, source_type)                                                         
backend-1   |                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                         
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 821, in _generate_schema_from_property
backend-1   |     schema = get_schema(
backend-1   |^^^^^^^^^^^
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 459, in __get_pydantic_core_schema__
backend-1   |     import_email_validator()
backend-1   |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 421, in import_email_validator
backend-1   |     raise ImportError('email-validator is not installed, run `pip install pydantic[email]`') from e
backend-1   | ImportError: email-validator is not installed, run `pip install pydantic[email]`
youthful_blackwell  | INFO:     Will watch for changes in these directories: ['/app']
youthful_blackwell  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
youthful_blackwell  | INFO:     Started reloader process [1] using WatchFiles
youthful_blackwell  | Process SpawnProcess-1:
youthful_blackwell  | Traceback (most recent call last):
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 419, in import_email_validator
youthful_blackwell  |     import email_validator
youthful_blackwell  | ModuleNotFoundError: No module named 'email_validator'
youthful_blackwell  |
youthful_blackwell  | The above exception was the direct cause of the following exception:
youthful_blackwell  |
youthful_blackwell  | Traceback (most recent call last):
youthful_blackwell  |   File "/usr/local/lib/python3.11/multiprocessing/process.py", line 314, in _bootstrap
youthful_blackwell  |     self.run()
youthful_blackwell  |   File "/usr/local/lib/python3.11/multiprocessing/process.py", line 108, in run
youthful_blackwell  |     self._target(*self._args, **self._kwargs)
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/_subprocess.py", line 80, in subprocess_started
youthful_blackwell  |     target(sockets=sockets)
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 65, in run
youthful_blackwell  |     return asyncio.run(self.serve(sockets=sockets))
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/asyncio/runners.py", line 190, in run
youthful_blackwell  |     return runner.run(main)
youthful_blackwell  |^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/asyncio/runners.py", line 118, in run
youthful_blackwell  |     return self._loop.run_until_complete(task)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 69, in serve
youthful_blackwell  |     await self._serve(sockets)
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/server.py", line 76, in _serve
youthful_blackwell  |     config.load()
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/config.py", line 434, in load
youthful_blackwell  |     self.loaded_app = import_from_string(self.app)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
youthful_blackwell  |     module = importlib.import_module(module_str)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
youthful_blackwell  |     return _bootstrap._gcd_import(name[level:], package, level)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
youthful_blackwell  |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
youthful_blackwell  |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
youthful_blackwell  |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
youthful_blackwell  |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
youthful_blackwell  |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
youthful_blackwell  |   File "/app/app/main.py", line 11, in <module>
youthful_blackwell  |     from app.api.auth import router as auth_router
youthful_blackwell  |   File "/app/app/api/auth.py", line 13, in <module>
youthful_blackwell  |     from app.schemas.schemas import UserCreate, UserResponse, Token
youthful_blackwell  |   File "/app/app/schemas/schemas.py", line 7, in <module>
youthful_blackwell  |     class UserCreate(BaseModel):
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_model_construction.py", line 224, in __new__
youthful_blackwell  |     complete_model_class(
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_model_construction.py", line 577, in complete_model_class
youthful_blackwell  |     schema = cls.__get_pydantic_core_schema__(cls, handler)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 671, in __get_pydantic_core_schema__
youthful_blackwell  |     return handler(source)
youthful_blackwell  |^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__    
youthful_blackwell  |     schema = self._handler(source_type)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 655, in generate_schema     
youthful_blackwell  |     schema = self._generate_schema_inner(obj)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 924, in _generate_schema_inner
youthful_blackwell  |     return self._model_schema(obj)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 739, in _model_schema       
youthful_blackwell  |     {k: self._generate_md_field_schema(k, v, decorators) for k, v in fields.items()},
youthful_blackwell  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 739, in <dictcomp>
youthful_blackwell  |     {k: self._generate_md_field_schema(k, v, decorators) for k, v in fields.items()},
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 1115, in _generate_md_field_schema
youthful_blackwell  |     common_field = self._common_field_schema(name, field_info, decorators)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 1308, in _common_field_schema
youthful_blackwell  |     schema = self._apply_annotations(
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 2107, in _apply_annotations 
youthful_blackwell  |     schema = get_inner_schema(source_type)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 83, in __call__    
youthful_blackwell  |     schema = self._handler(source_type)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 2086, in inner_handler      
youthful_blackwell  |     from_property = self._generate_schema_from_property(obj, source_type)
youthful_blackwell  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/_internal/_generate_schema.py", line 821, in _generate_schema_from_property
youthful_blackwell  |     schema = get_schema(
youthful_blackwell  |^^^^^^^^^^^
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 459, in __get_pydantic_core_schema__
youthful_blackwell  |     import_email_validator()
youthful_blackwell  |   File "/usr/local/lib/python3.11/site-packages/pydantic/networks.py", line 421, in import_email_validator
youthful_blackwell  |     raise ImportError('email-validator is not installed, run `pip install pydantic[email]`') from e
youthful_blackwell  | ImportError: email-validator is not installed, run `pip install pydantic[email]`
frontend-1          | 12:13:03 PM [vite] http proxy error: /api/auth/login
frontend-1          | Error: connect ECONNREFUSED 172.20.0.3:8000
frontend-1          |     at TCPConnectWrap.afterConnect [as oncomplete] (node:net:1611:16)                                                     
frontend-1          | 12:13:38 PM [vite] http proxy error: /api/auth/signup                                                                     
frontend-1          | Error: connect ECONNREFUSED 172.20.0.3:8000
frontend-1          |     at TCPConnectWrap.afterConnect [as oncomplete] (node:net:1611:16)                                                     
frontend-1          | 12:13:40 PM [vite] http proxy error: /api/auth/signup                                                                     
frontend-1          | Error: connect ECONNREFUSED 172.20.0.3:8000
frontend-1          |     at TCPConnectWrap.afterConnect [as oncomplete] (node:net:1611:16)                                                     
                                                                                                                                                

v View in Docker Desktop   o View Config   w Enable Watch