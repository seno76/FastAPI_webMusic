const API_BASE_URL = 'http://localhost:7777'; // Замените на ваш URL API

class MusicAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        try {
            const url = `${this.baseUrl}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Треки
    async getTracks() {
        return this.request('/tracks/');
    }

    async getTrack(id) {
        return this.request(`/tracks/${id}`);
    }

    async searchTracks(query) {
        return this.request(`/tracks/search/?title=${encodeURIComponent(query)}`);
    }

    async getTopTracks() {
        return this.request('/tracks/top');
    }

    async getTracksByAlbum(albumId) {
        return this.request(`/tracks/by-album/${albumId}`);
    }

    async getTracksByGenre(genreId) {
        return this.request(`/tracks/by-genre/${genreId}`);
    }

    async getTracksByAuthor(authorId) {
        return this.request(`/tracks/by-author/${authorId}`);
    }

    // Альбомы
    async getAlbums(offset = 0, limit = 100) {
        return this.request(`/albums/?offset=${offset}&limit=${limit}`);
    }

    async getAlbum(id) {
        return this.request(`/albums/${id}`);
    }

    async getAlbumsByGenre(genreId) {
        return this.request(`/albums/search/by-genre/${genreId}`);
    }

    // Плейлисты
    async getPlaylists(limit = 1000, offset = 0) {
        return this.request(`/playlists/?limit=${limit}&offset=${offset}`);
    }

    async getPlaylist(id) {
        return this.request(`/playlists/${id}`);
    }

    async getPlaylistTracks(playlistId) {
        return this.request(`/playlists/${playlistId}/tracks`);
    }

    // Артисты
    async getAuthors(offset = 0, limit = 100) {
        return this.request(`/authors/?offset=${offset}&limit=${limit}`);
    }

    async getAuthor(id) {
        return this.request(`/authors/${id}`);
    }

    // Жанры
    async getGenres(limit = 1000, offset = 0) {
        return this.request(`/genres/?limit=${limit}&offset=${offset}`);
    }

    async getGenre(id) {
        return this.request(`/genres/${id}`);
    }

    // Пользователи
    async getUser(id) {
        return this.request(`/users/${id}`);
    }

    // Предпочтения
    async getUserTrackPreferences(userId) {
        return this.request(`/preference/users/${userId}/tracks`);
    }

    async getUserAlbumPreferences(userId) {
        return this.request(`/preference/users/${userId}/albums`);
    }
}

// Создаем экземпляр API
const musicAPI = new MusicAPI(API_BASE_URL);