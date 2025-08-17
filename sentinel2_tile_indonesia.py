#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd
from shapely.geometry import box
import os
from pathlib import Path

def crop_sentinel_tiles_indonesia():
    """
    Crop Sentinel-2 tiles untuk area Indonesia dan tambahkan koordinat lat-lon
    """
    
    # Path file input dan output
    input_shapefile = r"Sentinel-2-Shapefile-Index-master\sentinel_2_index_shapefile.shp"
    output_dir = Path(r"tile_indonesia")
    output_shapefile = output_dir / "sentinel_tiles_indonesia.shp"
    output_csv = output_dir / "sentinel_tiles_indonesia.csv"  # Tambahan untuk CSV
    
    # Bounding box Indonesia [min_lon, min_lat, max_lon, max_lat]
    bbox_indonesia = [95.0, -11.0, 141.0, 6.0]
    
    print("=" * 60)
    print("CROP SENTINEL-2 TILES UNTUK INDONESIA")
    print("=" * 60)
    
    try:
        # 1. Baca shapefile Sentinel-2 UTM Tiling Grid
        print(f"📂 Membaca shapefile: {input_shapefile}")
        gdf_sentinel = gpd.read_file(input_shapefile)
        print(f"✅ Berhasil membaca {len(gdf_sentinel)} tiles")
        print(f"   Kolom yang tersedia: {list(gdf_sentinel.columns)}")
        print(f"   CRS: {gdf_sentinel.crs}")
        
        # 2. Buat polygon bounding box Indonesia
        print(f"\n🗺️ Membuat bounding box Indonesia: {bbox_indonesia}")
        bbox_polygon = box(bbox_indonesia[0], bbox_indonesia[1], 
                          bbox_indonesia[2], bbox_indonesia[3])
        
        # Buat GeoDataFrame untuk bounding box dengan CRS yang sama
        gdf_bbox = gpd.GeoDataFrame([1], geometry=[bbox_polygon], crs="EPSG:4326")
        
        # Pastikan kedua GeoDataFrame menggunakan CRS yang sama
        if gdf_sentinel.crs != gdf_bbox.crs:
            print(f"   Mengubah CRS dari {gdf_sentinel.crs} ke {gdf_bbox.crs}")
            gdf_sentinel = gdf_sentinel.to_crs(gdf_bbox.crs)
        
        # 3. Crop tiles yang berada dalam bounding box Indonesia
        print(f"\n✂️ Melakukan crop tiles yang berada dalam area Indonesia...")
        gdf_cropped = gpd.overlay(gdf_sentinel, gdf_bbox, how='intersection')
        print(f"✅ Berhasil crop {len(gdf_cropped)} tiles untuk area Indonesia")
        
        if len(gdf_cropped) == 0:
            print("⚠️ Tidak ada tiles yang berada dalam area Indonesia!")
            return
        
        # 4. Hitung centroid (titik tengah) setiap tile untuk mendapatkan lat-lon
        print(f"\n📍 Menghitung koordinat latitude-longitude untuk setiap tile...")
        
        # Pastikan menggunakan CRS geografis (WGS84) untuk menghitung centroid
        gdf_geo = gdf_cropped.to_crs("EPSG:4326")
        centroids = gdf_geo.geometry.centroid
        
        # Tambahkan kolom latitude dan longitude
        gdf_cropped['longitude'] = centroids.x
        gdf_cropped['latitude'] = centroids.y
        
        # 5. Buat DataFrame hasil dengan kolom yang diinginkan
        # Pastikan kolom 'Name' ada, jika tidak gunakan kolom pertama sebagai nama
        name_column = None
        possible_name_columns = ['Name', 'name', 'NAME', 'tile_id', 'TILE_ID']
        
        for col in possible_name_columns:
            if col in gdf_cropped.columns:
                name_column = col
                break
        
        if name_column is None:
            # Jika tidak ada kolom nama yang sesuai, gunakan kolom pertama
            name_column = gdf_cropped.columns[0]
            print(f"⚠️ Kolom 'Name' tidak ditemukan, menggunakan '{name_column}'")
        
        # Buat GeoDataFrame hasil dengan kolom yang diinginkan
        result_gdf = gpd.GeoDataFrame({
            'name': gdf_cropped[name_column],
            'latitude': gdf_cropped['latitude'],
            'longitude': gdf_cropped['longitude'],
            'geometry': gdf_cropped['geometry']
        }, crs=gdf_cropped.crs)
        
        # 6. Buat direktori output jika belum ada
        print(f"\n📁 Membuat direktori output: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 7. Simpan hasil ke shapefile
        print(f"💾 Menyimpan hasil ke shapefile: {output_shapefile}")
        result_gdf.to_file(output_shapefile)
        
        # 8. Simpan hasil ke CSV (tanpa kolom geometry)
        print(f"💾 Menyimpan hasil ke CSV: {output_csv}")
        # Buat DataFrame tanpa kolom geometry untuk CSV
        csv_df = pd.DataFrame({
            'name': result_gdf['name'],
            'latitude': result_gdf['latitude'],
            'longitude': result_gdf['longitude']
        })
        csv_df.to_csv(output_csv, index=False, encoding='utf-8')
        
        # 9. Tampilkan ringkasan hasil
        print(f"\n" + "=" * 60)
        print("RINGKASAN HASIL")
        print("=" * 60)
        print(f"📊 Total tiles Indonesia: {len(result_gdf)}")
        print(f"📂 File Shapefile: {output_shapefile}")
        print(f"📂 File CSV: {output_csv}")
        print(f"🗂️ Kolom yang disimpan: {list(result_gdf.columns)}")
        
        # Tampilkan 10 data pertama
        print(f"\n📋 Preview 10 data pertama:")
        preview_df = result_gdf.drop('geometry', axis=1).head(10)
        print(preview_df.to_string(index=False))
        
        # Statistik koordinat
        print(f"\n📍 Statistik Koordinat:")
        print(f"   Latitude  - Min: {result_gdf['latitude'].min():.4f}, Max: {result_gdf['latitude'].max():.4f}")
        print(f"   Longitude - Min: {result_gdf['longitude'].min():.4f}, Max: {result_gdf['longitude'].max():.4f}")
        
        print(f"\n✅ PROSES SELESAI! File berhasil disimpan dalam format Shapefile dan CSV.")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File tidak ditemukan - {e}")
        print("   Pastikan path file input sudah benar!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Pastikan semua library sudah terinstall: pip install geopandas shapely pandas")

def check_requirements():
    """
    Cek apakah semua library yang dibutuhkan sudah terinstall
    """
    required_packages = ['geopandas', 'shapely', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Library yang belum terinstall: {', '.join(missing_packages)}")
        print(f"   Install dengan: pip install {' '.join(missing_packages)}")
        return False
    return True

if __name__ == "__main__":
    print("🐍 Script Crop Sentinel-2 Tiles Indonesia")
    print("   Oleh: Assistant AI")
    print()
    
    # Cek requirements
    if check_requirements():
        crop_sentinel_tiles_indonesia()
    else:
        print("\n⚠️ Silakan install library yang dibutuhkan terlebih dahulu!")