import RLang
from flask import Flask, request,redirect,url_for, render_template
app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def index():
    if request.method=="POST":
        input=request.form["nm"]
        return redirect(url_for("ans",text=input))
    else:
        return render_template("form.html")

@app.route("/<text>")
def ans(text):
    #return text
        resu, error = RLang.result(text)
        if error:
            err_val=error.convert_to_string()
            return render_template("error.html",err_val=err_val)
            #return f"<h1>{error.convert_to_string()}<h1>"
        elif resu:
            return render_template("result.html",resu=resu)
            #return f"<h3>{resu}<h3>"

if __name__=='__main__':
    app.run(debug=True)

