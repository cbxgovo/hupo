from django.shortcuts import render, HttpResponse
import os
import csv




def index_test(request):
    return HttpResponse('index response!')
    



# def index(request):
#     # 去app目录下的templates目录寻找gdp_per_capita1.1.html（根据app的注册顺序，逐一去他们的templates目录中找） 
#     return render(request,"index.html")

###################################
# Create your views here.
from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()



# 创建了一个视图函数upload_file，它处理POST请求并验证表单的有效性。如果表单有效，我们获取上传的文件并调用handle_uploaded_file函数来处理它。
def upload_file(request):
    # if request.method == 'GET':
    #     return render(request, 'index.html')

    if request.method == 'POST':

        print("POST请求已收到-")

        # 实例化类
        form = UploadFileForm(request.POST, request.FILES)
        
        # 获取上传的表格文件
        file = request.FILES['file'] 
       
        if form.is_valid():
            print("上传的文件有效--")
            file = request.FILES['file']

            # 函数执行[函数执行 利用plotly将xlsx转图像]  file参数传出 文件转为可以处理的xlsx文件 
            handle_uploaded_file(file) 
            return render(request, 'index.html')
            # return render(request, 'index.html', {'success_message': "上传成功!"})
            # return HttpResponse('File uploaded successfully')
    else:
        form = UploadFileForm()
    return render(request, 'index.html')
    # return render(request, 'index.html', {'form': form})

# 在handle_uploaded_file函数中，我们使用csv.DictReader来解析上传的CSV文件。
# 对于文件的每一行，我们可以访问其键值对并执行相应的操作。在这个示例中，我们并没有真正处理数据，而是留了一个空占位符。
def handle_uploaded_file(file):
    import pandas as pd
    from io import TextIOWrapper
    # # # 1
    # # 使用InMemoryUploadedFile对象的read()方法读取文件内容
    # file_content = file.read().decode('utf-8')
    # # 将文件内容传递给io.StringIO对象
    # file_io = io.StringIO(file_content)
    # # 创建csv.DictReader对象，指定编码为utf-8
    # csv_reader = csv.DictReader(file_io)
    # # 将csv.DictReader对象转换为列表，然后使用pandas构造DataFrame对象
    # df = pd.DataFrame(list(csv_reader))

    # # 2
    # # print(type(file)) # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>类型的文件
    # csv_reader = csv.DictReader(file)
    # print(type(csv_reader)) # <class 'csv.DictReader'>
    # # # 将csv.DictReader对象转换为pandas.DataFrame对象 直接传入作 图像
    # df = pd.DataFrame(csv_reader) # DataFrame对象

    print("准备执行file变量转xlsx文件---")

    # for row in csv_reader:
    #     # 处理每一行的数据
    #     # 这里可以写入数据库或进行其他操作
    #     pass

    # 3. 写入csv xlsx csv一直有编码问题 使用InMemoryUploadedFile对象的read()方法读取文件内容，然后将内容写入到一个csv文件中
    with open('app01/csvfiles/file.xlsx', 'wb') as destination:
        for chunk in file.chunks(): # file参数传进来的直接进行操作
            destination.write(chunk)

    print("准备执行xlsx文件作图----")
    draw()

    

# 由xlsx文件绘制3D图像 保存静态html和png信息
def draw():
    import plotly.graph_objects as go
    import pandas as pd
    import plotly.io as pio

    # # Read data from a csv 直接由参数传进来pd pandas.DataFrame对象
    z_data = pd.read_excel('app01/csvfiles/file.xlsx')
    fig = go.Figure(data=[go.Surface(z=z_data.values)])
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                    highlightcolor="limegreen", project_z=True))
    fig.update_layout(title='Mt Bruno Elevation', autosize=True,
                    scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
                    
                    margin=dict(l=65, r=50, b=65, t=90)
    )
    
    fig.write_html("app01/static/gdp.html") # 保存为HTML文件
    fig.write_image("app01/static/scatter.png") # 保存为静态图片文件
    # fig.show()
    print("3D图像已绘制并保存-----")


# add跳转
def files(request):

    # 由前端指定的name获取到图片数据
    img = request.FILES.get('img')

    # 获取图片的全文件名
    img_name = img.name

    # 定义全局变量 文件后缀和文件名 方便其他函数图片处理时候的引用
    global mobile
    global ext

    # 截取文件后缀和文件名
    mobile = os.path.splitext(img_name)[0]
    ext = os.path.splitext(img_name)[1]
    # 重定义文件名
    img_name = f'avatar-{mobile}{ext}'
    # img_name = f'avatar-laker.png' # 这里可以固定命名替换为覆盖 覆盖还没写

    # 从配置文件中载入图片保存路径
    img_path = os.path.join("app01/static/img_upload", img_name)
    # 写入文件
    with open(img_path, 'ab') as fp:
        # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
        for chunk in img.chunks():
            fp.write(chunk) 
    # return HttpResponse('uploads success')

    # 全局函数调用 图像转xlsx [再转html嵌入]
    image_to_xlsx()

    return render(request, 'index.html')


def image_to_xlsx():
    from PIL import Image
    import csv
    from openpyxl import Workbook

    # 示例用法
    # image_path_0 = "app01/static/img_upload/avatar-"  # 替换成你的图片路径
    image_path = f'app01/static/img_upload/avatar-{mobile}{ext}'
  
    

    def image_to_matrix(image_path, max_depth=500, target_width=100, target_height=100):
        # 打开图片
        img = Image.open(image_path)
        
        # 将图片转换为灰度图像
        img_gray = img.convert('L')
        
        # 获取图片尺寸
        width, height = img_gray.size
        
        # 计算缩放比例
        scale_x = width // target_width
        scale_y = height // target_height
        
        # 创建一个二维矩阵来存储颜色深度数据
        depth_matrix = []
        
        # 遍历图片每个像素，将颜色深度转换为矩阵数据
        for y in range(0, height, scale_y):
            row = []
            for x in range(0, width, scale_x):
                # 获取像素的颜色深度
                color_depth = img_gray.getpixel((x, y))
                # 将颜色深度映射到指定范围内
                mapped_depth = max_depth * (1 - color_depth / 255)  # 假设255为最浅颜色
                row.append(mapped_depth)
            depth_matrix.append(row)
        
        return depth_matrix



    def save_matrix_to_xlsx(matrix, xlsx_filename):
        # 创建一个工作簿
        wb = Workbook()
        # 选择活动工作表
        ws = wb.active
        
        # 写入序号的编码
        ws.append([''] + list(range(len(matrix[0]))))
        
        # 写入矩阵数据
        for i, row in enumerate(matrix):
            ws.append([i] + row)
        
        # 保存为 XLSX 文件
        wb.save(xlsx_filename)



    # 内部函数调用 图像转表格
    depth_matrix = image_to_matrix(image_path)

    # 保存为 XLSX 文件
    xlsx_filename = "app01/csvfiles/file.xlsx"
    save_matrix_to_xlsx(depth_matrix, xlsx_filename)
    print(f"Depth matrix saved to {xlsx_filename}")

    # 全局函数调用 xlsx绘制图像
    draw()




