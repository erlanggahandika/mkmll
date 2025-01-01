from flask import Flask, request, jsonify

app = Flask(__name__)

# Fungsi untuk mendapatkan saran pernikahan
def get_marriage_advice(status_perkawinan, usia):
    if status_perkawinan == 'Belum Menikah' and usia > 20:
        return "Segera menikah lah."
    else:
        return ""

@app.route('/smoker', methods=['POST'])
def classify_smoker():
    try:
        # Cek apakah request berisi JSON dan data yang diperlukan
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Ambil data dari request
        required_fields = ['jenis_kelamin', 'usia', 'status_perkawinan', 'kualifikasi_tertinggi', 'kebangsaan', 
                           'etnis', 'pendapatan_kotor', 'wilayah', 'merokok', 'amt_akhir_pekan', 'amt_hari_kerja']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Parsing data
        jenis_kelamin = data['jenis_kelamin']
        usia = data['usia']
        status_perkawinan = data['status_perkawinan']
        kualifikasi_tertinggi = data['kualifikasi_tertinggi']
        kebangsaan = data['kebangsaan']
        etnis = data['etnis']
        pendapatan_kotor = data['pendapatan_kotor']
        wilayah = data['wilayah']
        merokok = data['merokok']
        amt_akhir_pekan = data['amt_akhir_pekan']
        amt_hari_kerja = data['amt_hari_kerja']

        # Panggil fungsi untuk mendapatkan saran pernikahan
        marriage_advice = get_marriage_advice(status_perkawinan, usia)

        # Cek kualifikasi tertinggi
        if kualifikasi_tertinggi == 'SMA':
            marriage_advice += "\nKualifikasi tertinggi: SMA"
        elif kualifikasi_tertinggi == 'S1':
            marriage_advice += "\nKualifikasi tertinggi: S1"
        elif kualifikasi_tertinggi == 'S2':
            marriage_advice += "\nKualifikasi tertinggi: S2"
        elif kualifikasi_tertinggi == 'S3':
            marriage_advice += "\nKualifikasi tertinggi: S3"
        else:
            marriage_advice += "\nKualifikasi tertinggi: Tidak diketahui"
        
        # Klasifikasi perokok
        jenis, total_merokok, cost, health_damage = classify_smoker_type(amt_akhir_pekan, amt_hari_kerja)

        # Pesan untuk pengguna
        user_message = (
            f"Anda terklasifikasi sebagai {jenis}.\n"
            f"Total rokok yang dikonsumsi dalam setahun: {total_merokok} batang.\n"
            f"Biaya yang dikeluarkan untuk merokok per tahun: IDR {cost:,}.\n"
            f"Kerugian kesehatan yang ditimbulkan per tahun: IDR {health_damage:,}.\n"
            "Merokok dapat menyebabkan berbagai masalah kesehatan, termasuk penyakit jantung, kanker, dan gangguan pernapasan."
            f"\n{marriage_advice}"
        )

        # Mengembalikan hasil klasifikasi tanpa menyimpan ke database
        response = {
            'jenis_kelamin': jenis_kelamin,
            'usia': usia,
            'status_perkawinan': status_perkawinan,
            'kualifikasi_tertinggi': kualifikasi_tertinggi,
            'kebangsaan': kebangsaan,
            'etnis': etnis,
            'pendapatan_kotor': pendapatan_kotor,
            'wilayah': wilayah,
            'merokok': merokok,
            'amt_akhir_pekan': amt_akhir_pekan,
            'amt_hari_kerja': amt_hari_kerja,
            'classification': jenis,
            'total_merokok': total_merokok,
            'cost_per_year': cost,
            'health_damage': health_damage,
            'message': user_message,
            'marriage_advice': marriage_advice
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def classify_smoker_type(amt_akhir_pekan, amt_hari_kerja):
    # Decision tree untuk klasifikasi perokok
    if amt_akhir_pekan >= 10 or amt_hari_kerja >= 10:
        jenis = 'Berat'
        cigarettes_per_day = 20  # Cigarettes per day for heavy smoker
    elif amt_akhir_pekan >= 5 or amt_hari_kerja >= 5:
        jenis = 'Sedang'
        cigarettes_per_day = 10  # Cigarettes per day for moderate smoker
    else:
        jenis = 'Ringan'
        cigarettes_per_day = 5  # Cigarettes per day for light smoker

    # Estimasi total merokok per tahun
    total_merokok = cigarettes_per_day * 365

    # Estimasi biaya merokok per tahun (harga per rokok dalam IDR)
    cost_per_cigarette = 20000   # Biaya per rokok dalam IDR
    cost = total_merokok * cost_per_cigarette  # Biaya per tahun dalam IDR

    # Estimasi kerugian kesehatan per tahun (biaya pengobatan dalam IDR)
    health_damage_per_cigarette = 5000  # Estimasi kerugian kesehatan per rokok dalam IDR
    health_damage = total_merokok * health_damage_per_cigarette  # Kerugian kesehatan per tahun dalam IDR

    return jenis, total_merokok, cost, health_damage

if __name__ == '__main__':
    app.run(debug=True)
