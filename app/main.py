from flask import Flask, render_template, request, abort
import jinja2

app = Flask(__name__, template_folder="./templates/", static_folder="./static/")
app.config['DEBUG'] = False

def generate_sanitized_object(name: str, age: int, description: str):
    template_string = """
        <div class="object">
            <h2>{{name|striptags}}</h2>
            <p><span class="age">Возраст:</span> {{age|striptags}} лет</p>
            <p><span class="description">Описание:</span> {{description|striptags}}</p>
        </div>
    """
    return jinja2.Template(template_string).render(
        name = name,
        age = age,
        description = description
    )



def validation(input_string):
    black_list = ['{{','}}', 'builtins','eval','import','class', 'subclasses', '__', 'init']
    for i in range(len(black_list)):
        if black_list[i] in input_string:
            input_string = input_string.replace(black_list[i],'')
    bool_vector = [bool(word in input_string) for word in black_list]
    if any(bool_vector):
        input_string = validation(input_string)
    return input_string


@app.errorhandler(404)
def page_not_found(_):
    return render_template("errors.html", number = 404, description = "Страница не найдена"), 404

@app.errorhandler(400)
def bad_request(_):
    return render_template("errors.html", number = 400, description = "Неправильные параметры name, age или description!"), 400

@app.route("/")
def return_index():
    return render_template("index.html")

@app.get("/get_user_info")
def return_user_info():
    try:
        name = request.args.get('name')
        age = request.args.get('age')
        description = request.args.get('description')
        if not name or not age or not description or len(name) == 0 or len(age) == 0 or len(description) == 0:
            abort(400)
        elif not age.isdigit():
            abort(400)
        else:
                templ = generate_sanitized_object(validation(name), validation(age), validation(description))
                templ += """\n
                <div class="debug-information" hidden>
                    <p>{{debug_info}}</p>
                </div>
                """
                return jinja2.Template(templ).render(debug_info = "some debug info", request = request)
    except Exception as e:
        abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8090)
