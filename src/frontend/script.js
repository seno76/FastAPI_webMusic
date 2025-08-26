// Глобальные переменные
let currentSection = 'tracks';
let currentData = [];

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    loadSectionData('tracks');

    // Закрытие модального окна
    document.querySelector('.close').addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('modal')) {
            closeModal();
        }
    });
});

// Инициализация навигации
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.getAttribute('data-section');

            // Обновляем активные кнопки
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Переключаем секции
            switchSection(section);
        });
    });
}

// Переключение между секциями
function switchSection(section) {
    // Скрываем все секции
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });

    // Показываем выбранную секцию
    document.getElementById(`${section}-section`).classList.add('active');

    // Загружаем данные для секции
    loadSectionData(section);
}

// Загрузка данных для секции
async function loadSectionData(section) {
    const container = document.getElementById(`${section}-list`);
    container.innerHTML = '<div class="loading">Загрузка...</div>';

    try {
        let data;

        switch(section) {
            case 'tracks':
                data = await musicAPI.getTracks();
                displayTracks(data, container);
                break;
            case 'albums':
                data = await musicAPI.getAlbums();
                displayAlbums(data, container);
                break;
            case 'playlists':
                data = await musicAPI.getPlaylists();
                displayPlaylists(data, container);
                break;
            case 'artists':
                data = await musicAPI.getAuthors();
                displayArtists(data, container);
                break;
            case 'genres':
                data = await musicAPI.getGenres();
                displayGenres(data, container);
                break;
        }

        currentData = data;
        currentSection = section;
    } catch (error) {
        container.innerHTML = `<div class="error">Ошибка загрузки: ${error.message}</div>`;
    }
}

// Поиск треков
async function searchTracks() {
    const query = document.getElementById('track-search').value;
    if (!query) return;

    const container = document.getElementById('tracks-list');
    container.innerHTML = '<div class="loading">Поиск...</div>';

    try {
        const data = await musicAPI.searchTracks(query);
        displayTracks(data, container);
    } catch (error) {
        container.innerHTML = `<div class="error">Ошибка поиска: ${error.message}</div>`;
    }
}

// Отображение треков
function displayTracks(tracks, container) {
    if (!tracks || tracks.length === 0) {
        container.innerHTML = '<div class="loading">Треки не найдены</div>';
        return;
    }

    container.innerHTML = '';
    tracks.forEach(track => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <div class="item-title">${track.title || 'Без названия'}</div>
            <div class="item-details">
                ${track.artist ? `Артист: ${track.artist}<br>` : ''}
                ${track.duration ? `Длительность: ${track.duration}<br>` : ''}
                ${track.rating ? `Рейтинг: ${track.rating}` : ''}
            </div>
        `;
        card.addEventListener('click', () => showTrackDetails(track));
        container.appendChild(card);
    });
}

// Отображение альбомов
function displayAlbums(albums, container) {
    if (!albums || albums.length === 0) {
        container.innerHTML = '<div class="loading">Альбомы не найдены</div>';
        return;
    }

    container.innerHTML = '';
    albums.forEach(album => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <div class="item-title">${album.title || 'Без названия'}</div>
            <div class="item-details">
                ${album.artist ? `Артист: ${album.artist}<br>` : ''}
                ${album.year ? `Год: ${album.year}<br>` : ''}
                ${album.genre ? `Жанр: ${album.genre}` : ''}
            </div>
        `;
        card.addEventListener('click', () => showAlbumDetails(album));
        container.appendChild(card);
    });
}

// Отображение плейлистов
function displayPlaylists(playlists, container) {
    if (!playlists || playlists.length === 0) {
        container.innerHTML = '<div class="loading">Плейлисты не найдены</div>';
        return;
    }

    container.innerHTML = '';
    playlists.forEach(playlist => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <div class="item-title">${playlist.name || 'Без названия'}</div>
            <div class="item-details">
                ${playlist.description || 'Описание отсутствует'}
            </div>
        `;
        card.addEventListener('click', () => showPlaylistDetails(playlist));
        container.appendChild(card);
    });
}

// Отображение артистов
function displayArtists(artists, container) {
    if (!artists || artists.length === 0) {
        container.innerHTML = '<div class="loading">Артисты не найдены</div>';
        return;
    }

    container.innerHTML = '';
    artists.forEach(artist => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <div class="item-title">${artist.name || 'Без названия'}</div>
            <div class="item-details">
                ${artist.bio ? `Биография: ${artist.bio.substring(0, 50)}...` : 'Информация отсутствует'}
            </div>
        `;
        card.addEventListener('click', () => showArtistDetails(artist));
        container.appendChild(card);
    });
}

// Отображение жанров
function displayGenres(genres, container) {
    if (!genres || genres.length === 0) {
        container.innerHTML = '<div class="loading">Жанры не найдены</div>';
        return;
    }

    container.innerHTML = '';
    genres.forEach(genre => {
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
            <div class="item-title">${genre.name || 'Без названия'}</div>
            <div class="item-details">
                ${genre.description ? `Описание: ${genre.description.substring(0, 50)}...` : 'Описание отсутствует'}
            </div>
        `;
        card.addEventListener('click', () => showGenreDetails(genre));
        container.appendChild(card);
    });
}

// Показать детали трека
async function showTrackDetails(track) {
    try {
        const fullTrack = await musicAPI.getTrack(track.id);
        openModal('Трек', formatTrackDetails(fullTrack));
    } catch (error) {
        openModal('Трек', formatTrackDetails(track));
    }
}

// Показать детали альбома
async function showAlbumDetails(album) {
    try {
        const fullAlbum = await musicAPI.getAlbum(album.id);
        const tracks = await musicAPI.getTracksByAlbum(album.id);

        let content = formatAlbumDetails(fullAlbum);
        content += `<h3>Треки в альбоме (${tracks.length})</h3>`;
        content += '<ul>';
        tracks.forEach(track => {
            content += `<li>${track.title} (${track.duration || 'неизвестно'})</li>`;
        });
        content += '</ul>';

        openModal('Альбом', content);
    } catch (error) {
        openModal('Альбом', formatAlbumDetails(album));
    }
}

// Показать детали плейлиста
async function showPlaylistDetails(playlist) {
    try {
        const tracks = await musicAPI.getPlaylistTracks(playlist.id);

        let content = `<p><strong>Название:</strong> ${playlist.name || 'Не указано'}</p>`;
        content += `<p><strong>Описание:</strong> ${playlist.description || 'Отсутствует'}</p>`;

        content += `<h3>Треки в плейлисте (${tracks.length})</h3>`;
        content += '<ul>';
        tracks.forEach(track => {
            content += `<li>${track.title} - ${track.artist || 'Неизвестный артист'} (${track.duration || 'неизвестно'})</li>`;
        });
        content += '</ul>';

        openModal('Плейлист', content);
    } catch (error) {
        openModal('Плейлист', `<p>Не удалось загрузить детали плейлиста: ${error.message}</p>`);
    }
}

// Показать детали артиста
function showArtistDetails(artist) {
    const content = `
        <p><strong>Имя:</strong> ${artist.name || 'Не указано'}</p>
        <p><strong>Биография:</strong> ${artist.bio || 'Отсутствует'}</p>
        <p><strong>Страна:</strong> ${artist.country || 'Не указана'}</p>
    `;
    openModal('Артист', content);
}

// Показать детали жанра
function showGenreDetails(genre) {
    const content = `
        <p><strong>Название:</strong> ${genre.name || 'Не указано'}</p>
        <p><strong>Описание:</strong> ${genre.description || 'Отсутствует'}</p>
    `;
    openModal('Жанр', content);
}

// Форматирование деталей трека
function formatTrackDetails(track) {
    return `
        <p><strong>Название:</strong> ${track.title || 'Не указано'}</p>
        <p><strong>Артист:</strong> ${track.artist || 'Неизвестен'}</p>
        <p><strong>Альбом:</strong> ${track.album || 'Не указан'}</p>
        <p><strong>Длительность:</strong> ${track.duration || 'Неизвестна'}</p>
        <p><strong>Рейтинг:</strong> ${track.rating || 'Не оценен'}</p>
        <p><strong>Жанр:</strong> ${track.genre || 'Не указан'}</p>
    `;
}

// Форматирование деталей альбома
function formatAlbumDetails(album) {
    return `
        <p><strong>Название:</strong> ${album.title || 'Не указано'}</p>
        <p><strong>Артист:</strong> ${album.artist || 'Неизвестен'}</p>
        <p><strong>Год выпуска:</strong> ${album.year || 'Не указан'}</p>
        <p><strong>Жанр:</strong> ${album.genre || 'Не указан'}</p>
    `;
}

// Открытие модального окна
function openModal(title, content) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal').style.display = 'block';
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}