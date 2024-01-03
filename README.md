[English Readme](./README_EN.md)  /  [👑捐助该项目](./about.md) / [加入Discord](https://discord.gg/TMCM2PfHzQ) / [Q群 902124277](https://qm.qq.com/cgi-bin/qm/qr?k=9VNSiJyInxyQ3HK3vmOTibo8pzcDekju&jump_from=webapi&authKey=xcW1+7N1E4SM+DXqyl5d61UOtNooA1C9WR5A/yfA0fmfyUDRRSZex1WD0l+9x1kO) <img src="https://github.com/jianchang512/clone-voice/assets/3378335/20858f50-6d47-411d-939b-272fe35e474c" width="50" title="点击看大图">

# 视频翻译和配音工具
[预编译版exe下载地址](https://github.com/jianchang512/pyvideotrans/releases)

>
> 这是一个视频翻译配音工具，可将一种语言的视频翻译为另一种语言配音和字幕的视频。
>
> 语音识别基于 `faster-whisper` 离线模型.
>
> 文字翻译支持 `google|baidu|tencent|chatGPT|Azure|Gemini|DeepL|DeepLX` ，
>
> 文字合成语音支持 `Microsoft Edge tts` `Openai TTS-1`.
>

# 主要用途和使用方式

【翻译视频并配音】根据需要设置各个选项，自由配置组合，实现翻译和配音、自动加减速、合并等

【提取字幕不翻译】选择视频文件，选择视频源语言，则从视频识别出文字并自动导出字幕文件到目标文件夹

【提取字幕并翻译】选择视频文件，选择视频源语言，设置想翻译到的目标语言，则从视频识别出文字并翻译为目标语言，然后导出双语字幕文件到目标文件夹

【字幕和视频合并】选择视频，然后将已有的字幕文件拖拽到右侧字幕区，将源语言和目标语言都设为字幕所用语言、然后选择配音类型和角色，开始执行

【为字幕创建配音】将本地的字幕文件拖拽到右侧字幕编辑器，然后选择目标语言、配音类型和角色，将生成配音后的音频文件到目标文件夹

【音视频识别文字】将视频或音频拖拽到识别窗口，将识别出文字并导出为srt字幕格式

【将文字合成语音】将一段文字或者字幕，使用指定的配音角色生成配音

【从视频分离音频】将视频文件分离为音频文件和无声视频

【音视频字幕合并】音频文件、视频文件、字幕文件合并为一个视频文件

【音视频格式转换】各种格式之间的相互转换
【文字字幕翻译】将文字或srt字幕文件翻译为其他语言

----




https://github.com/jianchang512/pyvideotrans/assets/3378335/c3d193c8-f680-45e2-8019-3069aeb66e01

[Youtube demo](https://youtu.be/-S7jptiDdtc)


# 使用win预编译exe版本(其他系统使用源码部署)

0. [点击下载去下载预编译版](https://github.com/jianchang512/pyvideotrans/releases)

1. 建议解压到英文路径下，并且路径中不含有空格。解压后双击 sp.exe(若遇到权限问题可右键使用管理员权限打开)

3. 未做免杀，国产杀软可能误报，可忽略或使用源码部署


# 源码部署

1. 配置好 python 3.9->3.11 环境
2. `git clone https://github.com/jianchang512/pyvideotrans`
3. `cd pyvideotrans`
4. `python -m venv venv`
5. win下执行 `%cd%/venv/scripts/activate`,linux和mac执行 `source ./venv/bin/activate`
6. `pip install -r requirements.txt`，如果遇到版本冲突报错，请使用 `pip install -r requirements.txt --no-deps`
7. win下解压 ffmpeg.zip 到根目录下 (ffmpeg.exe文件)，linux和mac 到 [ffmpeg官网](https://ffmpeg.org/download.html)下载对应版本ffmpeg，解压到根目录下，注意必须是直接将可执行文件 ffmpeg 放在根目录下
8. `python sp.py` 打开软件界面
9. 如果需要支持CUDA加速，需要设备具有 NVIDIA 显卡，具体安装防范见下方 [CUDA加速支持](https://github.com/jianchang512/pyvideotrans?tab=readme-ov-file#cuda-%E5%8A%A0%E9%80%9F%E6%94%AF%E6%8C%81)


# 使用方法

1. 原始视频：选择mp4/avi/mov/mkv/mpeg视频,可选择多个视频；

2. 输出视频目录：如果不选择，则默认生成在同目录下的 `_video_out`，同时在该目录下的srt文件夹中将创建原语言和目标语言的两种字幕文件

3. 选择翻译：可选 google|baidu|tencent|chatGPT|Azure|Gemini|DeepL|DeepLX 翻译渠道

4. 网络代理地址：如果你所在地区无法直接访问 google/chatGPT，需要在软件界面 网络代理 中设置代理，比如若使用 v2ray ，则填写 `http://127.0.0.1:10809`,若clash，则填写 `http://127.0.0.1:7890`. 如果你修改了默认端口或使用的其他代理软件，则按需填写

5. 视频原始语言：选择待翻译视频里的语言种类

6. 翻译目标语言：选择希望翻译到的语言种类

7. 选择配音：选择翻译目标语言后，可从配音选项中，选择配音角色；
   
   硬字幕: 是指始终显示字幕，不可隐藏，如果希望网页中播放时也有字幕，请选择硬字幕嵌入

   软字幕: 如果播放器支持字幕管理，可显示或者隐藏字幕，该方式网页中播放时不会显示字幕，某些国产播放器可能不支持,需要将生成的视频同名srt文件和视频放在一个目录下才会显示


8. 语音识别模型: 选择 base/small/medium/large-v3, 识别效果越来越好，但识别速度越来越慢，所需内存越来越大，内置base模型，其他模型请单独下载后，解压放到 `当前软件目录/models`目录下.如果GPU显存低于4G，不要使用 large-v3

   整体识别/预先分割: 整体识别是指直接发送整个语音文件给模型，由模型进行处理，分割可能更精确，但也可能造出30s长度的单字幕，适合有明确静音的音频;  预先分割时指先将音频按10s左右长度切割后再分别发送给模型处理。

    [全部模型下载地址](https://github.com/jianchang512/stt/releases/tag/0.0)
    
    下载后解压，将压缩包内的"models--Systran--faster-whisper-xx"文件夹复制到models目录内，解压复制后 models 目录下文件夹列表如下

    ![](https://github.com/jianchang512/stt/assets/3378335/5c972f7b-b0bf-4732-a6f1-253f42c45087)


   
    [VLC解码器下载](https://www.videolan.org/vlc/)

    [FFmepg下载(编译版已自带)](https://www.ffmpeg.org/)

9. 配音语速：填写 -90到+90 之间的数字，同样一句话在不同语言语音下，所需时间是不同的，因此配音后可能声画字幕不同步，可以调整此处语速，负数代表降速，正数代表加速播放。

10. 音视频对齐: 分别是“配音自动加速”和“视频自动降速”

>
> 翻译后不同语言下发音时长不同，比如一句话中文3s，翻译为英文可能5s，导致时长和视频不一致。
> 
> 2种解决方式:
>
>     1. 强制配音加速播放，以便缩短配音时长和视频对齐
> 
>     2. 强制视频慢速播放，以便延长视频时长和配音对齐。
> 
> 两者只可选其一
>  
 
  
11. 静音片段: 填写100到2000的数字，代表毫秒，默认 500，即以大于等于 500ms 的静音片段为区间分割语音

12. **CUDA加速**：确认你的电脑显卡为 N卡，并且已配置好CUDA环境和驱动，则开启选择此项，速度能极大提升，具体配置方法见下方[CUDA加速支持](https://github.com/jianchang512/pyvideotrans?tab=readme-ov-file#cuda-%E5%8A%A0%E9%80%9F%E6%94%AF%E6%8C%81)

13. TTS: 可用 edgeTTS 和 openai TTS模型中选择要合成语音的角色，openai需要使用官方接口或者开通了tts-1模型的三方接口

14. 点击 开始按钮 底部会显示当前进度和日志，右侧文本框内显示字幕

15. 字幕解析完成后，将暂停等待修改字幕，如果不做任何操作，60s后将自动继续下一步。也可以在右侧字幕区编辑字幕，然后手动点击继续合成

16. 将在目标文件夹中视频同名的子目录内，分别生成两种语言的字幕srt文件、原始语音和配音后的wav文件，以方便进一步处理

17. 设置行角色：可对字幕中的每行设定发音角色，首先左侧选好TTS类型和角色，然后点击字幕区右下方“设置行角色”，在每个角色名后面文本中中，填写要使用该角色配音的行编号，如下图：
    ![](./images/p2.png)




# 注意事项:

**字幕显示问题**
> 
> 采用软合成字幕：字幕作为单独文件嵌入视频，可再次提取出，如果播放器支持，可在播放器字幕管理中启用或禁用字幕；
> 
> 注意很多国内播放器必须将srt字幕文件和视频放在同一目录下且名字相同，才能加载软字幕，并且可能需要将srt文件转为GBK编码，否则显示乱码，
> 

**字幕语音对齐问题**

> 翻译后不同语言下发音时长不同，比如一句话中文3s，翻译为英文可能5s，导致时长和视频不一致。
> 
> 2种解决方式:
> 
>     1. 强制配音加速播放，以便缩短配音时长和视频对齐
> 
>     2. 强制视频慢速播放，以便延长视频时长和配音对齐。
> 
> 两者只可选其一

**背景音乐问题**

只识别人声并保存人声，即配音后音频中不会存在原背景音乐，如果你需要保留，请使用[人声背景音乐分离项目](https://github.com/jianchang512/vocal-separate)，将背景音提取出来，然后再和配音文件合并。

**语言克隆和自定义音色**
目前暂不支持该功能，如果有需要，你可以先识别出字幕，然后使用另一个[声音克隆项目](https://github.com/jiangchang512/clone-voice),输入字幕srt文件，选择自定义的音色合成为音频文件，然后再生成新视频。


**large-v3模型问题**

如果你没有N卡GPU，或者没有配置好CUDA环境，或者显存低于4G，请不要使用这个模型，否则会非常慢和卡顿



**提示ffmpeg错误**

如果你启用了CUDA，并遇到了该问题，请更新显卡驱动，然后重新配置CUDA环境


**提示缺少cublasxx.dll文件**

有时会遇到“cublasxx.dll不存在”的错误，此时需要下载 cuBLAS，然后将dll文件复制到系统目录下

[点击下载 cuBLAS](https://github.com/jianchang512/stt/releases/download/0.0/cuBLAS_win.7z)，解压后将里面的dll文件复制到 C:/Windows/System32下





# CUDA 加速支持

**安装CUDA工具** [详细安装方法](https://juejin.cn/post/7318704408727519270)


安装好CUDA后，如果有问题，执行 `pip uninstall torch torchaudio torchvision` 卸载，然后去 [https://pytorch.org/get-started/locally/]() 根据你的操作系统类型和 CUDA 版本，选择命令，将 `pip3` 改为 `pip`，再复制命令去执行。
 
安装完成后执行 `python testcuda.py` 如果输出均是  True,说明可用  

有时会遇到“cublasxx.dll不存在”的错误，此时需要下载 cuBLAS，然后将dll文件复制到系统目录下

[点击下载 cuBLAS](https://github.com/jianchang512/stt/releases/download/0.0/cuBLAS_win.7z)，解压后将里面的dll文件复制到 C:/Windows/System32下



# 软件预览截图

![](./images/p1.png?c)


## 视频前后对比

[Demo 原视频和翻译后视频](https://www.wonyes.org/demo.html)


# 相关联项目

[声音克隆工具:用任意音色合成语音](https://github.com/jianchang512/clone-voice)

[语音识别工具:本地离线的语音识别转文字工具](https://github.com/jianchang512/stt)

[人声背景乐分离:极简的人声和背景音乐分离工具，本地化网页操作](https://github.com/jianchang512/stt)

## 致谢

> 本程序依赖这些开源项目

1. pydub
2. ffmpeg
3. PyQt5
4. SpeechRecognition
5. edge-tts
6. openai-whisper
7. faster-whisper


