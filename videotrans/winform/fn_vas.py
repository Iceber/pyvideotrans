

def format_milliseconds(milliseconds):
    """
    将毫秒数转换为 HH:mm:ss.zz 格式的字符串。

    Args:
        milliseconds (int): 毫秒数。

    Returns:
        str: 格式化后的字符串，格式为 HH:mm:ss.zz。
    """
    if not isinstance(milliseconds, int):
        raise TypeError("毫秒数必须是整数")
    if milliseconds < 0:
        raise ValueError("毫秒数必须是非负整数")

    seconds = milliseconds / 1000

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds_part = int((seconds * 1000) % 1000) // 10  # 保留两位

    # 格式化为两位数字字符串
    formatted_hours = f"{int(hours):02}"
    formatted_minutes = f"{int(minutes):02}"
    formatted_seconds = f"{int(seconds):02}"
    formatted_milliseconds = f"{milliseconds_part:02}"

    return f"{formatted_hours}:{formatted_minutes}:{formatted_seconds}.{formatted_milliseconds}"


# 视频 字幕 音频 合并
def openwin():
    from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QCheckBox,QFileDialog
    import shutil
    import json
    import os
    from videotrans.configure.config import tr
    import time
    from pathlib import Path
    from PySide6.QtCore import QThread, Signal, QUrl,QTimer
    from PySide6.QtGui import QDesktopServices

    from videotrans.configure import config
    from videotrans.util import tools

    RESULT_DIR = config.HOME_DIR + "/vas"

    from videotrans.translator import LANGNAME_DICT,get_subtitle_code

    class CompThread(QThread):
        uito = Signal(str)

        def __init__(self, *, parent=None, video=None, audio=None, srt=None, saveraw=True, is_soft=False, language=None,
                     maxlen=30, audio_process=0,remain_hr=False):
            super().__init__(parent=parent)
            self.winobj=parent
            self.video = video
            self.audio = audio
            self.srt = srt
            self.saveraw = saveraw
            self.is_soft = is_soft
            self.language = language
            self.maxlen = maxlen
            self.remain_hr=remain_hr
            self.audio_process = audio_process
            self.file = f'{RESULT_DIR}/{Path(self.video).stem}-{int(time.time())}.mp4'
            self.video_info = tools.get_video_info(self.video)
            self.video_time = tools.get_video_duration(self.video)
            self.is_end=False

        def post(self, type='logs', text=''):
            self.uito.emit(json.dumps({"type": type, "text": text}))

        #
        def hebing_pro(self, protxt, video_time=0):
            percent = 0
            while 1:
                if percent >= 100 or self.is_end:
                    return
                if not os.path.exists(protxt):
                    time.sleep(1)
                    continue
                try:
                    content = Path(protxt).read_text(encoding='utf-8').strip().split("\n")
                except (OSError,ValueError,AttributeError):
                    continue

                if content[-1] == 'progress=end':
                    return
                idx = len(content) - 1
                end_time = "00:00:00"
                while idx > 0:
                    if content[idx].startswith('out_time='):
                        end_time = content[idx].split('=')[1].strip()
                        break
                    idx -= 1
                try:
                    h, m, s = end_time.split(':')
                    tmp1 = round((int(h) * 3600000 + int(m) * 60000 + int(s[:2]) * 1000) / video_time, 2)
                except ValueError:
                    tmp1 = 0
                if percent + tmp1 < 99.9:
                    percent += tmp1
                percent=min(percent,99)
                self.post(type='jd', text=f'{percent:.2f}%')
            time.sleep(1)

        def _save_set(self):
            # 保存各项配置
             ysphb = {
                "ysphb_replace": self.winobj.ysphb_replace.isChecked(),
                "audio_process": self.winobj.audio_process.currentIndex(),
                "ysphb_maxlen": self.winobj.ysphb_maxlen.text(),
                "remain_hr": self.winobj.remain_hr.isChecked(),
                "ysphb_issoft": self.winobj.ysphb_issoft.isChecked(),
                "language":  self.winobj.language.currentIndex(),
                "position": self.winobj.position.currentIndex(),
                "marginL":  self.winobj.marginL.text(),
                "marginV": self.winobj.marginV.text(),
                "marginR": self.winobj.marginR.text(),
                "outline": self.winobj.outline.text(),
                "shadow": self.winobj.shadow.text(),
                "font_size_edit": self.winobj.font_size_edit.text(),
                "ysphb_borderstyle": self.winobj.ysphb_borderstyle.isChecked(),
                "selected_font": self.winobj.selected_font.family(),
                "selected_color":   self.winobj.qcolor_to_ass_color(self.winobj.selected_color, type='fc'),
                "selected_backgroundcolor": self.winobj.qcolor_to_ass_color(self.winobj.selected_backgroundcolor, type='bg'),
                "selected_bordercolor": self.winobj.qcolor_to_ass_color(self.winobj.selected_bordercolor, type='bg')
             }
             with open(f'{config.ROOT_DIR}/videotrans/vas.json','w',encoding='utf-8') as f:
                import json
                f.write(json.dumps(ysphb,ensure_ascii=False))
             return ysphb

        def run(self):
            from pydub import AudioSegment
            try:
                # 有新的需要插入的音频，才涉及到 保留原声音 、 截断、加速、定格、声音混合等，才需要处理音频、分离无声视频
                if self.audio:
                    ext = self.audio.split('.')[-1].lower()
                    audio_time = int(tools.get_audio_time(self.audio) * 1000)

                    tmp_audio = config.TEMP_HOME + f"/{time.time()}-{Path(self.audio).name}"
                    # 如果音频时长小于视频，则音频直接添加末尾静音
                    if audio_time<self.video_time:
                        audio_data = AudioSegment.from_file(self.audio,format='mp4' if ext=='m4a' else ext)+AudioSegment.silent(duration=self.video_time-audio_time)
                        audio_data.export(self.audio,format="mp4" if ext=='m4a' else ext)
                    elif audio_time > self.video_time and self.audio_process == 0:
                        # 截断音频
                        tools.runffmpeg(
                            ['-y', '-i', self.audio, '-ss', '00:00:00.000', '-t', str(self.video_time / 1000), tmp_audio])
                        self.audio = tmp_audio
                    elif audio_time > self.video_time and self.audio_process == 1:
                        # 加速音频
                        tools.precise_speed_up_audio(file_path=self.audio, out=tmp_audio, target_duration_ms=self.video_time)
                        self.audio = tmp_audio
                    print(f'未混合前但加速 或截断后的音频 {self.audio=}')
                    # 需要保留原视频中声音，则需要混合 self.audio 和视频声音
                    if self.saveraw and  self.video_info['streams_audio']:
                        tmp_mp4a = config.TEMP_HOME + f"/{time.time()}-fromvideo.wav"
                        end_m4a = config.TEMP_HOME + f"/{time.time()}.m4a"
                        # 先取出来视频中的音频为 wav
                        tools.runffmpeg([
                            '-y',
                            '-i',
                            os.path.normpath(self.video),
                            "-vn",
                            tmp_mp4a]
                        )
                        # audio_process=0截断 1=音频加速 2=视频定格
                        # 音频时长小于视频时长时无需考虑，简单为音频加静音即可
                        # 需考虑音频时长大于视频时长,并且 2 需定格视频时，要延长视频中声音==self.audio
                        if audio_time > self.video_time and self.audio_process == 2:
                            audio_data = AudioSegment.from_file(tmp_mp4a)+AudioSegment.silent(duration=audio_time-self.video_time)
                            audio_data.export(tmp_mp4a,format="wav")

                        # 到此处，新插入的音频 self.audio和视频剥离的音频，时长已经一致了
                        # 开始混合 2个音频
                        tools.runffmpeg([
                            '-y',
                            '-i',
                            os.path.normpath(tmp_mp4a),
                            '-i',
                            os.path.normpath(self.audio),
                            '-filter_complex',
                            "[0:a][1:a]amix=inputs=2:duration=longest[aout]",
                            '-map',
                            '[aout]',
                            '-ac',
                            '2', end_m4a])
                        # 混合后新音频
                        self.audio = end_m4a
                        print(f'混合后新音频 {self.audio=}')
                        # 混合后音频时长，当大于视频时长，并且 audio_process == 2 需定格视频
                        audio_time = int(tools.get_audio_time(self.audio) * 1000)

                    # audio_process=0截断 1=音频加速 2=视频定格
                    # 如果存在 self.audio ，则无论是否保留原视频中声音，此时都已处理好，直接替换 视频中声音
                    # 分离出无声视频进行定格操作
                    cmd = [
                            '-y',
                            '-i',
                            self.video
                    ]
                    novoice_mp4 = config.TEMP_HOME + f"/{time.time()}-novice.mp4"
                    if self.audio_process == 2 and  audio_time >self.video_time:
                        # 如果定格视频并且音频时长大于视频时长
                        sec = max((audio_time - self.video_time) / 1000,1)
                        cmd += [
                            '-vf',
                            f'tpad=stop_mode=clone:stop_duration={sec}'
                        ]
                    cmd+=[
                        "-an",
                        '-c:v',
                        'libx264',
                        novoice_mp4
                    ]
                    print(f'{novoice_mp4=}')
                    tools.runffmpeg(cmd)

                    # 视频音频合并
                    audiovideoend_mp4 = config.TEMP_HOME + f"/{time.time()}-audiovideoend.mp4"
                    tools.runffmpeg([
                        '-y',
                        '-i',
                        novoice_mp4,
                        '-i',
                        os.path.normpath(self.audio),
                        '-c:v',
                        'copy',
                        "-c:a",
                        "aac",
                        audiovideoend_mp4
                    ])
                    print(f'222222 {self.video=}')
                    # 不存在字幕，则结束了
                    if not self.srt:
                        self.post(type='ok', text=self.file)
                        self.is_end=True
                        shutil.copy2(audiovideoend_mp4,self.file)
                        self._save_set()
                        return
                    self.video=audiovideoend_mp4
                # 软字幕
                os.chdir(os.path.dirname(self.srt))
                protxt = config.TEMP_HOME + f'/jd{time.time()}.txt'
                cmd = [
                    '-y',
                    "-progress",
                    protxt,
                    '-i',
                    self.video,
                ]
                if self.is_soft and self.language:
                    # 软字幕
                    subtitle_language = get_subtitle_code( show_target=self.language)
                    cmd+=[
                        '-i',
                        os.path.basename(self.srt),
                        '-c:v',
                        'copy',
                        "-c:s",
                        "mov_text",
                        "-metadata:s:s:0",
                        f"language={subtitle_language}",
                        self.file
                    ]
                    self._save_set()
                else:
                    # 硬字幕
                    sublist = tools.get_subtitle_from_srt(self.srt, is_file=True)
                    srt_string = ''
                    for i, it in enumerate(sublist):
                        if self.remain_hr:
                            txt_list = []
                            for txt_line in it['text'].strip().split("\n"):
                                txt_list.append(tools.textwrap(txt_line.strip(), self.maxlen))
                            tmp = "\n".join(txt_list)
                        else:
                            tmp = tools.textwrap(it['text'].strip(), self.maxlen)
                        srt_string += f"{it['line']}\n{it['time']}\n{tmp.strip()}\n\n"
                    tmpsrt = config.TEMP_HOME + f"/vas-{time.time()}.srt"
                    with Path(tmpsrt).open('w', encoding='utf-8') as f:
                        f.write(srt_string.strip())
                    assfile = config.TEMP_HOME + f"/vasrt{time.time()}.ass"
                    self.save_ass(tmpsrt, assfile)
                    os.chdir(config.TEMP_HOME)
                    cmd += [
                        '-c:v',
                        'libx264',
                        '-vf',
                        f"subtitles={os.path.basename(assfile)}:charenc=utf-8",
                        '-crf',
                        f'{config.settings.get("crf",23)}',
                        '-preset',
                        config.settings.get('preset','fast'),
                        self.file
                    ]
                from videotrans.task.simple_runnable_qt import run_in_threadpool
                run_in_threadpool(self.hebing_pro,protxt,self.video_time)
                tools.runffmpeg(cmd)
                self.post(type='ok', text=self.file)
                self.is_end=True
            except Exception as e:
                from videotrans.configure._except import get_msg_from_except
                self.post(type='error', text=get_msg_from_except(e))


        def save_ass(self,file_path, ass_file):
            ysphb=self._save_set()
            with open(ass_file, 'w', encoding='utf-8') as file:
                # 写入 ASS 文件的头部信息
                stem = Path(file_path).stem
                file.write("[Script Info]\n")
                file.write(f"Title: {stem}\n")
                file.write(f"Original Script: {stem}\n")
                file.write("ScriptType: v4.00+\n")
                file.write("PlayResX: 384\nPlayResY: 288\n")
                file.write("ScaledBorderAndShadow: yes\n")
                file.write("YCbCr Matrix: None\n")
                file.write("\n[V4+ Styles]\n")
                file.write(
                    f"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")

                align = config.POSTION_ASS_INDEX[ysphb["position"]]
                # 不同字幕渲染器为差异兼容
                if ysphb["ysphb_borderstyle"]:
                    ysphb["selected_bordercolor"] = ysphb["selected_backgroundcolor"]


                file.write(f'Style: Default,{ysphb["selected_font"]},{ysphb["font_size_edit"]},{ysphb["selected_color"]},{ysphb["selected_color"]},{ysphb["selected_bordercolor"]},{ysphb["selected_backgroundcolor"]},{int(self.winobj.selected_font.bold())},{int(self.winobj.selected_font.italic())},0,0,100,100,0,0,{3 if ysphb["ysphb_borderstyle"] else 1},{ysphb["outline"]},{ysphb["shadow"]},{align},{ysphb["marginL"]},{ysphb["marginR"]},{ysphb["marginV"]},1\n')
                file.write("\n[Events]\n")

                file.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
                srt_list = tools.get_subtitle_from_srt(file_path, is_file=True)
                for it in srt_list:
                    start_str = format_milliseconds(it['start_time'])
                    end_str = format_milliseconds(it['end_time'])
                    text = it['text'].replace("\n", "\\N")
                    file.write(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{text}\n")
            return True

    def feed(d):
        if winobj.has_done:
            return
        d = json.loads(d)
        if d['type'] == "error":
            winobj.has_done = True
            tools.show_error(d['text'])
            winobj.ysphb_startbtn.setText(tr("start operate"))
            winobj.ysphb_startbtn.setDisabled(False)
            winobj.ysphb_opendir.setDisabled(False)
        elif d['type'] == 'jd':
            winobj.ysphb_startbtn.setText(d['text'])
        elif d['type'] == 'logs':
            winobj.ysphb_startbtn.setText(d['text'])
        elif d['type'] == 'ok':
            winobj.has_done = True
            winobj.ysphb_startbtn.setText(tr('zhixingwc'))
            winobj.ysphb_startbtn.setDisabled(False)
            winobj.ysphb_out.setText(d['text'])
            winobj.ysphb_opendir.setDisabled(False)

    def get_file(type='video'):
        fname = None
        if type == 'video':
            format_str = " ".join(['*.' + f for f in config.VIDEO_EXTS])
            fname, _ = QFileDialog.getOpenFileName(winobj, 'Select Video', config.params.get('last_opendir',''),
                                                   f"Video files({format_str})")
        elif type == 'wav':
            format_str = " ".join(['*.' + f for f in config.AUDIO_EXITS])
            fname, _ = QFileDialog.getOpenFileName(winobj, 'Select Audio', config.params.get('last_opendir',''),
                                                   f"Audio files({format_str})")
        elif type == 'srt':
            fname, _ = QFileDialog.getOpenFileName(winobj, 'Select SRT', config.params.get('last_opendir',''),
                                                   "Srt files(*.srt)")

        if not fname:
            return

        if type == 'video':
            winobj.ysphb_videoinput.setText(fname.replace('\\', '/'))
        if type == 'wav':
            winobj.ysphb_wavinput.setText(fname.replace('\\', '/'))
        if type == 'srt':
            winobj.ysphb_srtinput.setText(fname.replace('\\', '/'))
        config.params['last_opendir'] = os.path.dirname(fname)
        config.getset_params(config.params)

    def start():
        winobj.has_done = False
        # 开始处理分离，判断是否选择了源文件
        video = winobj.ysphb_videoinput.text()
        audio = winobj.ysphb_wavinput.text()
        srt = winobj.ysphb_srtinput.text()
        is_soft = winobj.ysphb_issoft.isChecked()
        language = winobj.language.currentText()
        saveraw = winobj.ysphb_replace.isChecked()
        maxlen = 20
        try:
            maxlen = int(winobj.ysphb_maxlen.text())
        except ValueError:
            pass
        if not video:
            tools.show_error(tr("Video must be selected"))
            return
        if not audio and not srt:
            tools.show_error(
                tr("Choose at least one for audio and video"))
            return

        winobj.ysphb_startbtn.setText(
            tr("In Progress..."))
        winobj.ysphb_startbtn.setDisabled(True)
        winobj.ysphb_opendir.setDisabled(True)
        task = CompThread(parent=winobj,
                          video=video,
                          audio=audio if audio else None,
                          srt=srt if srt else None,
                          saveraw=saveraw,
                          is_soft=is_soft,
                          language=language,
                          maxlen=maxlen,
                          audio_process=winobj.audio_process.currentIndex(),
                          remain_hr=winobj.remain_hr.isChecked()
                          )
        task.uito.connect(feed)
        task.start()

    def opendir():
        QDesktopServices.openUrl(QUrl.fromLocalFile(RESULT_DIR))

    from videotrans.component.set_form import VASForm



    winobj = VASForm()
    config.child_forms['fn_vas'] = winobj
    winobj.show()
    def _init_ui():
        Path(RESULT_DIR).mkdir(exist_ok=True)
        winobj.ysphb_selectvideo.clicked.connect(lambda: get_file('video'))
        winobj.ysphb_selectwav.clicked.connect(lambda: get_file('wav'))
        winobj.ysphb_selectsrt.clicked.connect(lambda: get_file('srt'))
        winobj.ysphb_startbtn.clicked.connect(start)
        winobj.ysphb_opendir.clicked.connect(opendir)
        winobj.language.addItems(list(LANGNAME_DICT.values()))
        # 初始化上次配置
        cfg_file=f'{config.ROOT_DIR}/videotrans/vas.json'
        if not Path(cfg_file).exists():
            return
        from PySide6.QtGui import QFont, QColor
        with open(cfg_file, 'r', encoding='utf-8') as f:
            import json
            try:
                ysphb=json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return
            for k,v in ysphb.items():
                if k=='font_size_edit':
                    continue
                if k=='selected_font':
                    winobj.selected_font = QFont(v, int(ysphb['font_size_edit']))  # 默认字体
                elif k == 'selected_color':
                    winobj.selected_color = QColor(ysphb[k].upper().replace('&H','#'))  # 默认颜色
                elif k == 'selected_backgroundcolor':
                    winobj.selected_backgroundcolor = QColor(ysphb[k].upper().replace('&H','#'))  # 默认颜色
                elif k == 'selected_bordercolor':
                    winobj.selected_bordercolor = QColor(ysphb[k].upper().replace('&H','#'))  # 默认颜色
                else:
                    widget = winobj.findChild(QWidget, k)
                    if isinstance(widget, QLineEdit):
                        widget.setText(str(v))
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentIndex(int(v))
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(v))
            winobj._setfont()
    QTimer.singleShot(10,_init_ui)
