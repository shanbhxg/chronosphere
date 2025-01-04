<template>
  <div>
    <h1>Bluesky Posts Data</h1>

    <input 
      v-model="handle" 
      @keyup.enter="fetchPosts" 
      placeholder="Enter Bluesky handle" 
    />

    <div v-if="loading">Loading...</div>

    <div v-if="topWords.length > 0">
      <h3>Top 5 Words from {{ handle }}'s Posts</h3>
      <ul>
        <li v-for="(word, index) in topWords" :key="index">
          {{ word[0] }}: {{ word[1] }}
        </li>
      </ul>
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
      loading: false
    };
  },
  methods: {
    async fetchPosts() {
      if (!this.handle) return;

      this.loading = true;

      try {
        const response = await axios.get('http://127.0.0.1:5000/api/words', {
          params: { handle: this.handle }
        });

        this.topWords = response.data.top_words;

      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
