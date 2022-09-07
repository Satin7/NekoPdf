import os
import tkinter
from PIL import Image
import numpy as np
from shapely import Point,Polygon
def stop():
    return

def printconsole(_text,*argv):
    if _text=='on':
        return print(*argv)
    else:
        return

def printtest(_test,path,num,text):
    if _test=='on':
        if not os.path.exists(path+'\\.deb'):
            os.makedirs(path+'\\.deb')
        with open(path+'\\.deb\\{}.txt'.format(num),'a',encoding='utf-8') as file:
            file.write('{}\n'.format(str(text)))
    else:
        return

#弃用
def printframe(_test,path,page_id,page_edge,m_margin,f_frame,t_frame):
    if _test=='on':
        blood=20
        a=2    
        if _test=='on':
            
            page_id=1
            page_edge=[0,0,700,750]
            m_margin=[0,80,700,(750-50)]
            f_frame=[274.67325839999995, 150.80916000000002, 513.8802528599999, 593.00954]
            f_frame2=[10,400,50,590]
            #frame=[x0,y0,x1,y1]
            t_frame=[10,400,50,550]
            #x_frame=[min(f_frame[0],f_frame2[0]),min(f_frame[1],f_frame2[1]),max(f_frame[2],f_frame2[2]),max(f_frame[3],f_frame2[3])]
            x_frame=[56.68310009999996, 201.26034340000115, 538.5637829000001, 703.0054235000005]
            
        else:
            if not os.path.exists(path+'\\.deb\\frame'):
                os.makedirs(path+'\\.deb\\frame')
        
        window=tkinter.Tk()
        window.title(page_id)
        canvas=tkinter.Canvas(window,width=(page_edge[2]-page_edge[0]+2*blood)/a,height=(page_edge[3]-page_edge[1]+2*blood)/a,bg='#fbe0c3')
        canvas.create_rectangle((page_edge[0]+blood)/a,(page_edge[1]+blood)/a,(page_edge[2]+blood)/a,(page_edge[3]+blood)/a,fill='#ffbb98',outline='#ffbb98')
        canvas.create_rectangle((m_margin[0]+blood)/a,(m_margin[1]+blood)/a,(m_margin[2]+blood)/a,(m_margin[3]+blood)/a,fill='#ffcb90',outline='#ffcb90')
        if f_frame[2]-f_frame[0]>0 and f_frame[3]-f_frame[1]>0:
            f_frame=list(map(lambda x:(x+blood)/a,f_frame))
            canvas.create_rectangle(f_frame[0],m_margin[1]-f_frame[1],f_frame[2],m_margin[3]-f_frame[3],fill='#344648',outline='#344648')
        if t_frame[2]-t_frame[0]>0 and t_frame[3]-t_frame[1]>0:
            t_frame=list(map(lambda x:(x+blood)/a,t_frame))
            canvas.create_rectangle(t_frame[0],m_margin[1]-t_frame[1],t_frame[2],m_margin[3]-t_frame[3],fill='#7d8195',outline='#7d8195')
        if _test=='on' and x_frame[2]-x_frame[0]>0 and x_frame[3]-x_frame[1]>0:
                x_frame=list(map(lambda x:(x+blood)/a,x_frame))
                canvas.create_rectangle(x_frame[0],m_margin[1]-x_frame[1],x_frame[2],m_margin[3]-x_frame[3],fill='gray',outline='gray')
        #canvas.create_rectangle(0,590,10,600)
    else:
        return

def printframemono(_test,path,page_id,page_edge,m_margin,frames,types):
    if _test=='on':
        colors=[]
        mute=['image','curve','figure']

        for type in types:
            if type not in mute:
                if type=='text':
                    colors.append('#344648')
                if type[:4]=='image':
                    colors.append('#748b6f')
                if type=='curve':
                    colors.append('#c3cbd6')
                if type=='figure':
                    colors.append('#7d8195')
                if type=='img&tab':
                    colors.append('#7d8195')

        blood=20
        drift=0
        a=2    

        __test='off'
        if __test=='on':
            
            page_id=1
            page_edge=[0,0,700,750]
            window_edge=[(page_edge[2]-page_edge[0]+2*blood)/a,((page_edge[3]-page_edge[1]+2*blood)/a)]
            m_margin=[0,50,700,(750-80)]
            
        else:
            window_edge=[(page_edge[2]-page_edge[0]+2*blood)/a,((page_edge[3]-page_edge[1]+2*blood)/a)]
            if not os.path.exists(path+'\\.deb\\frame'):
                os.makedirs(path+'\\.deb\\frame')
        
        window=tkinter.Tk()
        window.title(page_id)
        

        canvas=tkinter.Canvas(window,width=window_edge[0],height=window_edge[1],bg='#fbe0c3')
        
        page_edge=list(map(lambda x:(x+blood)/a,page_edge))
        m_margin=list(map(lambda x:(x+blood)/a,m_margin))

        canvas.create_rectangle(page_edge[0],page_edge[1],page_edge[2],page_edge[3],fill='#ffbb98',outline='#ffbb98')
        canvas.create_rectangle(m_margin[0],page_edge[3]-m_margin[1]+blood/a,m_margin[2],page_edge[3]-m_margin[3]+blood/a,fill='#ffcb90',outline='#ffcb90')


        for i in range(len(colors)): 
            if frames[i][2]-frames[i][0]>0 and frames[i][3]-frames[i][1]>0:
                frame=list(map(lambda x:(x+blood)/a,frames[i]))
                canvas.create_rectangle(frame[0],page_edge[3]-frame[1]+blood/a,frame[2],page_edge[3]-frame[3]+blood/a,fill=colors[i],outline=colors[i])
    
        #标准标记
        std_frames=[]
        _luframe=[0,0,20,20]
        _ruframe=[40,0,60,20]
        _dlframe=[0,40,20,60]
        _debframe=[0,210,595,594]
        _luframe=list(map(lambda x:(x+drift)/a,_luframe))
        _ruframe=list(map(lambda x:(x+drift)/a,_ruframe))
        _dlframe=list(map(lambda x:(x+drift)/a,_dlframe))
        _debframe=list(map(lambda x:(x+drift)/a,_debframe))

        #_bugframe=[56.693,685.304,538.583,702.255]
        #_bugframe=list(map(lambda x:(x+blood)/a,_bugframe))
        std_frames.append(_luframe)
        std_frames.append(_ruframe)
        std_frames.append(_dlframe)
        #std_frames.append(_debframe)

        #std_frames.append(_bugframe)
        
        for frame in std_frames: 
            canvas.create_rectangle(frame[0],page_edge[3]-frame[1]+blood/a,frame[2],page_edge[3]-frame[3]+blood/a,fill='black',outline='black')
        
        canvas.pack()
        window.mainloop()
    else:
        return

def printframeimg(_test,path,page_id,page_edge,binarygrid,max_frame):
    if _test=='on':
        #zoom=4
        im=[]
        ma=0
        binarygrids=[binarygrid]
        #frame=Polygon([(frame[0],frame[1]),(frame[0],frame[3]),(frame[2],frame[3]),(frame[2],frame[1])])
        height=int(page_edge[0])
        width=int(page_edge[1])

        if not max_frame==None:
            binarygrids.append(np.zeros((height,width),'bool'))
            for x in range(height):
                for y in range(width):
                    if max_frame.intersects(Point(x,y)):
                        binarygrids[1][x][y]=True
            ma=1

        for binarygrid in binarygrids:
            im.append(Image.fromarray(binarygrid))

        if ma==0:
            im[0].save(path+'\\.deb\\frame\\{}_background.jpeg'.format(page_id))
        else:
            im[1].save(path+'\\.deb\\frame\\{}_forward.jpeg'.format(page_id))
            blend=Image.blend(im[0].convert('RGB'),im[1].convert('RGB'),0.3)
            blend.save(path+'\\.deb\\frame\\blend_{}.jpeg'.format(page_id))
        return
    else:
        return

#弃用
def outtypes(mark_list,mark_types,out_marks):
    out_types=[]
    for mark in out_marks:
        out_types.append(mark_types[mark_list.index(mark)])
    return out_types

def clean(_test,path):
    if _test=='on':
        for num in range(0,100):
            if os.path.exists(path+'\\.deb\\{}.txt'.format(num)):
                with open(path+'\\.deb\\{}.txt'.format(num),'r+',encoding='utf-8') as file:
                    file.truncate(0)
            else:
                return
    else:
        return

def makedeb(path):
    if not os.path.exists(path+'\\.deb'):
        os.makedirs(path+'\\.deb')
    return 

#printframe('on',0,0,0,0,0,0)
f_frame=[274.67325839999995, 150.80916000000002, 513.8802528599999, 593.00954]
f_frame2=[10,400,50,590]
#frame=[x0,y0,x1,y1]
t_frame=[10,400,50,550]
#x_frame=[min(f_frame[0],f_frame2[0]),min(f_frame[1],f_frame2[1]),max(f_frame[2],f_frame2[2]),max(f_frame[3],f_frame2[3])]
x_frame=[56.68310009999996, 201.26034340000115, 538.5637829000001, 703.0054235000005]
frames=[]
frames.append(f_frame)
frames.append(f_frame2)
frames.append(t_frame)
#printframemono('on',0,frames,0,0,0,0)

