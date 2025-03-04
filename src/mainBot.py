# This example requires the 'message_content' intent.
import requests
from bs4 import BeautifulSoup
import sys
import discord
import json


URL = "https://www.golem.es/golem/golem-alhondiga"






def obtener_peliculas():
    """Download the page and extract movie titles."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        print(f"Error {response.status_code} accessing the page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    peliculas = [h2.text.strip() for h2 in soup.find_all(class_ = "txtNegXXL m5")]

    return peliculas



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$alhondiga'):
        peliculas = obtener_peliculas()
        for pelicula in peliculas:
            await message.channel.send(pelicula)
    if message.content.startswith('$peli '):
        what = message.content[len("$peli "):]
        url = f"https://api.themoviedb.org/3/search/movie?query={what}&language=en-US&page=1"

        

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYzYxOWUwMmQyZWNlMDZkZGViZmJjMjQ5OGY2M2MwYSIsIm5iZiI6MTczOTgyMzQ4MS4yLCJzdWIiOiI2N2IzOTk3OTViOGM3ODllODQ5ZmJjMzMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.vzE5C9Zpezyn9UT85MwfxL0b9eeQDljjUipqMDs_ui8"
        }

        response = requests.get(url, headers=headers)
        data = response.json()  # Convierte la respuesta a JSON

        # Para mostrar las películas (que están en la clave 'results')
        if 'results' in data:
            for movie in data['results']:
                await message.channel.send(f"Titulo: {movie.get('title')}")
                #print(f"Fecha de estreno: {movie.get('release_date')}")
                #print(f"Descripción: {movie.get('overview')}")
                #print("-" * 50)  # Separador

client.run(TOKEN)
