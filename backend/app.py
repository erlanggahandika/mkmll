from flask import Flask, request, jsonify

app = Flask(__name__)

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

        # Klasifikasi perokok
        jenis, total_merokok, cost, health_damage = classify_smoker_type(amt_akhir_pekan, amt_hari_kerja)

        # Pesan untuk pengguna
        user_message = (
            f"Anda terklasifikasi sebagai {jenis}.\n"
            f"Total rokok yang dikonsumsi dalam setahun: {total_merokok} batang.\n"
            f"Biaya yang dikeluarkan untuk merokok per tahun: ${cost:.2f}.\n"
            f"Kerugian kesehatan yang ditimbulkan per tahun: ${health_damage:.2f}.\n"
            "Merokok dapat menyebabkan berbagai masalah kesehatan, termasuk penyakit jantung, kanker, dan gangguan pernapasan."
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
            'message': user_message
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

    # Estimasi biaya merokok per tahun (misal harga per bungkus rokok)
    cost_per_cigarette = 0.2  # Biaya per rokok dalam USD
    cost = total_merokok * cost_per_cigarette  # Biaya per tahun

    # Estimasi kerugian kesehatan per tahun (misal biaya pengobatan)
    health_damage_per_cigarette = 0.1  # Estimasi kerugian kesehatan per rokok dalam USD
    health_damage = total_merokok * health_damage_per_cigarette  # Kerugian kesehatan per tahun

    return jenis, total_merokok, cost, health_damage

if __name__ == '__main__':
    app.run(debug=True)
