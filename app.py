from flask import Flask, request, render_template, redirect, url_for
from random import randint
app = Flask(__name__)
Page_options_dict = {} #ideally this should be memcache / redis server
@app.route("/", methods = ['POST', 'GET'])
def get_utm_variant():
    if request.method == 'POST':
        variant = request.form.get('variant_type')
        if not variant:
            #redirect to get
            redirect(url_for("get_utm_variant"))
        if Page_options_dict.get(variant):
            Page_options_dict[variant] += 1
        else:
            Page_options_dict[variant] = 1
        variant=request.form.get('variant_type')
        return render_template('webpage.html', variant=variant,options_dict=Page_options_dict )
    else:
        utm_id = request.args.get('utm_id')
        variant_var = None
        if utm_id == '1':
            choices = ['A'] * (1+Page_options_dict.get('A', 0))\
                + ['B']  * (1+Page_options_dict.get('B', 0))\
                + ['C']  * (1+Page_options_dict.get('C', 0))
        elif utm_id == '2':
            choices = ['C']  * (1+Page_options_dict.get('C', 0))\
                + ['D']  * (1+Page_options_dict.get('D', 0))\
                + ['E']  * (1+Page_options_dict.get('E', 0))
        else:
            variant_var = 'Default'
        if not variant_var:
            length = len(choices)
            choice = randint(0, length-1)
            variant_var = choices[choice]
        return render_template('webpage.html', variant=variant_var,options_dict=Page_options_dict)

if __name__ == "__main__":
    app.run()
