# 🛰️ Sentinel-2 Indonesia Tiles Cropper

Script Python untuk memotong (crop) Sentinel-2 UTM Tiling Grid sesuai dengan area Indonesia dan menambahkan koordinat latitude-longitude untuk setiap tile. Script ini menghasilkan output dalam format Shapefile dan CSV.

## 📋 Deskripsi

Script ini dirancang untuk:
- Memotong grid tiles Sentinel-2 yang berada dalam bounding box Indonesia
- Menghitung koordinat centroid (latitude-longitude) untuk setiap tile
- Menyimpan hasil dalam format Shapefile (.shp) dan CSV (.csv)
- Memberikan statistik dan preview data hasil cropping

## 🎯 Fitur Utama

- ✅ **Cropping Otomatis**: Memotong tiles Sentinel-2 sesuai batas Indonesia
- 📍 **Koordinat Centroid**: Menghitung latitude-longitude titik tengah setiap tile
- 📊 **Dual Output**: Menghasilkan file Shapefile dan CSV
- 🔍 **Preview Data**: Menampilkan statistik dan preview hasil
- 🛡️ **Error Handling**: Penanganan error yang informatif
- 📋 **Requirements Check**: Pengecekan library yang dibutuhkan

## 🔧 Requirements

### Library Python yang Dibutuhkan:
```
geopandas
shapely
pandas
```

### Instalasi Requirements:
```bash
pip install geopandas shapely pandas
```

## 📁 Struktur File Input

Script ini membutuhkan:
- **Sentinel-2 Shapefile Index**: File shapefile yang berisi grid tiles Sentinel-2
- **Path Input**: File `.shp` dari Sentinel-2 UTM Tiling Grid

## 🚀 Cara Penggunaan

### 1. Persiapan
```bash
# Clone repository
git clone https://github.com/username/sentinel-2-indonesia-tiles-cropper.git
cd sentinel-2-indonesia-tiles-cropper

# Install dependencies
pip install geopandas shapely pandas
```

### 2. Konfigurasi Path
Edit path file input dan output dalam script:
```python
# Path file input
input_shapefile = r"C:\path\to\sentinel_2_index_shapefile.shp"

# Path direktori output
output_dir = Path(r"D:\output\directory")
```

### 3. Menjalankan Script
```bash
python sentinel_crop.py
```

## 📊 Output yang Dihasilkan

Script akan menghasilkan dua file output:

### 1. **Shapefile** (`sentinel_tiles_indonesia.shp`)
- Format: Shapefile dengan file pendukung (.shx, .dbf, .prj)
- Kolom: `name`, `latitude`, `longitude`, `geometry`
- Penggunaan: Analisis spasial di QGIS, ArcGIS, dll

### 2. **CSV** (`sentinel_tiles_indonesia.csv`)
- Format: Comma Separated Values
- Kolom: `name`, `latitude`, `longitude`
- Penggunaan: Excel, Google Sheets, analisis data tabular

### Contoh Format CSV:
```csv
name,latitude,longitude
48MYT,-6.2345,106.7890
48MZT,-6.1234,106.8901
49MCA,-6.0123,107.0012
```

## 🗺️ Area Coverage

Script menggunakan bounding box Indonesia:
- **Longitude**: 95.0° - 141.0° BT
- **Latitude**: -11.0° - 6.0° LU

Koordinat sistem: **WGS84 (EPSG:4326)**

## 🔧 Kustomisasi

### Mengubah Bounding Box
Untuk mengubah area coverage, edit variabel `bbox_indonesia`:
```python
# Format: [min_lon, min_lat, max_lon, max_lat]
bbox_indonesia = [95.0, -11.0, 141.0, 6.0]
```

### Mengubah Kolom Output
Edit bagian pembuatan `result_gdf` untuk menambah/mengubah kolom:
```python
result_gdf = gpd.GeoDataFrame({
    'name': gdf_cropped[name_column],
    'latitude': gdf_cropped['latitude'],
    'longitude': gdf_cropped['longitude'],
    'custom_column': gdf_cropped['custom_data'],  # Tambahan
    'geometry': gdf_cropped['geometry']
}, crs=gdf_cropped.crs)
```


## 📝 Changelog

### v1.1 (Latest)
- ✅ Menambahkan export ke format CSV
- ✅ Perbaikan handling kolom nama tile
- ✅ Penambahan encoding UTF-8 untuk CSV

### v1.0
- ✅ Fitur dasar cropping Sentinel-2 tiles
- ✅ Export ke format Shapefile
- ✅ Penghitungan koordinat centroid


## 📄 Lisensi

Copyright (c) 2025 Ilham Habibullah



## 👤 Author

**Ilham Habibullah**
- Instagram: [@masllhamm_](https://www.instagram.com/masllhamm_)

## 🙏 Acknowledgments

- [ESA Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) untuk data satelit
- [Sentinel Tile UTM Grid](https://catalogue.eatlas.org.au/geonetwork/srv/eng/catalog.search#/metadata/f7468d15-12be-4e3f-a246-b2882a324f59/formatters/xsl-view?root=div&view=advanced) untuk tile seluruh dunia
- [GeoPandas](https://geopandas.org/) untuk library geospatial Python
- Komunitas open source yang mendukung pengembangan tools geospatial

---

⭐ **Jika project ini membantu, jangan lupa beri star!** ⭐
