import io
import struct

from proxy import *

class Packet:
    def __init__(self):
        self.buffer = io.BytesIO()
    
    def write_int(self, value: int, hex_length: int):
        bytes_list = []
        for i in range(hex_length):
            byte = (value >> (8 * i)) & 0xFF
            bytes_list.append(byte)
        self.buffer.write(bytes(bytes_list))
        
    def write_string(self, s: str, is_null=True):
        encoded = s.encode('utf-8')
        if is_null:
            encoded += b'\x00'
        self.buffer.write(encoded)
    
    def writer(self, value: int):
        # dummy 0000
        self.buffer.write(b'\x00\x00')
        
        low = value & 0xFF
        high = (value >> 8) & 0xFF
        self.buffer.write(bytes([low, high]))
        
    def create_packet(self):
        self.buffer.seek(0)
        length = self.buffer.getbuffer().nbytes
            
        low = length & 0xFF
        high = (length >> 8) & 0xFF
        self.buffer.write(bytes([low, high]))
    
    async def send(self, writer: asyncio.StreamWriter):
        await send_data(writer, self.buffer.getvalue())
    
    def close(self):
        self.buffer.close()
        self = None

class client:
    class send:
        async def log(msg: str, client: Player):
            pkt = Packet()
            pkt.writer(4)

            pkt.write_string(msg)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        async def update_position(identifier: int, x: int, y: int, destroy_player: bool, client: Player):
            pkt = Packet()
            pkt.writer(13)

            pkt.write_int(identifier, 3)
            pkt.write_int(int(destroy_player), 2)
            pkt.write_int(x, 2)
            pkt.write_int(y, 2)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        async def display_sign(text: str, item_id: int, client: Player):
            pkt = Packet()
            pkt.writer(17)

            pkt.write_int(250, 2)
            pkt.write_int(item_id, 2)
            pkt.write_string(text)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        async def update_character(identifier: int, skin_color_red: int, skin_color_green: int, skin_color_blue: int, skin_alpha: int, sex: int, badge: int, side_badge: int, staff_badge: int, clothing1: int, clothing2: int, clothing3: int, clothing4: int, clothing5: int, clothing6: int, clothing7: int, clothing8: int, wing_jump: int, username: str, visible: bool, noclip: bool, frozen: bool, jump_height: int, walk_speed: int, client: Player):
            pkt = Packet()
            pkt.writer(14)

            pkt.write_int(identifier, 4)
            pkt.write_int(skin_color_red, 2)
            pkt.write_int(skin_color_green, 2)
            pkt.write_int(skin_color_blue, 2)
            pkt.write_int(skin_alpha, 2)
            pkt.write_int(sex, 1)
            pkt.write_int(badge, 2)
            pkt.write_int(wing_jump, 2)
            pkt.write_string(username)
            
            # clothes; the game sorts them out, you can put in random order.

            pkt.write_int(clothing1, 2)
            pkt.write_int(clothing2, 2)
            pkt.write_int(clothing3, 2)
            pkt.write_int(clothing4, 2)
            pkt.write_int(clothing5, 2)
            pkt.write_int(clothing6, 2)
            pkt.write_int(clothing7, 2)
            pkt.write_int(clothing8, 2)

            pkt.write_int(0, 4)

            pkt.write_int(0, 2) # invis feet
            
            pkt.write_int(0, 8)
            
            pkt.write_int(0, 2) # effects

            pkt.write_int(0, 10)

            pkt.write_int(100, 2) # health?
            pkt.write_int(side_badge, 2) # side badge
            pkt.write_int(int(visible), 1)
            pkt.write_int(int(noclip), 1)
            pkt.write_int(int(frozen), 1)
            pkt.write_int(int(False), 1)
            pkt.write_int(jump_height, 2)
            pkt.write_int(walk_speed, 2)

            pkt.write_int(0, 5)

            pkt.write_int(staff_badge, 1) # admin badge

            pkt.write_int(0, 3)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        async def update_tile(x: int, y: int, layer: int, id: int, client: Player):
            pkt = Packet()
            pkt.writer(11)

            pkt.write_int(x, 2)
            pkt.write_int(y, 2)
            pkt.write_int(layer, 2)
            pkt.write_int(id, 2)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        async def notification(header: str, content: str, footer: str, icon: int, time: int, client: Player):
            pkt = Packet()
            pkt.writer(35)

            pkt.write_int(time, 2)
            pkt.write_int(icon, 2)
            pkt.write_string(header)
            pkt.write_string(content)
            pkt.write_string(footer)

            pkt.create_packet()

            await pkt.send(client.writer)
            pkt.close()
        
        class dialog:
            async def create(pkt: Packet, name: str):
                pkt.buffer.write(struct.pack("<H", 0))
                pkt.buffer.write(struct.pack("<H", 5))
                pkt.buffer.write(struct.pack("<H", 0))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')

            async def text(pkt: Packet, breaker: bool, text: str, size: int):
                text = text.replace("\n", "").replace("\r\n", "")
                pkt.buffer.write(struct.pack("<H", 1))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(text.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", size))


            async def item_slot(pkt: Packet, breaker: bool, index: int, count: int, w: int, h: int):
                pkt.buffer.write(struct.pack("<H", 2))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(struct.pack("<H", index))
                pkt.buffer.write(struct.pack("<H", count))
                pkt.buffer.write(struct.pack("<H", w))
                pkt.buffer.write(struct.pack("<H", h))


            async def item_text(pkt: Packet, breaker: bool, text: str, size: int, item: int):
                text = text.replace("\n", "").replace("\r\n", "")
                pkt.buffer.write(struct.pack("<H", 3))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(text.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", size))
                pkt.buffer.write(struct.pack("<H", item))


            async def item_image(pkt: Packet, breaker: bool, size: int, item: int):
                pkt.buffer.write(struct.pack("<H", 3))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(b'\x00')
                pkt.buffer.write(struct.pack("<H", size))
                pkt.buffer.write(struct.pack("<H", item))


            async def item_picker(pkt: Packet, breaker: bool, name: str, item: int, w: int, h: int):
                pkt.buffer.write(struct.pack("<H", 8))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", item))
                pkt.buffer.write(struct.pack("<H", w))
                pkt.buffer.write(struct.pack("<H", h))


            async def button(pkt: Packet, breaker: bool, name: str, text: str):
                pkt.buffer.write(struct.pack("<H", 4))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(text.encode('utf-8') + b'\x00')


            async def textbox(pkt: Packet, breaker: bool, name: str, text: str, length: int):
                text = text.replace("\n", "").replace("\r\n", "")
                pkt.buffer.write(struct.pack("<H", 5))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(text.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<B", length))

            async def checkbox(pkt: Packet, breaker: bool, value: bool, name: str, text: str, size: int):
                pkt.buffer.write(struct.pack("<H", 6))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(struct.pack("<?", value))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(text.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", size))

            async def rgb(pkt: Packet, breaker: bool, name: str, w: int, h: int, r: int, g: int, b: int):
                pkt.buffer.write(struct.pack("<H", 7))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", w))
                pkt.buffer.write(struct.pack("<H", h))
                pkt.buffer.write(struct.pack("<H", r))
                pkt.buffer.write(struct.pack("<H", g))
                pkt.buffer.write(struct.pack("<H", b))

            async def space(pkt: Packet):
                pkt.buffer.write(struct.pack("<H", 9))
                pkt.buffer.write(struct.pack("<?", True))

            async def achievement(pkt: Packet, breaker: bool, icon: int, name: str, text: str, info: str):
                pkt.buffer.write(struct.pack("<H", 10))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(struct.pack("<H", icon))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(text.encode('utf-8') + b'\x00')
                pkt.buffer.write(info.encode('utf-8') + b'\x00')


            async def item_button(pkt: Packet, breaker: bool, name: str, item: int, size: int):
                pkt.buffer.write(struct.pack("<H", 11))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", item))
                pkt.buffer.write(struct.pack("<H", size))
                pkt.buffer.write(struct.pack("<H", size))


            async def icon_button(pkt: Packet, breaker: bool, name: str, icon: int, size: int):
                pkt.buffer.write(struct.pack("<H", 12))
                pkt.buffer.write(struct.pack("<?", breaker))
                pkt.buffer.write(name.encode('utf-8') + b'\x00')
                pkt.buffer.write(struct.pack("<H", icon))
                pkt.buffer.write(struct.pack("<H", size))
                pkt.buffer.write(struct.pack("<H", size))

    class receive:
        async def extract_place(data: bytes):
            pkt = io.BytesIO(data)
            pkt.read(4)
            x = struct.unpack('<H', pkt.read(2))[0] // 32
            y = struct.unpack('<H', pkt.read(2))[0] // 32
            id = struct.unpack('<H', pkt.read(2))[0]
            pkt.close()

            return x, y, id
        
        async def extract_chat(data: bytes) -> str:
            pkt = io.BytesIO(data)
            pkt.read(4)

            len = ord(pkt.read(1))
            message = pkt.read(len)

            pkt.close()
            return message.decode('utf-8')
    
        async def extract_movement(data: bytes):
            pkt = io.BytesIO(data)
            pkt.read(4)
            
            x = struct.unpack("<H", pkt.read(2))
            y = struct.unpack("<H", pkt.read(2))

            pkt.close()

            return x, y

class server:
    class send:
        async def place(x: int, y: int, id: int, server_writer: asyncio.StreamWriter):
            pkt = Packet()

            pkt.write_int(12, 2)
            pkt.write_int(11, 2)

            pkt.write_int(x*32, 2)
            pkt.write_int(y*32, 2)
            pkt.write_int(id, 2)

            pkt.write_int(0, 2)
        
            await pkt.send(server_writer)
            pkt.close()
        
        async def pickup(x: int, y: int, id: int, quantity: int, server_writer: asyncio.StreamWriter):
            pkt = Packet()

            pkt.write_int(13, 2)
            pkt.write_int(12, 2)

            pkt.write_int(1, 1)
            pkt.write_int(id, 2)
            pkt.write_int(quantity, 2)

            pkt.write_int(x, 2)
            pkt.write_int(y, 2)

            await pkt.send(server_writer)
            pkt.close()

    class receive:
        async def extract_log(data: bytes):
            pkt = io.BytesIO(data)
            pkt.read(4)

            message = pkt.read((pkt.getbuffer().nbytes - 5))

            return message.decode('utf-8')
    
        async def extract_chat_bubble(data: bytes):
            pkt = io.BytesIO(data)
            pkt.read(4)
            identifier = struct.unpack("<L", pkt.read(4))
            message = pkt.read().removesuffix(b'\x00\x19\x00')

            pkt.close()

            return identifier, message.decode()
        
        async def extract_character_update(data: bytes):
            buffer = io.BytesIO(data)
            buffer.read(2)
            
            opcode = int.from_bytes(buffer.read(2), byteorder='little')
            
            identifier = int.from_bytes(buffer.read(4), byteorder='little')
            skin_color_red = int.from_bytes(buffer.read(2), byteorder='little')
            skin_color_green = int.from_bytes(buffer.read(2), byteorder='little')
            skin_color_blue = int.from_bytes(buffer.read(2), byteorder='little')
            skin_alpha = int.from_bytes(buffer.read(2), byteorder='little')
            sex = int.from_bytes(buffer.read(1), byteorder='little')
            badge = int.from_bytes(buffer.read(2), byteorder='little')
            wing_jump = int.from_bytes(buffer.read(2), byteorder='little')
            
            username_bytes = bytearray()
            while True:
                byte = buffer.read(1)
                if not byte or byte == b'\x00':
                    break
                username_bytes.extend(byte)
            username = username_bytes.decode('utf-8')
            
            clothing1 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing2 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing3 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing4 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing5 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing6 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing7 = int.from_bytes(buffer.read(2), byteorder='little')
            clothing8 = int.from_bytes(buffer.read(2), byteorder='little')
            
            buffer.read(4 + 2 + 8 + 2 + 10)
            
            buffer.read(2)
            side_badge = int.from_bytes(buffer.read(2), byteorder='little')
            visible = bool(int.from_bytes(buffer.read(1), byteorder='little'))
            noclip = bool(int.from_bytes(buffer.read(1), byteorder='little'))
            frozen = bool(int.from_bytes(buffer.read(1), byteorder='little'))
            buffer.read(1)
            jump_height = int.from_bytes(buffer.read(2), byteorder='little')
            walk_speed = int.from_bytes(buffer.read(2), byteorder='little')
            
            buffer.read(5)
            staff_badge = int.from_bytes(buffer.read(1), byteorder='little')
            buffer.read(3)
            
            return identifier, skin_color_red, skin_color_green, skin_color_blue, skin_alpha, sex, badge, wing_jump, username, clothing1, clothing2, clothing3, clothing4, clothing5, clothing6, clothing7, clothing8, side_badge, visible, noclip, frozen, jump_height, walk_speed, staff_badge
        
        async def extract_update_position(data: bytes):
            pkt = io.BytesIO(data)

            identifier = struct.unpack("<L", pkt.read(4))
            destroy = struct.unpack("<B", pkt.read(1))

            x = -1
            y = -1

            if destroy == 0:
                x = struct.unpack("<H", pkt.read(2))
                y = struct.unpack("<H", pkt.read(2))
            
            pkt.close()

            return identifier, destroy, x, y