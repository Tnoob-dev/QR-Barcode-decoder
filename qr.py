from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyzbar.pyzbar import decode
from PIL import Image
import os
from infos import Creds
import qrcode
import random


bot = Client(
    "bot",
    api_id=Creds.API_ID,
    api_hash=Creds.API_HASH,
    bot_token=Creds.BOT_TOKEN,
)

# Decode QR Codes and Bar Codes
@bot.on_message()
async def qr_bar(client, message: Message):

    # Checar si el mensaje es una foto
    if message.photo:
        try:

            photo = message.photo
            # Descargar la foto
            p = await client.download_media(photo)
            # Decodificar la foto
            qr_code = decode(Image.open(p))
            # Checar si el QR Code es valido
            if qr_code:
                
                data = qr_code[0].data.decode("utf-8")
                # Enviarselo al usuario 
                await message.reply(data)
                os.remove(p)
        except Exception as e:
            print(e)
            await message.reply("No Se encontro Codigo QR ni Codigo de barras.")


#######################################
# Y lo mismo con el video y el sticker#
#######################################
    
    elif message.sticker:
        try:
        
            sticker = message.sticker
            
            s = await client.download_media(sticker)
            
            qr_code = decode(Image.open(s))
            
            if qr_code:
                
                data = qr_code[0].data.decode("utf-8")
                await message.reply(data)

                os.remove(s)
        except Exception as e:
            print(e)
            await message.reply("No Se encontro Codigo QR ni Codigo de barras.")
    
    elif message.video:
        
        video = message.video
        try:
        
            v = await client.download_media(video)
            
            qr_code = decode(Image.open(v))
            
            if qr_code:
                
                data = qr_code[0].data.decode("utf-8")
                await message.reply(data)

                os.remove(v)
        except Exception as e:
            print(e)
            await message.reply("No Se encontro Codigo QR ni Codigo de barras.")


    # Si el message es texto
    elif message.text:
        if message.text == "/start":
            await message.reply(f"Hola👋 @{message.from_user.username} Soy un Bot para Decodificar Codigos QR y Bar Codes; para utilizarme es simple, " 
                                "solo envie una foto/video/sticker con el Código QR o Código de Barras que desee decodificar. "
                                "Tambien puede enviar un texto para generar un Código QR.\n\n"
                                "Intenta decodificar mi foto de perfil para ver como funciona.😅",
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton("Canal de origen🤙", url="https://t.me/softwareyprogramacion"),
                                            InlineKeyboardButton("Grupo de Origen😎", url="https://t.me/SPGrupo")
                                        ]
                                    ]
                                )
                                )
        else:
            filenam = "qr.png"
            # Crear el QR Code
            qr = qrcode.QRCode(
                version=1,  # 1-40
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # L, M, Q, H
                box_size=10,    # 1-100
                border=4    # 0-4
            )

            qr.add_data(message.text)

            qr.make(fit=True)

            # Determinas el color que quieres de fondo(back_color)
            # Y el Color que quieres de los datos(fill_color)
            # Puedes usar incluso valores Hexadecimales

            # Una lista con varios colores para hacerlo mas divertido xD, asi se sale del monotono Negro-Blanco
            color_list = ['#e06c75', '#98c379', '#d19a66', '#61afef', '#ff0080', '#6441a5', '#f696af', '#ffce30'] # Colores tomados de https://github.com/adrianrl99/theme/blob/main/theme.png
            for i in range(1):
                img = qr.make_image(fill_color=random.choice(color_list), back_color="white")

            img.save(filenam)

            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(filenam)

            os.remove(filenam)

if __name__ == "__main__":
    print("Bot is running")
    bot.run()
