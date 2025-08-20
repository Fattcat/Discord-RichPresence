from pypresence import Presence
import time

# Tvoj Client ID z Discord Developer Portal
CLIENT_ID = "YourCode Client ID"  # Nahraď svojím Client ID z discord stránky
# Pripoj sa k RPC
RPC = Presence(CLIENT_ID)
RPC.connect()

# Aktualizuj stav
RPC.update(
    state="Test hello",                    # Dolný riadok
    details="Hram neru ma pls",               # Horný riadok
    start=time.time(),                      # Čas spustenia (pre "odpočet")
    large_image="img.jpg",               # ID obrázku (z Rich Presence assets)
    large_text="Čo furt chceš ?",                 # Text pri prejdení myšou nad obrázkom
    small_image="img.jpg",               # Malý obrázok (napr. logo)
    small_text="Verzia 1.0",
    buttons=[{"label": "Stiahnuť hru", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]  # Voliteľné tlačidlo
)

print("Rich Presence je aktívne! Stlač Ctrl+C pre ukončenie.")
try:
    while True:
        time.sleep(15)  # Discord odporúča aktualizovať každých 15-20 sekúnd
except KeyboardInterrupt:
    RPC.close()
    print("RPC ukončené.")
