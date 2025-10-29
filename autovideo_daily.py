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

# --- Base directory = location of this script ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Folders ---
os.makedirs(os.path.join(BASE_DIR, "SOHO_videos"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "solar_activity"), exist_ok=True)

# =========================
# SOHO
# =========================
def download_soho_images(yesterday):
    date_str = yesterday.strftime('%Y%m%d')
    year = yesterday.strftime('%Y')
    folder_date_str = yesterday.strftime('%d%m%Y')
    base_folder = os.path.join(BASE_DIR, "SOHO_videos", f"soho_{folder_date_str}_images")
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
    return output_path

# =========================
# PROTONS
# =========================
def get_noaa_proton_data_for_yesterday():
    url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["time_tag"] = pd.to_datetime(df["time_tag"], utc=True)
    df["flux"] = df["flux"].astype(float)
    df["energy_value"] = df["energy"].str.extract(r'>=(\d+)').astype(float)

    now_utc = datetime.now(timezone.utc)
    start = (now_utc - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
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
    url = (
        "https://www.nmdb.eu/nest/draw_graph.php?formchk=1&" +
        "&".join([f"stations[]={s}" for s in stations]) +
        "&output=ascii&tabchoice=ori&dtype=corr_for_efficiency&date_choice=bydate&"
        f"start_year={start_date.year}&start_month={start_date.month:02d}&start_day={start_date.day:02d}&start_hour=00&start_min=00&"
        f"end_year={end_date.year}&end_month={end_date.month:02d}&end_day={end_date.day:02d}&end_hour=00&end_min=00&tresolution=1&yunits=0"
    )
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    lines = [l.strip() for l in r.text.splitlines() if re.match(r'^\d{4}-\d{2}-\d{2}', l)]
    if not lines:
        raise ValueError("No valid data found.")
    data = [line.split(";") for line in lines]
    df = pd.DataFrame(data[1:], columns=[c.strip() for c in data[0]])
    df["datetime"] = pd.to_datetime(df.iloc[:,0], errors="coerce")
    df = df.dropna(subset=["datetime"])
    station_cols = df.columns[1:-1]
    for c in station_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
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
        if current_data.empty:
            continue
        ymin = current_data[station_cols].min().min()*0.9
        ymax = current_data[station_cols].max().max()*1.1
        ax.set_ylim(ymin, ymax)
        for i, station in enumerate(stations):
            if i >= len(station_cols):
                continue
            ax.plot(current_data["datetime"], current_data[station_cols[i]], label=station, color=colors.get(station, "blue"))
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
        cv2.putText(frame, "NMDB (R)", (w-120, h-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA)
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
# OLD FILE CLEANER
# =========================
def delete_old_videos(base_dir, days=14):
    cutoff = datetime.now() - timedelta(days=days)
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".mp4"):
                path = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < cutoff:
                    try:
                        os.remove(path)
                        print(f"🗑 Deleted old video: {path}")
                    except OSError:
                        pass

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    yesterday = datetime.utcnow() - timedelta(days=1)
    date_folder_str = yesterday.strftime('%d%m%Y')
    year_str = yesterday.strftime('%Y')
    month_name = calendar.month_name[yesterday.month].capitalize()

    # --- SOHO ---
    soho_imgs = download_soho_images(yesterday)
    soho_vid_path = os.path.join(BASE_DIR, "SOHO_videos", f"soho_{date_folder_str}.mp4")
    soho_vid = create_soho_video(soho_imgs, soho_vid_path)

    for img_path in soho_imgs:
        try:
            os.remove(img_path)
        except OSError:
            pass
    soho_folder = os.path.dirname(soho_imgs[0])
    if not os.listdir(soho_folder):
        os.rmdir(soho_folder)

    # --- PROTONS ---
    proton_df, start, end = get_noaa_proton_data_for_yesterday()
    proton_vid_path = os.path.join(BASE_DIR, f"protons_{date_folder_str}.mp4")
    proton_vid = create_proton_video(proton_df, start, end, proton_vid_path)

    # --- NEUTRONS ---
    neutron_stations = ["KERG", "OULU", "TERA"]
    altitudes = {"KERG":33, "OULU":15, "TERA":32}
    neutron_df, neutron_cols = fetch_neutron_data(yesterday, yesterday + timedelta(days=1), neutron_stations)
    correlations = calculate_correlations(neutron_df, neutron_cols, neutron_stations)
    neutron_vid_path = os.path.join(BASE_DIR, f"neutrons_{date_folder_str}.mp4")
    neutron_vid = create_neutron_video(neutron_df, neutron_cols, neutron_stations, altitudes, neutron_vid_path)

    # --- FINAL VIDEO OUTPUT ---
    final_dir = os.path.join(BASE_DIR, "solar_activity", year_str, month_name)
    os.makedirs(final_dir, exist_ok=True)
    final_vid_path = os.path.join(final_dir, f"{date_folder_str}_solar_activity.mp4")
    final_vid = assemble_videos_vertically([soho_vid, proton_vid, neutron_vid], final_vid_path)

    print("✅ Final video generated:", final_vid)

    # --- DELETE OLD VIDEOS (>14 days) ---
    delete_old_videos(os.path.join(BASE_DIR, "SOHO_videos"), 14)
    delete_old_videos(os.path.join(BASE_DIR, "solar_activity"), 14)