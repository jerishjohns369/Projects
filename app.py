from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])
def loadhomepage():
    return render_template('index.html')


@app.route('/scrap', methods=['POST'])
def index():
    querystring = request.form['content']
    querystring_adjusted = querystring.replace(" ","%20")
    try:
        url = "https://www.flipkart.com/search?q=" + querystring_adjusted
        uclient = uReq(url)
        page = uclient.read()
        uclient.close()
        flipkart_html = bs(page, "html.parser")
        big_boxes = flipkart_html.find_all("div", {"class": "_1YokD2 _3Mn1Gg"})
        box = big_boxes[1]
        box_filtered = box.find("div", {"class": "_1YokD2 _2GoDe3 col-12-12"}).decompose()

        product_link = "https://www.flipkart.com"+ box.div.div.div.a['href']
        result = requests.get(product_link)
        result_html = bs(result.text, "html.parser")
        comments = result_html.find_all('div', {'class': '_16PBlm'})
        reviews = []

        for commentbox in comments:
            try:
                name = commentbox.find_all('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
            except:
                name = 'No_Name'
            try:
                rating = commentbox.find_all('div',{'class':'_3LWZlK _1BLPMq'})[0].text
            except:
                rating = 'No Rating'
            try:
                comment_heading = commentbox.div.div.div.p.text
            except:
                comment_heading = 'No comment heading'
            try:
                comtag = commentbox.div.div.find_all('div',{'class':'t-ZTKy'})
                cust_comment = comtag[0].div.div.text
            except:
                cust_comment = 'No customer comment'

            my_dict = {"Product":querystring,"Name":name,'Rating':rating,"CommentHead":comment_heading,"Comment":cust_comment}
            reviews.append(my_dict)
        return render_template('results.html', reviews =reviews)
    except Exception as ex:
        raise


if __name__ == '__main__':
    app.run(debug=True)
