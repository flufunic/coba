from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Path ke file Excel
EXCEL_FILE = 'assets/baru.xlsx'

def cari_data_berdasarkan_nik(nik):
    try:
        # Baca file Excel, pastikan kolom NIK dibaca sebagai string
        df = pd.read_excel(EXCEL_FILE, dtype={'NIK': str})

        # Cari data berdasarkan NIK
        result = df[df['NIK'].str.strip() == nik.strip()]

        if result.empty:
            return None  # Jika data tidak ditemukan

        # Pilih kolom yang diperlukan
        output = result[[
            "Nama", "SEMBAKO", "PKH", "PBI", "RST", "BLT ELNINO", "BLT BBM",
            "SEMBAKO ADAPTIF", "BLT MIGOR", "YATIM PIATU", "PERMAKANAN",
            "PENA", "BPNT-PPKM", "BST", "ATENSI"
        ]]

        # Konversi ke dictionary untuk output
        return output.to_dict(orient='records')[0]

    except FileNotFoundError:
        return "File Excel tidak ditemukan!"
    except Exception as e:
        return f"Terjadi error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    nik = request.form.get('nik')
    if nik:
        hasil = cari_data_berdasarkan_nik(nik)
        if hasil:
            return jsonify(hasil)
        else:
            return jsonify({'error': 'Data tidak ditemukan!'}), 404
    return jsonify({'error': 'NIK tidak diberikan!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
