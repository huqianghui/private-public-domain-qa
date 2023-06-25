# Azure OpenAI on your data 功能介绍
随着新版本API的2023-06-01-preview的release， azure openAI也引入一些新的功能，其中 on your data就是其中之一。

## 1. 首先来对比一下，2023-03-15-preview 和 2023-06-01-preview在API schema层面有哪些不同。
<img width="1137" alt="Screen Shot 2023-06-25 at 10 22 29 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/adc72dbd-4bd6-4bb4-a35d-44f427a787bf">

从后侧边栏，绿色部分就是2023-06-01-preview 与 2023-03-15-preview 不同的地方。
可以观察到2023-06-01-preview版本，新增了大量的内容。具体的新增内容如下：

2023-03-15-preview：

<img width="1146" alt="Screen Shot 2023-06-25 at 10 27 45 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/a449990c-40ac-4033-88c5-429cb817e79b">

2023-06-01-preview：

**1172行的datasource就在其中。**

<img width="1138" alt="Screen Shot 2023-06-25 at 10 28 00 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/8f1ffae7-2816-465c-a5f9-866182417b0f">


## 2. 指定datasource之后，来看一下一个调用示例。

从浏览器的控制台，可以得知，绑定datasource的时候，调用就是2023-06-01-preview版本的API。
**请注意：示例中的API版本还是2023-03-15-preview**

sample payload
```javascript
{
  "dataSources": [
    {
      "type": "AzureCognitiveSearch",
      "parameters": {
        "endpoint": "https://gptkb-zjpky6jixgcx2.search.windows.net",
        "key": "XXXXXX",
        "indexName": "auto-upload-index03",
        "semanticConfiguration": "",
        "queryType": "simple",
        "fieldsMapping": null,
        "inScope": true,
        "roleInformation": "You are an AI assistant that helps people find information."
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "what's the gpt4 model's main purpose?"
    }
  ],
  "deployment": "chat",
  "temperature": 0,
  "top_p": 1,
  "max_tokens": 800,
  "stop": null,
  "stream": true
}
```

<img width="1440" alt="Screen Shot 2023-06-25 at 9 29 39 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/fb4ea8fd-b399-4d8c-886f-10a955b0ab34">


<img width="1438" alt="Screen Shot 2023-06-25 at 9 29 57 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/f735cae5-5ae6-4bdd-96c8-36ade4999564">


