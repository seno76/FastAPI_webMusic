import flet as ft
import requests
import os
from pathlib import Path

# Настройки API - ЗАМЕНИТЕ НА ВАШИ РЕАЛЬНЫЕ ЭНДПОИНТЫ!
API_BASE_URL = "http://localhost:8000"  # или ваш удаленный URL
API_ENDPOINTS = {
    "tracks": "/api/tracks",
    "search": "/api/search",
    "playlists": "/api/playlists",
    "play": "/api/play/",
    "pause": "/api/pause",
    "auth": "/api/auth/login"
}


class MusicApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.current_track = None
        self.is_playing = False
        self.tracks = []

        # Создаем интерфейс
        self.create_ui()

        # Загружаем музыку при запуске
        self.load_initial_tracks()

    def setup_page(self):
        self.page.title = "Музыкальный плеер"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def create_ui(self):
        # Создаем элементы интерфейса
        self.create_header()
        self.create_content()
        self.create_player_controls()

        # Собираем все вместе
        self.page.add(
            ft.Column([
                self.header,
                ft.Divider(height=1, color=ft.colors.GREY_700),
                self.content,
                ft.Divider(height=1, color=ft.colors.GREY_700),
                self.player_controls
            ], expand=True)
        )

    def create_header(self):
        self.search_field = ft.TextField(
            hint_text="Поиск музыки...",
            expand=True,
            on_submit=lambda e: self.search_tracks(),
            border_radius=20,
            content_padding=10
        )

        self.header = ft.Container(
            content=ft.Row([
                ft.Text("🎵 Музыкальный плеер", size=24, weight=ft.FontWeight.BOLD),
                self.search_field,
                ft.IconButton(
                    icon=ft.icons.SEARCH,
                    on_click=lambda e: self.search_tracks()
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor=ft.colors.SURFACE_VARIANT
        )

    def create_content(self):
        self.track_list = ft.ListView(expand=True, spacing=10)
        self.content = ft.Container(
            content=self.track_list,
            padding=20,
            expand=True
        )

    def create_player_controls(self):
        self.now_playing = ft.Text("Выберите трек для воспроизведения", size=16)
        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            on_click=self.toggle_playback
        )

        self.player_controls = ft.Container(
            content=ft.Row([
                ft.Column([
                    self.now_playing,
                    ft.Text("00:00 / 00:00", size=12)
                ], expand=True),
                ft.Row([
                    ft.IconButton(ft.icons.SKIP_PREVIOUS),
                    self.play_button,
                    ft.IconButton(ft.icons.SKIP_NEXT),
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor=ft.colors.SURFACE_VARIANT
        )

    def load_initial_tracks(self):
        """Загрузка треков при запуске"""
        try:
            # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ЗАПРОС К API
            response = requests.get(f"{API_BASE_URL}{API_ENDPOINTS['tracks']}")
            if response.status_code == 200:
                self.tracks = response.json()
                self.display_tracks(self.tracks)
            else:
                self.show_error("Ошибка загрузки треков")
        except Exception as e:
            self.show_error(f"Ошибка соединения: {str(e)}")
            # Покажем демо-данные если API недоступно
            self.show_demo_data()

    def search_tracks(self):
        """Поиск треков"""
        query = self.search_field.value
        if not query:
            self.display_tracks(self.tracks)
            return

        try:
            # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ЗАПРОС К API
            response = requests.get(f"{API_BASE_URL}{API_ENDPOINTS['search']}?q={query}")
            if response.status_code == 200:
                results = response.json()
                self.display_tracks(results)
            else:
                self.show_error("Ошибка поиска")
        except Exception as e:
            self.show_error(f"Ошибка поиска: {str(e)}")

    def display_tracks(self, tracks):
        """Отображение списка треков"""
        self.track_list.controls.clear()

        for track in tracks:
            # АДАПТИРУЙТЕ ПОД СТРУКТУРУ ВАШИХ ДАННЫХ
            track_name = track.get('title', 'Без названия')
            artist = track.get('artist', 'Неизвестный исполнитель')
            duration = track.get('duration', '0:00')

            self.track_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.MUSIC_NOTE),
                    title=ft.Text(track_name),
                    subtitle=ft.Text(f"{artist} • {duration}"),
                    on_click=lambda e, t=track: self.play_track(t)
                )
            )

        self.page.update()

    def play_track(self, track):
        """Воспроизведение трека"""
        self.current_track = track
        self.is_playing = True

        # ОБНОВИТЕ ДЛЯ ВАШЕГО API
        track_name = track.get('title', 'Без названия')
        artist = track.get('artist', 'Неизвестный исполнитель')

        self.now_playing.value = f"{track_name} - {artist}"
        self.play_button.icon = ft.icons.PAUSE

        # ЗДЕСЬ ДОБАВЬТЕ ВЫЗОВ ВАШЕГО API ДЛЯ ВОСПРОИЗВЕДЕНИЯ
        print(f"Воспроизведение: {track_name}")

        self.page.update()

    def toggle_playback(self, e):
        """Пауза/воспроизведение"""
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.icon = ft.icons.PAUSE
            # ВЫЗОВ API: возобновить воспроизведение
        else:
            self.play_button.icon = ft.icons.PLAY_ARROW
            # ВЫЗОВ API: пауза

        self.page.update()

    def show_error(self, message):
        """Показать сообщение об ошибке"""
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def show_demo_data(self):
        """Показать демо-данные если API недоступно"""
        demo_tracks = [
            {"title": "Демо трек 1", "artist": "Исполнитель 1", "duration": "3:45"},
            {"title": "Демо трек 2", "artist": "Исполнитель 2", "duration": "4:20"},
            {"title": "Демо трек 3", "artist": "Исполнитель 3", "duration": "2:55"}
        ]
        self.display_tracks(demo_tracks)
        self.show_error("API недоступно. Показаны демо-данные.")


def main(page: ft.Page):
    MusicApp(page)


if __name__ == "__main__":
    ft.app(target=main)