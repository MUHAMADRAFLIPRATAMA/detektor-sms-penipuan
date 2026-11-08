from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from src.detector import predict

HTML = '''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Detektor Pesan Penipuan</title><style>*{box-sizing:border-box}body{margin:0;background:#f4f7fb;font:16px Arial;color:#182235}.wrap{max-width:850px;margin:48px auto;padding:20px}.card{background:white;border-radius:18px;padding:30px;box-shadow:0 12px 35px #19355d18}.tag{color:#2563eb;font-weight:bold}.sub{color:#64748b}textarea{width:100%;min-height:150px;border:1px solid #dbe3ef;border-radius:12px;padding:15px;font:inherit;resize:vertical}button{margin-top:15px;border:0;border-radius:10px;padding:13px 20px;background:#2563eb;color:white;font-weight:bold;cursor:pointer}button:hover{background:#1d4ed8}.result{display:none;margin-top:24px;padding:18px;border-radius:12px}.danger{display:block;background:#fee2e2;color:#991b1b}.safe{display:block;background:#dcfce7;color:#166534}.confidence{font-size:25px;font-weight:bold}.error{display:block;background:#fff7ed;color:#9a3412}</style></head><body><main class="wrap"><section class="card"><div class="tag">MACHINE LEARNING</div><h1>Detektor Pesan Penipuan</h1><p class="sub">Masukkan pesan SMS atau WhatsApp untuk diperiksa oleh model.</p><form id="form"><textarea id="message" placeholder="Contoh: Selamat Anda memenangkan hadiah..." required></textarea><br><button type="submit">Periksa Pesan</button></form><div id="result" class="result"></div></section></main><script>form.onsubmit=async e=>{e.preventDefault();let r=document.getElementById('result');r.className='result';r.textContent='Memeriksa...';r.style.display='block';let x=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:message.value})});let d=await x.json();if(!x.ok){r.className='result error';r.textContent=d.error;return}let scam=d.label==='PENIPUAN';r.className='result '+(scam?'danger':'safe');r.innerHTML='<strong>Hasil: '+d.label+'</strong><div class="confidence">'+(d.confidence*100).toFixed(2)+'%</div><div>Tingkat keyakinan model</div>'}</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def send(self, code, content, kind='text/html'):
        raw = content.encode(); self.send_response(code); self.send_header('Content-Type', kind+'; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path == '/': self.send(200, HTML)
        else: self.send(404, 'Not found', 'text/plain')
    def do_POST(self):
        if self.path != '/predict': return self.send(404, json.dumps({'error':'Not found'}), 'application/json')
        try:
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
            msg=str(data.get('message','')).strip()
            if not msg: raise ValueError('Pesan tidak boleh kosong.')
            self.send(200, json.dumps(predict(msg), ensure_ascii=False), 'application/json')
        except Exception as e: self.send(400, json.dumps({'error':str(e)}, ensure_ascii=False), 'application/json')

if __name__ == '__main__':
    print('Buka http://127.0.0.1:8000')
    HTTPServer(('127.0.0.1',8000), Handler).serve_forever()
