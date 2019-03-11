import Vue from 'vue'
import Vuex from 'vuex'
import { listHeroes } from '../api';

Vue.use(Vuex)

const state = {
    heroes: []
    // single source of data
}

const actions = {
    loadHeroes(context) {
        return listHeroes()
            .then((response) => context.commit('setHeroes', { heroes: response }))
    }
    // asynchronous operations
}

const mutations = {
    // isolated data mutations
}


const getters = {
    // reusable data accessors
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store