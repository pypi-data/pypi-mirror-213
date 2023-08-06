from sdks.webull_sdk.webull_sdk import AsyncWebullSDK
webull =AsyncWebullSDK()


import asyncio
import aiohttp
import pandas as pd


top_options_channels = {
    '1': "1117530682047078541",
    '2': "1117530680151265340",
    '3': "1117530678561624194",
    '4': "1117530676779036693",
    '5': "1117530683506692156",
    '6': "1118258134121717850",
    '7': '1118258136202088618',
    '8': "1118258137888215161",
    '9': "1118258139289112666",
    '10': "1118258140924870817",


}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Authorization": "Mzc1ODYyMjQwNjAxMDQ3MDcw.GE5kZ8.scHZxVpyK8WKEcyCCER_VBfgEzZ79u3HhS4ZEw"
}


async def update_channel():
    async with aiohttp.ClientSession() as session:
        while True:
            # Retrieve the top options and relevant data
            df, top_options = await webull.top_options_chains('posDecrease')


            for i, row in df.head(10).iterrows():
                symbol = row['underlying_symbol']
                expiry = str(row['expiry'])[6:].replace('-', '▫️')

                contract_type = row['direction']
                if contract_type == "call":
                    result = "🟢"

                if contract_type == "put":
                    result = "🔴"            
                channel_id = top_options_channels.get(str(i + 1))  # Get the channel ID based on the iteration index

                # Update channel name with symbol and expiration
                new_name = f"{symbol}{result}{expiry}"  # Modify this according to your desired channel name format

                async with session.patch(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers, json={"name": new_name}) as resp:
                    if resp.status != 200:
                        print(f"Error updating channel name: {resp.status}, {await resp.text()}")
                    else:
                        print(f"Successfully updated channel name for {symbol}.")

            await asyncio.sleep(360)  # Delay for one minute


async def main():
    while True:
        await update_channel()


asyncio.run(main())