# Image-Captioner
This is a very simple app that is useful for quickly editing image captions one by one.

# Windows Installation:
_(you need to have python and git installed)_
- open cmd and run:
```
git clone https://github.com/DavidSchobl/Image-Captioner/
cd Image-Captioner
setup.bat
```
- Start ```run.bat``` - it will open UI for you and you are free to add captions to your images!

# Usage:
- First, open the folder containing your source images, Image Captioner will then open the first image in the folder.
- After that, you just click next or previous and edit the captions captions. It automatically creates .txt file next to each image file.
- When .txt files already exist, it will load existent content (for eg. if you used BLIP to caption your images automatically).
- If you want, you can press **BLIP IT!** and a caption will be generated automatically for you. 

I wanted to make my life easier while training LoRAs or another checkpoint for Stable Diffusion, maybe someone will find this useful as well.

It is easy to compile this app for win users using PyInstaller.

Enjoy!

PS: Maybe I will make some updates later if you let me know, what you would like in the app.
