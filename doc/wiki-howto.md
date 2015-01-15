#危害公共安全事件的关联关系挖掘及预测代码说明文档

<pre><code>
团队名称：OmniEye团队 
团队成员:陈夏明，强思维，王海洋，孙莹，石开元  
指导老师：上海交通大学网络信息中心 金耀辉 教授  
联系方式：chenxm35@gmail.com 
</code></pre>
## 概述  
>本危害公共安全事件的关联关系挖掘及预测案例,提供了基于多维（时间、空间、语义）数据分析的公共安全事件管理方法，包括同类、异类事件的相关性分析，以及预测未来一段时间内同地区发生类似事件的可能性。该系统提供了完整的媒体数据处理和模型生成方法，主要分为关联性分析和未来事件预测两部分。包含以下核心模块可供单独调用：  
>*  媒体事件识别、提取、分类  
>*  众包事件标注与事件分类校验    
>*  时空、语义特征提取  
>*  媒体传播规律、事件发生时空关联性分析  
>*  基于Gradient-Boosting算法的事件预测、交叉验证  

## 运行环境    
>*  操作系统:Mac OS X,Linux or Windows
>*  平台:Hadoop 1.2.1,Spark 1.1.1    
>*  语言:PHP,R,SQL,Python  
>*  拓展平台:SAE,微信公众平台,CKAN平台  
 

##  代码集介绍:  

###data_process:  
>该代码包中是数据处理部分，数据处理分四步进行:事件提取、分类，时空语义特征提取，时空相关性分析，事件预测。具体思路如下：   
>*  `event_classify`:媒体事件识别、提取、分类
>*  `feature_spatio-temporal`:时空、语义特征提取
>*  `correlation_analysis`:媒体传播规律、事件发生时空关联性分析
>*  `critical_forecast`:基于Gradient-Boosting算法的事件预测、交叉验证   
  
###data_public:  
>该代码包部分是基于开放数据以众包的方式进行人工标注与校验，原始报道数据集存储于CKAN平台，通过微信公众平台调用CKAN数据，并通过微信公众帐号将数据记录推送给大众进行事件类型标注，并将标注结果上传CKAN平台，通过大众的力量做事件分类校准集。  
>*  `index.php`:通过CKAN平台进行数据管理，微信公众平台实现众包标注，并实现两个平台实时通信  

##编译及配置  
###源码下载  
  
>该工程源码使用github仓库进行管理，克隆仓库到本地：
 
    git clone git@github.com:OMNI-Lab/CCFBDC2014.git

>或直接`Download ZIP`打包下载源码  
  
###源码编译  
  
####**`data_process`**  
    
>* **`event_classify`**    
>首先对公开的新闻和微博报道数据，结合其他多种数据源(如地区人口分布数据、GDP数据等)对公交，车爆炸、暴力恐怖、校园砍杀三类事件进行识别和提取、分类，采用TF-IDF相似度匹配算法对进行事件提取，余弦相似度计算对事件分类，相似度达到一定阈值的一簇媒体报导均属于同一类事件。事件提取、分类结果详见[新闻分类子数据集](http://data.sjtu.edu.cn/dataset/ccfbd/resource/a2d960a0-8d5e-4be0-b20a-42b9a6210c9f)和[微博分类子数据集](http://data.sjtu.edu.cn/dataset/ccfbd/resource/2b3e552a-815f-4664-9dc1-e580a2ed25f7)(提供如下本地和Hadoop两种运行环境)  
> 本地环境：  
1) 新闻分类，在`python/classify_news`文件夹中运行`python classify_news.py`   
2) 微博分类，在`python/classify_weibo`文件夹中运行`python classify_weibo.py`   
> Hadoop环境：  
1) 新闻分类，在`spark/classify_news`运行 `pyspark news_classify.py`  
2) 微博分类，在`spark/classify_weibo`运行 `pyspark weibo_classify.py` 
    
>* **`feature_spatio-temporal`**    
>我们从时间、空间、语义三个方面对事件进行了特征提取，共提取52个特征，特征详见[事件特征子数据集](http://data.sjtu.edu.cn/dataset/ccfbd/resource/67c855a0-e3e5-4263-a7fd-52f6610b9dfd) 
>*时间特征提取，事件发生期间的节日、周几，事件第一篇报道出现时间，事件最后一篇报道出现时间，事件报道持续时长，50%，75%，95%新闻报道集中出现所占时长等特征进行统计：`feature_temporal`文件夹下，python运行： `python feature_temporal.py`  
>*空间特征提取，从事件发生城市、所在城市、面积、人口、GDP情况进行统计：`feature_spatio`文件夹下运行 `python feature_spatio.py`  
>*语义特征提取，从事件相关报道数、报道评论数、报道篇幅长度等特征进行提取： `$ R -f features_spatio.R`  

>* **`correlation_analysis`:**    
>通过相关性分析与数据可视化的方法，对已提取事件的媒体传播规律、事件发生的时空共性进行分析研究，空间维度上，中国主要地区使用Pearson Coefficient定义相似系数，并通过区域矩阵给出。在时间维度上，我们通过分析类似事件的时间顺序，检测显著事件重复出现的时间间隔。   
>R环境下运行:  `$ R -f corellation_analysis.R`

>* **`critical_forecast`：**  
>采用Gradient-Boosting算法对未来一段时间内某地区公共安全事件是否发生进行预测，同时利用回归树(Regression Trees)算法对该地区发生的频次进行预测，最后用交叉验证方法验证预测的准确度。  
>spark环境下运行`prediction.py`  
  
####**`data_public`**  

>将`index.php`托管于新浪SAE实现代码管理，并设置微信公众平台，在开发者中心配置微信公众平台与sae代码服务器接口及Token。  
> **微信公众平台**：`OmniEye`  
> **CKAN平台**：<http://data.sjtu.edu.cn/dataset/ccfbd>


<center>编辑时间：2014-12-04<center>  
<center>**大赛网址**<http://activity.hylanda.com/><center>