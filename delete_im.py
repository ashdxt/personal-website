import os
import re
import shutil

# Settings 
VAULT_PATH = "/home/snake/quartz/content"
IMAGE_FOLDER = os.path.join(VAULT_PATH, "/home/snake/test")
DELETE_UNUSED = False  # Change to True once you're sure it's correct

# Regex to catch Obsidian-style and Markdown-style image embeds
image_pattern = re.compile(r'!\[\[(.*?)\]\]|!\[.*?\]\((.*?)\)')

# Step 1: Find images referenced in notes
used_images = set()

for root, _, files in os.walk(VAULT_PATH):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                content = f.read()
                matches = image_pattern.findall(content)

                for match in matches:
                    for group in match:
                        if group:
                            used_images.add(os.path.basename(group))

# Step 2: Find all images in target folder
all_images = {file for file in os.listdir(IMAGE_FOLDER) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))}

# Step 3: Determine which images are unused
unused_images = all_images - used_images

print(f"Total images: {len(all_images)}")
print(f"Used images: {len(used_images)}")
print(f"Unused images: {len(unused_images)}")
print("\nFiles to delete:\n", "\n".join(unused_images))

# Step 4: Delete if confirmed
if DELETE_UNUSED:
    for img in unused_images:
        os.remove(os.path.join(IMAGE_FOLDER, img))
    print("Unused images deleted.")
else:
    print("\nNo files deleted. Set DELETE_UNUSED = True to proceed.")

