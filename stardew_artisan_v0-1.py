from tkinter import *

root = Tk()

artisanStatus = IntVar()
qualityOptions = ["Normal", "Silver Star", "Gold Star", "Iridium Star"]
seasonOptions = ["Spring", "Summer", "Fall", "Winter", "All"]
processingOptions = ["Keg", "Jar"]
frames = []

def initialize_window():
    root.title("Stardew Artisan v 0.1")
    root.geometry("800x800")
    def make_frames():
        pictureFrame = Frame(root, height = 50)
        pictureFrame.pack()
        frames.append(pictureFrame)
        def artisan_frame():
            frameLabel = Label(pictureFrame, text="image goes here")
            frameLabel.pack()
            artisanProf = Frame(root, height = 20)
            artisanProf.pack()
            frames.append(artisanProf)
            artisanCheck = Checkbutton(artisanProf, text="Artisan Profession", variable = artisanStatus, command = log_prof).grid(sticky = W)
            artisanHelpLabel = Label(artisanProf, text="If you have Artisan Profession (Farming Level 10 profession = \
Artisan Goods are worth 40% more) check this box.", justify = LEFT, anchor = W).grid(sticky = W)
        def main_frame():
            mainFrame = LabelFrame(root, text="Artisan Goods")
            mainFrame.pack(fill="both", expand="yes", side = BOTTOM)
            frames.append(mainFrame)
            qualityVar = StringVar()
            seasonVar = StringVar()
            processingVar = StringVar()
            qualityVar.set(qualityOptions[0])
            seasonVar.set(seasonOptions[0])
            processingVar.set(processingOptions[0])
            qualityMenu = OptionMenu(mainFrame, qualityVar, *qualityOptions, command = quality_option).grid(row = 0, column = 0, sticky = W)
            seasonMenu = OptionMenu(mainFrame, seasonVar, *seasonOptions, command = season_option).grid(row = 0, column = 1, sticky = W)
            processMenu = OptionMenu(mainFrame, processingVar, *processingOptions, command = process_option).grid(row = 0, column = 2, sticky = W)
        artisan_frame()
        main_frame()
    make_frames()

def quality_option(newValue):
    recalculate(newValue, None, None)
    print(newValue)

def season_option(newValue):
    recalculate(None, newValue, None)

def process_option(newValue):
    recalculate(None, None, newValue)

def recalculate(quality, season, process):
    image = PhotoImage(file = "Images\Potato.png")
    potatoImage = Label(frames[2], image = image)
    potatoImage.grid(row = 1, column = 0, sticky = W)
    potatoImage.image = image
    potatoCost = Label(frames[2], text="50g", anchor = W)
    potatoCost.grid(row = 1, column = 1, sticky = W)

def log_prof():
    logFile = open("stardew_artisan_log.txt", "w")
    if artisanStatus.get() == 0:
        statusText = "OFF"
    else:
        statusText = "ON"
    logFile.write("Artisan Profession=%s\n" %statusText)

def read_log():
    logFile = open("stardew_artisan_log.txt", "r")
    data = logFile.readlines()
    for line in data:
        status = line.split("=")
        status[1] = status[1].strip("\n")
        if status[1] == "OFF":
            artisanStatus.set(0)
        elif status[1] == "ON":
            artisanStatus.set(1)

def main():
    initialize_window()
    read_log()
    root.mainloop()

main()
        
