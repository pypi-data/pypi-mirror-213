from weathon.utils.json_utils import JsonUtils  # Json 操作相关工具类
from weathon.utils.label_studio_utils import LabelStudioUtils  # Label Studio 相关操作工具类
from weathon.utils.gpu_utils import GPUUtils  # GPU相关操作工具类
from weathon.utils.file_utils import FileUtils  # 文件工具类
from weathon.utils.file_utils import FileDecomposeUtils  # 文件解压缩工具类
from weathon.utils.union_find import UnionFind  # 并查集
from weathon.utils.ip_utils import IpUtils  # IP相关操作工具类
from weathon.utils.email_utils import EmailUtils  # 邮件相关操作工具类：发邮件
from weathon.utils.pdf_utils import PDFUtils  # pdf 相关操作工具类
# --------------------------------------------- constants ---------------------------------------------
from weathon.utils.constants import number2melody, emoji_face

# --------------------------------------------- string ---------------------------------------------
from weathon.utils.dictionary import Dictionary  # 词库
from weathon.utils.number_utils import NumberUtils  # 字符数值处理工具类
from weathon.utils.word_finder import AhoCorasick  # AC自动机:多模式匹配中的经典算法
from weathon.utils.word_finder import WordFinder  # 快速高效的多模匹配算法，允许使用levensthein进行模糊查询
from weathon.utils.word_discover import WordDiscoverer  # 新词发现 的工具包
from weathon.utils.keyword_extract import TFIDF, TextRank, Rake  # TFIDF, TextRank 进行关键词抽取
from weathon.utils.minjoin import MinJoin  # 文本召回方案
from weathon.utils.encrypt_utils import EncryptUtils  # 字符串加密工具类
from weathon.utils.char_utils import CharUtils  # 字符处理
from weathon.utils.string_utils import StringUtils  # 字符串处理工具类

# --------------------------------------------- deep learning ---------------------------------------------
# transformers 下载、权重转换相关
from weathon.utils.transformer_utils import TransformerUtils

# 模型训练相关
from weathon.utils.environment_utils import EnvironmentUtils  # 训练环境设置
from weathon.utils.sampler import ImbalancedDatasetSampler  # 模型采样
from weathon.utils.optimizer_utils import OptimizerUtils  # 优化器
from weathon.utils.schedule_utils import ScheduleUtils  # 优化器 scheduler
from weathon.utils.loss_utils import LossUtils  # 损失函数
from weathon.utils.attack import FGM, PGD  # 模型训练trick
from weathon.utils.ema import EMA  # 模型训练trick

# 模型集成相关
from weathon.utils.model_ensemble import ModelEnsemble  # 模型集成相关操作类

# 任务相关
from weathon.utils.ner_utils import NERUtils  # 命名实体识别

# --------------------------------------------- music utils ---------------------------------------------
# 人声 转 钢琴 :
#   1. 录音: Recorder,
#   2. 切分: OnsetFrameSplitter , 将一个文件拆分成多个起始帧
#   3. 转谱: NotePoltter

from weathon.utils.sound_recorder import Recorder
from weathon.utils.nextpow2 import next_pow2, get_next_power_2  # 辅助函数
from weathon.utils.noise_reduction import NoiseReduction        # 降噪
from weathon.utils.onset_frames_split import OnsetFrameSplitter # 端点检测
from weathon.utils.wav_utils import WaveProperties
from weathon.utils.sound_plot_utils import SoundPlotUtils
from weathon.utils.midi_detector import MIDIDetector            # 音符检测
from weathon.utils.note_plotter import NotePlotter              # 打谱
from weathon.utils.music import Music


# TODO: 2. 下载类 3. 性能分析类 4. 日志类
