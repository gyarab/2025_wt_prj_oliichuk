<template>
  <main class="page">
    <section class="card">
      <h1>Valorant Stats Tracker</h1>
      <p class="subtitle">Enter your details to start tracking your stats.</p>

      <form class="form" @submit.prevent="handleSubmit">
        <label class="field">
          <span>Name</span>
          <input
            v-model="form.name"
            type="text"
            placeholder="e.g. TenZ"
            required
          >
        </label>

        <label class="field">
          <span>Tag</span>
          <input
            v-model="form.tag"
            type="text"
            placeholder="e.g. NA1"
            required
          >
        </label>

        <label class="field">
          <span>API key</span>
          <small class="help-text">
            Generate the key at
            <a href="https://api.henrikdev.xyz/dashboard/api-keys" target="_blank" rel="noopener noreferrer">
              https://api.henrikdev.xyz/dashboard/api-keys
            </a>
          </small>
          <input
            v-model="form.apiKey"
            type="password"
            placeholder="Paste your API key"
            required
          >
        </label>

        <button type="submit">Track Stats</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
    </section>
  </main>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      form: {
        name: '',
        tag: '',
        apiKey: ''
      },
      message: ''
    }
  },
  methods: {
    handleSubmit() {
      this.message = `Ready to track ${this.form.name}#${this.form.tag}.`
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;700&display=swap');

:root {
  --bg: #061229;
  --bg-soft: #0b1f3f;
  --card: #0f274c;
  --border: #1f3b68;
  --text: #d7f2e8;
  --muted: #9dc5b7;
  --accent: #39ff14;
  --accent-strong: #2fe312;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  min-height: 100%;
  background: var(--bg);
}

.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.2rem;
  background: radial-gradient(circle at 20% 20%, var(--bg-soft), var(--bg));
  color: var(--text);
  font-family: 'Exo 2', 'Segoe UI', sans-serif;
}

.card {
  width: 100%;
  max-width: 420px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem;
  box-shadow: 0 14px 28px rgba(3, 10, 24, 0.35);
}

h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--accent);
  text-align: center;
  text-shadow: 0 0 12px rgba(57, 255, 20, 0.45);
}

.subtitle {
  margin: 0.4rem 0 1rem;
  color: var(--muted);
}

.form {
  display: grid;
  gap: 0.9rem;
}

.field {
  display: grid;
  gap: 0.35rem;
}

.field span {
  font-size: 0.92rem;
  color: var(--muted);
}

.help-text {
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.45;
}

.help-text a {
  color: var(--muted);
  text-decoration: underline;
}

.help-text a:hover {
  color: var(--muted);
  text-decoration: underline;
}

input {
  border: 1px solid #2d4a79;
  background: #0a1d3a;
  color: var(--text);
  border-radius: 8px;
  padding: 0.62rem 0.72rem;
  outline: none;
}

input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(57, 255, 20, 0.2), 0 0 14px rgba(57, 255, 20, 0.28);
}

button {
  margin-top: 0.3rem;
  border: 0;
  border-radius: 8px;
  background: var(--accent);
  color: #042a19;
  font-family: inherit;
  font-weight: 700;
  padding: 0.65rem;
  cursor: pointer;
  box-shadow: 0 0 12px rgba(57, 255, 20, 0.38);
}

button:hover {
  background: var(--accent-strong);
  box-shadow: 0 0 18px rgba(57, 255, 20, 0.55);
}

.message {
  margin: 0.9rem 0 0;
  color: #8bff6a;
  text-shadow: 0 0 8px rgba(139, 255, 106, 0.45);
}
</style>
