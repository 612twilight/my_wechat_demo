import jieba
import pkuseg
from tuning import tuning_reply
import re


def task_controller(task_input_str: str):
    if ":" in task_input_str or "：" in task_input_str:
        task_input_str = re.sub(r"：", ":", task_input_str)
        task = task_input_str.split(":")[0]
        input_str = "".join(task_input_str.split(":")[1:])
    else:
        task = "default"
        input_str = task_input_str
    if task in task_types:
        return task_types[task](input_str)
    else:
        return task_types["default"](input_str)


def word_seg_task(input_str):
    jieba_result = " ".join(jieba.cut(input_str))
    seg = pkuseg.pkuseg()  # 以默认配置加载模型
    text = " ".join(seg.cut(input_str))  # 进行分词
    return "jieba分词：" + jieba_result + "\npkuseg分词：" + text


def default_task(input_str):
    if "你是谁" in input_str:
        relpy_text = "我是月光如水的夏夜，融化冰雪的深情"
    elif "我是鸣夏" in input_str:
        relpy_text = "说啥都是爱你"
    else:
        relpy_text = tuning_reply(input_str)
    return relpy_text


task_types = {"分词": word_seg_task, "default": default_task}

if __name__ == '__main__':
    fenci_input = "分词:你是人间的四月天"
    # fenci_input = "我是鸣夏"
    # fenci_input = "你是谁"
    print(task_controller(fenci_input))
