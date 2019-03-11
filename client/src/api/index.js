import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api'

export function listHeroes() {
    return axios.get(`${API_URL}/heroes`)
}