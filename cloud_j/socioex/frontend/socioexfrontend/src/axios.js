import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000/twitter/';

const axiosInstance = axios.create({
	baseURL: baseURL,
	timeout: 20000
});

export default axiosInstance