import sqlite3
from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')
DB_NAME = 'techfix.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            watts INTEGER,
            image TEXT,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            brandKey TEXT NOT NULL,
            slogan TEXT,
            description TEXT,
            bgGradient TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prebuilts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            specs TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        brands = [
            ('nvidia', 'NVIDIA', 'Nvidia', 'GeForce RTX Serie 40 Ada Lovelace', 'Líder absoluto en rendimiento gráfico con trazado de rayos y DLSS 3.5.', 'from-emerald-950/60 via-tech-card to-tech-card'),
            ('intel', 'INTEL', 'Intel', 'Procesadores Intel Core 14va Generación', 'Rendimiento híbrido extremo para gaming competitivo y creación de contenido.', 'from-blue-950/60 via-tech-card to-tech-card'),
            ('amd', 'AMD', 'AMD', 'Ryzen 7000 Series & 3D V-Cache', 'Los procesadores con la tecnología de caché 3D más rápida del mundo para videojuegos.', 'from-red-950/60 via-tech-card to-tech-card'),
            ('asus', 'ASUS ROG', 'Asus', 'Republic of Gamers', 'Motherboards, Placas de video y sistemas de refrigeración de calidad entusiasta.', 'from-rose-950/60 via-tech-card to-tech-card'),
            ('corsair', 'CORSAIR', 'Corsair', 'Memorias DDR5 y Fuentes Modulares', 'Kits de RAM de ultra alta velocidad y componentes con ecosistema iCUE.', 'from-amber-950/60 via-tech-card to-tech-card'),
            ('logitech', 'LOGITECH G', 'Logitech', 'Periféricos eSports LIGHTSPEED', 'Mouse ultraligeros y periféricos inalámbricos de nivel profesional.', 'from-cyan-950/60 via-tech-card to-tech-card'),
            ('msi', 'MSI', 'MSI', 'True Gaming Hardware', 'Tarjetas gráficas con disipadores Tri Frozr y motherboards de alto desempeño.', 'from-red-950/60 via-tech-card to-tech-card'),
            ('gigabyte', 'GIGABYTE', 'Gigabyte', 'Team Up. Fight On.', 'Monitores eSports de alta tasa de refresco y componentes AORUS.', 'from-orange-950/60 via-tech-card to-tech-card'),
            ('kingston', 'KINGSTON', 'Kingston', 'Kingston Fury Memory', 'Unidades SSD M.2 NVMe PCIe 4.0 y memorias RAM Fury DDR5.', 'from-red-950/50 via-tech-card to-tech-card'),
            ('samsung', 'SAMSUNG', 'Samsung', 'Almacenamiento NVMe y Pantallas Odyssey', 'Discos M.2 de velocidad máxima e iluminación curvo en monitores.', 'from-blue-950/60 via-tech-card to-tech-card'),
            ('hyperx', 'HYPERX', 'HyperX', 'We\'re All Gamers', 'Auriculares con sonido envolvente y teclados mecánicos de alta durabilidad.', 'from-rose-950/60 via-tech-card to-tech-card')
        ]
        cursor.executemany('INSERT INTO brands VALUES (?, ?, ?, ?, ?, ?)', brands)

        products = [
            ('gpu-1', 'Nvidia GeForce RTX 4090 24GB GDDR6X', 'Nvidia', 'gpu', 2850000, 450, 'https://imgs.search.brave.com/Zedp4tvS_bf-Yjs59RWwFRrqRTd5jmrIMdsf8Lq-wLE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9j1C5u/ZXdlZ2dpbWFnZXMu/Y29tL3Byb2R1Y3Rp/bWFnZS9uYjMwMC9C/RENBUzIzMDEwNzA0/VEEyWkI1LmpwZw', 'La placa gráfica más potente para gaming 4K con tecnología DLSS 3.5 y disipación de triple cooler.'),
            ('gpu-2', 'Asus ROG Strix RTX 4080 Super 16GB GDDR6X', 'Asus', 'gpu', 1650000, 320, 'https://imgs.search.brave.com/PXuq-rpVomZ35C2dvX8rvYmKO2NaAFrcxHZyfm0y3sw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cGNzdHVkaW8uaW4v/d3AtY29udGVudC91/cGxvYWRzLzIwMjUv/MDEvQXN1cy1Sb2ct/U3RyaXgtUnR4LTQw/ODAtU3VwZXItMTZH/Yi1HRERSNlgtT2Mt/RWRpdGlvbi1HcmFw/aGljcy1DYXJkLTEt/MS53ZWJw', 'Edición especial ROG Strix con chasis de aluminio, RGB direccionable y cámaras de vapor.'),
            ('gpu-3', 'MSI Gaming X Slim RTX 4070 Super 12GB', 'MSI', 'gpu', 980000, 220, 'https://thumb.pccomponentes.com/w-530-530/articles/1081/10810493/158-msi-gaming-x-slim-geforce-rtx-4070-super-12gb-gddr6x-dlss3.jpg', 'Arquitectura Ada Lovelace ultrasilenciosa con diseño de tres ventiladores TORX Fan 5.0.'),
            ('gpu-4', 'Gigabyte GeForce RTX 4060 Eagle OC 8GB', 'Gigabyte', 'gpu', 480000, 115, 'https://imgs.search.brave.com/Yz2oBd5T6INpmLoOSZst5oRzT0EjPVlQ5j2mTy7XM5w/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9odHRw/Mi5tbHN0YXRpYy5j/b20vRF9OUV9OUF84/NDI2NTktTUxVNzc5/NzQyMzEwMTlfMDcy/MDI0LU8ud2VicA', 'Excelente rendimiento en 1080p y 1440p con consumo energético reducido y enfriamiento Windforce.'),
            ('cpu-1', 'Intel Core i9-14900K 24-Cores 5.8GHz LGA1700', 'Intel', 'cpu', 920000, 250, 'https://imgs.search.brave.com/T1qUk1ssVGdLdgOnEB7Bhry8DqIB3ltX47nUX9SC13A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jb21w/dXRlY2hzdG9yZS5p/bi9tZWRpYS91cGxv/YWRzL3dwLzIwMjMv/MTAvSW50ZWwtQ29y/ZS1pOS0xNDkwMEst/MTR0aC1HZW4tMjQt/Q29yZS04UDE2RS1M/R0EtMTcwMC1EZXNr/dG9wLVByb2Nlc3Nv/ci0xLTEuanBn', 'Microprocesador entusiasta Intel de 24 núcleos y 32 hilos desbloqueado para overclocking.'),
            ('cpu-2', 'AMD Ryzen 7 7800X3D 5.0GHz Socket AM5', 'AMD', 'cpu', 650000, 120, 'https://imgs.search.brave.com/skGmLD8nY4TOi1mGCELyOgr8h6sYY-LxgWeCbKOktr0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/b3ZlcmNsb2NrZXJz/LmNvLnVrL2ltYWdl/cy/DUC0zRFQtQU0v/NTczMzlmZmJhZmQ5/YTc2M2NhOTc3NTNl/Y2QzMzc1ZTEuanBn', 'Procesador con tecnología 3D V-Cache diseñado específicamente para máximo FPS en videojuegos.'),
            ('cpu-3', 'Intel Core i5-13400F 10 Núcleos 4.6GHz', 'Intel', 'cpu', 310000, 65, 'https://imgs.search.brave.com/Ja_RKNgwLWMZdq_56-8MnZkP-AkQzJ6eEXdx2ePDr9c/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zMy1z/YS1lYXN0LTEuYW1h/em9uYXdzLmNvbS9z/YWFzYXJnZW50aW5h/L3ZyQk9NeVNXVDhy/YUhQQzlvUWJ0L2lt/YWdlbg', 'Procesador equilibrado de 10 núcleos ideal para ensambles de excelente costo/beneficio.'),
            ('moth-1', 'Asus ROG Strix Z790-F Gaming WiFi LGA1700', 'Asus', 'motherboard', 480000, 40, 'https://imgs.search.brave.com/cukyQUUZi8ygBWcG5G-etQe_nNaqG-YfaLf1Pq2Ws_0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NzFvcDZKNHFPVUwu/anBn', 'Placa base de gama alta con soporte PCIe 5.0, WiFi 6E e iluminación Aura Sync.'),
            ('moth-2', 'MSI MAG B650 Tomahawk WiFi AM5', 'MSI', 'motherboard', 320000, 35, 'https://imgs.search.brave.com/9mcq58iAkr0JqJ0clUB0C-aDPoaNo4GVUA355QZ7gvk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jMS5u/ZXdlZ2dpbWFnZXMu/Y29tL3Byb2R1Y3Rp/bWFnZS9uYjY0MC8x/My0xNDQtNTU3LTA2/LmpwZw', 'Motherboard Socket AM5 con robusto disipador sobre las fases VRM y soporte DDR5.'),
            ('ram-1', 'Corsair Vengeance RGB DDR5 32GB (2x16GB) 6000MHz', 'Corsair', 'ram', 185000, 15, 'https://imgs.search.brave.com/ec6l-iVYxO6YVyMceqGiQBT6HCk4gNRYGfBkKnpC1qo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jY2lt/Zy5jYW5hZGFjb21w/dXRlcnMuY29tL1By/b2R1Y3RzLzI1MHgy/NTAvMjk4LzE4My8y/NTU4ODcvMjkyMjE1/LmpwZw', 'Par de memorias RAM DDR5 de alta frecuencia con disipador de aluminio negro e iluminación ARGB.'),
            ('ram-2', 'Kingston Fury Beast 16GB DDR4 3200MHz', 'Kingston', 'ram', 52000, 10, 'https://imgs.search.brave.com/lvrlOKMwFk5qPsDABuvWOgnZ3SjwfevD4ySgLvKG3i4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/dmVuZXguY29tLmFy/L3Byb2R1Y3RzX2lt/YWdlcy8xNjQyNTI4/MTI0X3Npbl90X3R1/bG8tMS5wbmc', 'Módulo DDR4 con disipador pasivo optimizado para plataformas Intel y AMD.'),
            ('st-1', 'Samsung 990 PRO NVMe M.2 SSD 2TB PCIe 4.0', 'Samsung', 'storage', 240000, 10, 'https://imgs.search.brave.com/OEnXSC4NkKijyG1y5PG780Tyjhgz6Ut5gbXbAY1JcEM/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NDFKZjJ5R3BBZ0wu/anBn', 'Unidad de estado sólido M.2 ultra veloz alcanzando hasta 7.450 MB/s de lectura continua.'),
            ('st-2', 'SSD NVMe Kingston NV2 1TB M.2 PCIe 4.0', 'Kingston', 'storage', 95000, 5, 'https://imgs.search.brave.com/dvzC3_gZZHnEZRF8jxLzp5F04P8uFEploaSQf7fG9UI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wZXJp/dGFzdGVjaC5jb20u/YXIvd3AtY29udGVu/dC91cGxvYWRzLzIw/MjIvMTEvU1NELTFU/Qi1OVjItS0lOR1NU/T04tMDAyLmpwZw', 'SSD M.2 compacto y rápido para iniciar juegos y aplicaciones pesadas en segundos.'),
            ('psu-1', 'Corsair RM850x 850W 80 Plus Gold Modular', 'Corsair', 'psu', 210000, 0, 'https://imgs.search.brave.com/-4vOaJS8vt0J9XRzhtIkph3F8s_DE-6jt70cxrzGVv0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9hcHAu/Y29udGFiaWxpdW0u/Y29tL2ZpbGVzL2V4/cGxvcmVyLzQ4NDI4/L1Byb2R1Y3Rvcy1T/ZXJ2aWNpb3MvY29u/Y2VwdG8tMTQwMDAw/MzIuanBn', 'Fuente de alimentación 100% modular con capacitores japoneses a 105°C y certificación Gold.'),
            ('mon-1', 'Monitor Gigabyte M27Q 27" 2K QuadHD 170Hz IPS', 'Gigabyte', 'monitores', 490000, 45, 'https://imgs.search.brave.com/GZ-qZwJgPp5aRuvPE2bv6bgMGZq7IttAfNmDgWM9WKc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pNS53/YWxtYXJ0aW1hZ2Vz/LmNvbS9zZW8vR0lH/QUJZVEUtTTI3US0y/Ny0xNzBIei0xNDQw/UC1LVk0tR2FtaW5n/LU1vbml0b3ItMjU2/MC14LTE0NDAtU1Mt/SVBTLTAtNW1zLU1Q/UlQtOTItRENJLVAz/LUhEUi1SZWFkeS1G/cmVlU3luYy1QcmVt/aXVtLTF4LURpc3Bs/YXlQb3J0LTEtMi0y/eC1IRE1JLTItMC0y/eF84dkE5Zjg0NC0z/MDJiLTRmNmMtYjNl/Zi0xOWVjNTcyY2Q0/NzEuNDkwMzg3OTAw/NTE3MjQzNmQ0M2Ey/MmY2NDg5NDA4MWUu/anBlZz9vZG5IZWln/aHQ9NTczJm9kbldp/ZHRoPTU3MyZvZG5C/Zz1GRkZGRkY', 'Pantalla 1440p con panel Super Speed IPS, tiempo de respuesta de 0.5ms y KVM integrado.'),
            ('mon-2', 'Monitor Gamer Samsung Odyssey G4 24" 240Hz IPS', 'Samsung', 'monitores', 280000, 35, 'https://imgs.search.brave.com/KRhcYOwJlvyVZpgEjES04s1C0n_u5q06R-NWpYBTPtI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9odHRw/Mi5tbHN0YXRpYy5j/b20vRF9OUV9OUF82/Nzc2NzYtTUxBOTEz/NDAxNjkwNjVfMDgy/MDI1LU8ud2VicA', 'Tasa de refresco ultra rápida de 240Hz y compatibilidad con Nvidia G-Sync para eSports.'),
            ('peri-1', 'Mouse Wireless Logitech G PRO X Superlight 2 (Black)', 'Logitech', 'perifericos', 168000, 0, 'https://imgs.search.brave.com/OdXbSrU7oW2QXN2AbGAfr7JHj-o80MUDeWlPqh77jlg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NTF1eThnT0ctaUwu/anBn', 'Ratón eSports de nivel profesional ultraligero (60g) con switches híbridos LIGHTFORCE.'),
            ('peri-2', 'Teclado Mecánico HyperX Alloy Origins Core RGB', 'HyperX', 'perifericos', 75000, 0, 'https://imgs.search.brave.com/Dg399sL1UuJYl4cTw6fL0HFKw0Bjzh_LDi1Yrmhwh8I/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9yb3cu/aHlwZXJ4LmNvbS9j/ZG4vc2hvcC9maWxl/cy9rZi00Lhy5l/eGVyZS1hbGxveS1vcmln/aW5zLWNvcmUtbWVj/aGFuaWNhbC1nYW1p/bmcta2V5Ym9hcmQu/anBn', 'Teclado mecánico formato TKL en chasis completo de aluminio con switches red lineales.')
        ]
        cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?)', products)

        prebuilts = [
            ('pc-1', 'TechFix Gamer Starter 1080p', 890000, 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=800&q=80', 'Intel Core i5-13400F|Nvidia GeForce RTX 4060 8GB|16GB RAM DDR4 3200MHz|SSD NVMe 1TB M.2|Fuente 600W 80 Plus'),
            ('pc-2', 'TechFix Cyber-Gamer Advanced AM5', 1550000, 'https://cdn.noxiestore.com/13-10-2026-12-52-49_d374cc0bbdbdfdf7d3696c71b2d93acd_1portadajoltconplaca.webp', 'AMD Ryzen 5 7600 AM5|MSI RTX 4070 Super 12GB|32GB RAM DDR5 6000MHz RGB|SSD NVMe 1TB Kingston NV2|Watercooling 240mm ARGB'),
            ('pc-3', 'TechFix Pro Streamer i7 Edition', 2450000, 'https://imgs.search.brave.com/SbXAeWHTzsBGPe2_v5_rsBVriShHx52l6bh43yXcmlM/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9waXNj/ZXMuYmJ5c3RhdGlj/LmNvbS9pbWFnZTIv/QmVzdEJ1eV9VUy9p/bWFnZXMvcHJvZHVj/dHMvOGYyNzRmYmUt/YWVmZi00ZWY3LTg0/NzYtMGZlNTRiM2I3/NmVmLmpwZw', 'Intel Core i7-14700K 20-Cores|Asus ROG Strix RTX 4070 Ti Super|32GB RAM DDR5 Corsair Vengeance|SSD NVMe 2TB Samsung 990 PRO|Gabinete Aquario Cristal 4x ARGB'),
            ('pc-4', 'TechFix Ultra Beast 4K X3D', 3450000, 'https://cdn.qloud.ar/274/09-01-2026-04-01-01_8.webp', 'AMD Ryzen 7 7800X3D|Nvidia GeForce RTX 4080 Super 16GB|64GB DDR5 RAM 6000MHz Corsair|SSD NVMe 2TB PCIe 4.0|Fuente 850W Gold Modular')
        ]
        
        for p in prebuilts:
            cursor.execute('INSERT INTO prebuilts VALUES (?, ?, ?, ?, ?)', p)

        conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM brands')
    brands = [{'id': r[0], 'name': r[1], 'brandKey': r[2], 'slogan': r[3], 'desc': r[4], 'bgGradient': r[5]} for r in cursor.fetchall()]
    cursor.execute('SELECT * FROM products')
    products = [{'id': r[0], 'name': r[1], 'brand': r[2], 'category': r[3], 'price': r[4], 'watts': r[5], 'image': r[6], 'desc': r[7]} for r in cursor.fetchall()]
    cursor.execute('SELECT * FROM prebuilts')
    prebuilts = [{'id': r[0], 'name': r[1], 'price': r[2], 'image': r[3], 'specs': r[4].split('|')} for r in cursor.fetchall()]
    conn.close()
    return jsonify({'brands': brands, 'products': products, 'prebuilts': prebuilts})

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    items_str = str(data.get('items'))
    total = data.get('total')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (items, total) VALUES (?, ?)', (items_str, total))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'order_id': order_id})

@app.route('/api/contacts', methods=['POST'])
def create_contact():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (data.get('name'), data.get('email'), data.get('message')))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
