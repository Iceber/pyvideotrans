def openwin():
    from PySide6 import QtWidgets
    from pathlib import Path
    from pydub import AudioSegment
    from videotrans.configure.config import tr

    from videotrans.configure import config
    from videotrans.util import tools
    from videotrans.util.ListenVoice import ListenVoice
    def feed(d):
        if d == "ok":
            QtWidgets.QMessageBox.information(winobj, "ok", "Test Ok")
        else:
            tools.show_error(d)
        winobj.test.setText(tr('Test'))

    def test():
        url = winobj.api_url.text().strip()
        if not url.startswith('http'):
            url = 'http://' + url
        
        role = winobj.role.toPlainText().strip()
        if not role:
            return tools.show_error(tr('"The reference audio path name and the text corresponding to the reference audio must be filled in the settings"'))
        
        config.params["cosyvoice_url"] = url

        config.params["cosyvoice_role"] = role
        
        config.getset_params(config.params)
        
        for it in role.split("\n"):
            file=it.split('#')[0]
            file=config.ROOT_DIR+f'/f5-tts/{file}'
            if not Path(file).exists():
                return tools.show_error(tr("No reference audio {} exists",file))
            if not file.endswith('.wav'):
                return tools.show_error(tr('Please upload reference audio in wav format'))
            if len(AudioSegment.from_file(file))>=10000:
                return tools.show_error(tr('Please ensure that the reference audio duration is less than 10 seconds'))
        
        
        winobj.test.setText(tr('Testing...'))
        from videotrans import tts
        import time
        wk = ListenVoice(parent=winobj, queue_tts=[{
            "text": '你好啊我的朋友',
            "role": role.split("\n")[0].split('#')[0],
            "filename": config.TEMP_HOME + f"/{time.time()}-cosyvoice.wav",
            "tts_type": tts.COSYVOICE_TTS}],
                         language="zh",
                         tts_type=tts.COSYVOICE_TTS)
        wk.uito.connect(feed)
        wk.start()

    def save():
        url = winobj.api_url.text().strip()
        if not url.startswith('http'):
            url = 'http://' + url
        role = winobj.role.toPlainText().strip()
        if not role:
            return tools.show_error(tr("Please upload reference audio in wav format"))

        config.params["cosyvoice_url"] = url

        config.params["cosyvoice_role"] = role
        config.getset_params(config.params)
        tools.set_process(text='cosyvoice', type="refreshtts")

        winobj.close()

    from videotrans.component import CosyVoiceForm
    winobj = CosyVoiceForm()
    config.child_forms['cosyvoice'] = winobj
    if config.params["cosyvoice_url"]:
        winobj.api_url.setText(config.params["cosyvoice_url"])
    if config.params["cosyvoice_role"]:
        winobj.role.setPlainText(config.params["cosyvoice_role"])

    winobj.save.clicked.connect(save)
    winobj.test.clicked.connect(test)
    winobj.show()
