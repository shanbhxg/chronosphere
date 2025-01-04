<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4 text-primary">Bluesky Top 5 Words</h1>

    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-lg">
          <div class="card-body">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                v-model="handle"
                placeholder="Enter Bluesky handle"
                @keyup.enter="fetchPosts"
              />
            </div>
            <button
              class="btn btn-primary btn-block mt-3"
              @click="fetchPosts"
              :disabled="loading"
            >
              Fetch Word Bank
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-if="topWords.length > 0" class="mt-5">
      <div class="card shadow-lg">
        <div class="card-body">
          <h5 class="card-title text-center">Top 5 Words</h5>
          <ul class="list-group list-group-flush">
            <li
              v-for="(word, index) in topWords"
              :key="index"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              {{ word[0] }}
              <span class="badge badge-primary badge-pill">{{ word[1] }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 alert alert-danger text-center">
      {{ error }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      handle: '',
      topWords: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchPosts() {
      if (!this.handle) return;

      this.loading = true;
      this.error = null;
      const baseUrl = window.location.hostname.includes('localhost')
        ? 'http://127.0.0.1:5000/api/words'
        : 'https://atmosphere.vercel.app/api/words';

      try {
        const response = await axios.get(baseUrl, {
          params: { handle: this.handle },
        });

        if (response.data.top_words && response.data.top_words.length) {
          this.topWords = response.data.top_words;
        } else {
          this.error = 'No posts found or unable to fetch words.';
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        this.error = error.response
          ? `Error fetching data from server: ${error.response.statusText}`
          : 'Error fetching data from server.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
}

.card {
  border-radius: 10px;
}

.card-body {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.7rem;
}

button:disabled {
  opacity: 0.6;
}

.form-control::placeholder { 
  color: grey;
}

.list-group-item {
  font-size: 1.1rem;
  padding: 0.6rem;
}

.badge {
  font-size: 1.2rem;
  color: black !important;
}
</style>
