<template>
  <div id="parent">
    <div>
      <el-row>
        <el-button type="primary" icon="el-icon-edit" circle @click="record()">record</el-button>
        <el-button type="success" icon="el-icon-check" circle @click="stop()">stop</el-button>
        <el-button type="info" icon="el-icon-message" circle @click="download()">translate</el-button>
        <el-button type="warning" icon="el-icon-star-off" circle @click="clear">clear</el-button>

      </el-row>
    </div>
    <div>
      <audio  controls :src="audio_src">
        您的浏览器不支持 audio 标签。
      </audio>
    </div>
    <div>
      <el-form>
        <el-form-item label="翻译结果">
          <el-input type="textarea" v-model="translate_result"></el-input>
        </el-form-item>
      </el-form>
    </div>

  </div>

</template>


<script>
  import Recorderx, {RECORDER_STATE, ENCODE_TYPE } from "recorderx";
  const rc = new Recorderx({
    recordable: true,
    sampleRate: 16000,
  });
  const axios = require('axios');

  export default {
    data () {
      return {
        isVoice: false,
        isFinished: false,
        audio_src:'',
        translate_result:'hello '
      }
    },
    methods: {
      // 开始录音
      record () {
        if (rc.state === RECORDER_STATE.READY) {
          rc.start()
                  .then(() => {
                    console.log('start recording');
                  })
                  .catch((error) => {
                    console.log('Recording failed.', error);
                  });
        }
      },

      //
      download () {
        var wav = rc.getRecord({
          encodeTo: ENCODE_TYPE.WAV,
          compressible: true
        });
        console.log(wav)
        this.upload(wav)
      },
      upload(param){
        const  that  = this
        that.translate_result = '正在翻译，请稍后.....'
        let formData = new FormData();
        formData.append("file", param);
        axios({
          method: 'post',
          url: 'https://qdhuazhiyao.cn/audio2text/uploadFile', //地址填写自己本地启动的 suc-web-audio 项目
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          data:formData
        }).then(function (res) {
          console.log(res)
          that.translate_result = res.data.message
        });
      },

      //  清空
      clear () {
        rc.clear();
        this.audio_src = ''
        this.translate_result = 'hello'
      },

      // 停止播放录音
      stop () {
        if (rc && rc.state === RECORDER_STATE.RECORDING) {
          rc.pause();
          this.audio_src = URL.createObjectURL(rc.getRecord({
            encodeTo: ENCODE_TYPE.WAV,
            compressible: true,
          }));
          console.log('pause recording');
        }
      }
    }
  }
</script>