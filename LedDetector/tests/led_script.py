'''
Created on 24 mai 2012

@author: jlengrand
'''
import cv

def init_video(video_file):
    """
    Given the name of the video, prepares the flux and checks that everything works as attended
    """
    capture = cv.CaptureFromFile(video_file)

    nFrames = int(  cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( capture, cv.CV_CAP_PROP_FPS )
    if fps != 0:
        waitPerFrameInMillisec = int( 1/fps * 1000/1 )

        print 'Num. Frames = ', nFrames
        print 'Frame Rate = ', fps, ' frames per sec'

        print '----'
        
        return capture
    else:
        return None

def display_img(img, delay=1000):
    """
    One liner that displays the given image on screen
    """
    cv.NamedWindow("Vid", cv.CV_WINDOW_AUTOSIZE)
    cv.ShowImage("Vid", img)
    cv.WaitKey(delay)

def display_video(my_video, frame_inc=100, delay=100):
    """
    Displays frames of the video in a dumb way.
    Used to see if everything is working fine
    my_video = cvCapture object
    frame_inc = Nmber of increments between each frame displayed
    delay = time delay between each image 
    """
    cpt = 0    
    img = cv.QueryFrame(my_video)

    if img != None:
        cv.NamedWindow("Vid", cv.CV_WINDOW_AUTOSIZE)
    else:
        return None

    nFrames = int(  cv.GetCaptureProperty( my_video, cv.CV_CAP_PROP_FRAME_COUNT ) )
    while cpt < nFrames:
        for ii in range(frame_inc):
            img = cv.QueryFrame(my_video)
            cpt + 1
            
        cv.ShowImage("Vid", img)
        cv.WaitKey(delay)


def grab_images(video_file, frame_inc=100, delay = 100):
    """
    Walks through the entire video and save image for each increment
    """
    my_video = init_video(video_file)
    if my_video != None:
        # Display the video and save evry increment frames
        cpt = 0    
        img = cv.QueryFrame(my_video)
    
        if img != None:
            cv.NamedWindow("Vid", cv.CV_WINDOW_AUTOSIZE)
        else:
            return None
    
        nFrames = int(  cv.GetCaptureProperty( my_video, cv.CV_CAP_PROP_FRAME_COUNT ) )
        while cpt < nFrames:
            for ii in range(frame_inc):
                img = cv.QueryFrame(my_video)
                cpt += 1
                
            cv.ShowImage("Vid", img)
            out_name = "data/output/" + str(cpt) + ".jpg"
            cv.SaveImage(out_name, img)
            print out_name, str(nFrames)
            cv.WaitKey(delay)
    else: 
        return None

if __name__ == '__main__':
    video_file =  "data/MusicLEDBox.avi"

    if 0:
        # do once once, create some images out of the video
        grab_images(video_file, frame_inc=100, delay = 100)

    img = cv.LoadImage("data/output/600.jpg")
    if img != None:
        # Displays the image I ll be working with
        display_img(img, delay = 100)
    else:
        print "IMG not found !"

    ####
    # Start processing here 
    ####
    
     # Turns to one channel image
    grey_img = cv.CreateImage(cv.GetSize(img), img.depth, 1)
    cv.CvtColor(img, grey_img, cv.CV_RGB2GRAY )
    display_img(grey_img, 100) 
    # Detect brightest point in image :
    
    ## USed to calculate max of histogram
    #hist_size = [64]
    #h_ranges = [0, 255]
    #hist = cv.CreateHist([64] , cv.CV_HIST_ARRAY, [[0, 255]], 1)
    #cv.CalcHist([grey_img], hist)
    #[minValue, maxValue, minIdx, maxIdx] = cv.GetMinMaxHistValue(hist)
    #print minValue, maxValue, minIdx, maxIdx

    [minVal, maxVal, minLoc, maxLoc] = cv.MinMaxLoc(grey_img)
    print minVal, maxVal, minLoc, maxLoc
    # could use histogram here to find where to stop
    
    # Threshold at 80% 
    margin = 0.8
    thresh = int( maxVal * margin)
    print thresh

    thresh_img = cv.CreateImage(cv.GetSize(img), img.depth, 1)
    cv.Threshold(grey_img, thresh_img , thresh, 255, cv.CV_THRESH_BINARY)

    display_img(thresh_img, delay = 100)

    # Want to get the number of points now
    contours = cv.FindContours(thresh_img, 
                               cv.CreateMemStorage(), 
                               mode=cv.CV_RETR_EXTERNAL , 
                               method=cv.CV_CHAIN_APPROX_NONE , 
                               offset=(0, 0))

    regions = []
    while contours:
        pts = [ pt for pt in contours ]
        x, y = zip(*pts)    
        min_x, min_y = min(x), min(y)
        width, height = max(x) - min_x + 1, max(y) - min_y + 1
        regions.append((min_x, min_y, width, height))
        contours = contours.h_next()

    out_img = cv.CreateImage(cv.GetSize(grey_img), 8, 3)
    for x,y,width,height in regions:
        pt1 = x,y
        pt2 = x+width,y+height
        color = (0,0,255,0)
        cv.Rectangle(out_img, pt1, pt2, color, 2)

    print len(regions)
    display_img(out_img)

    print "Finished!"