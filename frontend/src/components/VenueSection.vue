<script setup>
defineProps({
  venue: { type: Array, default: () => [] },
})
</script>

<template>
  <section id="lapangan" class="section section--soft">
    <div class="wrap">
      <span class="eyebrow">Lapangan</span>
      <h2 class="section-title">Dua titik main di Bandung</h2>
      <p class="section-lead">
        Sesi berpindah antara lapangan indoor kampus dan lapangan outdoor,
        menyesuaikan program dan cuaca.
      </p>

      <div class="venue__grid">
        <article v-for="v in venue" :key="v.nama" class="card venue__card">
          <span class="venue__type" :class="`venue__type--${v.tipe.toLowerCase()}`">
            {{ v.tipe }}
          </span>
          <h3>{{ v.nama }}</h3>
          <p class="venue__city">{{ v.kota }}</p>
          <p class="venue__use">{{ v.dipakai_untuk }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.venue__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.venue__card {
  padding: 30px 26px;
}

.venue__type {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 4px 11px;
  border-radius: 999px;
  margin-bottom: 16px;
}

.venue__type--indoor {
  background: var(--navy-800);
  color: #fff;
}

.venue__type--outdoor {
  background: var(--lime-400);
  color: var(--navy-900);
}

.venue__card h3 {
  font-size: 1.5rem;
  margin-bottom: 6px;
}

.venue__city {
  font-size: 0.82rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted-light);
  margin-bottom: 14px;
}

.venue__use {
  color: var(--muted);
  font-size: 0.95rem;
}
</style>
