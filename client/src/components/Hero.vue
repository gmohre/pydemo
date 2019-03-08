<template>
  <div>
    <div class="container">
    <h3>{{ name }}</h3>
    <img class="comic" :src="img">
    <button type="button" class="btn btn-primary">{{ name }}</button>
  </div>
  </div>
</template>
<script>
export default {
  name: 'Hero',
  props: ['id', 'marvel_id', 'img', 'name']
/*   data () {
    return {
      id: 21,
      marvel_id: 1009243,
      name: 'Colossus',
      thumbnail_url:
        'http://i.annihil.us/u/prod/marvel/i/mg/6/e0/51127cf4b996f.jpg'
    }
  } */
}
</script>
