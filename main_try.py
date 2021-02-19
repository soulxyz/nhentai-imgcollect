from threading import Thread
from queue import Queue
from PIL import Image
from sys import argv
import requests
import os
import re

class GetHentaiImg():

    def __init__(self,http_url,thread_num):
        global save_dir
        self.thread_num = thread_num
        self.save_dir = self.find_element('/([0-9]+)/',http_url)[0]
        save_dir = self.save_dir
        self.http_url = http_url + '1/'
        self.download_queue = Queue()

    def get_base_data(self):
        global galleries_num
        gethtml = requests.get(self.http_url)  # Get方式获取网页数据
        self.num_list = self.find_element('<span class="num-pages">(.+?)</span>',gethtml.text)
        print (self.num_list)
        pic_num = int(self.num_list[0])
        #galleries_num = self.find_element('<img src="https://i.nhentai.net/(.+?\1.jpg)" width=',gethtml.text)[0]
        print(galleries_num)
        self.img_list = ['https://i.nhentai.net/'+ self.find_element('<img src="https://i.nhentai.net/(.+?\)" width=',gethtml.text)[0]]
        #print(self.img_list)
        for img_index in range(2,pic_num + 1):
            self.img_list.append(self.img_list[0].replace('/1.','/' + str(img_index) + '.'))
        for url in self.img_list:
            print(url)
            self.download_queue.put(url, block=False)
        for i in range(pic_num):
            global pic_name
            pic_name = []
            pic_name.append(str(i)+'.jpg')
        print(pic_name)

    def find_element(self,reg,strhtml):
        element_re = re.compile(reg)
        element_list = re.findall(element_re, strhtml)
        return element_list

    def createFile(self,filePath):
        if os.path.exists(filePath):
            print('%s:存在'%filePath)
        else:
            try:
                os.mkdir(filePath)
                print('新建文件夹：%s'%filePath)
            except Exception as e:
                os.makedirs(filePath)
                print('新建多层文件夹：%s' % filePath)

    def save_img(self,img_path):
        while not self.download_queue.empty():
                img_url = self.download_queue.get()
                img_url_list = re.findall(re.compile('/([0-9]*).jpg'), img_url)
                img_save_index = int(img_url_list[0])
                print("○第{}张图片开始下载".format(img_save_index))
                try:
                    img_content = requests.get(img_url)
                    filename = '{}/{}.jpg'.format(img_path,img_save_index)
                    with open(filename, 'wb') as f_img:
                        f_img.write(img_content.content)
                    print("✔第{}张图片下载完成".format(img_save_index))
                    '''
                    if img_content.status_code == 404:
                        print("○第{}张图片404故障，尝试下载png文件".format(img_save_index))
                        img_url = "https://i.nhentai.net/galleries/"+ galleries_num+"/"+img_save_index+".png"
                        print("○第{}张图片开始下载".format(img_save_index))
                        try:
                            img_content = requests.get(img_url)
                            filename = '{}/{}.png'.format(img_path,img_save_index)
                            with open(filename, 'wb') as f_img:
                                f_img.write(img_content.content)
                            print("✔第{}张图片下载完成".format(img_save_index))
                        except Exception as e:
                            print(f'请求出错,地址：{img_url} 错误：{e} ')
                            time.sleep(0.5)
                    else:
                        continue
                        '''
                except Exception as e:
                    print(f'请求出错,地址：{img_url} 错误：{e} ')
                    time.sleep(0.5)


    def start(self):
        img_path=os.getcwd() + '\\画册' + self.save_dir
        self.createFile(img_path)
        print("获取图片列表:")
        self.get_base_data()
        print('开始下载')
        print('--------------------------------------------------------------------')
        threads = []

        for i in range(self.thread_num):
            t = Thread(target=self.save_img,args=(img_path,))
            t.setDaemon(True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(f'✔下载完毕，文件保存在{img_path}')
        #input("\nPress ENTER to exit.")
        
def image2pdf(path,pdf_name,pic_name):
    file_list = os.listdir(path)
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)
 
    pic_name.sort()
    new_pic = []
 
    for x in pic_name:
        if "jpg" in x:
            new_pic.append(x)
 
    for x in pic_name:
        if "png" in x:
            new_pic.append(x)
 
    print("hec", new_pic)
 
    im1 = Image.open(os.path.join(path, new_pic[0]))
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(os.path.join(path, i))
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)
'''
if __name__ == '__main__':
    try:
        http_url = input("请输入要爬取图册的海报页URL(形如: https://xxxxtai.net/g/297941/): \n")
        thraed_num = input("请输入要使用的线程数(默认10): ")
        if thraed_num == '':thraed_num = 10
        is_image2pdf = input("是否将画册转为PDF？(Y/N，默认Y): ")
        if thraed_num == '':thraed_num = 'Y'
        print(http_url,thraed_num)
        crawler = GetHentaiImg(http_url , int(thraed_num) )
        crawler.start()
        image2pdf(os.getcwd()+"\\画册"+save_dir,os.getcwd()+"\\画册"+save_dir+".pdf",pic_name)
    except Exception as e:
        print(f'✘发生错误，错误信息：{e} ')
        input("Press ENTER to exit.")
'''
if __name__ == '__main__':
    http_url = input("请输入要爬取图册的海报页URL(形如: https://xxxxtai.net/g/297941/): \n")
    thraed_num = input("请输入要使用的线程数(默认10): ")
    if thraed_num == '':thraed_num = 10
    is_image2pdf = input("是否将画册转为PDF？(Y/N，默认Y): ")
    if thraed_num == '':thraed_num = 'Y'
    print(http_url,thraed_num)
    crawler = GetHentaiImg(http_url , int(thraed_num) )
    crawler.start()
    image2pdf(os.getcwd()+"\\画册"+save_dir,os.getcwd()+"\\画册"+save_dir+".pdf",pic_name)
