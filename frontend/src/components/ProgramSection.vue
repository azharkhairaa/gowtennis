<script setup>
defineProps({
  program: { type: Array, default: () => [] },
})
</script>

<template>
  <section id="program" class="section section--dark">
    <div class="wrap">
      <div class="prog__head">
        <div>
          <span class="eyebrow">Program &amp; Biaya</span>
          <h2 class="section-title">Pilih sesi yang cocok</h2>
        </div>
        <p class="section-lead">
          Jadwal berjalan tetap tiap pekan. Kelas Senin dan Selasa di UPI sudah
          termasuk raket, bola, dan ballboy, jadi tidak perlu beli perlengkapan
          dulu untuk mencoba.
        </p>
      </div>

      <div class="prog__grid">
        <article
          v-for="p in program"
          :key="p.nama"
          class="prog__card"
          :class="{ 'prog__card--unggulan': p.nama === 'Coaching Beginner' }"
        >
          <span v-if="p.nama === 'Coaching Beginner'" class="prog__tag">
            Termurah
          </span>

          <h3 class="prog__name">{{ p.nama }}</h3>
          <p v-if="p.level || p.hari" class="prog__level">
            {{ [p.hari, p.level].filter(Boolean).join(' · ') }}
          </p>

          <p class="prog__price">{{ p.harga }}</p>

          <dl class="prog__meta">
            <div v-if="p.jadwal">
              <dt>Jadwal</dt>
              <dd>{{ p.jadwal }}</dd>
            </div>
            <div v-if="p.durasi">
              <dt>Durasi</dt>
              <dd>{{ p.durasi }}</dd>
            </div>
            <div v-if="p.kapasitas">
              <dt>Kuota</dt>
              <dd>{{ p.kapasitas }}</dd>
            </div>
            <div v-if="p.lokasi">
              <dt>Lokasi</dt>
              <dd>{{ p.lokasi }}</dd>
            </div>
          </dl>

          <ul v-if="p.termasuk?.length" class="prog__incl">
            <li v-for="t in p.termasuk" :key="t">{{ t }}</li>
          </ul>

          <ul v-if="p.belum_termasuk?.length" class="prog__excl">
            <li v-for="t in p.belum_termasuk" :key="t">{{ t }} dihitung terpisah</li>
          </ul>

          <!-- Kelas privat: sewa lapangan ditagih di luar biaya coaching. -->
          <table v-if="p.tarif_lapangan?.length" class="prog__tarif">
            <caption>
              Total per sesi 2 jam
            </caption>
            <thead>
              <tr>
                <th scope="col">Lapangan</th>
                <th scope="col">Sewa</th>
                <th scope="col">Coaching</th>
                <th scope="col">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in p.tarif_lapangan" :key="t.lapangan">
                <th scope="row">{{ t.lapangan }}</th>
                <td>{{ t.sewa_lapangan }}</td>
                <td>{{ t.coaching }}</td>
                <td class="prog__tarif-total">{{ t.total }}</td>
              </tr>
            </tbody>
          </table>

          <p v-if="p.tambahan?.length" class="prog__tambahan">
            <span v-for="t in p.tambahan" :key="t.nama">
              +{{ t.harga }} {{ t.nama.toLowerCase() }}<template v-if="t.keterangan"> ({{ t.keterangan }})</template>
            </span>
          </p>

          <a href="#gabung" class="btn btn--primary btn--sm prog__cta">Daftar</a>
        </article>
      </div>

      <p class="prog__note">
        Harga dan jadwal di atas mengikuti poster resmi Gow! Tennis per 25
        September 2026. Konfirmasi ulang lewat grup WhatsApp atau DM sebelum
        datang, karena agenda bisa berubah mengikuti ketersediaan lapangan.
      </p>
    </div>
  </section>
</template>

<style scoped>
.prog__head {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: end;
  margin-bottom: 46px;
}

.prog__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(276px, 1fr));
  gap: 20px;
}

.prog__card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 30px 26px 28px;
  border: 1px solid var(--line-dark);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.035);
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.prog__card:hover {
  transform: translateY(-5px);
  border-color: rgba(215, 232, 75, 0.45);
  background: rgba(255, 255, 255, 0.06);
}

.prog__card--unggulan {
  border-color: var(--lime-400);
  background: rgba(215, 232, 75, 0.07);
}

.prog__tag {
  position: absolute;
  top: -11px;
  left: 26px;
  background: var(--lime-400);
  color: var(--navy-900);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 11px;
  border-radius: 999px;
}

.prog__name {
  font-size: 1.62rem;
  margin-bottom: 5px;
}

.prog__level {
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--lime-400);
  margin-bottom: 18px;
}

.prog__price {
  font-family: var(--font-display);
  font-size: 2.15rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 22px;
}

.prog__meta {
  margin: 0 0 20px;
  display: grid;
  gap: 11px;
}

.prog__meta > div {
  display: grid;
  grid-template-columns: 74px 1fr;
  gap: 10px;
  align-items: baseline;
}

.prog__meta dt {
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
}

.prog__meta dd {
  margin: 0;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.86);
}

.prog__incl {
  list-style: none;
  margin: 0 0 24px;
  padding: 18px 0 0;
  border-top: 1px solid var(--line-dark);
  display: grid;
  gap: 8px;
}

.prog__incl li {
  position: relative;
  padding-left: 22px;
  font-size: 0.89rem;
  color: rgba(255, 255, 255, 0.78);
}

.prog__incl li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.48em;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--lime-400);
}

.prog__excl {
  list-style: none;
  margin: -12px 0 20px;
  padding: 0;
  display: grid;
  gap: 6px;
}

.prog__excl li {
  position: relative;
  padding-left: 22px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
}

.prog__excl li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 9px;
  height: 1.5px;
  background: rgba(255, 255, 255, 0.35);
}

.prog__tarif {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 18px;
  font-size: 0.82rem;
}

.prog__tarif caption {
  caption-side: top;
  text-align: left;
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
  padding-bottom: 7px;
}

.prog__tarif th,
.prog__tarif td {
  text-align: right;
  padding: 6px 0 6px 8px;
  border-bottom: 1px solid var(--line-dark);
  color: rgba(255, 255, 255, 0.82);
  font-weight: 450;
}

.prog__tarif thead th {
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
  font-weight: 700;
}

.prog__tarif th[scope='row'],
.prog__tarif thead th:first-child {
  text-align: left;
  padding-left: 0;
  color: #fff;
  font-weight: 650;
}

.prog__tarif-total {
  color: var(--lime-400) !important;
  font-weight: 700 !important;
}

.prog__tambahan {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 20px;
}

.prog__cta {
  margin-top: auto;
  align-self: flex-start;
}

.prog__note {
  margin-top: 34px;
  font-size: 0.86rem;
  color: rgba(255, 255, 255, 0.5);
  max-width: 76ch;
}

@media (max-width: 820px) {
  .prog__head {
    grid-template-columns: 1fr;
    gap: 16px;
    align-items: start;
  }
}
</style>
