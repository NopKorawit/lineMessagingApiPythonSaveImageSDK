# SDK Test by

## 1. install requirement library and install ngrok
```
pip install -r .\requirements.txt
```
## 2. run api 
```
uvicorn main:app --reload
```
## 3. port forward for line messaging API
```
ngrok http 8000  
```
## 4. add path to messaging API
```
(forward domain.app)/callback
```
