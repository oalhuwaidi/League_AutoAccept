from lcu_driver import Connector
import customtkinter
import threading
import time
import asyncio
import os

currentphase = "Client not Detected"
connector = Connector()

@connector.ready
async def connect(connection):
    time.sleep(1)
    global currentphase
    while True:
        gamephase = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
        currentphase = await gamephase.json()
        label.configure(text=currentphase)
        if checkbox_var_AutoAccept.get():
            await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
        if checkbox_var_AutoQueue.get():
            await connection.request('post', '/lol-lobby/v2/lobby/matchmaking/search')
# Start the GUI in the main thread
def main():
    global checkbox_var_AutoQueue
    global checkbox_var_AutoAccept
    global label
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    root.geometry("500x350")
    root.title("Auto League")

    frame = customtkinter.CTkFrame(root)
    frame.pack(pady=2, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(frame, text=currentphase, font=("Robonto", 24))
    label.pack(pady=12, padx=10)

    checkbox_var_AutoAccept = customtkinter.BooleanVar()
    checkbox1 = customtkinter.CTkCheckBox(frame, text="Auto Accept", variable=checkbox_var_AutoAccept)
    checkbox1.pack(pady=12, padx=10)

    checkbox_var_AutoQueue = customtkinter.BooleanVar()
    checkbox2 = customtkinter.CTkCheckBox(frame, text="Auto Queue", variable=checkbox_var_AutoQueue)
    checkbox2.pack(pady=12, padx=10)

    root.mainloop()
    asyncio.run(stop_connect())

async def stop_connect():
    await connector.stop()
    os._exit(0)    

if __name__ == "__main__":
    # Start the GUI in the main thread
    threading.Thread(target=main, daemon=True).start()
    # starts the connector
    connector.start()
