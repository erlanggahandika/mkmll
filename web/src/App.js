import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [jenisKelamin, setJenisKelamin] = useState('');
  const [usia, setUsia] = useState('');
  const [statusPerkawinan, setStatusPerkawinan] = useState('');
  const [kualifikasiTertinggi, setKualifikasiTertinggi] = useState('');
  const [kebangsaan, setKebangsaan] = useState('');
  const [etnis, setEtnis] = useState('');
  const [pendapatanKotor, setPendapatanKotor] = useState('');
  const [wilayah, setWilayah] = useState('');
  const [merokok, setMerokok] = useState('');
  const [amtAkhirPekan, setAmtAkhirPekan] = useState('');
  const [amtHariKerja, setAmtHariKerja] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    // // Validasi input
    // if (!jenisKelamin || !usia || !statusPerkawinan || !kualifikasiTertinggi || !kebangsaan || !etnis || !pendapatanKotor || !wilayah || !merokok || !amtAkhirPekan || !amtHariKerja) {
    //   setResponse({ error: 'Semua field harus diisi.' });
    //   return;
    // }

    try {
      const result = await axios.post('https://dcb3-103-169-238-23.ngrok-free.app/smoker', {
        jenis_kelamin: jenisKelamin,
        usia: parseInt(usia),
        status_perkawinan: statusPerkawinan,
        kualifikasi_tertinggi: kualifikasiTertinggi,
        kebangsaan: kebangsaan,
        etnis: etnis,
        pendapatan_kotor: parseInt(pendapatanKotor),
        wilayah: wilayah,
        merokok: merokok,
        amt_akhir_pekan: parseInt(amtAkhirPekan),
        amt_hari_kerja: parseInt(amtHariKerja),
      });
      setResponse(result.data);
    } catch (error) {
      console.error('API Error:', error.response || error);
      setResponse({ error: error.response ? error.response.data : 'An error occurred' });
    }
  };

  return (
    <div className="container">
      <div className="form">
        <select value={jenisKelamin} onChange={(e) => setJenisKelamin(e.target.value)}>
          <option value="">Jenis Kelamin</option>
          <option value="laki-laki">Laki-laki</option>
          <option value="perempuan">Perempuan</option>
        </select>
        <input
          type="number"
          placeholder="Usia"
          value={usia}
          onChange={(e) => setUsia(e.target.value)}
        />

        <select value={statusPerkawinan} onChange={(e) => setStatusPerkawinan(e.target.value)}>
          <option value="">Status Perkawinan</option>
          <option value="belum">Belum Menikah</option>
          <option value="menikah">Menikah</option>
        </select>
        <select value={kualifikasiTertinggi} onChange={(e) => setKualifikasiTertinggi(e.target.value)}>
          <option value="">Kualifikasi Tertinggi</option>
          <option value="sd">SD</option>
          <option value="smp">SMP</option>
          <option value="sma">SMA</option>
          <option value="sarjana">Sarjana</option>
          <option value="magister">Magister</option>
          <option value="doktor">Doktor</option>
        </select>

        <select value={kebangsaan} onChange={(e) => setKebangsaan(e.target.value)}>
          <option value="">Kebangsaan</option>
          <option value="indonesia">Indonesia</option>
          <option value="malaysia">Malaysia</option>
          <option value="singapura">Singapura</option>
        </select>
        <select value={etnis} onChange={(e) => setEtnis(e.target.value)}>
          <option value="">Etnis</option>
          <option value="jawa">Jawa</option>
          <option value="sunda">Sunda</option>
          <option value="batak">Batak</option>
        </select>

        <select value={pendapatanKotor} onChange={(e) => setPendapatanKotor(e.target.value)}>
          <option value="">Pendapatan Kotor</option>
          <option value="0-5 juta">0-5 Juta</option>
          <option value="5-10 juta">5-10 Juta</option>
          <option value="10+ juta">10+ Juta</option>
        </select>
        <select value={wilayah} onChange={(e) => setWilayah(e.target.value)}>
          <option value="">Wilayah</option>
          <option value="jakarta">Jakarta</option>
          <option value="bandung">Bandung</option>
          <option value="surabaya">Surabaya</option>
        </select>

        <input
          type="number"
          placeholder="Jumlah Rokok di Akhir Pekan"
          value={amtAkhirPekan}
          onChange={(e) => setAmtAkhirPekan(e.target.value)}
        />
        <input
          type="number"
          placeholder="Jumlah Rokok di Hari Kerja"
          value={amtHariKerja}
          onChange={(e) => setAmtHariKerja(e.target.value)}
        />
      </div>

      <button onClick={handleSubmit}>Submit</button>

      {response && (
        <div className="response-container">
          {response.error ? (
            <p>{response.error}</p>
          ) : (
            <>
              <p>Anda terklasifikasi sebagai perokok {response.classification}.</p>
              <p>Total rokok yang dikonsumsi dalam setahun: {response.total_merokok} batang.</p>
              <p>Biaya yang dikeluarkan untuk merokok per tahun: IDR {response.cost_per_year.toLocaleString()}.</p>
              <p>Kerugian kesehatan yang ditimbulkan per tahun: IDR {response.health_damage.toLocaleString()}.</p>
              {response.marriage_advice && response.marriage_advice !== "" && (
                <p>{response.marriage_advice}</p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
