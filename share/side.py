from flask import Flask, request, render_template
import pymysql as pql


app = Flask(__name__)
connection = pql.connect(host='localhost',user='root',password='',database='project',)

cur=connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data (id INT NOT NULL AUTO_INCREMENT,name varchar(16) NOT NULL,Email varchar(30) NOT NULL,PRIMARY KEY (id))")
connection.commit()


@app.route("/", methods=["POST","GET"])
def main():
    
    return render_template('sidemain.html')

@app.route("/home",methods=["post","get"])
def remain():
    if request.method=="post":
        name=request.form["name"]
        email=request.form["email"]
        with connection:
            with connection.cursor() as cursor:
                qry="INSERT INTO data('name','E-mail') values(%s,%s)"
                cursor.execute(qry,(name,email))
            connection.commit()
    else:
          name=request.args["name"]
          email=request.args["email"]
          
    return f"name: {name}\nemail: {email}"
@app.route("/contact",methods=["post"])
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)