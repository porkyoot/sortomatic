import os
import random
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
BASE_DIR = Path("/data/input") if os.path.exists("/data") else Path("./data/input")
SAMPLE_DIR = Path("./sample")
CATEGORIES = {
    "Code": [".py", ".js", ".cpp", ".html", ".css", ".ts", ".rs", ".go"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md"],
    "Images": [".jpg", ".png", ".gif", ".webp", ".svg", ".heif", ".heic", ".tiff", ".jpeg"],
    "Music": [".mp3", ".flac", ".wav", ".aac"],
    "Movies": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".tar.gz", ".rar", ".7z"],
    "Software": [".exe", ".msi", ".app", ".bin", ".apk"],
    "Config": [".ini", ".cfg", ".conf", ".env", ".yml", ".json"]
}

# Scan samples
SAMPLES = {}
if SAMPLE_DIR.exists():
    for f in SAMPLE_DIR.iterdir():
        if f.is_file():
            ext = f.suffix.lower()
            if ext not in SAMPLES:
                SAMPLES[ext] = []
            SAMPLES[ext].append(f)

FOLDERS = [
    "Downloads",
    "Desktop",
    "My Documents",
    "Old Hard Drive Backup/Windows/System32",
    "Old Hard Drive Backup/Users/Etoile/Pictures",
    "Camera Uploads/2023",
    "Camera Uploads/2024",
    "Projects/Sortomatic",
    "Projects/Abandoned/GameEngine",
    "Funny Memes",
    "New Folder/New Folder",
    "Work/Reports/2022",
    "Work/Reports/Final",
    "DCIM/100CANON",
    "Tools_Bin", # Weighted Test
    "Settings/AppConfig" # Config Test
]

def create_file_from_template(path: Path, ext: str, size_kb: int = 1):
    """Creates a file, using a sample as template if available, else random content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Handle duplicates by picking from a small pool of names/contents
    is_dupe = random.random() < 0.2
    
    samples = SAMPLES.get(ext.lower(), [])
    
    if samples:
        # Use a sample
        sample = random.choice(samples)
        if is_dupe:
            # For duplicates, we force the same sample occasionally
            sample = samples[0]
        
        shutil.copy2(sample, path)
    else:
        # Fallback to random content
        if is_dupe:
            content = f"DUPLICATE_{ext}_{random.randint(1, 5)}".encode() * 1024
        else:
            content = os.urandom(int(size_kb * 1024))
        with open(path, "wb") as f:
            f.write(content)
    
    # Randomize mtime (shutil.copy2 preserves it, so we overwrite after)
    days_ago = random.randint(0, 365 * 5)
    mod = (datetime.now() - timedelta(days=days_ago)).timestamp()
    os.utime(path, (mod, mod))

def create_fake_repo(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    (path / ".git").mkdir(exist_ok=True)
    with open(path / ".git" / "config", "w") as f: f.write("[core]\n")
    create_file_from_template(path / "src" / "main.py", ".py")

def generate_specific_test_cases(base_dir: Path):
    """Generates specific edge-case files for testing features."""
    target_dir = base_dir / "EdgeCases"
    target_dir.mkdir(exist_ok=True)
    
    # 1. Archives
    print("Creating Archive test cases...")
    import zipfile
    import tarfile
    from io import BytesIO
    
    # Valid Multi-Item Zip
    with zipfile.ZipFile(target_dir / "valid_multi.zip", 'w') as zf:
        zf.writestr('folder/file1.txt', 'Content 1')
        zf.writestr('folder/file2.txt', 'Content 2')
        zf.writestr('root_file.txt', 'Root Content')
    
    # Valid Single-Root Zip (Auto-Expand Test)
    with zipfile.ZipFile(target_dir / "valid_single_root.zip", 'w') as zf:
        zf.writestr('root_folder/child.txt', 'Child Content')
        zf.writestr('root_folder/sub/grandchild.txt', 'Grandchild')

    # Valid Tarball
    with tarfile.open(target_dir / "valid.tar.gz", "w:gz") as tar:
        # Create a dummy file object
        data = b"Hello Tar"
        info = tarfile.TarInfo(name="hello.txt")
        info.size = len(data)
        tar.addfile(info, BytesIO(data))

    # Corrupt Zip (Text file with zip extension)
    with open(target_dir / "corrupt.zip", "w") as f:
        f.write("This is not a zip file.")
        
    # Corrupt Tar (Random bytes)
    with open(target_dir / "corrupt.tar", "wb") as f:
        f.write(os.urandom(1024))

    # 2. Executables (Mock Headers)
    print("Creating Executable test cases...")
    
    # Windows PE (MZ header)
    with open(target_dir / "app_win.exe", "wb") as f:
        f.write(b'MZ' + os.urandom(512))
        
    # Linux ELF
    with open(target_dir / "app_linux", "wb") as f:
        f.write(b'\x7fELF' + os.urandom(512))
        
    # Mac Mach-O (One of the magics)
    with open(target_dir / "app_mac", "wb") as f:
        f.write(b'\xce\xfa\xed\xfe' + os.urandom(512))
        
    # Fake Binary (Random bytes, should fail validation logic but be categorized as software if ext matches)
    with open(target_dir / "fake_binary.exe", "wb") as f:
        f.write(os.urandom(1024))

    # 3. Corruption Mocks
    print("Creating Corruption test cases...")
    
    # Corrupt Image
    with open(target_dir / "bad_image.jpg", "wb") as f:
        f.write(b'\xFF\xD8\xFF' + os.urandom(100)) # Start of JPG valid, then junk
        
    # Corrupt PDF
    with open(target_dir / "bad_doc.pdf", "wb") as f:
        f.write(b'%PDF-1.4\n' + os.urandom(200)) # Header valid, body junk

    # 4. Large Depth Layout (optional, separate folder)
    deep_dir = target_dir / "DeepLayout/Level1/Level2/Level3/Level4"
    deep_dir.mkdir(parents=True, exist_ok=True)
    create_file_from_template(deep_dir / "deep_file.txt", ".txt")

def generate_chaos(count: int = 500):
    """
    Generate comprehensive test data for all workflow steps:
    - Category Analysis: all file categories
    - Smart Explorer: complex metadata scenarios
    - Folder Duplicates: exact and near-duplicate folder structures
    """
    print(f"Generating {count} files in {BASE_DIR}...")
    if BASE_DIR.exists():
        try: shutil.rmtree(str(BASE_DIR))
        except: pass
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Track files for duplicate generation
    created_files = []
    
    # Copy sample folders as-is
    if SAMPLE_DIR.exists():
        print(f"Copying folders from {SAMPLE_DIR}...")
        for item in SAMPLE_DIR.iterdir():
            if item.is_dir():
                dest = BASE_DIR / item.name
                # Avoid overwriting if possible, or merge? 
                # "insert them as is" usually implies taking the whole thing.
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"  Copied folder: {item.name}")
            elif item.is_file():
                # Also ensure root files are copied at least once "as is" so they exist in the set?
                # The user said "Use all the files... for data generation" but "For folders inert them as is".
                # It's ambiguous if files should also be copied as-is or just used as templates.
                # Given "For folders insert them as is", implication is files are treated differently (as templates).
                pass

    # Atomic Repos (for Smart Explorer testing)
    print("Creating atomic project structures...")
    for _ in range(3):
        create_fake_repo(BASE_DIR / "Projects" / f"Atomic_Project_{random.randint(1000, 9999)}")
        
    # Weighted Test: Tools_Bin should be Software even if mostly text
    print("Generating Weighted Test Case: Tools_Bin...")
    tools_dir = BASE_DIR / "Tools_Bin"
    # 1 Heavy Software file (Weight 10)
    create_file_from_template(tools_dir / "installer.exe", ".exe", 5000)
    # 8 Light Text files (Weight 1 * 8 = 8)
    for i in range(8):
        create_file_from_template(tools_dir / f"readme_{i}.txt", ".txt")
        
    # Config Test
    print("Generating Config Test Case...")
    conf_dir = BASE_DIR / "Settings/AppConfig"
    create_file_from_template(conf_dir / ".env", ".env")
    create_file_from_template(conf_dir / "config.ini", ".ini")
    create_file_from_template(conf_dir / "unknown.conf", ".conf")

    folder_biases = {
        "Downloads": None,
        "Desktop": None,
        "My Documents": "Documents",
        "Old Hard Drive Backup/Windows/System32": "Code",
        "Old Hard Drive Backup/Users/Etoile/Pictures": "Images",
        "Camera Uploads/2023": "Images",
        "Camera Uploads/2024": "Images",
        "Projects/Sortomatic": "Code",
        "Projects/Abandoned/GameEngine": "Code",
        "Funny Memes": "Images",
        "Work/Reports/2022": "Documents",
        "DCIM/100CANON": "Images",
        "Tools_Bin": "Software",
        "Settings/AppConfig": "Config"
    }

    print("Populating biased folders...")
    for i in range(count):
        folder_name = random.choice(FOLDERS)
        bias = folder_biases.get(folder_name)
        
        if bias and random.random() < 0.85:
            category = bias
        else:
            category = random.choice(list(CATEGORIES.keys()))
            
        ext = random.choice(CATEGORIES[category])
        base_name = f"file_{i}"
        
        # Inject "config" in name occasionally
        if category == "Config" or random.random() < 0.02:
             if random.random() < 0.5: base_name += "_config"
        
        filename = f"{base_name}{ext}"
        full_path = BASE_DIR / folder_name / filename
        
        size = 1
        if category == "Movies": size = 100
        elif category == "Images": size = 50
        elif category == "Software": size = 2000
        
        create_file_from_template(full_path, ext, size_kb=size)
        created_files.append((full_path, ext, size))
    
    # Generate exact duplicates
    print("Creating exact duplicates...")
    num_exact_dupes = min(50, len(created_files) // 10)
    for _ in range(num_exact_dupes):
        if not created_files:
            break
        source_path, ext, size = random.choice(created_files)
        
        dupe_folder = random.choice(FOLDERS)
        dupe_name = f"copy_{random.randint(1, 999)}{ext}"
        dupe_path = BASE_DIR / dupe_folder / dupe_name
        
        try:
            dupe_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dupe_path)
        except:
            pass
    
    # Generate near duplicates (similar content)
    print("Creating near-duplicate test cases...")
    # 1. Text/Code near duplicates (slightly modified content)
    text_samples = [f for f, e, s in created_files if e in [".py", ".txt", ".md", ".js"]]
    for i in range(5):
        if text_samples:
            src = random.choice(text_samples)
            dest = src.parent / f"near_dupe_{i}{src.suffix}"
            with open(src, "r", errors="ignore") as f:
                content = f.read()
            with open(dest, "w") as f:
                f.write(content + f"\n# Small modification {i}\n")
    
    # 2. Image near duplicates using PIL (Resize, Rotate, Quality)
    print("Creating PIL-generated near-duplicate images...")
    try:
        from PIL import Image, ImageFilter
        image_samples = [f for f, e, s in created_files if e in [".jpg", ".png", ".jpeg", ".webp"]]
        
        count_generated = 0
        max_limit = 10
        
        # Shuffle to get random candidates
        random.shuffle(image_samples)
        
        for src in image_samples:
            if count_generated >= max_limit:
                break
                
            try:
                with Image.open(src) as img:
                    # distinct filename
                    dest = src.parent / f"near_dupe_pil_{count_generated}_{src.name}"
                    
                    # Random transformation
                    action = random.choice(['resize', 'rotate', 'grayscale', 'quality'])
                    
                    if action == 'resize':
                        # Resize to 90-95%
                        factor = random.uniform(0.90, 0.95)
                        new_size = (int(img.width * factor), int(img.height * factor))
                        new_img = img.resize(new_size, Image.Resampling.LANCZOS)
                        new_img.save(dest)
                        
                    elif action == 'rotate':
                        # Rotate 1-2 degrees, expand to fit
                        angle = random.uniform(1, 2)
                        new_img = img.rotate(angle, expand=True)
                        new_img.save(dest)
                        
                    elif action == 'grayscale':
                        # Convert to grayscale
                        new_img = img.convert("L")
                        new_img.save(dest)
                        
                    elif action == 'quality':
                        # Save with lower quality (only works well for JPG/WebP)
                        if src.suffix.lower() in ['.jpg', '.jpeg', '.webp']:
                            img.save(dest, quality=60)
                        else:
                            # Fallback for PNG -> Blur
                            new_img = img.filter(ImageFilter.GaussianBlur(1))
                            new_img.save(dest)
                            
                    count_generated += 1
            except Exception as e:
                # File might be random bytes from fallback template, just skip
                pass
                
    except ImportError:
        print("PIL not installed, skipping advanced image generation.")

    # 3. generate_specific_test_cases replacement
    print("Generating specific test cases for UI validation...")
    generate_specific_test_cases(BASE_DIR)
    
    # Smart Explorer test cases - complex files
    print("Creating Smart Explorer test cases...")
    smart_test_dir = BASE_DIR / "SmartExplorer_Tests"
    smart_test_dir.mkdir(parents=True, exist_ok=True)
    
    # Multi-language code file
    code_mix = smart_test_dir / "polyglot.txt"
    with open(code_mix, "w", encoding="utf-8") as f:
        f.write("# Python\ndef hello(): print('Hello')\n")
        f.write("// JavaScript\nfunction hello() { console.log('Hello'); }\n")
        f.write("<!-- HTML -->\n<html><body>Hello</body></html>\n")
    
    # Large document/pdf simulation if sample exists
    if SAMPLES.get(".pdf"):
        shutil.copy2(SAMPLES[".pdf"][0], smart_test_dir / "sample.pdf")
    
    # Video simulation
    if SAMPLES.get(".mp3"): # Using mp3 as dummy if no video
        shutil.copy2(SAMPLES[".mp3"][0], smart_test_dir / "dummy_video.mp4")

    # Advanced Context: Document extraction
    print("Creating Document extraction test cases...")
    doc_dir = smart_test_dir / "Documents"
    doc_dir.mkdir(exist_ok=True)
    if SAMPLES.get(".docx"):
        shutil.copy2(SAMPLES[".docx"][0], doc_dir / "report.docx")
    else:
        # Create a dummy text file but with docx extension to test Gotenberg fallback/error handling
        with open(doc_dir / "dummy.docx", "w") as f: f.write("This is a dummy DOCX content for testing.")

    # Advanced Context: Image Description
    print("Creating AI Image Description test cases...")
    img_dir = smart_test_dir / "AI_Images"
    img_dir.mkdir(exist_ok=True)
    if SAMPLES.get(".jpg"):
        shutil.copy2(SAMPLES[".jpg"][0], img_dir / "landscape.jpg")
    else:
        # Create a tiny dummy image
        from PIL import Image
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(img_dir / "dummy_red.jpg")

    # 4. Folder Duplicates
    print("Creating folder duplicate scenarios...")
    folder_dupe_dir = BASE_DIR / "FolderDuplicates"
    folder_dupe_dir.mkdir(exist_ok=True)
    
    # EXACT FOLDER DUPLICATE (Folder A and Folder B are identical)
    f_a = folder_dupe_dir / "Exact_A"
    f_b = folder_dupe_dir / "Exact_B"
    f_a.mkdir(exist_ok=True)
    create_file_from_template(f_a / "core.py", ".py", 10)
    create_file_from_template(f_a / "README.md", ".md", 5)
    (f_a / "assets").mkdir(exist_ok=True)
    create_file_from_template(f_a / "assets" / "logo.png", ".png", 50)
    
    # Copy A to B to ensure 100% identity
    if f_b.exists(): shutil.rmtree(f_b)
    shutil.copytree(f_a, f_b)
    
    # NEAR-DUPLICATE FOLDER (Folder C is ~75% similar to Folder A)
    # 3 files exist in A, we'll keep 2, and add 1 new
    f_c = folder_dupe_dir / "Near_C"
    f_c.mkdir(exist_ok=True)
    shutil.copy2(f_a / "core.py", f_c / "core.py")
    shutil.copy2(f_a / "README.md", f_c / "README.md")
    create_file_from_template(f_c / "new_experimental.py", ".py", 15)
    
    # DEEP NEAR-DUPLICATE FOLDER (Folder D has same structure as A but different hashes for some files)
    f_d = folder_dupe_dir / "Near_D"
    if f_d.exists(): shutil.rmtree(f_d)
    shutil.copytree(f_a, f_d)
    # Modify one file to change its hash
    with open(f_d / "core.py", "a") as f:
        f.write("\n# Near duplicate modification\n")

    print(f"Chaos generation complete. Created ~{len(created_files) + num_exact_dupes + 25} files.")

if __name__ == "__main__":
    generate_chaos(300)
