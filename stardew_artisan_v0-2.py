from tkinter import *

root = Tk()

artisanStatus = IntVar()
qualityOptions = ["Normal", "Silver Star", "Gold Star", "Iridium Star"]
seasonOptions = ["All", "Spring", "Summer", "Fall", "Winter"]
processingOptions = ["Keg", "Jar"]
options = ["Normal", "All", "Keg"]
frames = []
cropData = []
images = []

def initialize_window():
    root.title("Stardew Artisan v 0.2")
    root.geometry("800x800")
    def make_frames():
        pictureFrame = Frame(root, height = 50)
        pictureFrame.pack()
        frames.append(pictureFrame)
        def artisan_frame():
            frameLabel = Label(pictureFrame, text="image goes here")
            frameLabel.pack()
            artisanProf = Frame(root, height = 20)
            artisanProf.pack(fill = X)
            frames.append(artisanProf)
            artisanCheck = Checkbutton(artisanProf, text="Artisan Profession", variable = artisanStatus, command = log_prof).grid(sticky = W)
            artisanHelpLabel = Label(artisanProf, text="If you have Artisan Profession (Farming Level 10 profession = \
Artisan Goods are worth 40% more) check this box.", justify = LEFT, anchor = W).grid(sticky = W)
        def main_frame():
            mainFrame = LabelFrame(root, text="Artisan Goods")
            mainFrame.pack(fill="both", expand="yes", side = BOTTOM)
            frames.append(mainFrame)
        def menu_frame():
            menuFrame = Frame(root)
            menuFrame.pack(fill = X, expand = "no", pady = 10, side = TOP)
            frames.append(menuFrame)
            qualityVar = StringVar()
            seasonVar = StringVar()
            processingVar = StringVar()
            qualityVar.set(qualityOptions[0])
            seasonVar.set(seasonOptions[0])
            processingVar.set(processingOptions[0])
            qualityMenu = OptionMenu(menuFrame, qualityVar, *qualityOptions, command = quality_option).grid(row = 0, column = 0, sticky = W)
            seasonMenu = OptionMenu(menuFrame, seasonVar, *seasonOptions, command = season_option).grid(row = 0, column = 1, sticky = W)
            processMenu = OptionMenu(menuFrame, processingVar, *processingOptions, command = process_option).grid(row = 0, column = 2, sticky = W)
        artisan_frame()
        menu_frame()
        main_frame()
    make_frames()

def quality_option(newValue):
    options[0] = newValue
    recalculate(newValue, options[1], options[2])
    print(newValue)

def season_option(newValue):
    options[1] = newValue
    recalculate(options[0], newValue, options[2])

def process_option(newValue):
    options[2] = newValue
    recalculate(options[0], options[1], newValue)

def recalculate(quality, season, process):
    for widget in frames[3].grid_slaves():
        widget.destroy()
    order = [i for i in range(len(cropData))]
    if process == "Keg":
        cost = 1
    elif process == "Jar":
        cost = 3
    if artisanStatus.get() == 1:
        cost = cost + 1
    order = sort_order(cost, order)
    row = 0
    for i in order:
        row += 1
        if cropData[i][5] == season or season == "All":
            image = PhotoImage(file = cropData[i][7])
            cropImage = Label(frames[3], image = image)
            cropImage.grid(row = row, column = 0, sticky = W)
            cropImage.image = image
            images.append(cropImage.image)
            cropCost = Label(frames[3], text=cropData[i][cost], anchor = W)
            cropCost.grid(row = row, column = 1, sticky = W)

def sort_order(cost, order):
    costs = []
    for i in range(len(cropData)):
        costs.append(cropData[i][cost])
    order = [x for _, x in sorted(zip(costs, order))]
    order.reverse()
    return order
    
def log_prof():
    logFile = open("stardew_artisan_log.txt", "w")
    if artisanStatus.get() == 0:
        statusText = "OFF"
    else:
        statusText = "ON"
    logFile.write("Artisan Profession=%s\n" %statusText)
    recalculate(options[0], options[1], options[2])

def read_data():
    dataFile = open("crops_data.txt", "r")
    file = dataFile.readlines()
    for line in file:
        data = line.split(";")
        data[7] = data[7].strip("\n")
        cropData.append(data)
    
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
    read_data()
    print(cropData)
    root.mainloop()

main()
        
