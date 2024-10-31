from flask import Flask, render_template, request, redirect, url_for

class Kondisi:
    def __init__(self, gejala, penyakit):
        self.gejala = gejala 
        self.penyakit = penyakit

class SistemPakar:
    def __init__(self):
        self.basis_pengetahuan = []
        self.nama_pasien = ""

    def tambah_kondisi(self, kondisi):
        self.basis_pengetahuan.append(kondisi)

    def set_nama_pasien(self, nama):
        self.nama_pasien = nama

    def diagnosis(self, gejala):
        diagnosa = []
        for kondisi in self.basis_pengetahuan:
            if all(symptom in gejala for symptom in kondisi.gejala):
                diagnosa.append(kondisi.penyakit)
        if diagnosa:
            return diagnosa
        else:
            return ["Tidak dapat mengidentifikasi dampak atau penyakit berdasarkan gejala yang diberikan."]

# Membuat basis pengetahuan dari kondisi yang diberikan
basis_pengetahuan = [
    Kondisi(["kecanduan penggunaan smartphone", "cemas atau gelisah", "mengabaikan tanggung jawab sulit tidur"], "Gangguan Kecemasan"),
    Kondisi(["sulit tidur", "sakit kepala", "rasa lemas", "rasa mengantuk", "mata lelah", "pengelihatan kabur"], "Insomnia"),
    Kondisi(["pengelihatan kabur", "rasa pusing melihat objek jauh", "sulit melihat dimalam hari"], "Myopia"),
    Kondisi(["nyeri bahu", "nyeri leher", "rasa kaku"], "Repetitive Strain Injury (RSI)"),
    Kondisi(["sulit fokus / konsentrasi", "pelupa"], "Gangguan konsentrasi"),
    Kondisi(["nyeri bahu", "nyeri punggung", "postur bungkuk"], "Skoliosis"),
    Kondisi(["sulit tidur", "penurunan massa otot", "gangguan nafsu makan"], "Obesitas"),
    Kondisi(["nyeri bahu", "nyeri leher", "kesulitan merasakan benda dengan tangan", "sensasi tersengat listrik"], "Carpal Tunnel Syndrome (CTS)"),
    Kondisi(["sulit fokus / konsentrasi", "kesulitan mendengar suara pelan", "sulit memahami percakapan", "telinga terasa tersumbat"], "Gangguan Pendengaran"),
    Kondisi(["mata lelah", "pengelihatan kabur", "mata kering / iritasi", "sensitif melihat cahaya terang", "mengalami migrain"], "Computer Vision Syndrome (CVS)"),
    Kondisi(["sakit kepala", "pengelihatan kabur", "mengalami migrain", "rasa mual / muntah"], "Vertigo"),
    Kondisi(["kecanduan penggunaan smartphone", "cemas atau gelisah", "mudah marah / tersinggung", "merasa terisolasi / kesepian", "mengalami depresi"], "Nomophobia"),
    Kondisi(["sakit kepala", "sulit fokus / konsentrasi", "pelupa", "mudah marah / tersinggung", "bertindak agresif", "sulit menenangkan diri"], "Gangguan kognitif"),
]

pertanyaan = {
    "kecanduan penggunaan smartphone": "Apakah Anda merasa kecanduan penggunaan smartphone?",
    "cemas atau gelisah": "Apakah Anda merasa cemas atau gelisah?",
    "mengabaikan tanggung jawab sulit tidur": "Apakah Anda sulit tidur dan mengabaikan tanggung jawab?",
    "sulit tidur": "Apakah Anda mengalami kesulitan tidur?",
    "sakit kepala": "Apakah Anda mengalami sakit kepala?",
    "rasa lemas": "Apakah Anda merasa lemas?",
    "rasa mengantuk": "Apakah Anda merasa mengantuk?",
    "mata lelah": "Apakah Anda mengalami mata lelah?",
    "pengelihatan kabur": "Apakah Anda mengalami pengelihatan kabur? ",
    "rasa pusing melihat objek jauh": "Apakah Anda merasa pusing ketika melihat objek jauh?",
    "sulit melihat dimalam hari": "Apakah Anda sulit melihat di malam hari? ",
    "nyeri bahu": "Apakah Anda mengalami nyeri bahu?",
    "nyeri leher": "Apakah Anda mengalami nyeri leher?",
    "rasa kaku": "Apakah Anda merasa kaku?",
    "sulit fokus / konsentrasi": "Apakah Anda sulit fokus atau konsentrasi? (y/n)",
    "pelupa": "Apakah Anda sering pelupa? (y/n)",
    "nyeri punggung": "Apakah Anda mengalami nyeri punggung? (y/n)",
    "postur bungkuk": "Apakah Anda memiliki postur bungkuk? (y/n)",
    "penurunan massa otot": "Apakah Anda mengalami penurunan massa otot? ",
    "gangguan nafsu makan": "Apakah Anda mengalami gangguan nafsu makan? ",
    "kesulitan merasakan benda dengan tangan": "Apakah Anda kesulitan merasakan benda dengan tangan? ",
    "sensasi tersengat listrik": "Apakah Anda merasakan sensasi tersengat listrik?",
    "kesulitan mendengar suara pelan": "Apakah Anda kesulitan mendengar suara pelan? ",
    "sulit memahami percakapan": "Apakah Anda sulit memahami percakapan? ",
    "telinga terasa tersumbat": "Apakah telinga Anda terasa tersumbat? ",
    "mata kering / iritasi": "Apakah mata Anda kering atau iritasi? ",
    "sensitif melihat cahaya terang": "Apakah Anda sensitif melihat cahaya terang? ",
    "mengalami migrain": "Apakah Anda mengalami migrain? ",
    "rasa mual / muntah": "Apakah Anda merasa mual atau muntah? ",
    "mudah marah / tersinggung": "Apakah Anda mudah marah atau tersinggung? ",
    "merasa terisolasi / kesepian": "Apakah Anda merasa terisolasi atau kesepian? : ",
    "mengalami depresi": "Apakah Anda mengalami depresi? ",
    "bertindak agresif": "Apakah Anda bertindak agresif? : ",
    "sulit menenangkan diri": "Apakah Anda sulit menenangkan diri? ",
}

# Membuat sistem pakar dan menambahkan Kondisi ke basis pengetahuan
sistem_pakar = SistemPakar()
for kondisi in basis_pengetahuan:
    sistem_pakar.tambah_kondisi(kondisi)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/input_nama', methods=['GET', 'POST'])
def input_nama():
    if request.method == 'POST':
        nama = request.form['nama']
        if nama.isalpha():
            sistem_pakar.set_nama_pasien(nama)
            return redirect(url_for('input_gejala'))
        else:
            error = "Nama hanya boleh mengandung karakter alfabet. Silakan coba lagi."
            return render_template('input_nama.html', error=error)
    return render_template('input_nama.html', error=None)

@app.route('/input_gejala', methods=['GET', 'POST'])
def input_gejala():
    if request.method == 'POST':
        gejala = request.form.getlist('gejala')
        diagnosa = sistem_pakar.diagnosis(gejala)
        return redirect(url_for('hasil_diagnosa', diagnosa=diagnosa, nama=sistem_pakar.nama_pasien))
    return render_template('input_gejala.html', pertanyaan=pertanyaan)

@app.route('/hasil_diagnosa')
def hasil_diagnosa():
    diagnosa = request.args.getlist('diagnosa')
    nama = request.args.get('nama')
    return render_template('hasil_diagnosa.html', diagnosa=diagnosa, nama=nama)

if __name__ == '__main__':
    app.run(debug=True)
