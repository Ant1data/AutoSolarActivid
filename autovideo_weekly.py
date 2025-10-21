import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, timezone
import calendar
import requests
from concurrent.futures import ThreadPoolExecutor
import re
from scipy.stats import pearsonr

# --- Parameters ---
FPS = 60
DURATION_SEC = 15
TOTAL_FRAMES = FPS * DURATION_SEC
MAX_WEEKLY_VIDEOS = 4

# --- Base directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOHO_DIR = os.path.join(BASE_DIR, "SOHO_7days")
PROTON_DIR = os.path.join(BASE_DIR, "Protons_7days")
NEUTRON_DIR = os.path.join(BASE_DIR, "Neutrons_7days")
SOLAR_DIR = os.path.join(BASE_DIR, "Solar_Activity_7days")
for d in [SOHO_DIR, PROTON_DIR, NEUTRON_DIR, SOLAR_DIR]:
    os.makedirs(d, exist_ok=True)

# =========================
# SOHO
# =========================
def download_soho_images(date):
    date_str = date.strftime('%Y%m%d')
    year = date.strftime('%Y')
    folder_date_str = date.strftime('%d%m%Y')
    base_folder = os.path.join(SOHO_DIR, f"soho_{folder_date_str}_images")
    os.makedirs(base_folder, exist_ok=True)
    lst_url = f"https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/{year}/c2/{date_str}/.full_512.lst"
    r = requests.get(lst_url, timeout=10)
    r.raise_for_status()
    image_filenames = r.text.strip().split('\n')
    def download_image(img_name):
        img_url = f"https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/{year}/c2/{date_str}/{img_name}"
        img_path = os.path.join(base_folder, img_name)
        if not os.path.exists(img_path):
            resp = requests.get(img_url, timeout=10)
            resp.raise_for_status()
            with open(img_path, 'wb') as f:
                f.write(resp.content)
        return img_path
    with ThreadPoolExecutor(max_workers=10) as executor:
        image_paths = list(executor.map(download_image, image_filenames))
    return sorted(image_paths)

def create_soho_video(image_paths, output_path):
    frame_width, frame_height = 512, 512
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, FPS, (frame_width, frame_height))
    if len(image_paths) < TOTAL_FRAMES:
        indices = np.linspace(0, len(image_paths)-1, TOTAL_FRAMES)
        frames_to_use = [image_paths[int(i)] for i in indices]
    else:
        frames_to_use = image_paths[:TOTAL_FRAMES]
    for img_path in frames_to_use:
        img = Image.open(img_path).convert('RGB').resize((frame_width, frame_height))
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.putText(frame, "NASA (R)", (frame_width-120, frame_height-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2, cv2.LINE_AA)
        video_writer.write(frame)
    video_writer.release()
    # Supprimer les images temporaires
    for img_path in image_paths:
        os.remove(img_path)
    folder = os.path.dirname(image_paths[0])
    if os.path.exists(folder):
        os.rmdir(folder)
    return output_path

def merge_soho_videos_temporally(video_paths, output_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    cap = cv2.VideoCapture(video_paths[0])
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    out = cv2.VideoWriter(output_path, fourcc, FPS, (w, h))
    for path in video_paths:
        cap = cv2.VideoCapture(path)
        while True:
            ret, frame = cap.read()
            if not ret: break
            out.write(frame)
        cap.release()
    out.release()
    return output_path

# =========================
# PROTONS
# =========================
def get_noaa_proton_data_for_week():
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["time_tag"] = pd.to_datetime(df["time_tag"], utc=True)
    df["flux"] = pd.to_numeric(df["flux"], errors="coerce")
    df["energy_value"] = df["energy"].str.extract(r'>=(\d+)').astype(float)
    now_utc = datetime.now(timezone.utc)
    start = (now_utc - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = now_utc
    df = df[df["time_tag"].between(start, end)]
    df = df[df["energy_value"].isin([10,50,100,500])]
    return df, start, end

def create_proton_video(df, start, end, output_path):
    fig, ax = plt.subplots(figsize=(12,4))
    energies = sorted(df["energy_value"].unique())
    time_range = pd.date_range(start, end, periods=TOTAL_FRAMES)
    frame_images = []
    for t in time_range:
        ax.clear()
        for energy in energies:
            sub = df[df["energy_value"]==energy]
            sub_plot = sub[sub["time_tag"] <= t]
            ax.plot(sub_plot["time_tag"], sub_plot["flux"], label=f">= {int(energy)} MeV", linewidth=1.8)
        ax.set_xlim(start, end)
        current_data = df[df["time_tag"] <= t]
        if not current_data.empty:
            ymin = current_data["flux"].min()*0.9
            ymax = current_data["flux"].max()*1.1
            ax.set_ylim(ymin, ymax)
        ax.set_xlabel("UTC Time")
        ax.set_ylabel("Flux (protons·cm⁻²·s⁻¹·sr⁻¹)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        plt.tight_layout()
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        frame_images.append(img)
    plt.close(fig)
    h, w, _ = frame_images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, FPS, (w, h))
    for img in frame_images:
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.putText(frame, "NOAA (R)", (w-120, h-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA)
        video_writer.write(frame)
    video_writer.release()
    return output_path

# =========================
# NEUTRONS
# =========================
def fetch_neutron_data(start_date, end_date, stations):
    """
    Récupère les données NMDB pour les stations listées entre start_date et end_date.
    Renvoie un DataFrame et la liste des colonnes de stations valides.
    """
    url = (
        "https://www.nmdb.eu/nest/draw_graph.php?formchk=1&" +
        "&".join([f"stations[]={s}" for s in stations]) +
        "&output=ascii&tabchoice=ori&dtype=corr_for_efficiency&date_choice=bydate&"
        f"start_year={start_date.year}&start_month={start_date.month:02d}&start_day={start_date.day:02d}&start_hour=00&start_min=00&"
        f"end_year={end_date.year}&end_month={end_date.month:02d}&end_day={end_date.day:02d}&end_hour=00&end_min=00&tresolution=1&yunits=0"
    )

    r = requests.get(url, timeout=20)
    r.raise_for_status()

    # Filtrer uniquement les lignes qui commencent par une date
    lines = [l.strip() for l in r.text.splitlines() if re.match(r'^\d{4}-\d{2}-\d{2}', l)]
    if not lines:
        raise ValueError("No valid data found from NMDB.")

    data = [line.split(";") for line in lines]

    # Construction du DataFrame
    df = pd.DataFrame(data[1:], columns=[c.strip() for c in data[0]])
    df["datetime"] = pd.to_datetime(df.iloc[:,0], errors="coerce")
    df = df.dropna(subset=["datetime"])

    station_cols = []
    for c in df.columns[1:-1]:
        # Forcer la colonne à une Series 1D
        col_series = pd.Series(df[c].values.flatten())
        # Convertir en numérique
        df[c] = pd.to_numeric(col_series, errors="coerce")
        if df[c].notna().any():
            station_cols.append(c)

    if not station_cols:
        raise ValueError("No valid neutron station columns found.")

    return df, station_cols

def calculate_correlations(df, station_cols, stations):
    correlations = {}
    for i, station1 in enumerate(stations):
        for j, station2 in enumerate(stations):
            if i < j and j < len(station_cols):
                data1 = df[station_cols[i]].dropna()
                data2 = df[station_cols[j]].dropna()
                common_index = data1.index.intersection(data2.index)
                data1_aligned = data1.loc[common_index]
                data2_aligned = data2.loc[common_index]
                if len(data1_aligned) > 0 and len(data2_aligned) > 0:
                    r, _ = pearsonr(data1_aligned, data2_aligned)
                    correlations[f"{station1}_vs_{station2}"] = r
    return correlations

def create_neutron_video(df, station_cols, stations, altitudes, output_path):
    fig, ax = plt.subplots(figsize=(12,4))
    colors = {"TERA":"red","OULU":"orange","KERG":"gold"}
    time_range = pd.date_range(df["datetime"].min(), df["datetime"].max(), periods=TOTAL_FRAMES)
    frame_images = []
    for t in time_range:
        ax.clear()
        current_data = df[df["datetime"] <= t]
        if current_data.empty: continue
        ymin = current_data[station_cols].min().min()*0.9
        ymax = current_data[station_cols].max().max()*1.1
        ax.set_ylim(ymin, ymax)
        for i, station in enumerate(stations):
            if i >= len(station_cols): continue
            ax.plot(current_data["datetime"], current_data[station_cols[i]], label=station, color=colors.get(station,"blue"))
        ax.set_xlim(df["datetime"].min(), df["datetime"].max())
        ax.set_xlabel("UTC Time")
        ax.set_ylabel("Neutron Flux (particles·cm⁻²·s⁻¹·sr⁻¹)")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        plt.tight_layout()
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        frame_images.append(img)
    plt.close(fig)
    h, w, _ = frame_images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, FPS, (w, h))
    for img in frame_images:
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.putText(frame, "NMDB (R)", (w-120, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA)
        video_writer.write(frame)
    video_writer.release()
    return output_path

# =========================
# VERTICAL ASSEMBLY
# =========================
def assemble_videos_vertically(video_paths, output_path):
    caps = [cv2.VideoCapture(v) for v in video_paths]
    widths = [int(c.get(cv2.CAP_PROP_FRAME_WIDTH)) for c in caps]
    heights = [int(c.get(cv2.CAP_PROP_FRAME_HEIGHT)) for c in caps]
    target_width = min(widths)
    total_height = sum(heights)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (target_width, total_height))
    for f in range(TOTAL_FRAMES):
        frames = []
        for c, h in zip(caps, heights):
            ret, frame = c.read()
            if not ret:
                frame = np.zeros((h, target_width, 3), dtype=np.uint8)
            frame = cv2.resize(frame, (target_width, frame.shape[0]))
            frames.append(frame)
        out.write(np.vstack(frames))
    out.release()
    for c in caps:
        c.release()
    return output_path

# =========================
# Cleanup old videos (>MAX_WEEKLY_VIDEOS)
# =========================
def cleanup_old_videos(folder, max_videos=MAX_WEEKLY_VIDEOS):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp4")]
    files.sort(key=os.path.getmtime)
    while len(files) > max_videos:
        try:
            os.remove(files[0])
        except OSError:
            pass
        files.pop(0)

# =========================
# MAIN WEEKLY
# =========================
if __name__ == "__main__":
    today = datetime.utcnow()
    start_date = today - timedelta(days=7)
    date_folder_str = today.strftime('%d%m%Y')
    year_str = today.strftime('%Y')
    month_name = calendar.month_name[today.month].capitalize()

    # --- SOHO weekly ---
    soho_video_paths = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        try:
            soho_imgs = download_soho_images(day)
            vid_path = os.path.join(SOHO_DIR, f"soho_{day.strftime('%d%m%Y')}.mp4")
            create_soho_video(soho_imgs, vid_path)
            soho_video_paths.append(vid_path)
        except Exception as e:
            print(f"⚠️ SOHO skipped {day.date()}: {e}")
    weekly_soho_vid = os.path.join(SOHO_DIR, f"soho_weekly_{date_folder_str}.mp4")
    merge_soho_videos_temporally(soho_video_paths, weekly_soho_vid)
    cleanup_old_videos(SOHO_DIR)

    # --- PROTONS weekly ---
    proton_df, start, end = get_noaa_proton_data_for_week()
    proton_vid_path = os.path.join(PROTON_DIR, f"protons_weekly_{date_folder_str}.mp4")
    create_proton_video(proton_df, start, end, proton_vid_path)
    cleanup_old_videos(PROTON_DIR)

    # --- NEUTRONS weekly ---
    neutron_stations = ["KERG","OULU","TERA"]
    altitudes = {"KERG":33,"OULU":15,"TERA":32}
    neutron_df, neutron_cols = fetch_neutron_data(start_date, today, neutron_stations)
    correlations = calculate_correlations(neutron_df, neutron_cols, neutron_stations)
    neutron_vid_path = os.path.join(NEUTRON_DIR, f"neutrons_weekly_{date_folder_str}.mp4")
    create_neutron_video(neutron_df, neutron_cols, neutron_stations, altitudes, neutron_vid_path)
    cleanup_old_videos(NEUTRON_DIR)

    # --- FINAL vertical assembly ---
    final_dir = os.path.join(SOLAR_DIR, year_str, month_name)
    os.makedirs(final_dir, exist_ok=True)
    final_vid_path = os.path.join(final_dir, f"{date_folder_str}_solar_activity_weekly.mp4")
    assemble_videos_vertically([weekly_soho_vid, proton_vid_path, neutron_vid_path], final_vid_path)
    print("✅ Weekly final video:", final_vid_path)
    cleanup_old_videos(SOLAR_DIR)