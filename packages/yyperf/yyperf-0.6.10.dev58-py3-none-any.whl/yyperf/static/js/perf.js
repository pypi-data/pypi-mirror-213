window.LOCAL_URL = '/'; // http://localhost:17310/';
window.LOCAL_VERSION = '0.0.3'

window.vm = new Vue({
  el: '#perf',
  data: {
    error: '',
    params:{},
    selected_device:localStorage.selected_device || "",
    platform:'android',
    device_list:[],
    selected_app:localStorage.selected_app || "",
    package_list:[],
    perf_chart_data:[],
    colWidth: {"width": "100%", "height": "300px"},
    echart_object:{},
    echart_show:false,
    is_capture:false,
    capture_time: localStorage.capture_time || 24,
    timer:null,
    perfws:null,
    perf_filepath: null,
    file_name:"",
    interval_time:2,
    test_time: 0,
    fresh_interval_timer: null,
    fresh_test_timer: null,
    simple_perf_data: [],
    save_detail:localStorage.save_detail || false,
    divided_core_nums: false,
    all_install: localStorage.all_install || false,
    app_path: "",
    getting: false,
  },
  watch: {
    selected_device: function (newval) {
      if(this.selected_device.indexOf('iPhone')!==-1 || this.selected_device.indexOf('iOS')!==-1){
        this.platform = 'ios'
      }
      else if(this.selected_device.toLowerCase().indexOf("windows")!==-1){
        this.platform = "windows"
      }
      else{
        this.platform = 'android'
      }
      localStorage.setItem('platform', this.platform);
      localStorage.setItem('selected_device', newval);
      this.serial = this.selected_device.split('|')[1]
      if(newval){
        this.getPackageList()
      }
      this.initChartData()
    },
    selected_app:function (newval) {
      if(this.selected_app){
        localStorage.setItem('selected_app', newval);
        // console.log('selected app is '+newval)
        if(this.package_list.indexOf(this.selected_app)!==-1 && this.platform !== "windows"){
          this.startAPP(false)
        }
        this.echart_show = true
      }
      else{
        this.echart_show = false
      }
    },
    interval_time:function (newval){
      this.interval_time = newval
      if (this.interval_time>0 && this.perfws){
        let data = {
          platform:this.platform,
          device: this.selected_device,
          package: this.selected_app.toString(),
          action:'change',
          filename:this.file_name,
          intervaltime: this.interval_time
        }
        this.perfws.send(JSON.stringify(data))
      }
    },
    save_detail:function (newval){
      localStorage.setItem('save_detail', newval);
    },
    all_install:function (newval){
      localStorage.setItem('all_install', newval);
    },
    capture_time:function (newval){
      localStorage.setItem('capture_time', newval);
    },
  },
  created() {
    //this.colWidth['width'] = (window.outerWidth - 200) / 2 + "px"
  },
  mounted: function () {
    //var URL = window.URL || window.webkitURL;
    if(this.selected_device.indexOf('iPhone')!==-1 || this.selected_device.indexOf('iOS')!==-1){
      this.platform = 'ios'
    }
    else if(this.selected_device.toLowerCase().indexOf("windows")!==-1){
      this.platform = "windows"
    }
    else{
      this.platform = 'android'
    }
    this.params = GetRequestParam(window.location.search)
    console.log(this.params)
    this.platform = this.params['platform'] || this.platform
    this.echart_show = false
    this.divided_core_nums = false

    this.getDeviceList()
    this.getPackageList()
    this.initChartData()
    this.initPerfWebSocket()
  },
  methods: {
    setAvgResult: function (row , column){
      let result = -1
      Object.keys(row).forEach(key=>{
        if(row[key].title===column.label){
          result = row[key].avg_result
        }
      })
      return result
    },
    initChartData: function(){
      Highcharts.setOptions({
		global : {
		  useUTC : false
		}
      });
      this.echart_object = {}
      this.perf_chart_data = {
        app_cpu:{
          title:"App CPU利用率(%)",label:"app_cpu",
          ydata:[{data: [ ], name: "App CPU利用率(%)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        total_cpu:{
          title:"整体CPU利用率(%)",label:"total_cpu",
          ydata:[{data: [ ], name: "整体CPU利用率(%)", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        memory:{
          title:"内存使用量(MB)",label:"memory",
          ydata:[{data: [ ], name: "内存使用量(MB)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        virtual_mem:{
          title:"虚拟内存使用量(MB)",label:"virtual_mem",
          ydata:[{data: [ ], name: "虚拟内存使用量(MB)", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        threads:{
          title:"线程数",label:"threads",
          ydata:[{data: [ ], name: "线程数", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        gpu:{
          title:"GPU利用率(%)",label:"gpu",
          ydata:[{data: [ ], name: "GPU利用率(%)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        fps:{
          title:"帧率(FPS)",label:"fps",
          ydata:[{data: [ ], name: "帧率(FPS)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        traffic_down:{
          title:"下行流量(KB)",label:"traffic_down",
          ydata:[{data: [ ], name: "下行流量(KB)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        traffic_up:{
          title:"上行流量(KB)",label:"traffic_up",
          ydata:[{data: [ ], name: "上行流量(KB)", type: 'line'}],
          show:true,avg_result:"-1",sum:0,disable:false,count:0
        },
        mediasvrd_cpu:{
          title:"media CPU 占用(%)",label:"mediasvrd_cpu",
          ydata:[{data: [ ], name: "media CPU 占用(%)", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        },
        wakeups:{
          title:"唤醒次数",label:"wakeups",
          ydata:[{data: [], name: "唤醒次数", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        activity:{
          title:"Activities数量",label:"activity",
          ydata:[{data:[],name:"Activities数量",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        native_mem:{
          title:"Native使用量(MB)",label:"native_mem",
          ydata:[{data:[],name:"Native使用量(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        dalvik_mem:{
          title:"Dalvik使用量(MB)",label:"dalvik_mem",
          ydata:[{data:[],name:"Dalvik使用量(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        },
        rss:{
          title:"rss内存(MB)",label:"rss",
          ydata:[{data:[],name:"rss内存(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        },
        gpu_mem:{
          title:"GPU 显存使用量(MB)",label:"gpu_mem",
          ydata:[{data:[],name:"GPU 显存使用量(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        },
        battery: {
          title:"battery",label:"battery",
          ydata:[{data:[],name:"battery",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        },
        gpu_temperature:{
          title:"GPU温度(℃)",label:"gpu_temperature",
          ydata:[{data: [ ], name: "GPU温度(℃)", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        },
        handle_count:{
          title:"句柄数量",label:"handle_count",
          ydata:[{data: [ ], name: "句柄数量", type: 'line'}],
          show:false,avg_result:"-1",sum:0,disable:true,count:0
        }
      }
      if(this.platform==='ios'){
        this.perf_chart_data['activity'].show = false
        this.perf_chart_data['activity'].disable = true
        this.perf_chart_data['mediasvrd_cpu'].show = true
        this.perf_chart_data['mediasvrd_cpu'].disable = false
        this.perf_chart_data['native_mem'] = {
          title:"Real Mem使用量(MB)",label:"native_mem",
          ydata:[{data:[],name:"Real Mem使用量(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        }
        this.perf_chart_data['dalvik_mem'] = {
          title:"Real Private Mem使用量(MB)",label:"dalvik_mem",
          ydata:[{data:[],name:"Real Private Mem使用量(MB)",type:"line"}],
          show:false,avg_result:"-1",sum:0,disable:false,count:0
        }
      }
      else if(this.platform==='windows'){
        this.perf_chart_data['native_mem'].show = false
        this.perf_chart_data['dalvik_mem'].show = false
        this.perf_chart_data['native_mem'].disable = true
        this.perf_chart_data['dalvik_mem'].disable = true
        this.perf_chart_data['activity'].show = false
        this.perf_chart_data['activity'].disable = true
        this.perf_chart_data['handle_count'].disable = false
        this.perf_chart_data['gpu_temperature'].disable = false
        this.perf_chart_data['gpu_mem'].disable = false
        this.perf_chart_data['rss'].disable = false
        this.perf_chart_data['total_cpu'].disable = true
        this.perf_chart_data['wakeups'].disable = true
        this.perf_chart_data['fps'].disable = true
        this.perf_chart_data['handle_count'].show = true
        this.perf_chart_data['gpu_temperature'].show = false
        this.perf_chart_data['gpu_mem'].show = false
        this.perf_chart_data['rss'].show = false
        this.perf_chart_data['total_cpu'].show = false
        this.perf_chart_data['wakeups'].show = false
        this.perf_chart_data['fps'].show = false
      }
      this.simple_perf_data = [this.perf_chart_data]
    },
    getDeviceList: function(){
      this.getting = true
      $.ajax({
        url: LOCAL_URL + "api/v1/devices/list",
        type: "GET",
      })
      .done((ret) => {
          this.device_list = ret.data;
          for(let index=0;index<this.device_list.length;index++) {
            let device = this.device_list[index]
            if (device.indexOf(this.params['serial']) !== -1 || device === this.selected_device) {
              this.selected_device = device
              this.getPackageList()
              break
            }
          }
      })
      .fail((ret) => {
        this.showAjaxError(ret);
      }).always(() => {
          this.getting = false;
        })
    },
    getPackageList: function(){
      if(this.selected_device && this.device_list.indexOf(this.selected_device) !== -1){
        this.selected_app = "应用列表加载中，请稍后"
        $.ajax({
          url: LOCAL_URL + "api/v1/devices/"+ encodeURIComponent(this.selected_device) + "/packagelist",
          type: "GET",
        })
        .done((ret) => {
            this.package_list = ret.data;
            if(this.package_list.indexOf(this.selected_app) !== -1){
              this.startAPP(false)
            }
            else{
              this.selected_app = ""
            }
        })
        .fail((ret) => {
          this.showAjaxError(ret);
        })
      }
      else{
        this.package_list = []
        this.selected_app = "请先选择测试设备"
      }
    },
    startAPP: function(stop=true){
      if(this.selected_device && this.selected_app && this.platform!=="windows"){
        $.ajax({
          url: LOCAL_URL + "api/v1/devices/app",
          method: 'POST',
          data: {
            deviceinfo: this.selected_device,
            package: this.selected_app,
            stop: stop
          },
        })
        .fail((ret) => {
          this.showAjaxError(ret);
        })
      }
    },
    install: function (){
      if (!this.all_install && !this.selected_device)
        return
      if(this.app_path){
        document.getElementById("install").disabled = true
        $.ajax({
          url: LOCAL_URL + "api/v1/devices/install",
          method: 'POST',
          data: {
            deviceinfo: this.selected_device,
            all_install: this.all_install,
            app_path: this.app_path
          },
        }).done((ret) => {
          document.getElementById("install").disabled = false
        }).fail((ret) => {
          this.showAjaxError(ret);
        })
      }
    },
    startCapture: function(){
      let data = {
        platform:this.platform,
        device: this.selected_device,
        package: this.selected_app.toString(),
        action:'start',
        filename:this.file_name,
        intervaltime: this.interval_time,
        save_detail: this.save_detail,
        divided_core_nums: this.divided_core_nums,
        capture_time: this.capture_time
      }
      this.perf_filepath = null
      //点击后设置按钮不可用
      document.title = "性能工具-"+this.selected_device
      this.echart_show = false
      if (this.is_capture === false) {
        this.is_capture = true
        this.initChartData()
        document.getElementById("capture_start").innerHTML = "停止采集"
        if (this.selected_device && this.selected_app) {
          data['action'] = 'start'
        }
        if (this.fresh_interval_timer === null) {
          let _this = this
          this.fresh_interval_timer = setInterval(function (){
            _this.interval_time += 5
            if (_this.interval_time>120){
              _this.interval_time = 120
            }
          }, 60 * 60 * 1000)
        }
        if (this.fresh_test_timer === null){
          let _this = this
          this.fresh_test_timer = setInterval(function (){
            _this.test_time += 1
            document.getElementById("test_time").innerText = "当前已采集 " + _this.test_time + " 分钟"
          }, 60*1000)
        }
      } else {
        this.is_capture = false
        document.getElementById("capture_start").innerHTML = "开始采集"
        data['action'] = 'stop'
        this.test_time = 0
        if (this.fresh_interval_timer) {
          clearInterval(this.fresh_interval_timer)
          this.fresh_interval_timer = null
        }
        if (this.fresh_test_timer) {
          clearInterval(this.fresh_test_timer)
          this.fresh_test_timer = null
        }
      }
      if(this.perfws){
        this.perfws.send(JSON.stringify(data))
      }
    },
    getEchartOption: function(title, label){
      return {
        rangeSelector: {
          buttons: [],
          inputEnabled: false,
        },
        chart: {
          //alignTicks: false,
          //zoomType: 'x'
        },
        credits: {
          enabled: false
        },
        title: {
          text: title
        },
        yAxis: {
		  title: {
		    text: label
          },
          opposite:false,
		},
        exporting: {
          enabled: false
        },
        legend: false,
        series: [
          {
            name:title,
            type: "spline",
            data:[],
            tooltip: {
              pointFormat: '{point.series.name}:{point.y}'
            },
            dataGrouping: {
                approximation: 'average',
                units: [[
                    'minute',
                    [1]
                ]]
            },
          }
        ]
      }
    },
    initPerfWebSocket() {
      // 初始化变量
      const ws = this.perfws = new WebSocket("ws://" + location.host + "/ws/v1/captrue")
      ws.onopen = () => {
        console.log("websocket opened")
      }
      ws.onmessage = (message) => {
        //数据返回，设置按钮可用
        this.echart_show = true
        const data = JSON.parse(message.data)
        if(data.hasOwnProperty('filepath')){
          this.perf_filepath = data['filepath']
        }
        else if(data.hasOwnProperty('dumphprof')){
          document.getElementById("dump_hprof").disabled = false
        }
        else {
          for (let index = 0; index < data.length; index++) {
            let perfdata = data[index]
            Object.keys(this.perf_chart_data).forEach(key => {
              if (this.perf_chart_data[key].show) {
                let value = parseFloat(perfdata[key])
                this.perf_chart_data[key].show = value >= 0;
                this.perf_chart_data[key].sum += value
                this.perf_chart_data[key].count += 1
                this.perf_chart_data[key].avg_result = (this.perf_chart_data[key].sum / this.perf_chart_data[key].count).toFixed(2)

                let chart_data = this.perf_chart_data[key]
                if(!this.echart_object[chart_data.label]){
                  let chart_option = this.getEchartOption(chart_data.title,chart_data.label)
                  this.echart_object[chart_data.label] = Highcharts.stockChart(chart_data.label, chart_option)
                }
                else{
                  let time = (new Date()).getTime()
                  this.echart_object[chart_data.label].series[0].addPoint([time,value],false)
                  this.echart_object[chart_data.label].redraw(false)
                }
              }
            })
          }
        }
      }
      ws.onclose = () => {
        this.perfws = null
        console.log("websocket closed")
      }
    },

    dumpHprof: function () {
      if (this.selected_device && this.selected_app && this.is_capture && this.perfws){
        document.getElementById("dump_hprof").disabled = true
        let data = {
          platform:this.platform,
          device: this.selected_device,
          package: this.selected_app.toString(),
          action:'dumphprof',
          filename:this.file_name,
          intervaltime: this.interval_time
        }
        this.perfws.send(JSON.stringify(data))
      }
    },

    exportData: function (){
      if(this.perf_filepath){
        let url = LOCAL_URL + "api/v1/export/"+encodeURIComponent(this.perf_filepath) + "/" + encodeURIComponent(this.file_name)
        window.open(url)
      }
    },

    clearData: function(){
      this.echart_show = true;
      this.perf_chart_data = {}
      this.initChartData()
    },
    dateFormat: function(fmt, date) {
      let ret
      const opt = {
          "Y+": date.getFullYear().toString(),        // 年
          "m+": (date.getMonth() + 1).toString(),     // 月
          "d+": date.getDate().toString(),            // 日
          "H+": date.getHours().toString(),           // 时
          "M+": date.getMinutes().toString(),         // 分
          "S+": date.getSeconds().toString()          // 秒
          // 有其他格式化字符需求可以继续添加，必须转化成字符串
      }
      for (let k in opt) {
          ret = new RegExp("(" + k + ")").exec(fmt);
          if (ret) {
              fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
          }
      }
      return fmt
    },
    showError: function (error) {
      this.loading = false;
      this.error = error;
      $('.modal').modal('show');
    },
    showAjaxError: function (ret) {
      if (ret.responseJSON && ret.responseJSON.description) {
        this.showError(ret.responseJSON.description);
      } else {
        this.showError("<p>Local server not started, start with</p><pre>$ python -m weditor</pre>");
      }
    },
  }
})