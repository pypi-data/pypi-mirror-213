import VueSocketIO from 'vue-socket.io';
import SocketIO from 'socket.io-client';

export default function (Vue) {
Vue.use(new VueSocketIO({
  debug: true,
  connection: SocketIO('http://localhost:17310', {
    withCredentials: true,
    extraHeaders: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
    }
  })
}));

}


