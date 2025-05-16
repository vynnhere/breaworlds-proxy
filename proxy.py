import asyncio
import io
import struct
import sys
import packet

class Player:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

        self.proxy_god = False
        self.proxy_noclip = False
        self.proxy_dev = False
        self.proxy_notp = False

        self.proxy_ghost = False
        self.proxy_ghost_buffer = b''

        self.proxy_jump_height = 15
        self.proxy_walk_speed = 1
        self.proxy_wing_jump = 0

        self.identifier = None
        self.skin_color_red = None
        self.skin_color_green = None
        self.skin_color_blue = None
        self.skin_alpha = None
        self.sex = None
        self.badge = None
        self.wing_jump = None
        self.username = None
        self.clothing1 = None
        self.clothing2 = None
        self.clothing3 = None
        self.clothing4 = None
        self.clothing5 = None
        self.clothing6 = None
        self.clothing7 = None
        self.clothing8 = None
        self.side_badge = None
        self.visible = None
        self.noclip = None
        self.frozen = None
        self.jump_height = None
        self.walk_speed = None
        self.staff_badge = None
    
    async def log(self, message: str):
        await packet.client.send.log(f"~1[~rBREAPROXY~1]~0 {message}", self)
    
    async def notify(self, header: str, content: str, footer: str, icon: int):
        await packet.client.send.notification(header, content, footer, icon, 200, self)
    
    async def sync_character(self):
        await packet.client.send.update_character(identifier=self.identifier, skin_color_red=self.skin_color_red, skin_color_green=self.skin_color_green, skin_color_blue=self.skin_color_blue, skin_alpha=self.skin_alpha, sex=self.sex, badge=self.badge, side_badge=self.side_badge, staff_badge=self.staff_badge, clothing1=self.clothing1, clothing2=self.clothing2, clothing3=self.clothing3, clothing4=self.clothing4, clothing5=self.clothing5, clothing6=self.clothing6, clothing7=self.clothing7, clothing8=self.clothing8, wing_jump=self.proxy_wing_jump, username=self.username, visible=self.visible, noclip=self.proxy_noclip, frozen=self.frozen, jump_height=self.proxy_jump_height, walk_speed=self.proxy_walk_speed, client=self)

async def read_packet(reader):
    packets = []
    buffer = b''
    
    while True:
        if len(buffer) < 2:
            chunk = await reader.read(4096)
            if not chunk:
                return packets if packets else None
            buffer += chunk
            continue
        
        packet_length = struct.unpack("<H", buffer[:2])[0]
        
        if len(buffer) >= packet_length:
            packet_data = buffer[:packet_length]
            packets.append(packet_data)
            
            buffer = buffer[packet_length:]
            
            if len(buffer) < 2:
                return packets
        else:
            chunk = await reader.read(4096)
            if not chunk:
                return packets if packets else None
            
            buffer += chunk

async def handle_client(client_reader, client_writer):
    player = Player(client_reader, client_writer)
    server_reader = None
    server_writer = None
    
    try:
        server_reader, server_writer = await asyncio.open_connection(
            'host.breaworldsgame.com', 1800
        )
        print("Connected to Breaworlds server")
        
        async def client_to_server():
            try:
                while True:
                    packets = await read_packet(player.reader)
                    if not packets:
                        break
                    
                    for pack in packets:
                        pkt = io.BytesIO(pack)
                        pkt.read(2)
                        pkt_type = pkt.read(1)

                        cancelled = False

                        match pkt_type:
                            case b'\x04':
                                message = await packet.client.receive.extract_chat(pack)

                                args = message.split()

                                if args[0].startswith("!"):
                                    match args[0]:
                                        case "!proxy":
                                            pkt = packet.Packet()

                                            await packet.client.send.dialog.create(pkt, "Proxy")

                                            await packet.client.send.dialog.item_text(pkt, True, "~rBREAPROXY ~1Gazette", 75, 689)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1Welcome to ~rBREAPROXY~1!", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1This is a rewritten, newer, better version! :O", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!proxy", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Opens ts menu", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!jump", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Modifies normal character behaviour to achieve infinite jumps", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!notp", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Bypasses position changing packets", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!god", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Bypasses death packets to turn you ~o~pINVIN~6CIBLE~o", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!ghost", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Movement and pickup packets will be queued", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1to be sent when the feature is turned off", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!noclip", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Useful for standing on bounce blocks", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Can't go through blocks", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!speed <integer>", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Multiplies walk-speed and jump-height by argument", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!developer", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Lets you place client-sided blocks anywhere anyhow", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!reset", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Resets all custom player attributes to default", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.text(pkt, True, "~1!reset", 50)
                                            await packet.client.send.dialog.text(pkt, True, "~1Resets everything in the proxy to default", 50)

                                            await packet.client.send.dialog.space(pkt)

                                            await packet.client.send.dialog.button(pkt, True, "Finish", "~1OKE")

                                            pkt.create_packet()

                                            await pkt.send(player.writer)
                                            pkt.close()
                                        
                                        case "!god":
                                            player.proxy_god = not player.proxy_god

                                            await player.log(f"~1God {"~4enabled" if player.proxy_god else "~3disabled"}~1")

                                        case "!notp":
                                            player.proxy_notp = not player.proxy_notp

                                            await player.log(f"~1No Teleport {"~4enabled" if player.proxy_notp else "~3disabled"}~1")


                                        case "!developer":
                                            player.proxy_dev = not player.proxy_dev

                                            await player.log(f"~1Developer {"~4enabled" if player.proxy_dev else "~3disabled"}~1")

                                        case "!noclip":
                                            player.proxy_noclip = not player.proxy_noclip

                                            await player.log(f"~1Noclip {"~4enabled" if player.proxy_noclip else "~3disabled"}~1")

                                            await player.sync_character()
                                        
                                        case "!ghost":
                                            if len(player.proxy_ghost_buffer) != 0:
                                                if not player.proxy_ghost == False:
                                                    await send_data(server_writer, player.proxy_ghost_buffer)
                                                    player.proxy_ghost_buffer = b''

                                                    await player.log("~1Woosh! Traveling a lot.")
                                            
                                            player.proxy_ghost = not player.proxy_ghost

                                            await player.log(f"~1Ghost {"~4enabled" if player.proxy_ghost else "~3disabled"}~1")

                                        case "!speed":
                                            if len(args) == 2:
                                                try:
                                                    player.proxy_jump_height = player.jump_height * int(args[1])
                                                    player.proxy_walk_speed = player.walk_speed * int(args[1])

                                                    await player.sync_character()
                                                
                                                except:
                                                    await player.log("~1Failed to increment, Possible invalid argument(s)")

                                        case "!jump":
                                            match player.proxy_wing_jump:
                                                case player.wing_jump:
                                                    player.proxy_wing_jump = 65535

                                                    await player.sync_character()
                                                    await player.log("~1Infinite Jump ~4enabled")
                                                
                                                case 65535:
                                                    player.proxy_wing_jump = player.wing_jump

                                                    await player.sync_character()
                                                    await player.log("~1Infinite Jump ~3disabled~1")
                                        
                                        case "!reset":
                                            player.proxy_jump_height = player.jump_height
                                            player.proxy_walk_speed = player.walk_speed
                                            player.proxy_wing_jump = player.wing_jump

                                            await player.sync_character()

                                            await player.log("~1Player attributes have been reset")
                                        
                                        case "!panic":
                                            player.proxy_god = False
                                            player.proxy_noclip = False
                                            player.proxy_dev = False
                                            player.proxy_notp = False
                                            player.proxy_ghost = False
                                            player.proxy_ghost_buffer = b''
                                            player.proxy_jump_height = 15
                                            player.proxy_walk_speed = 1
                                            player.proxy_wing_jump = 0

                                            await player.sync_character()

                                            await player.log("~1All attributes reset & all features turned off")

                                        case _:
                                            await player.log("~1Invalid proxy command")
                                        
                                    cancelled = True

                            case b'\x0b':
                                if player.proxy_dev:
                                    x, y, id = await packet.client.receive.extract_place(pack)

                                    if id == 1: id = 0

                                    await packet.client.send.update_tile(x, y, 2, id, player)

                                    cancelled = True

                                    print("\n[PROXY]\nDeveloper enabled, Bypassed placing")

                            case b'\x1a':
                                await send_data(server_writer, b'\x10\x00\x1a\x00\x01\x01\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00')
                                cancelled = True
                                print("\n[PROXY]\nBypassed verification packet")
                            
                            case b'+':
                                if player.proxy_god:
                                    print("\n[PROXY]\nBypassed death packet")
                                    cancelled = True
                            
                            case b'.':
                                if player.proxy_god:
                                    print("\n[PROXY]\nBypassed death packet")
                                    cancelled = True
                            
                            case b')':
                                if player.proxy_god:
                                    print("\n[PROXY]\nBypassed death packet")
                                    cancelled = True
                            
                            case b'\x1d':
                                if player.proxy_god:
                                    print("\n[PROXY]\nBypassed death packet")
                                    cancelled = True
                            
                            case b'\r':
                                if player.proxy_ghost:
                                    player.proxy_ghost_buffer += pack
                                    print("\n[PROXY]\nMovement packet queued to buffer")
                                    cancelled = True
                            
                            case b'\x0c':
                                if player.proxy_ghost:
                                    player.proxy_ghost_buffer += pack
                                    print("\n[PROXY]\nItem pickup packet queued to buffer")
                                    cancelled = True

                        if not cancelled:
                            await send_data(server_writer, pack)
                            packet_length = struct.unpack("<H", pack[:2])[0]
                            print(f"\n[CLIENT] Packet length: {packet_length}\n{pack}")
                    
            except Exception as e:
                print("Client->Server error, on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            
            finally:
                if not server_writer.is_closing():
                    server_writer.close()
                    await server_writer.wait_closed()
        
        async def server_to_client():
            try:
                while True:
                    packets = await read_packet(server_reader)
                    if not packets:
                        break
                    
                    for pack in packets:
                        pkt = io.BytesIO(pack)
                        pkt.read(2)
                        pkt_type = pkt.read(1)

                        cancelled = False

                        match pkt_type:
                            case b'\x04':
                                message = await packet.server.receive.extract_log(pack)

                                await player.log(message)

                                cancelled = True
                            
                            case b'\r':
                                if player.proxy_notp:
                                    pkt = io.BytesIO(pack)

                                    pkt.read(2)
                                    if pkt.read(7) == b'\r\x00\x00\x00\x00\x00\x00':
                                        cancelled = True

                            case b'\x0e':
                                identifier, skin_color_red, skin_color_green, skin_color_blue, skin_alpha, sex, badge, wing_jump, username, clothing1, clothing2, clothing3, clothing4, clothing5, clothing6, clothing7, clothing8, side_badge, visible, noclip, frozen, jump_height, walk_speed, staff_badge = await packet.server.receive.extract_character_update(pack)

                                if identifier == 0:
                                    player.identifier = identifier
                                    player.skin_color_red = skin_color_red
                                    player.skin_color_green = skin_color_green
                                    player.skin_color_blue = skin_color_blue
                                    player.skin_alpha = skin_alpha
                                    player.sex = sex
                                    player.badge = badge
                                    player.wing_jump = wing_jump
                                    player.username = username
                                    player.clothing1 = clothing1
                                    player.clothing2 = clothing2
                                    player.clothing3 = clothing3
                                    player.clothing4 = clothing4
                                    player.clothing5 = clothing5
                                    player.clothing6 = clothing6
                                    player.clothing7 = clothing7
                                    player.clothing8 = clothing8
                                    player.side_badge = side_badge
                                    player.visible = visible
                                    player.noclip = noclip
                                    player.frozen = frozen
                                    player.jump_height = jump_height
                                    player.walk_speed = walk_speed
                                    player.staff_badge = staff_badge
                                else:
                                    if (player.identifier == identifier) and (player.skin_color_red == skin_color_red) and (player.skin_color_green == skin_color_green) and (player.skin_color_blue == skin_color_blue) and (player.skin_alpha == skin_alpha) and (player.sex == sex) and (player.badge == badge) and (player.wing_jump == wing_jump) and (player.username == username) and (player.clothing1 == clothing1) and (player.clothing2 == clothing2) and (player.clothing3 == clothing3) and (player.clothing4 == clothing4) and (player.clothing5 == clothing5) and (player.clothing6 == clothing6) and (player.clothing7 == clothing7) and (player.clothing8 == clothing8) and (player.side_badge == side_badge) and (player.visible == visible) and (player.noclip == noclip) and (player.frozen == frozen) and (player.jump_height == jump_height) and (player.walk_speed == walk_speed) and (player.staff_badge == staff_badge):
                                        continue

                                    if visible == False or noclip == True or ((staff_badge > 0) and (staff_badge != 7)):
                                        await player.log(f"~1Moderator {username}~1 detected!")
                                        await player.notify("~1[~rBREAPROXY~1]~0 ", "~3WARNING!", f"~1Moderator {username}~1 detected!", 1)
                                    else:
                                        await player.log(f"~1Player {username} updated; ID [{identifier}]")
                                
                                print("\n[PROXY]\nReceived Update Character")
                            
                            case b'\x15':
                                identifier, message = await packet.server.receive.extract_chat_bubble(pack)

                                if identifier != 0:
                                    await packet.client.send.display_sign(f"~1[~rBREACHAT~1]~0 {message}", 689, player)

                        if not cancelled:
                            await send_data(player.writer, pack)
                            packet_length = struct.unpack("<H", pack[:2])[0]
                            print(f"\n[SERVER] Packet length: {packet_length}\n{pack}")
                    
            except Exception as e:
                print("Server->Client error, on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            
            finally:
                if not player.writer.is_closing():
                    player.writer.close()
                    await player.writer.wait_closed()
        
        await asyncio.gather(
            client_to_server(),
            server_to_client()
        )

    except Exception as e:
        print(f"Connection error: {e}")
    
    finally:
        if server_writer and not server_writer.is_closing():
            server_writer.close()
            await server_writer.wait_closed()
        
        if player.writer and not player.writer.is_closing():
            player.writer.close()
            await player.writer.wait_closed()
        
        print("Client connection closed")

async def send_data(writer, data):
    writer.write(data)
    await writer.drain()

async def main():
    server = await asyncio.start_server(
        handle_client, 'localhost', 1800
    )
    async with server:
        print("BreaProxy running on localhost:1800")
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Proxy server stopped")