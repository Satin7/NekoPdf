import os

import random
import re
from io import open
#pygoogletranslate引用名称不对，可能是包冲突了
#import Translatetochzh
from timeit import default_timer as timer

import fitz
import largestinteriorrectangle as lir
#数组
import numpy as np
import pandas as pd
import pytesseract
import shapely
#pdf内容获取
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTAnno, LTTextBox
from PIL import Image, ImageOps
#图象处理
from shapely.geometry import Point, Polygon

#自用库，排错，元数据和翻译
import debugger
import MetaInfo

"""
def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    #lines = str(content).split("\n")
    lines = str(content)
    return lines
"""
#弃用
def ext_image(pdf):

    # open the my_pdf
    #my_pdf = fitz.open(pdf)
    my_pdf='null'
    # STEP 3
    # iterate over PDF pages
    for page_index in range(len(my_pdf)):
        
        # get the page itself
        page = my_pdf[page_index]
        image_list = page.getImageList()
        
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            
            # get the XREF of the image
            xref = img[0]
            
            # extract the image bytes
            base_image = my_pdf.extractImage(xref)
            image_bytes = base_image["image"]
            
            # get the image extension
            image_ext = base_image["ext"]

def replace_special_char(text):
    char={
        'ﬁ':'fi',
        'ﬂ':'fl',
        '  ':' '
    }
    for key, value in char.items():
        text.replace(key,value)
    return text

#弃用
def recompose_tab(tab_info):
    #提取表格和信息窗口
    table=[]
    return table

def ext_info(deb,pdf,name,path,ext_type):

    #前两页循环得到正文标记,标题标记和完成标记
    main_text_mark=[]
    main_title_mark=[]
    pre_ext=0
    

    page_id=0

    mark_list=[]
    mark_chr_num=[]
    mark_size=[]
    mark_index=0
    figure_table_frame=[]
    main_text_frame=[]
    main_title_frame=[]

    #动态页眉页脚,默认初始值80，50
    page_box_height=[]#高，宽
    page_box_width=[]
    up_margin=80
    low_margin=50
    
    #正文框体信息
    first_cycle_boxes=[]#位置
    first_cycle_boxes_marks=[]#标记类型

    #处理下载版pdf首部的信息页

    #查找正文和标题标记
    for page_layout in extract_pages(pdf):
        #遍历layout，layout里面就是要拆的东西了
        
        #设置图表框和正文文本框
        x00=x0=page_layout.width
        x11=x1=0
        y00=y0=page_layout.height
        y11=y1=0
        page_box_height.append(y0)
        page_box_width.append(x0)
        main_margin=[[0,0,page_layout.width,page_layout.height]]
        page_id+=1

        #首次循环确定正文标记
        for out in page_layout:
            #统计一个选框中的文字mark和mark对应的字数
            out_marks=[]
            chr_num=[]
            debugger.printtest(deb,path,0,'{}\n'.format(str(out)))
            if isinstance(out,LTTextBox) and contain([out.x0,out.y0,out.x1,out.y1],main_margin):
                    for out_objs in out:
                        #标记赋值
                        font1=out_objs._objs[0].fontname
                        font0=out_objs._objs[-2].fontname
                        size1=float(format(out_objs._objs[0].size,'.3f'))
                        size0=float(format(out_objs._objs[-2].size,'.3f'))
                        #拆分内部差异
                        if font1==font0 and size1==size0:
                            chr_num.append(len(out.get_text()))
                            out_marks.append([font1,size1])
                            
                            #用于识别页眉页脚的框体信息
                            first_cycle_boxes.append([out.x0,out.y0,out.x1,out.y1])
                            first_cycle_boxes_marks.append([font1,size1])
                        else:
                            x=out_objs.__iter__()
                            x.__next__()
                            start,close = 0, 0
                            for chr in out_objs:
                                if isinstance(chr,LTAnno):
                                    continue
                                else:
                                    if x.__next__()==True:
                                        font0=x.__next__().fontname
                                        if chr.fontname!=font0:
                                            out_marks.append([chr.fontname,float(format(chr.size,'.3f'))])
                                            chr_num.append((close+1)-start)
                                            start=close+1
                                        else:
                                            close+=1
                                    else:
                                        out_marks.append([chr.fontname,float(format(chr.size,'.3f'))])

                                    chr_num.append(close-start)
                                    continue

                        for mark in out_marks:
                            if not mark in mark_list:
                                #类型序号
                                #mark.append(mark_index)

                                mark_list.append(mark)
                                #Sep_by_mark.append([])
                                #Sep_by_mark[mark_list.index(mark)].append(text)
                                #类型字数
                                mark_chr_num.append(0)
                                mark_chr_num[mark_index]+=chr_num[out_marks.index(mark)]
                                mark_size.append(mark[1])
                                mark_index+=1
                            else:
                                mark_chr_num[mark_list.index(mark)]+=chr_num[out_marks.index(mark)]
                                #Sep_by_mark[mark_list.index(mark)].append(text)
            #如果处理到第三页就带着正文标记重新开始
        if pre_ext==0 and (page_id not in [1,2]):
            main_text_mark=mark_list[np.argsort(mark_chr_num)[-1]]
            main_title_mark=mark_list[np.argsort(mark_size)[-1]]
            pre_ext=1
            break
    
    #站点、杂志信息页区分信息

    standard_height=max(set(page_box_height),key=page_box_height.count)
    standard_width=max(set(page_box_width),key=page_box_height.count)
    
    site_append_info=0
    for page_width in page_box_width:
        if page_width!=standard_width:
            site_append_info+=1
    #如果标题字体不在首页或是页面大小不同
    #if (not main_title_mark in page_box_mono[0]) or page_box[0][1]!=standard_width:
    #    site_append_info=1

    i=0
    for i in range(len(first_cycle_boxes)):
        if first_cycle_boxes_marks[i]==main_text_mark:
            low_margin=min(first_cycle_boxes[i][1],low_margin)
            up_margin=min(standard_height-first_cycle_boxes[i][3],up_margin)
    
    #debugger.printconsole(deb,low_margin,up_margin)

    #第二次循环
    page_id=0

    title=''
    recomposed_art=[]

    #文本
    mark_list=[]
    mark_type=[]
    mark_index=0
    
    #框体
    main_f_t_frame=[]
    finish=[]
    
    #循环页面并提取正文，同时判断标题信息
    for page_layout in extract_pages(pdf):
        #遍历layout，layout里面就是要拆的东西了
        #跳过信息页
        if site_append_info>=1:
            site_append_info-=1
            continue
        page_id+=1
        
        #设置图表框
        page_edge=[[0,0,page_layout.width,page_layout.height]]
        #margin改为基于正文范围的动态
        x0=0
        y0=low_margin
        x1=page_layout.width
        y1=page_layout.height-up_margin
        #设置文档主信息范围
        main_margin=[[x0,y0,x1,y1]]

        debugger.printtest(deb,path,5,'{}\n'.format(str(main_text_frame)))

        #文本
        out_marks=[]
        texts=[]
        text_mark_types=[]
        page_main_text_frame=[]
        in_text_frame=[]        
        paraposition=[]

        #框体
        out_frame=[]
        out_types=[]
        page_main_frame=[]
        out_objs_frame=[]
        

        for out in page_layout:
            
            debugger.printtest(deb,path,0,'{}\n'.format(str(out)))

            
            if contain([out.x0,out.y0,out.x1,out.y1],main_margin):
                if isinstance(out,LTTextBox):
                    if 'evolution and assembly' in out.get_text():
                        a=0
                    for out_objs in out:
                        #标记赋值
                        font1=out_objs._objs[0].fontname
                        font0=out_objs._objs[-2].fontname
                        size1=float(format(out_objs._objs[0].size,'.3f'))
                        size0=float(format(out_objs._objs[-2].size,'.3f'))
                        #拆分内部差异
                        if font1==font0 and size1==size0:
                            #若是正文则直接退出对out的遍历
                            if [font0,size0]==main_title_mark:
                                texts.append(out_objs.get_text())
                                text_mark_types.append('TITL1')
                                page_main_text_frame.append([out.x0,out.y0,out.x1,out.y1])
                                out_objs_frame.append([out_objs.x0,out_objs.y0,out_objs.x1,out_objs.y1])

                            if [font0,size0]==main_text_mark:
                                text=out_objs.get_text()
                                texts.append(text)
                                text_mark_types.append('SENTS')
                                out_objs_frame.append([out.x0,out.y0,out.x1,out.y1])

                                out_types.append('text')
                                out_frame.append([out.x0,out.y0,out.x1,out.y1])
                                if not [out.x0,out.y0,out.x1,out.y1] in page_main_text_frame:
                                    if out.y1+30<=standard_height-up_margin:
                                        expand=out.y1+main_text_mark[1]*2.5
                                    else:
                                        expand=out.y1
                                    page_main_text_frame.append([out.x0,out.y0,out.x1,expand])
                                debugger.printtest(deb,path,6,str(out))
                            else:
                                text=out_objs.get_text()
                                texts.append(text)
                                try:
                                    a=mark_type[mark_list.index(font1,size1)]
                                    text_mark_types.append(a)
                                except:
                                    mark_list.append([font1,size1])
                                    a=distinguish([[font1,size1]],main_text_mark,main_title_mark)[0]
                                    mark_type.append(a)
                                    text_mark_types.append(a)
                                #框体
                                out_objs_frame.append([out.x0,out.y0,out.x1,out.y1])

                                out_types.append('text')
                                out_frame.append([0,0,0,0])
                                debugger.printtest(deb,path,6,str(out))
                        else:
                            out_types.append('text')
                            out_frame.append([0,0,0,0])
                            debugger.printtest(deb,path,6,str(out))
                            ''''''
                            start,close = 0, 0
                            
                            for i in range(len(out_objs.get_text())-1):
                                if not (i==0 or i==len(out_objs.get_text())-2):
                                    x=out_objs._objs[i-1]
                                    chr=out_objs._objs[i]
                                    y=out_objs._objs[i+1]
                                    #框内标题不太可能用同一字体，为了处理速度所以只用字体一个标准应该就可以了
                                    #mark=[i.fontname,float(format(i.size,'.3f'))]
                                    if isinstance(chr,LTAnno):
                                        if chr.get_text()==' ':
                                            if x.fontname!=y.fontname:
                                                #文本
                                                texts.append(out_objs.get_text()[start:close+2])
                                                #类型
                                                try:
                                                    a=mark_type[mark_list.index(font1,size1)]
                                                    text_mark_types.append(a)
                                                except:
                                                    mark_list.append([font1,size1])
                                                    a=distinguish([[font1,size1]],main_text_mark,main_title_mark)[0]
                                                    mark_type.append(a)
                                                    text_mark_types.append(a)
                                                #是否框内
                                                out_objs_frame.append([out.x0,out.y0,out.x1,out.y1])

                                                start=close+2
                                                close+=1
                                    close+=1
                                    i+=1
                                else:#首位或末位不会出现带回车的标记类型变化
                                    if i!=0:
                                        if y._text=='\n':
                                            #文本
                                            texts.append(out_objs.get_text()[start:close+3])
                                            #类型
                                            try:
                                                text_mark_types.append(mark_type[mark_list.index([font1,size1])])
                                            except:
                                                mark_list.append([font1,size1])
                                                a=distinguish([[font1,size1]],main_text_mark,main_title_mark)[0]
                                                mark_type.append(a)
                                                text_mark_types.append(a)
                                            #是否框内
                                            out_objs_frame.append([out.x0,out.y0,out.x1,out.y1])
                                    i+=1
                    if texts[-1][-2:]=='.\n':
                        texts[-1]+='\n'
        

        n=''
        for j in range(len(text_mark_types)):
            if contain(out_objs_frame[j],page_main_text_frame):
                if "TITL1" in text_mark_types[j]:
                    a=0
                if not j==len(text_mark_types)-1:
                    if text_mark_types[j]==text_mark_types[j+1]:
                        n+=' '
                        n+=texts[j][:-1]
                    else:
                        n+=' '
                        n+=texts[j][:-1]
                        debugger.printtest(deb,path,2,n)
                        recomposed_art.append(markdown(n,text_mark_types[j]))
                        n=''
                else:
                    n+=' '
                    n+=texts[j][:-1]
                    debugger.printtest(deb,path,2,n)
                    recomposed_art.append(markdown(n,text_mark_types[j]))


                '''基于pdfminer.six的图片提取方法，已弃用
                if isinstance(out,LTImage):
                    images.append(out)
                    out_types.append('image')
                    out_frame.append([out.x0,out.y0,out.x1,out.y1])

                #当是figure类型时，需要取出它里面的东西来。figure可遍历，所以for循环取。
                #如果figure里面还是figure，就接着遍历(虽然我没见过多层figure的情况)
                if isinstance(out,LTCurve):
                    out_types.append('curve')
                    out_frame.append([out.x0,out.y0,out.x1,out.y1])

                if isinstance(out,LTFigure):
                    out_types.append('figure')
                    out_frame.append([out.x0,out.y0,out.x1,out.y1])
                    while figurestack:
                        figure=figurestack.pop()
                        for f in figure:
                            if isinstance(f,LTTextBox):
                                if len(f.get_text())>=100:
                                    texts.append(f)
                                else:
                                    tables.append(f)
                            if isinstance(f,LTImage):
                                f_images.append(f)
                            if isinstance(f,LTFigure):
                                figurestack.append(f)'''
        #生成图表框
        #在首页以外处理图表框
        if page_id!=1:
            figure_table_frame=reversedarea(page_edge[0],main_margin[0],out_frame,out_types,deb,path,page_id)
            main_f_t_frame.append(figure_table_frame)
        else:
            figure_table_frame=[0,0,0,0]
            main_f_t_frame.append([0,0,0,0])
        have_main_text=0
        for i in out_frame:
            if i!=[0,0,0,0]:
                have_main_text+=1
        finish.append(have_main_text)
        page_main_frame.append([out_frame,out_types])
        #debugger.printtest(path,5,'{}\n'.format(str(main_text_frame)))
        out_frame.append(figure_table_frame)
        out_types.append('img&tab')
        debugger.printframemono(deb,path,page_id,page_edge[0],main_margin[0],out_frame,out_types)
        debugger.printframemono(deb,path,page_id,page_edge[0],main_margin[0],page_main_text_frame,['text']*len(page_main_text_frame))
    
    #加载正文
    #print(title)
    ReAndTcompose(title,'\n'.join(recomposed_art),name+'Article',path,ext_type)
    
    #加载图片
    #去除正文后的图表框架,一般而言不会在正文后放图表
    finish=finish[::-1]
    for i in range(len(finish)):
        if finish[i]!=0:
            finpage=len(finish)-i-1
            break
    main_f_t_frame[finpage:]=[[0,0,0,0]]*(i+1)
    figuretabgenerator(path,main_f_t_frame,standard_height)

    #随机問候
    greetings=['Good fawell','GOOD LUCK','Have a nice day!','Bye Bye','Finished','Nice to share knowledge with you.']
    return print(greetings[random.randint(0,len(greetings)-1)])

def distinguish(mark_list,main_text_mark,main_title_mark):
    '''
    #按字体大小排序
    #_temp1=[i[1] for i in sorted_list]
    #_temp2=[i[0] for i in sorted_list]
    #dict=zip(_temp1,_temp2)

    main_text_index=np.argsort(mark_chr_num)[-1]
    if mark_list[main_text_index][1]>8.500:
        main_text_size=mark_list[main_text_index][1]
        main_text_font=mark_list[main_text_index][0]
    else:
        main_text_index=np.argsort(mark_chr_num)[-2]
        main_text_size=mark_list[main_text_index][1]
        main_text_font=mark_list[main_text_index][0]
    
    size=[]
    for i in mark_list:
        size.append(float(i[1]))
    #main_title_size=mark_list[size.index(max(size))][1]
    main_title_size=size[np.argsort(size)[-1]]
    sub_title_size=size[np.argsort(size)[-2]]
    #选择标题字体
    bigtext=[]
    bigtext_num=[]
    for i in mark_list:
        if i[1]==main_title_size:
            bigtext.append(i)
            bigtext_num.append(mark_chr_num[mark_list.index(i)])
    main_title_font=bigtext[np.argsort(bigtext_num)[-1]][0]
    '''
    main_title_font=main_title_mark[0]
    main_title_size=main_title_mark[1]
    main_text_font=main_text_mark[0]
    main_text_size=main_text_mark[1]

    mark_type=[]
    for i in mark_list:
        if i[1]==main_title_size and i[0]==main_title_font:
            mark_type.append('TITL1')
        if i[1]==main_title_size and i[0]!=main_title_font:
            mark_type.append('INFOS')
        if i[1]>main_text_size and i[1]!=main_title_size:
            mark_type.append('TITL5')
        if i[1]==main_text_size and i[0]!=main_text_font and 'Italic' in i[0]:
            mark_type.append('ABSAU')
        if i[1]==main_text_size and i[0]!=main_text_font and 'Bold' in i[0]:
            mark_type.append('TITL5')
        if i[1]==main_text_size and i[0]!=main_text_font:
            mark_type.append('ABSAU')
        if i[1]==main_text_size and i[0]==main_text_font:
            mark_type.append('SENTS')
        if i[1]<main_text_size:
            mark_type.append('INFOS')
    """
    sorted_list=sorted(mark_list, key= lambda x:x[1])

    type_num=pd.value_counts(_temp1)
    for i in type_num:
        if i[1]>3:
            sorted_list[dict[i]].append('Title')     
    """

    return mark_type

def contain(out,frame):
    for subframe in frame:
        if out[0]>=subframe[0] and out[1]>=subframe[1] and out[2]<=subframe[2] and out[3]<=subframe[3]:
            return True
    return False


def reversedarea(page_edge,ori_frame,cut_frame,cut_type,deb,path,page_id):
    #ori_frame=[0,0,595,660]
    #删去重复项并转换为整数

    cut_frame=pd.concat([pd.DataFrame(cut_frame),pd.DataFrame(cut_type)],axis=1)
    temp_frame=cut_frame.drop_duplicates()
    cut_frame=[]
    cut_type=[]
    for i in range(len(temp_frame)):
        cut_frame.append(list(map(lambda x:int(x),np.array(temp_frame.iloc[i,:4]).tolist())))
        cut_type.append(temp_frame.iloc[i,4])

    #取主信息范围和正文的差集
    #生成缩略图以减少运算量
    zoom=8
    ori=list(map(lambda x:int(x/zoom),ori_frame))
    
    height=int((page_edge[3]-page_edge[1])/zoom)
    width=int((page_edge[2]-page_edge[0])/zoom)

    ori=Polygon([(ori[1],ori[0]),(ori[3],ori[0]),(ori[3],ori[2]),(ori[1],ori[2])])
    orig=ori

    for i in range(len(cut_frame)):
        if cut_type[i]=='text' and cut_frame!=[0,0,0,0]:
            frame=list(map(lambda x:int(x/zoom),cut_frame[i]))
            frame=Polygon([(frame[1],frame[0]),(frame[3],frame[0]),(frame[3],frame[2]),(frame[1],frame[2])])
            ori=ori.difference(frame)

    #若裁剪后与原始矩形的交并比不足0.3则直接退出函数
    if iou(ori,orig)<0.3:
        return [0,0,0,0]
    else:
        #图片与表格是在其中一个宽度至少达到一栏（最多三栏）的最大矩形
        #创建largest-interior-rectangle包所需的二值数组
        binarygrid=np.zeros((height,width),"bool")

        #根据shapely的交集函数判断是否在内部，内部生成True        
        for x in range(height):
            for y in range(width):
                if ori.intersects(Point(x,y)):
                    binarygrid[x][y]=True
        debugger.printframeimg(deb,path,page_id,[height,width],binarygrid,None)

        #判断最大矩形
        max_frame=(lir.lir(binarygrid)).tolist()
        #lir的返回值是端点加长宽
        max_frame=[max_frame[0],max_frame[1],max_frame[0]+max_frame[2],max_frame[1]+max_frame[3]]
        debugger.printframeimg(deb,path,page_id,[height,width],binarygrid,Polygon([(max_frame[1],max_frame[0]),(max_frame[3],max_frame[0]),(max_frame[3],max_frame[2]),(max_frame[1],max_frame[2])]))

        max_frame=list(map(lambda x:x*zoom,max_frame))
        #max_frame=[width-(max_frame[2]+max_frame[0]-1),height-(max_frame[3]+max_frame[1]-1),width-max_frame[0],height-max_frame[1]]
        
        return max_frame

def to_poly(frame):
    a=1
    return Polygon([(frame[0]/a,frame[1]/a),(frame[0]/a,frame[3]/a),(frame[2]/a,frame[3]/a),(frame[2]/a,frame[1]/a)])

#参考https://blog.csdn.net/weixin_43794311/article/details/120783677
def iou(poly1,poly2):
    try:
        inter_area = poly1.intersection(poly2).area  # 相交面积
        iou = float(inter_area) / (poly1.area + poly2.area - inter_area)
    except shapely.geos.TopologicalError:
        print('shapely.geos.TopologicalError occured, iou set to 0')
        iou = 0
    return iou

#弃用
def reframe(deb,mark_list,mark_type,main_frame,figure_table_frames,name,pdf,path,file_type):
    
    recomposed_art=[]

    for page_layout in extract_pages(pdf):
        #遍历layout，layout里面就是要拆的东西了
        text_frame=[]
        for out in page_layout:

            for i in range(len(main_frame[page_layout.pageid-1][0])):
                if main_frame[page_layout.pageid-1][1][i]=='text':
                    text_frame.append(main_frame[page_layout.pageid-1][0][i])

            if contain([out.x0,out.y0,out.x1,out.y1],text_frame):
                texts=[]
                marks=[]
                if isinstance(out,LTTextBox):#如果是文本
                    debugger.printtest(deb,path,1,out)
                    #out_objs对应的是每一行
                    for out_objs in out:
                        text=replace_special_char(out_objs.get_text())
                        #text=text.replace('\n','')
                        
                        font1=out_objs._objs[0].fontname
                        font0=out_objs._objs[-2].fontname
                        size1=float(format(out_objs._objs[0].size,'.3f'))
                        size0=float(format(out_objs._objs[-2].size,'.3f'))

                        #考虑完全处理内部字体的可能性...速度指数下降了，
                        if font1==font0 and size1==size0:#如果框首末标记相同
                            texts.append(text)
                            marks.append([font1,size1])
                        else:#若不同
                            #迭代框体内部字符，并按照mark类型拆分

                            #x=out_objs.__iter__()#回车前一个字符
                            #y=out_objs.__iter__()#回车后一个字符
                            #x.__next__()
                            
                            #标记类型文本的起始，末尾
                            start, close = 0, 0
                            #迭代标记，本来想用内置迭代器但没有很熟悉
                            i=0
                            mark_change_check=0
                            for chr in out_objs:
                                #排除首位和末位的情况
                                if not (i==0 or i==len(out_objs)-1):
                                    x=out_objs._objs[i-1]
                                    y=out_objs._objs[i+1]
                                    #框内标题不太可能用同一字体，为了处理速度所以只用字体一个标准应该就可以了
                                    #mark=[i.fontname,float(format(i.size,'.3f'))]
                                    if isinstance(chr,LTAnno):
                                        if chr.get_text()==' ':
                                            font_x=x.fontname
                                            if x.fontname!=y.fontname:
                                                texts.append(out_objs.get_text()[start:close+2])
                                                marks.append([font_x,float(format(x.size,'.3f'))])
                                                start=close+2
                                                close+=1
                                                mark_change_check+=1
                                    close+=1
                                    i+=1
                                else:#首位或末位不会出现带回车的标记类型变化
                                    if i!=0:
                                        if y._text=='\n':
                                            texts.append(out_objs.get_text()[start:close+3]) 
                                            marks.append([x.fontname,float(format(x.size,'.3f'))])
                                    i+=1

                    debugger.printtest(deb,path,3,texts)
                    debugger.printtest(deb,path,4,marks)
                    n=''
                    for j in range(len(marks)):
                        if not j==len(marks)-1:
                            if mark_type[mark_list.index(marks[j])]==mark_type[mark_list.index(marks[j+1])]:
                                n+=' '
                                n+=texts[j][:-1]
                            else:
                                n+=' '
                                n+=texts[j][:-1]
                                debugger.printtest(deb,path,2,n)
                                recomposed_art.append(markdown(n,0))
                                n=''
                        else:
                            n+=' '
                            n+=texts[j][:-1]
                            debugger.printtest(deb,path,2,n)
                            recomposed_art.append(markdown(n,mark_type[mark_list.index(marks[j])]))
                    
                    #recomposed_art.append('\n\n')


    ReAndTcompose('\n'.join(recomposed_art),name+'Article',path,file_type)
    figuretabgenerator(path,figure_table_frames,page_layout.height)
    #recompose('\n'.join(recomposed_img),name+'Imginfo',path,file_type)
    #recompose('\n'.join(recomposed_inf),name+'INFOS',path,file_type)
    #recompose_tab('\n'.join(recomposed_tab),name+'Tabinfo',path,file_type)

    return 0

def figuretabgenerator(path,frame,height):
    #将信息页导出为图片
    doc=fitz.open('%s.pdf'%path)
    i=0
    info=1

    #控制缩放
    height=height*4

    zoom_x=4
    zoom_y=4
    
    mat=fitz.Matrix(zoom_x,zoom_y)
    
    for page in doc:
        if frame[i]==[0,0,0,0]:
            i+=1
            continue
        else:
            if not os.path.exists(path+'\\.deb\\img&tab'):
                os.makedirs(path+'\\.deb\\img&tab')
            pix=page.get_pixmap(matrix=mat)
            pix.save(path+'\\.deb\\img&tab\\info_%s.png'%info)
            info+=1
            i+=1

    #将图片裁剪为合适的大小
    info=1
    padding=[10,20,10,20]
    fig=tab=0
    for i in range(len(frame)):
        if frame[i]==[0,0,0,0]:
            continue
        else:
            img=Image.open(path+'\\.deb\\img&tab\\info_%s.png'%info)
            frame[i]=list(map(lambda x:x*zoom_x,frame[i]))
            #裁剪为选框
            cropped=img.crop((frame[i][0],height-frame[i][3]+30,frame[i][2],height-frame[i][1]-30))
            invert=ImageOps.invert(cropped)
            #如果直接用invert,bbox就会识别不出来。。大概是一个bug
            invert.save(path+'\\.deb\\img&tab\\{}_invert.jpeg'.format(i))
            #裁剪为去白边
            invert2=Image.open(path+'\\.deb\\img&tab\\{}_invert.jpeg'.format(i))
            bbox=invert2.getbbox()
            #添加边缘
            left = bbox[0] - padding[0]
            top = bbox[1] - padding[1]
            right = bbox[2] + padding[2]
            bottom = bbox[3] + padding[3]
            cropped = invert2.crop([left, top, right, bottom])
            cropped = ImageOps.invert(cropped)
            
            #限制一下文字识别范围
            partocr=cropped.crop([0,0,200,200])
            code=pytesseract.image_to_string(partocr,lang='eng')
            if 'Table' in code[0:20]:
                imgtype='table'
                tab+=1
                cropped.save(path+'\\.deb\\img&tab\\info_%s.png'%info)
                if not os.path.exists(path+'\\%s'%imgtype):
                    os.makedirs(path+'\\%s'%imgtype)
                cropped.save(path+'\\%s\\%s_%s.png'%(imgtype,imgtype,tab))
                #code=pd.DataFrame(code)
                #with open(path+'\\deb\\%s\\%s_%s.csv'%(imgtype,imgtype,tab)) as file:
                #    file.writelines(code)
                #code.to_csv(path+'\\deb\\%s\\%s_%s.csv'%(imgtype,imgtype,tab))
            else:
                imgtype='figure' 
                fig+=1
                cropped.save(path+'\\.deb\\img&tab\\info_%s.png'%info)
                if not os.path.exists(path+'\\%s'%imgtype):
                    os.makedirs(path+'\\%s'%imgtype)
                cropped.save(path+'\\%s\\%s_%s.png'%(imgtype,imgtype,fig))
                
            info+=1  

def markdown(out,type):
    if type[:4]=='TITL':
        rank=int(type[4])
        text='TITLESTART'+'#'*rank+' '+out+'TITLECLOSE'
        #text='\n%s %s#\n'%('#'*rank,out.get_text()[:-1]))
    if type=='ABSAU':
        text='ABSAUSTART%sABSAUCLOSE'%out
    if type=='SENTS':
        text='SENTSSTART'+out+'SENTSCLOSE'
    if type=='IMGTX':
        text=out
    if type=='TABLE':
        text=out
    if type=='INFOS':
        text='TITLESTART'+'#'*6+' '+out+'TITLECLOSE'
    return text

def ReAndTcompose(title,txt,name,path,file_type):
    global deb,translate,transloci
    #负责最终的重排和显示文档
    #重排文档
    name1='Rcomposed：'+name
    name2='Tcomposed：'+name
    
    #txt=str(txt)
    #txt.find('\r\n')
    

    txt=replace_special_char(txt)
    debugger.printtest(deb,path,7,txt)
    
    #删除前、后文章
    txt=txt[txt.index('\nTITLESTART# '):]
    txt=txt[::-1]
    txt=txt[txt.index(' #TRATSELTIT\n')+3:]
    txt=txt[::-1]


    #print(txt)
    #txt=txt.replace('_','UnderScore01923')
    #txt=txt.replace('-\n\n','PAGECHANGE')
    #txt=txt.replace('\n\n','PAGECHANGE2')
    
    
    #txt=txt.replace('-\n','')
    #txt=txt.replace('\n',' ')
    txt=txt.replace('\n ','\n* PARASTART\n')
    txt=txt.replace('- SENTSCLOSESENTSSTART','')
    txt=txt.replace('. SENTSCLOSE\nSENTSSTART','.\n* PARASTART\n')
    txt=txt.replace('.SENTSCLOSE\nSENTSSTART','.\n* PARASTART\n')
    txt=txt.replace('SENTSCLOSE\nSENTSSTART',' ')
    txt=txt.replace('TITLESTART','')
    txt=txt.replace('TITLECLOSE','\n')
    txt=txt.replace('SENTSCLOSE\nABSAUSTART ',' ')
    txt=txt.replace('SENTSCLOSE\nABSAUSTART',' ')
    txt=txt.replace('ABSAUCLOSE\nSENTSSTART','')
    #strinfo=re.compile(r'SENTSCLOSE.+SENTSSTART|SENTSCLOSE\n.+\nSENTSSTART')
    #txt=strinfo.sub('',txt)
    txt=txt.replace('- ','')
    txt=txt.replace('  ',' ')
    txt=txt.replace('* PARASTART\n','\n  ')

    txt=txt.replace('SENTSCLOSE','\n')
    txt=txt.replace('SENTSSTART',' ')
    txt=txt.replace('   ','  ')
    #txt=txt.replace('')
    #txt=txt.replace('TITLECLOSE SENTSSTART','\n')
    '''txt=txt.replace('PAGECHANGE2',' ')
    txt=txt.replace('TITLECLOSETITLESTART#','')
    
    #txt=txt.replace('TITLECLOSE',' ')
    txt=txt.replace('SENTSCLOSESENTSSTART',' ')
    txt=txt.replace('SENTSSTART','')
    txt=txt.replace('SENTSCLOSE','')
    txt=txt.replace('PAGECHANGE','')
    
    
    
    txt=txt.replace('ABSAUSTART'info,'\n_')
    txt=txt.replace('ABSAUCLOSE','_\n')
    txt=txt.replace(' _\n','_\n')
    txt=txt.replace('UnderScore01923','_')
    '''
    
    #生成标题和目录
    metainfo,cite=MetaInfo.sch(title)
    if translate=='off':
        info='Strongly 💙 powered by *Pdfminer.six* *PyMμPdf* and *SemanticScholar*, made by Satin7 with love and loneliness.'
    else:
        info='Strongly 💙 powered by *Pdfminer.six* *PyMμPdf* *SemanticScholar* and *DeepL*, made by Satin7 with love and loneliness.'

    if 'sorry' in metainfo:
        metainfo0=''
    else:
        metainfo0=''

    recomposed_text=metainfo0+metainfo+txt+'\n'+info
    path1=path+'\\%s.'%name1+file_type
    with open(path1,'w',encoding='utf-8') as file:
        print(recomposed_text,file=file)
        #path = os.path.abspath(file)
	# path为需要打开文件夹的路径
    
    path3=path+'\\Cites.csv'
    if not (cite=='timeout' or cite=='Not Found by S.S.'):
        pd.DataFrame(cite).to_csv(path3)
        
    if translate=='on':
        if transloci=='deepl':
            tcomposed_text=Translatetochzh.deepl(metainfo+txt)+'# Refs\n'+cite+'\n'+info
        
            #path = os.path.abspath(file)
        # path为需要打开文件夹的路径
        #os.startfile(path2)
    #os.startfile(path1)
        if transloci=='google':
            tcomposed_text=Translatetochzh.google(path1)
        
        path2=path+'\\%s.'%name2+file_type
        with open(path2,'w',encoding='utf-8') as file:
            print(tcomposed_text,file=file)
    
    return 0

def deldir(dir):
    if not os.path.exists(dir):
        return False
    if os.path.isfile(dir):
        os.remove(dir)
        return
    for i in os.listdir(dir):
        t = os.path.join(dir, i)
        if os.path.isdir(t):
            deldir(t)#重新调用次方法
        else:
            os.unlink(t)
    os.rmdir(dir) #递归删除目录下面的空文件夹

if __name__ == '__main__':
    #with open(sys.argv,"rb") as my_pdf:
    #开启时间
    time='on'
    if time=='on':
        tic=timer()
    
    #是否开启调试 
    deb='on'
    translate='off'
    transloci='google'

    file_name='2019'
    dir_path='C:\\Users\\14491\\Desktop\\文献转换\\pdf2md\\lib\\examples\\{}'.format(file_name)
    deldir(dir_path)
    os.makedirs(dir_path)
    file_path='C:\\Users\\14491\\Desktop\\文献转换\\pdf2md\\lib\\examples\\{}.pdf'.format(file_name)


    with open(file_path, "rb") as my_pdf:
        debugger.makedeb(dir_path)
        debugger.clean(deb,dir_path)
        
        ext_info(deb,my_pdf,file_name,dir_path,'md')
    
    if time=='on':
        toc=timer()
        print(toc-tic)
    """
    with open('C:\\Users\\14491\\Desktop\\文献转换\\pdf2md\\lib\\examples\\102891312.txt') as file:  
        path='C:\\Users\\14491\\Desktop\\文献转换\\pdf2md\\lib\\examples'
        recompose(file.read(),'102891312',path,'txt')
    """    #del_publish(my_pdf)
        #ext_image(my_pdf)
        #ext_table(my_pdf)
        #recompose(read_pdf(my_pdf))
        #or use recompose(read_pdf(ext_table(ext_image(del_publish(my_pdf)))))
