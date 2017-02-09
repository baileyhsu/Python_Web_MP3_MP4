
from flask import Flask, render_template, request, session, redirect
from Module import item
from Module.user import User
from Common.database import Database
from Module.video import Video

app = Flask(__name__)
app.secret_key = "bailey"

@app.before_first_request
def init_db():
    Database.initialize()

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/login", methods= ['GET','POST'])
def login_method():
    if request.method == 'POST':
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = User.is_login_valid(account,password)
        if check == True:
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            return redirect("/")
        else:

            message = "Your Account/Password is wrong"
            return render_template("login.html", message=message)

    else:
        return render_template("login.html")

@app.route("/logout")
def logout_method():
    session['account'] = None
    return redirect("/")


@app.route("/register", methods= ['GET','POST'])
def register_method():
    if request.method == 'POST':
        name = request.form['InputName']
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        result = User.register(name, account, password)
        if result:
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            return redirect("/")
        else:
            message = "Your account is already registered!"
            return render_template("register.html",message=message)
    else:
        return render_template("register.html")


@app.route("/favorite", methods=['GET','POST'])
def favorite_video():
    if session['account']:
        if request.method == 'POST':
            url = request.form['url']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            account = session['account']
            Video(account, title, link, img).save_to_db()
            return redirect(url)

        else:
            account = session['account']
            user_video = Video.find_video(account)
            return render_template("favorite.html", user_video=user_video)

    else:
        return redirect('/login')





@app.route("/results")
def result_page():

    page = request.args.get('sp')
    search = request.args.get('search')

    if page == None:
        url = request.url
        soup = item.find_search_content(search)
        all_item={}
        all_item2 = item.find_video(soup, all_item)
        all_item3 = item.video_time(soup, all_item2)
        print(all_item3)
        all_page1 = item.page_bar(soup)
        return render_template("result.html", search=search, all_item=all_item3, all_page=all_page1, url= url)

    elif page != None:
        url = request.url
        search = request.args.get('q')
        value = "sp={}".format(page)+"&"+"q={}".format(search)
        soup = item.find_page_content(value)
        all_item={}
        all_item2 = item.find_video(soup, all_item)
        all_item3 = item.video_time(soup, all_item2)
        print(all_item3)
        all_page1 = item.page_bar(soup)
        return render_template("result.html", search=search, all_item=all_item3, all_page=all_page1, url= url)

@app.route("/download")
def download():
    value = request.args.get('value')
    download_type, url = value.split("&")
    if download_type == "MP3":
        item.download_mp3(url)
        print(url)
    elif download_type == "MP4":
        item.download_mp4(url)
    return render_template("download.html")




if __name__ == "__main__":
    app.run(debug=True)