import subprocess
import re
import os
MapFileName=r'syany_update_2013-02-26.png'
DivideWidth = 8
DivideHeight = 8
XSymbol = 'A'


def run_cmd(str):
		print str
		proc = subprocess.Popen(str, shell=True, stdout=subprocess.PIPE)
		return proc.stdout.readlines()

# write txt file with sorted strings		
def sort_file_strings(filename, filename_output):
		strings=[]
		for line in open(filename,'r').readlines():
				line = line.replace(',',' - ').replace("\n", "")
				strings.append(line)		
		strings.sort()
		
		f = open('list_sorted.txt','w')
		for item in strings:
				f.write("%s\n" % item)
		f.close()		
		return 0
		
#cut count strings from head of filename_input, and write them to filename_output		
def move_strings_to_file(filename_input, filename_output, start_string, end_string):
        strings=[]
        for line in open(filename_input,'r').readlines():	
		strings.append(line)
                        
        fo = open(filename_output,'w')
        cnt=start_string
       

       
        if end_string>len(strings):
            end_string = len(strings)-1
        while cnt<end_string:
                fo.write("%s" %  strings[cnt])
                cnt = cnt+1
                
        fo.close()
 
def draw_column(filename,pointsize,start_string,end_string,PosX,PosY): 
        move_strings_to_file(filename,'list_sorted_part.txt',start_string,end_string)		
        print start_string,end_string
        run_cmd('convert  -font "Arial" -size 600x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
        run_cmd('composite -alpha on  -gravity NorthWest  -geometry +'+str(PosX)+'+'+str(PosY)+'  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')
	return 0
	
proc = subprocess.Popen('identify -format "%w" '+MapFileName, shell=True, stdout=subprocess.PIPE)
out = proc.stdout.readlines()

ImageWhdth = run_cmd('identify -format "%w" '+MapFileName)
ImageHeight = run_cmd('identify -format "%h" '+MapFileName)



s = str(ImageWhdth[0])
s.replace("\n", "").replace("\r", "")
ImageWhdth=int(s)
#print ImageWhdth

s = str(ImageHeight[0])
s.replace("\n", "").replace("\r", "")
ImageHeight=int(s)
#print ImageWhdth

print "Image dimmessions are "+str(ImageWhdth)+"x"+str(ImageHeight)

SquareWidth = ImageWhdth / DivideWidth
SquareHeight = ImageHeight / DivideHeight

print "Square size will be "+str(SquareWidth)+"x"+str(SquareHeight)


DrawCommands=[]
LabelsCommands=[]
CurrentSquareX = 0
while CurrentSquareX < DivideWidth:
		CurrentXLeft = CurrentSquareX*SquareWidth
		CurrentXRight = (CurrentSquareX+1)*SquareWidth
		
		CurrentSquareY = 0
		while CurrentSquareY < DivideHeight:
				CurrentYTop = CurrentSquareY * SquareHeight
				CurrentYBottom = (CurrentSquareY+1) * SquareHeight
				CurrentSquareY = CurrentSquareY+1
				#print str(CurrentXLeft) + "-" + str(CurrentXRight) + "   " + str(CurrentYTop) + "-" + str(CurrentYBottom)
				DrawCommands.append(' -draw "rectangle ' + str(CurrentXLeft) + ',' + str(CurrentYTop) + ',' + str(CurrentXRight) + ',' + str(CurrentYBottom) +'" ')
				ref='A1'
				
				#" -draw \"rectangle   $x1,$y1 $x2,$y2\""
		
		
		CurrentSquareX = CurrentSquareX+1

#draw names of grid cells		
CurrentSquareX = 0
CurrentSquareY = 0
HalfWidth = SquareWidth/2
XLabelCode=ord(XSymbol)

while CurrentSquareX < DivideWidth:
		CurrentXLeft = CurrentSquareX*SquareWidth
		CurrentXRight = (CurrentSquareX+1)*SquareWidth
		ref=chr(XLabelCode)
		LabelsCommands.append(' -draw "text ' + str(CurrentXLeft+HalfWidth) + ',' + str(10) + " '" + str(ref)+"'"+'"')
		LabelsCommands.append(' -draw "text ' + str(CurrentXLeft+HalfWidth) + ',' + str(ImageHeight-10) + " '" + str(ref)+"'"+'"')
		CurrentSquareX = CurrentSquareX+1
		XLabelCode = XLabelCode+1


		
#`convert $filename.png  -fill none -stroke red -strokewidth 10  ".implode($commands,' ')."  $filename-index.png \n

#print ','.join([str(i) for i in DrawCommands])

run_cmd('convert -size '+str(ImageWhdth)+'x'+str(ImageHeight)+' xc:white -fill none -stroke gray -strokewidth 10  '+ ''.join([str(i) for i in DrawCommands]) +'  ' + 'overlay_grid.png' )
run_cmd('convert -size '+str(ImageWhdth)+'x'+str(ImageHeight)+' xc:white -fill none -stroke black -pointsize 15 -strokewidth 1  '+ ''.join([str(i) for i in LabelsCommands]) +'  ' + 'overlay_grid_labels.png' )
run_cmd('composite overlay_grid.png '+MapFileName+'  -compose Darken map_with_grid.png' )
run_cmd('composite map_with_grid.png overlay_grid_labels.png  -compose Darken map_with_grid.png' )

run_cmd('convert   "map_with_grid.png"  "map_with_text.png"')
sort_file_strings('syans_objects.txt','list_sorted.txt')
pointsize=24
PosX = 10-150
PosY = 10
StringCounter=0






ColumnHeight = 30
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 30
PosXIncrement = 150
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 150
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 135
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#5
ColumnHeight = 20
PosXIncrement = 135
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 170
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 80+20
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#9
ColumnHeight = 20
PosXIncrement = 120
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#10
ColumnHeight = 20
PosXIncrement = 160
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#11 
ColumnHeight = 20
PosXIncrement = 170
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#12
ColumnHeight = 40-16
PosXIncrement = 200+60
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 40
PosXIncrement = 320
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 40
PosXIncrement = 200+80
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#15
ColumnHeight = 20
PosXIncrement = 300
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#16
ColumnHeight = 20
PosXIncrement = 200+80
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#17
ColumnHeight = 20
PosXIncrement = 200+90
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#18
ColumnHeight = 70
PosXIncrement = 200+80

PosX = PosX+PosXIncrement
PosX = 20
PosY = 1870
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 70
PosXIncrement = 200+80
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#20
PosY = 1920
ColumnHeight = 70
PosXIncrement = 200+80
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 70
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

ColumnHeight = 20
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight

#24
ColumnHeight = 20
PosXIncrement = 200
PosX = PosX+PosXIncrement
draw_column('list_sorted.txt',pointsize,StringCounter,StringCounter+ColumnHeight,PosX,PosY)
StringCounter = StringCounter + ColumnHeight


run_cmd('convert -crop 50%x100% +repage map_with_text.png map_with_text_half%d.png')


#remove temp files
os.remove('overlay_grid.png')
os.remove('overlay_grid_labels.png')
os.remove('map_with_grid.png')
os.remove('list_sorted_part.txt')
os.remove('list_sorted.txt')
os.remove('text_plate.png')

'''
move_strings_to_file('list_sorted.txt','list_sorted_part.txt',0,40)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +20+10  "text_plate.png"  "map_with_grid.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',41,78)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +150+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',79,120)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +300+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',121,159)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +450+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',160,190)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +700+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',191,220)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +850+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

# 7 left to -30
move_strings_to_file('list_sorted.txt','list_sorted_part.txt',221,250)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +970+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',251,280)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1150+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')


move_strings_to_file('list_sorted.txt','list_sorted_part.txt',281,310)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1300+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',311,340)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1450+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',341,370)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1600+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',371,400)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1750+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',401,430)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +1900+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')

move_strings_to_file('list_sorted.txt','list_sorted_part.txt',431,510)		
run_cmd('convert  -font "Tahoma-Bold" -size 400x2000 -pointsize '+str(pointsize)+'  -background "#fffffd" -transparent "#fffffd" -fill "#000000"  -weight Lighter  caption:@list_sorted_part.txt  -alpha On  text_plate.png')
run_cmd('composite -alpha on  -gravity NorthWest  -geometry +2150+10  "text_plate.png"  "map_with_text.png"  "map_with_text.png"')
'''