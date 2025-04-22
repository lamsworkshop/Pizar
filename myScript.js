class PizarExtension {
  constructor(){
    this.connected = false;
  }

  connect(ip) {
    if (this.connected) return;
    this.ws = new WebSocket('ws://'+ip+':9001');
    this.dataReady = false;
    this.ws.onerror = () => { this.connected = false; }
    this.ws.onopen = () => { this.connected = true; }
    this.ws.onclose = () => { this.connected = false; }
    this.ws.onmessage = (event) => {
      this.dataReady = true;
      this.message = String(event.data);
      document.getElementById("read").disabled = false;
    }
  }

  replied() { return this.dataReady; }

  close() { if (this.connected) this.ws.close(); }

  led(state) { if (this.connected) this.ws.send("LED " + state[1]); }

  wheel(side, pwm) { if (this.connected) this.ws.send("WHL" + side[0] + pwm); }

  servo(num, angle) { if (this.connected) this.ws.send("SRV" + num + angle); }

  stop() { if (this.connected) this.ws.send("STP"); }

  read(device) {
    if (!this.connected) return;
    this.dataReady = false;
    this.ws.send("TRG" + device[0]);
  }

  getReading() {
    this.dataReady = false;
    return this.message;
  }

}

const pizar = new PizarExtension();

function request(device) {
  pizar.read(device);
  document.getElementById("read").disabled = true;
}

function read() {
  document.getElementById("read").disabled = true;
  document.getElementById("message").value = pizar.message;
}
