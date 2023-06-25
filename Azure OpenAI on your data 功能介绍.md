## Azure OpenAI on your data 功能介绍
随着新版本API的2023-06-01-preview的release， azure openAI也引入一些新的功能，其中 on your data就是其中之一。

### 1. 首先来对比一下，2023-03-15-preview 和 2023-06-01-preview在API schema层面有哪些不同。
<img width="1137" alt="Screen Shot 2023-06-25 at 10 22 29 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/adc72dbd-4bd6-4bb4-a35d-44f427a787bf">

从后侧边栏，绿色部分就是2023-06-01-preview 与 2023-03-15-preview 不同的地方。
可以观察到2023-06-01-preview版本，新增了大量的内容。具体的新增内容如下：

2023-03-15-preview：

<img width="1146" alt="Screen Shot 2023-06-25 at 10 27 45 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/a449990c-40ac-4033-88c5-429cb817e79b">

2023-06-01-preview：

**1172行的datasource就在其中。**

<img width="1138" alt="Screen Shot 2023-06-25 at 10 28 00 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/8f1ffae7-2816-465c-a5f9-866182417b0f">


### 2. 指定datasource之后，来看一下一个调用示例。

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


### 3. 这里的datasource指的就是 azure cognitive search。

可以使用以及创建好的azure cognitive search 的索引。如果没有的话，可以通过上传文件，或者指定blob storage的位置，让相应文件索引到azure cognitive search里面。

按照步骤，一步步往下就可以。
创建过程大致如下：

<img width="997" alt="Screen Shot 2023-06-25 at 9 24 19 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/b63ae715-b13e-4c6e-a28c-c67475226fcb">

创建好了之后，就可以对的datasource 进行聊天了。
也可以选择发布到 azure app service中，供更多人使用。

<img width="1034" alt="Screen Shot 2023-06-25 at 11 20 19 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/091c1286-289e-40de-8425-1fcd5135f8d8">

访问的时候，需要认证信息。等会，就能访问了。

<img width="1440" alt="Screen Shot 2023-06-25 at 8 55 07 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/ce567e78-7863-44db-92a1-0c936f97cf60">

<img width="1438" alt="Screen Shot 2023-06-25 at 1 43 51 PM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/448c5918-b8cd-406c-9763-1c38621543a4">



### 4. 源码分析

代码github连接如下：
https://github.com/microsoft/sample-app-aoai-chatGPT/tree/main

和在之前视频中介绍的相似，主要内容也如下四块：

1） scripts ： 通过python和表单识别等，实现文件的切割，索引创建，内容上传等。
2） frontend & static： 前端UI的展示
3） app.py : 相当于backend，通过新的API版本2023-06-01-preview来请求服务。
4） infra & infrastructure： 这一套内容的bicep脚本，实现azure组件的创建。

需要进行对比的，还是文件处理：
在具体的data_util.py中，可以看到使用的默认都是英语环境和文档，而且认知搜索的话，只支持英语。
参考官方文档链接如下：
https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/use-your-data
<img width="702" alt="Screen Shot 2023-06-25 at 1 29 24 PM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/125ed5dc-2ed7-4c62-af2e-3c5411f14bff">


<img width="1039" alt="Screen Shot 2023-06-25 at 11 33 42 AM" src="https://github.com/huqianghui/private-public-domain-qa/assets/7360524/eeec11a0-998d-4d0f-b537-345ccbbb7f52">
**https://github.com/microsoft/sample-app-aoai-chatGPT/blob/main/scripts/data_utils.py**



