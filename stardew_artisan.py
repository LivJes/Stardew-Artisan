from tkinter import *
from tk_ToolTip import *

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
    root.iconbitmap("Keg.ico")
    root.title("Stardew Artisan")
    root.geometry("800x800")
    def make_frames():
        pictureFrame = Frame(root, height = 50)
        pictureFrame.pack()
        image = PhotoImage(file = "Images\stardew_artisan.png")
        imageLabel = Label(pictureFrame, image = image)
        imageLabel.image = image
        images.append(imageLabel.image)
        imageLabel.pack()
        frames.append(pictureFrame)
        def artisan_frame():
            artisanProf = Frame(root, height = 20)
            artisanProf.pack(fill = X)
            frames.append(artisanProf)
            artisanCheck = Checkbutton(artisanProf, text="Artisan Profession", variable = artisanStatus, command = log_prof).grid(sticky = W)
            artisanHelpLabel = Label(artisanProf, text="If you have Artisan Profession (Farming Level 10 profession = \
Artisan Goods are worth 40% more) check this box.", justify = LEFT, anchor = W).grid(sticky = W)
        def main_frame():
            mainFrame = LabelFrame(root, text="Artisan Goods")
            mainFrame.pack(fill=BOTH, expand="yes", side = TOP)
            frames.append(mainFrame)
            rows = 0
            while rows < 12:
                mainFrame.rowconfigure(rows, weight=1)
                mainFrame.columnconfigure(rows,weight=1)
                rows += 1
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

def season_option(newValue):
    options[1] = newValue
    recalculate(options[0], newValue, options[2])

def process_option(newValue):
    options[2] = newValue
    recalculate(options[0], options[1], newValue)

def recalculate(quality, season, process):
    qualityOpt = "no"
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
    column = 0
    for i in order:
        if quality != "Normal":
            qualityOpt = "yes"
        if  season in cropData[i][5] or season == "All":
            if (qualityOpt == "yes" and cropData[i][8] == "yes" and process == "Keg") or qualityOpt == "no":
                if row % 12 == 0 and row != 0:
                    row = 0
                    column = column + 2
                image = PhotoImage(file = cropData[i][7])
                cropImage = Label(frames[3], image = image)
                cropImage.grid(row = row, column = column, columnspan = 6, sticky =  NW)
                cropImage.image = image
                cropImageTooltip = CreateToolTip(cropImage, "%s" %cropData[i][0])
                images.append(cropImage.image)
                if qualityOpt == "yes":
                    golds = calculate_cost(quality, cropData[i][cost], cropData[i][9])
                    cropCost = Label(frames[3], text="%d g" % golds, anchor = W)
                else:
                    cropCost = Label(frames[3], text="%d g" % int(cropData[i][cost]), anchor = W)
                cropCost.grid(row = row, column = column + 1, columnspan = 6, sticky = W)
                row += 1

def calculate_cost(quality, cost, goodType):
    cost = int(cost)
    if goodType == "wine":
        if quality == "Silver Star":
            cost = cost*1.25
        if quality == "Gold Star":
            cost = cost*1.50
        if quality == "Iridium Star":
            cost = cost*2
    elif goodType == "paleale":
        if quality == "Silver Star":
            if artisanStatus.get() == 0:
                cost = cost + 75
            else:
                cost = cost + 105
        if quality == "Gold Star":
            if artisanStatus.get() == 0:
                cost = cost + 2*75
            else:
                cost = cost + 2*105
        if quality == "Iridium Star":
            if artisanStatus.get() == 0:
                cost = cost + 4*75
            else:
                cost = cost + 4*105
    elif goodType == "beer":
        if quality == "Silver Star":
            if artisanStatus.get() == 0:
                cost = cost + 50
            else:
                cost = cost + 70
        if quality == "Gold Star":
            if artisanStatus.get() == 0:
                cost = cost + 2*50
            else:
                cost = cost + 2*70
        if quality == "Iridium Star":
            if artisanStatus.get() == 0:
                cost = cost + 4*50
            else:
                cost = cost + 4*70
    return cost

def sort_order(cost, order):
    costs = []
    for i in range(len(cropData)):
        costs.append(int(cropData[i][cost]))
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
        data[9] = data[9].strip("\n")
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
    recalculate(options[0], options[1], options[2])

if __name__ == '__main__':main()
root.mainloop()
