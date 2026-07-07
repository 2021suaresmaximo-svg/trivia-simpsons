from flask import Flask, request, render_template
from random import shuffle
import os

app = Flask(__name__)

preguntas = [
    ("¿Cuántas temporadas tiene?", ["32", "37", "35", "41"], "37"),
    ("¿En qué año salió la primera temporada?", ["1967", "1992", "1989", "1976"], "1989"),
    ("¿Cuántos personajes aparecen en absolutamente todos los episodios, sin contar la intro?", ["1", "5", "3", "2"], "1"),
    ("¿Quién le disparó a Burns?", ["Homero", "Maggie", "Smithers", "Jefe Gorgory"], "Maggie"),
    ("¿En qué año se estrenó la película?", ["2006", "2002", "2008", "2007"], "2007"),
    ("En el episodio 'Llamarada Moe', ¿cuál es el ingrediente secreto y poco convencional que Homero le añade al trago y que Moe le termina robando?", ["Jarabe para la tos", "Líquido para encendedor", "Cloro de pileta", "Salsa picante"], "Jarabe para la tos"),
    ("¿Qué negocio operaba originalmente Moe antes de convertirse en bar?", ["Una iglesia comunitaria", "Una carnicería", "Una desmontadora de algodón", "Un consultorio dental"], "Una desmontadora de algodón"),
    ("¿Cuál es el verdadero nombre del sujeto de las historietas?", ["Stuart Jenkins", "Jeff Albertson", "Albertson Jones", "Matthew Williams"], "Jeff Albertson"),
    ("¿Cuál es la marca de los cigarrillos que fuman constantemente Patty y Selma?", ["Marlboro", "Springfield Lights", "Laramie", "Buzz"], "Laramie"),
    ("¿Qué objeto temático construyen Lisa y Allison para competir en la feria escolar?", ["Un volcán de bicarbonato", "Un saxofón de material reciclado", "Una maqueta de la planta nuclear", "Un diorama"], "Un diorama"),
    ("¿Cuál es el objeto de infancia del Sr. Burns?", ["Un reloj de bolsillo de oro", "Un oso de peluche", "Un trineo de nieve", "Un centavo de la suerte"], "Un oso de peluche"),
    ("En el capítulo 'La boda de Lisa', ¿de dónde es su prometido?", ["Inglaterra", "Gales", "Escocia", "Irlanda"], "Inglaterra"),
    ("¿Qué identidad falsa adopta Homero para hacerse pasar por el esposo de Selma ante las autoridades asiáticas?", ["Un multimillonario monarca petrolero", "Un general de ejército estadounidense", "Un Buda viviente", "Un acróbata chino"], "Un Buda viviente"),
    ("¿Qué personaje está obsesionado con Marge?", ["Artie Ziff", "Homero Simpson", "Disco Stu", "Moe Szyslak"], "Artie Ziff"),
    ("¿Quién quiere matar a Bart?", ["Sr. Burns", "Nelson", "Skinner", "Bob Patiño"], "Bob Patiño")
]

@app.route("/")
def inicio():
    datos_para_html = []
    for i, (pregunta, opciones, correcta) in enumerate(preguntas):
        opciones_mezcladas = opciones[:]
        shuffle(opciones_mezcladas)
        datos_para_html.append({
            "id": i, "numero": i + 1, "texto": pregunta, "opciones": opciones_mezcladas
        })
    return render_template("index.html", datos_preguntas=datos_para_html)

@app.route("/verificar", methods=["POST"])
def verificar():
    puntaje = 0
    total_preguntas = len(preguntas)
    html_resultados = ""
    
    for i, (pregunta, opciones, correcta) in enumerate(preguntas):
        seleccionada = request.form.get(f"respuesta_{i}")
        
        if seleccionada == correcta:
            puntaje += 1
            html_resultados += f"<div class='pregunta-repaso'><span style='color: green;'>✅</span> <b>{i+1}. {pregunta}</b><br>Tú respondiste: <b>{seleccionada}</b> (¡Correcto!)</div><hr style='border: 1px solid #eee;'>"
        elif seleccionada == None:
             html_resultados += f"<div class='pregunta-repaso'><span style='color: orange;'>⚠️</span> <b>{i+1}. {pregunta}</b><br>La dejaste en blanco. La correcta era: <b>{correcta}</b></div><hr style='border: 1px solid #eee;'>"
        else:
            html_resultados += f"<div class='pregunta-repaso'><span style='color: red;'>❌</span> <b>{i+1}. {pregunta}</b><br>Tú respondiste: <del>{seleccionada}</del>. La correcta era: <b>{correcta}</b></div><hr style='border: 1px solid #eee;'>"

    porcentaje_aciertos = (puntaje / total_preguntas) * 100
    
    if porcentaje_aciertos == 100:
        mensaje_final = "¡EXCELENTE! Eres el Sujeto de las Historietas (Jeff Albertson). Lo sabes todo."
        imagen_final = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHgxbHE0eG9tb2MxencyeGk4YWI1ODJ1ZWxsMzFtMHJtYm9peWxzZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6Mbsje9fXoeVzSVy/giphy.gif"
    elif porcentaje_aciertos >= 70:
        mensaje_final = "¡MUY BIEN! Tienes el nivel de conocimiento de Lisa Simpson."
        imagen_final = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTFjMmhpOTZpMDZuODI5Y2l3anUwc2lhYW5penRrZ3V6amZwMzljNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Bi9hWuzf53wt5IdUsm/giphy.gif"
    elif porcentaje_aciertos >= 40:
        mensaje_final = "NADA MAL... pero te equivocaste bastante. Nivel: Homero Simpson."
        imagen_final = "https://media.giphy.com/media/8EmeieJAGjvUI/giphy.gif"
    else:
        mensaje_final = "¡AY CARAMBA! Te falta ver mucha más televisión. Nivel: Rafa Gorgory."
        imagen_final = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHI4YnpwZzh2bzhvaGRhdjZibzhmaW5hOGN1djExM3Y1d241cDdhaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/amWPELxpf0DEA/giphy.gif"

    return render_template("resultados.html", 
                           puntaje=puntaje, 
                           total=total_preguntas, 
                           porcentaje=round(porcentaje_aciertos, 2), 
                           mensaje=mensaje_final,
                           imagen=imagen_final,
                           detalle_html=html_resultados)

if __name__ == '__main__':
    # Esto le permite a Render asignar dinámicamente el puerto del servidor
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
