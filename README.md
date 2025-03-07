

#第二届中国大数据技术创新大赛作品

## 危害公共安全事件的关联关系挖掘及预测

本危害公共安全事件的关联关系挖掘及预测案例，提供了基于多维（时间、空间、语义）数据分析的公共安全事件管理方法，包括同类、异类事件的相关性分析，以及预测未来一段时间内同地区发生类似事件的可能性。

* 团队名称：OmniEye团队 
* 团队成员：陈夏明，强思维，王海洋，孙莹，石开元  
* 指导老师：上海交通大学网络信息中心 金耀辉 教授  
* 联系方式：chenxm35@gmail.com 
* 项目地址：http://omnilab.github.io/CCFBDC2014

## 项目资料

项目包含参赛过程中的数据集、源代码、文档、以及BDTC报告幻灯片(PDF)。有需要进一步咨询或交流的童鞋可联系OmniEye团队成员，我们希望能和大家有更多的交流。

### 数据集

本赛题的数据集由[海量公司提供](http://www.hylanda.com/)。原始数据集主要包括从网络媒体
（包括新闻和微博）爬取的2011-2014年三类公共安全事件（公交爆炸、暴力恐怖、校园砍杀）的报道数据。[原始数据集](http://pan.baidu.com/s/1kTBUrSr) 我们也提供了下载（**提取密码**: k4zd）。除此之外，我们还公开了比赛过程中采集到其他数据集，以及分析过程中生成的重要结果，如事件量化特征；此类[扩展数据集](http://data.sjtu.edu.cn/dataset/ccfbd)托管在我们OMNILab基于CKAN的数据共享平台上，可免费下载。

### 源代码

针对比赛数据，该项目代码提供了完整的媒体数据处理和模型生成方法，主要分为关联性分析和未来事件预测两部分。源代码[托管在Github](https://github.com/OMNILab/CCFBDC2014)上，主要包含以下核心模块:

*  媒体事件识别、提取、分类
*  众包事件标注与事件分类校验
*  时空、语义特征提取
*  媒体传播规律、事件发生时空关联性分析
*  基于Gradient-Boosting算法的事件预测、交叉验证

代码的详细使用文档请参考[Wiki说明](https://github.com/OMNILab/CCFBDC2014/wiki)。

### 文档及报告

参赛过程中的总体分析思路和结果，最终以文档的形式提交给比赛组委会。这里我们共享出提交文档以及BDTC2014会议的专场报告。文档包含在[该项目](https://github.com/OMNI-Lab/CCFBDC2014)源代码根目录下：

* [BDC-PAPER-OmniEye](https://github.com/OMNILab/CCFBDC2014/raw/master/BDC-PAPER-OmniEye.pdf): 该文档为比赛提交论文
* [BDC-Talk-2014-OmniEye](https://github.com/OMNILab/CCFBDC2014/raw/master/BDC-Talk-2014-OmniEye.pdf): 该文档为BDTC2014赛事专场报告的Slides

如果您使用的是Web浏览器，可直接访问论文的[网页版本](http://omnilab.github.io/CCFBDC2014/paper)。

### 公共安全事件可视化

经过语境过滤的事件分类和事件提取之后，我们获得了～1200件大小事件的发生时间、地点、以及媒体影响。针对这些数据的可视化展示请访问：http://omnilab.github.io/CCFBDC2014/map 。

## 赛事链接

* **大赛网址：**<http://bigdatacontest.ccf.org.cn/>  
* **公共安全赛题：**<http://activity.hylanda.com/>

<center>编辑时间 2014-12-24<center>
