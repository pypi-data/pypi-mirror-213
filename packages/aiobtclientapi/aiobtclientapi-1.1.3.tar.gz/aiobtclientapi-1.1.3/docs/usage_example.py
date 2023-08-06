import asyncio
import aiobtclientapi

async def run():
    # Create API instance
    try:
        api = aiobtclientapi.api(
            name="qbittorrent",
            url="localhost:5000",
            username="AzureDiamond",
            password="hunter2",
        )
    except aiobtclientapi.ValueError as e:
        # Invalid client name or URL
        print('Error:', e)
        exit(1)

    # Add torrents
    response = await api.add(
        "path/to/my.first.torrent",
        "path/to/my.second.torrent",
        "path/to/my.third.torrent",
        stopped=True,
    )

    # success is only True if all of the torrents were added
    if not response.success:
        print("Something went wrong!")

    # Handle errors
    for error in response.errors:
        print("Error:", error)

    # Handle warnings
    for warning in response.warnings:
        print("Warning:", warning)

    # Show which torrents were actually added
    for infohash in response.added:
        print("Added:", infohash)

    # Get a list of existing torrents
    try:
        infohashes = await api.get_infohashes()
    except aiobtclientapi.ConnectionError as e:
        print("Unable to get infohashes:", e)
    else:
        print("Infohashes:")
        for infohash in infohashes:
            print(f" * {infohash}")

asyncio.run(run())
