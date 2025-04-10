# Simple ChatGPT client
It is a Python application that serves as the frontend for Azure Open AI's ChatGPT.
It is assumed to be deployed on Azure App Service.

![image](https://github.com/07JP27/openai-client/assets/11060273/39fe32fd-3046-431a-8d39-36d64130faa8)

# 1. Deploy App Service
Deploy Python Stack Web Apps

# 2.Deploy this application
Web Apps > Deployment Center > Setting
- Source : External Git
- Repository : https://github.com/07JP27/az_km_aoai_chatapp/
- Branch : main
- Repository Type : Public

![image](https://github.com/07JP27/openai-client/assets/11060273/ddb1893c-6384-47a2-bf17-ebe7b90e2139)

And click Save button.

# 3.Set startup command
Web Apps > Configuration > General settings > Startup Command

```
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0
```

![image](https://github.com/07JP27/openai-client/assets/11060273/32fe52a8-15d6-40e2-80ea-10dae3e6457b)

And click Save button.

# 4. Set Enviroment variables
Web Apps > Configuration > Application settings

- OPENAI_API_ENDPOINT : Your Azure Open AI API endpoint URL
- OPENAI_API_VERSION : API Version (2024-10-21)
- OPENAI_DEPLOYMENT : The model name you deployed

![image](https://github.com/07JP27/openai-client/assets/11060273/a34ffd2d-f044-4202-be09-fe04ad6f7c79)

And click Save button.

# Access and Enjoy your private ChatGPT!
If you want to set up authentication to client app, Please refer to following document.
https://learn.microsoft.com/azure/app-service/scenario-secure-app-authentication-app-service
