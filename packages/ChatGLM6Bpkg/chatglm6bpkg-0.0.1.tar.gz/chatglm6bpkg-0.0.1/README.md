# ChatGLM6Bpkg

这是一个针对[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B/tree/main)封装的包，通过ChatGLM6Bpkg，用户可以简便地使用[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B/tree/main)支持的多种功能。

## 使用方式

### 硬件需求

| **量化等级**  | **最低 GPU 显存**（推理） | **最低 GPU 显存**（高效参数微调） |
| --------- | ----------------- | --------------------- |
| FP16（无量化） | 13 GB             | 14 GB                 |
| INT8      | 8 GB              | 9 GB                  |
| INT4      | 6 GB              | 7 GB                  |
### 模型加载 

可以通过如下代码调用 ChatGLM-6B 模型来生成对话：

```python
>>> from transformers import AutoTokenizer, AutoModel
>>> tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
>>> model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
>>> model = model.eval()
>>> response, history = model.chat(tokenizer, "你好", history=[])
>>> print(response)
你好👋!我是人工智能助手 ChatGLM-6B,很高兴见到你,欢迎问我任何问题。
>>> response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
>>> print(response)
晚上睡不着可能会让你感到焦虑或不舒服,但以下是一些可以帮助你入睡的方法:

1. 制定规律的睡眠时间表:保持规律的睡眠时间表可以帮助你建立健康的睡眠习惯,使你更容易入睡。尽量在每天的相同时间上床,并在同一时间起床。
2. 创造一个舒适的睡眠环境:确保睡眠环境舒适,安静,黑暗且温度适宜。可以使用舒适的床上用品,并保持房间通风。
3. 放松身心:在睡前做些放松的活动,例如泡个热水澡,听些轻柔的音乐,阅读一些有趣的书籍等,有助于缓解紧张和焦虑,使你更容易入睡。
4. 避免饮用含有咖啡因的饮料:咖啡因是一种刺激性物质,会影响你的睡眠质量。尽量避免在睡前饮用含有咖啡因的饮料,例如咖啡,茶和可乐。
5. 避免在床上做与睡眠无关的事情:在床上做些与睡眠无关的事情,例如看电影,玩游戏或工作等,可能会干扰你的睡眠。
6. 尝试呼吸技巧:深呼吸是一种放松技巧,可以帮助你缓解紧张和焦虑,使你更容易入睡。试着慢慢吸气,保持几秒钟,然后缓慢呼气。

如果这些方法无法帮助你入睡,你可以考虑咨询医生或睡眠专家,寻求进一步的建议。
```
模型的实现仍然处在变动中。如果希望固定使用的模型实现以保证兼容性，可以在 `from_pretrained` 的调用中增加 `revision="v1.1.0"` 参数。`v1.1.0` 是当前最新的版本号，完整的版本列表参见 [Change Log](https://huggingface.co/THUDM/chatglm-6b#change-log)。

### 从本地加载模型
以上代码会由 `transformers` 自动下载模型实现和参数。完整的模型实现可以在 [Hugging Face Hub](https://huggingface.co/THUDM/chatglm-6b)。如果你的网络环境较差，下载模型参数可能会花费较长时间甚至失败。此时可以先将模型下载到本地，然后从本地加载。

从 Hugging Face Hub 下载模型需要先[安装Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)，然后运行
```Shell
git clone https://huggingface.co/THUDM/chatglm-6b
```

如果你从 Hugging Face Hub 上下载 checkpoint 的速度较慢，可以只下载模型实现
```Shell
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/THUDM/chatglm-6b
```
然后从[这里](https://cloud.tsinghua.edu.cn/d/fb9f16d6dc8f482596c2/)手动下载模型参数文件，并将下载的文件替换到本地的 `chatglm-6b` 目录下。

将模型下载到本地之后，将以上代码中的 `THUDM/chatglm-6b` 替换为你本地的 `chatglm-6b` 文件夹的路径，即可从本地加载模型。

**Optional** 模型的实现仍然处在变动中。如果希望固定使用的模型实现以保证兼容性，可以执行
```Shell
git checkout v1.1.0
```

## Demo & API

我们提供了一个基于 [Gradio](https://gradio.app) 的网页版 Demo 和一个命令行 Demo。

### 网页版 Demo

![web-demo](resources/web-demo.gif)

示例代码如下： 

```python
import ChatGLM6Bpkg

model_name_or_path = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).half().cuda()
model = model.eval()
ChatGLM6Bpkg.launch_web_demo(model=model, tokenizer=tokenizer)
```

程序会运行一个 Web Server，并输出地址。在浏览器中打开输出的地址即可使用。最新版 Demo 实现了打字机效果，速度体验大大提升。注意，由于国内 Gradio 的网络访问较为缓慢，启用 `demo.queue().launch(share=True, inbrowser=True)` 时所有网络会经过 Gradio 服务器转发，导致打字机体验大幅下降，现在默认启动方式已经改为 `share=False`，如有需要公网访问的需求，可以重新修改为 `share=True` 启动。

### 命令行 Demo

![cli-demo](resources/cli-demo.png)

示例代码如下

```python
import ChatGLM6Bpkg

model_name_or_path = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).half().cuda()
model = model.eval()
ChatGLM6Bpkg.launch_cli_demo(model=model, tokenizer=tokenizer)
```

程序会在命令行中进行交互式的对话，在命令行中输入指示并回车即可生成回复，输入 `clear` 可以清空对话历史，输入 `stop` 终止程序。

### API部署
示例代码如下：
```python
import ChatGLM6Bpkg

model_name_or_path = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).half().cuda()
model = model.eval()
ChatGLM6Bpkg.launch_server(model=model, tokenizer=tokenizer)
```
默认部署在本地的 8000 端口，通过 POST 方法进行调用
```shell
curl -X POST "http://127.0.0.1:8000" \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "你好", "history": []}'
```
得到的返回值为
```shell
{
  "response":"你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。",
  "history":[["你好","你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"]],
  "status":200,
  "time":"2023-03-23 21:38:40"
}
```

## 低成本部署
### 模型量化
默认情况下，模型以 FP16 精度加载，运行上述代码需要大概 13GB 显存。如果你的 GPU 显存有限，可以尝试以量化方式加载模型，使用方法如下：

```python
# 按需修改，目前只支持 4/8 bit 量化
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(8).half().cuda()
```

进行 2 至 3 轮对话后，8-bit 量化下 GPU 显存占用约为 10GB，4-bit 量化下仅需 6GB 占用。随着对话轮数的增多，对应消耗显存也随之增长，由于采用了相对位置编码，理论上 ChatGLM-6B 支持无限长的 context-length，但总长度超过 2048（训练长度）后性能会逐渐下降。

模型量化会带来一定的性能损失，经过测试，ChatGLM-6B 在 4-bit 量化下仍然能够进行自然流畅的生成。使用 [GPT-Q](https://arxiv.org/abs/2210.17323) 等量化方案可以进一步压缩量化精度/提升相同量化精度下的模型性能，欢迎大家提出对应的 Pull Request。

量化过程需要在内存中首先加载 FP16 格式的模型，消耗大概 13GB 的内存。如果你的内存不足的话，可以直接加载量化后的模型，INT4 量化后的模型仅需大概 5.2GB 的内存：
```python
# INT8 量化的模型将"THUDM/chatglm-6b-int4"改为"THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).half().cuda()
```
量化模型的参数文件也可以从[这里](https://cloud.tsinghua.edu.cn/d/674208019e314311ab5c/)手动下载。

### CPU 部署
如果你没有 GPU 硬件的话，也可以在 CPU 上进行推理，但是推理速度会更慢。使用方法如下（需要大概 32GB 内存）
```python
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).float()
```

如果你的内存不足，可以直接加载量化后的模型：
```python
# INT8 量化的模型将"THUDM/chatglm-6b-int4"改为"THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4",trust_remote_code=True).float()
```

如果遇到了报错 `Could not find module 'nvcuda.dll'` 或者 `RuntimeError: Unknown platform: darwin` (MacOS) ，请[从本地加载模型](README.md#从本地加载模型)

### Mac 部署
对于搭载了 Apple Silicon 或者 AMD GPU 的Mac，可以使用 MPS 后端来在 GPU 上运行 ChatGLM-6B。需要参考 Apple 的 [官方说明](https://developer.apple.com/metal/pytorch) 安装 PyTorch-Nightly（正确的版本号应该是2.1.0.dev2023xxxx，而不是2.0.0）。

目前在 MacOS 上只支持[从本地加载模型](README.md#从本地加载模型)。将代码中的模型加载改为从本地加载，并使用 mps 后端：
```python
model = AutoModel.from_pretrained("your local path", trust_remote_code=True).half().to('mps')
```

加载半精度的 ChatGLM-6B 模型需要大概 13GB 内存。内存较小的机器（比如 16GB 内存的 MacBook Pro），在空余内存不足的情况下会使用硬盘上的虚拟内存，导致推理速度严重变慢。此时可以使用量化后的模型如 chatglm-6b-int4。因为 GPU 上量化的 kernel 是使用 CUDA 编写的，因此无法在 MacOS 上使用，只能使用 CPU 进行推理。
```python
# INT8 量化的模型将"THUDM/chatglm-6b-int4"改为"THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4",trust_remote_code=True).float()
```
为了充分使用 CPU 并行，还需要[单独安装 OpenMP](FAQ.md#q1)。

### 多卡部署
如果你有多张 GPU，但是每张 GPU 的显存大小都不足以容纳完整的模型，那么可以将模型切分在多张GPU上。示例代码如下：
```python
import ChatGLM6Bpkg

model = ChatGLM6Bpkg.load_model_on_gpus("THUDM/chatglm-6b", num_gpus=2)
```
即可将模型部署到两张 GPU 上进行推理。你可以将 `num_gpus` 改为你希望使用的 GPU 数。默认是均匀切分的，你也可以传入 `device_map` 参数来自己指定。 

## 高效参数微调
本项目实现了对于 ChatGLM-6B 模型基于 [P-Tuning v2](https://github.com/THUDM/P-tuning-v2) 的微调。P-Tuning v2 将需要微调的参数量减少到原来的 0.1%，再通过模型量化、Gradient Checkpoint 等方法，最低只需要 7GB 显存即可运行。

下面以 [ADGEN](https://aclanthology.org/D19-1321.pdf) (广告生成) 数据集为例介绍代码的使用方法。

### 下载数据集

ADGEN 数据集任务为根据输入（content）生成一段广告词（summary）。

```json
{
    "content": "类型#上衣*版型#宽松*版型#显瘦*图案#线条*衣样式#衬衫*衣袖型#泡泡袖*衣款式#抽绳",
    "summary": "这件衬衫的款式非常的宽松，利落的线条可以很好的隐藏身材上的小缺点，穿在身上有着很好的显瘦效果。领口装饰了一个可爱的抽绳，漂亮的绳结展现出了十足的个性，配合时尚的泡泡袖型，尽显女性甜美可爱的气息。"
}
```

从 [Google Drive](https://drive.google.com/file/d/13_vf0xRTQsyneRKdD1bZIr93vBGOczrk/view?usp=sharing) 或者 [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/b3f119a008264b1cabd1/?dl=1) 下载处理好的 ADGEN 数据集，将解压后的 `AdvertiseGen` 目录放到当前目录下。

### 训练

示例代码如下：

```python
import ChatGLM6Bpkg

ChatGLM6Bpkg.ptuning.ptuning(
    do_train=True,
    train_file="AdvertiseGen/train.json",
    validation_file="AdvertiseGen/dev.json",
    prompt_column="content",
    response_column="summary",
    overwrite_cache=True,
    model_name_or_path="THUDM/chatglm-6b",
    output_dir="output/adgen-chatglm-6b-pt-128-2e-2",
    overwrite_output_dir=True,
    max_source_length=64,
    max_target_length=64,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=16,
    predict_with_generate=True,
    max_steps=3000,
    logging_steps=10,
    save_steps=100,
    learning_rate=2e-2,
    pre_seq_len=128,
    quantization_bit=4
)
```

`pre_seq_len` 和 `learning_rate` 分别是 soft prompt 长度和训练的学习率，可以进行调节以取得最佳的效果。P-Tuning-v2 方法会冻结全部的模型参数，可通过调整 `quantization_bit` 来被原始模型的量化等级，不加此选项则为 FP16 精度加载。

在默认配置 `quantization_bit=4`、`per_device_train_batch_size=1`、`gradient_accumulation_steps=16` 下，INT4 的模型参数被冻结，一次训练迭代会以 1 的批处理大小进行 16 次累加的前后向传播，等效为 16 的总批处理大小，此时最低只需 6.7G 显存。若想在同等批处理大小下提升训练效率，可在二者乘积不变的情况下，加大 `per_device_train_batch_size` 的值，但也会带来更多的显存消耗，请根据实际情况酌情调整。

如果你想要[从本地加载模型](../README_en.md#load-the-model-locally)，可以将上述代码中的 `THUDM/chatglm-6b` 改为你本地的模型路径。

### 推理

在 P-tuning v2 训练时模型只保存 PrefixEncoder 部分的参数，所以在推理时需要同时加载原 ChatGLM-6B 模型以及 PrefixEncoder 的权重，示例代码如下：

```python
import ChatGLM6Bpkg

ChatGLM6Bpkg.ptuning.ptuning(
    do_predict=True,
    validation_file="AdvertiseGen/dev.json",
    test_file="AdvertiseGen/dev.json",
    overwrite_cache=True,
    prompt_column="content",
    response_column="summary",
    model_name_or_path="THUDM/chatglm-6b",
    ptuning_checkpoint="./output/adgen-chatglm-6b-pt-128-2e-2/checkpoint-100",
    output_dir="./output/adgen-chatglm-6b-pt-128-2e-2",
    overwrite_output_dir=True,
    max_source_length=64,
    max_target_length=64,
    per_device_eval_batch_size=1,
    predict_with_generate=True,
    pre_seq_len=128,
    quantization_bit=4
)
```

其中，`model_name_or_path`是原 ChatGLM-6B 模型的路径，`ptuning_checkpoint`是 PrefixEncoder 的权重路径。

仍然兼容旧版全参保存的 Checkpoint，只需要设定 `model_name_or_path`为训练后模型的权重路径：

```python
model_name_or_path=$CHECKPOINT_PATH
```

评测指标为中文 Rouge score 和 BLEU-4。生成的结果保存在
`./output/adgen-chatglm-6b-pt-128-2e-2/generated_predictions.txt`。

### 模型加载

在 P-tuning v2 训练后，可通过如下方式加载模型（原 ChatGLM-6B 模型以及 PrefixEncoder 的权重）：

```python
import ChatGLM6Bpkg

tokenizer, config, model = ChatGLM6Bpkg.ptuning.load_ptuning_checkpoint(
        model_name_or_path="THUDM/chatglm-6b",
        ptuning_checkpoint="./output/adgen-chatglm-6b-pt-128-2e-2/checkpoint-100",
        pre_seq_len=128,
        quantization_bit=4
    )
model = model.cuda()
model = model.eval()
ChatGLM6Bpkg.launch_web_demo(model=model, tokenizer=tokenizer)
```

## ChatGLM-6B 示例

以下是一些使用 `web_demo.py` 得到的示例截图。更多 ChatGLM-6B 的可能，等待你来探索发现！

<details><summary><b>自我认知</b></summary>

![](examples/self-introduction.png)

</details>

<details><summary><b>提纲写作</b></summary>

![](examples/blog-outline.png)

</details>

<details><summary><b>文案写作</b></summary>

![](examples/ad-writing-2.png)

![](examples/comments-writing.png)

</details>

<details><summary><b>邮件写作助手</b></summary>

![](examples/email-writing-1.png)

![](examples/email-writing-2.png)

</details>

<details><summary><b>信息抽取</b></summary>

![](examples/information-extraction.png)

</details>

<details><summary><b>角色扮演</b></summary>

![](examples/role-play.png)

</details>

<details><summary><b>评论比较</b></summary>

![](examples/sport.png)

</details>

<details><summary><b>旅游向导</b></summary>

![](examples/tour-guide.png)

</details>

## 局限性

由于 ChatGLM-6B 的小规模，其能力仍然有许多局限性。以下是我们目前发现的一些问题：

- 模型容量较小：6B 的小容量，决定了其相对较弱的模型记忆和语言能力。在面对许多事实性知识任务时，ChatGLM-6B 可能会生成不正确的信息；它也不擅长逻辑类问题（如数学、编程）的解答。
    <details><summary><b>点击查看例子</b></summary>

    ![](limitations/factual_error.png)

    ![](limitations/math_error.png)

    </details>

- 产生有害说明或有偏见的内容：ChatGLM-6B 只是一个初步与人类意图对齐的语言模型，可能会生成有害、有偏见的内容。（内容可能具有冒犯性，此处不展示）

- 英文能力不足：ChatGLM-6B 训练时使用的指示/回答大部分都是中文的，仅有极小一部分英文内容。因此，如果输入英文指示，回复的质量远不如中文，甚至与中文指示下的内容矛盾，并且出现中英夹杂的情况。

- 易被误导，对话能力较弱：ChatGLM-6B 对话能力还比较弱，而且 “自我认知” 存在问题，并很容易被误导并产生错误的言论。例如当前版本的模型在被误导的情况下，会在自我认知上发生偏差。
    <details><summary><b>点击查看例子</b></summary>

    ![](limitations/self-confusion_google.jpg)

    ![](limitations/self-confusion_openai.jpg)

    ![](limitations/self-confusion_tencent.jpg)

    </details>

## 协议

本项目的代码依照 [Apache-2.0](LICENSE) 协议开源，ChatGLM-6B 模型的权重的使用则需要遵循 [Model License](MODEL_LICENSE)。

## 引用

如果你觉得我们的工作有帮助的话，请考虑引用下列论文

```
@article{zeng2022glm,
  title={Glm-130b: An open bilingual pre-trained model},
  author={Zeng, Aohan and Liu, Xiao and Du, Zhengxiao and Wang, Zihan and Lai, Hanyu and Ding, Ming and Yang, Zhuoyi and Xu, Yifan and Zheng, Wendi and Xia, Xiao and others},
  journal={arXiv preprint arXiv:2210.02414},
  year={2022}
}
```
```
@inproceedings{du2022glm,
  title={GLM: General Language Model Pretraining with Autoregressive Blank Infilling},
  author={Du, Zhengxiao and Qian, Yujie and Liu, Xiao and Ding, Ming and Qiu, Jiezhong and Yang, Zhilin and Tang, Jie},
  booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={320--335},
  year={2022}
}
```
