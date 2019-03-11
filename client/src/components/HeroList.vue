<template>
  <div id="comicslist">
    <ul>
      <li is="Hero" v-bind:key="index" v-bind:img="hero.thumbnail_url" v-bind:name="hero.name" v-for="(hero, index) in heroes"></li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import Hero from './Hero.vue'
let API_URL = 'http://localhost:5000/api/heroes'
export default {
  name: 'HeroList',
  components: {
    Hero: Hero
  },
  data () {
    return {
      heroes: [],
      index: 0,
      bottom: false
    }
  },
  methods: {
    bottomVisible () {
      const scrollY = window.scrollY
      const visible = document.documentElement.clientHeight
      const pageHeight = document.documentElement.scrollHeight
      const bottomOfPage = visible + scrollY >= pageHeight
      return bottomOfPage || pageHeight < visible
    },
    getInitialHeroes () {
      axios.get(API_URL).then(response => {
        if (!response.error) {
          let heroes = response.data
          this.index = heroes[heroes.length - 1]['num'] - 1
          this.heroes.push(...heroes)
        }
      })
    }
  },
  watch: {
    bottom (bottom) {
      if (bottom) {
        // this.addComic();
      }
    }
  },
  beforeMount () {
    this.getInitialHeroes()
  },
  created () {
    // window.addEventListener('scroll', () => {
    //  this.bottom = this.bottomVisible()
    // })
    // this.addComic()
    this.getInitialHeroes()
  }
}
</script>
