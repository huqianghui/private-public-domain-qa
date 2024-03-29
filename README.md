# CognitiveSearchChatGPTDemo
Combine Cognitive Search, Bing Search, TTS, STT with ChatGPT to provide Q&amp;A chatbot

哔哩哔哩地址：https://www.bilibili.com/video/BV1bF411d7io/

youtube地址：https://youtu.be/x97ftlavJDM



## Preview
![Preview](https://github.com/huqianghui/private-public-domain-qa/assets/7360524/e6cfa9ab-752b-4718-b52c-ac2b228ac944)
![Preview](/docs/images/Slide3.JPG)
![Preview](/docs/images/Slide4.JPG)

## Setup

### Dependencies
- [Azure Bing Search Service](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/quickstarts/python)
- [Azure Speech Service](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/text-to-speech/quickstart-python)

### Prerequisites
Install python libraries
```bash
pip install -r requirements.txt
``` 
Build front end
```bash
cd frontend
npm install
npm run build
```

### Create Azure resources

#### Login to Azure CLI
```bash
az login
```
#### Create Azure Resource Group
```bash
az group create --name <resource-group-name> --location <location>
```


##### Create Azure Cognitive Search Index
Create a new Azure Cognitive Search index.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search index create --service-name <search-service-name> --resource-group <resource-group-name> --name <index-name> --fields <fields>
```
##### Create Azure Cognitive Search Data Source
Create a new Azure Cognitive Search data source.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search datasource create --service-name <search-service-name> --resource-group <resource-group-name> --name <data-source-name> --type <data-source-type> --credentials <credentials> --container <container> --data-change-impact <data-change-impact> --data-deletion-impact <data-deletion-impact> --description <description> --data-format <data-format> --eTag <eTag> --name <name> --query <query> --schedule <schedule> --type <type>
```

##### Create Azure Cognitive Search Indexer
Create a new Azure Cognitive Search indexer.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search indexer create --service-name <search-service-name> --resource-group <resource-group-name> --name <indexer-name> --data-source-name <data-source-name> --target-index-name <index-name> --skillset-name <skillset-name>
```


#### Create Azure Bing Search Service
Create a new Azure Bing Search Service resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  

#### Create Azure Speech Service
Create a new Azure Speech Service resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az cognitiveservices account create --name <speech-service-name> --resource-group <resource-group-name> --kind <kind> --sku <sku> --location <location>
```


#### Create Azure Web App
Create a new Azure Web App resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az webapp create --name <web-app-name> --resource-group <resource-group-name> --plan <app-service-plan-name>
```

## To run locally
```bash
cd frontend
npm install
npm run build
cd ..
cd backend
python app.py
```

## To deploy to Azure
Open Azure portal and navigate to your web app resource.  Click on the Deployment Center and select GitHub as the source.  Select the repository and branch you want to deploy.  Click on Save and deploy.  The web app will be deployed to Azure.



