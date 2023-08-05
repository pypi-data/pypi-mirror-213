import webview
import sys
import json

STYLES = """
    <style>
        *{
            padding: 0px;
            margin: 0px;
        }

        h5{
            color: #D71920;
            padding: 1rem;
            padding-left: 1rem;
            Margin-left: 10rem;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 1rem;

        }
        ul {
            list-style-type: disc; /* Tipo de viñeta, en este caso un círculo lleno */
            margin: 0;
            padding: 0;
        }

        li {
            color:#D71920;
            margin: 0 0 0 1em; /* Margen izquierdo para que se vea la viñeta */
            font-family: Arial, Helvetica, sans-serif;
            font-size: 15px;
        }
        span{
            color: #757575;
            font-size: 15px;
            font-family: Arial, Helvetica, sans-serif;  
        }
        .btn{
            color: #D71920;
            border: 1px solid #D71920;
            border-radius: 20px;
            background: #FFFFFF 0% 0% no-repeat padding-box;
            box-shadow: 0px 2px 4px #00000029;
            font-size: 1rem;
            margin: 0.3rem;
            padding: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            width: 7.5rem;
            font-family: Arial, Helvetica, sans-serif;
        }   
        .btn-red{
            color: #FFFFFF ;
            background-color:#D71920 ;

        }
        .btn:hover{
            color: #B6040B;
            border: 1px solid #B6040B;
        }   
        .btn-red:hover{
            color: #FFFFFF ;
            background-color:#B6040B;
        }
        .btn:active{
            /* UI Properties */
            border: 1px solid #D71920 ;
            box-shadow: 5px 5px 5px #0000000F;
            border-radius: 25px;
            opacity: 1;
        }   
        .message{
            margin-top: 0.5rem;
            height: 3.5rem;
            max-width: 25rem;
            max-height: 3.5rem;
            margin-bottom: 1.5rem;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .exception {
            height: 1rem;
            max-width: 25rem;
            max-height: 1rem;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        p{
            font: normal;
            font-family: Arial, Helvetica, sans-serif;
            padding-bottom: 1rem;
            padding-left: 1rem;
            color: #616161;
            text-align: left;
        }
        .container{
            background-color: #FFFFFF;
            display: inline-block;
            width: 100%;
            padding: 0;
        }
        .byflex{
            display: flex;
        }
        .container-buttons{
            display: inline-block;
            float: right;
            margin-right: 1rem;
        }
        .container-message{
            float: right;
            width: 70%;
            padding-right: 1rem;
            margin-top: 1rem;
        }
        .container-icon{
            width: 20%;
            color:#D71920 ;
            display: inline-block;
            margin: 1rem;
            float: left;
        }
        /* clases nuevas */
        .container-titles{
            margin-top: 1rem;
            width: 49%;
            display: inline-block;
        }
        .container-locator label {
            font: normal;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 1rem;
            color: #616161;
            margin-right: 2rem;
        }
        .container-titles p {
            padding-bottom: 0.5rem;
        }
        .container-locator p {
            padding-bottom: 0.5rem;
        }
        .entity {
            display: inline-block;
            font: normal;
            font-family: Arial, Helvetica, sans-serif;
            padding: 0rem 0rem 1rem 1rem;
            color: #616161;
            text-align: left;
            max-width: 15rem;
            max-height: 1rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .container-locator {
            margin-top: 1rem;
            width: 49%;
            display: inline-block;
        }
        .container-options {
            width: 100%;
            display: inline-block;
        }
        .option{
            display: block;
            align-content: center;
            margin-left: 1rem;
            padding: 0px 0px 0.5rem 0px;
        }
        textarea {
            padding: 1rem;
            margin: 0.5rem 0rem 0rem 0.6rem;
            width: 33rem;
            height: 2rem;
            border: 1px solid #9E9E9E;
            border-radius: 9px;
            opacity: 1;
            resize: None;
            overflow: hidden;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 1rem;
            }
        textarea:focus {
            border-color: #707070; /* cambia el color del borde del textarea cuando está enfocado */
            box-shadow: 0 0 5px 0 #707070; /* agrega una sombra azul cuando está enfocado */
            outline: none;
            opacity: 1;
        }
        .opt-radio {
            background-color: #D71920;
            border: 2px solid #D71920;
            color: #D71920;
            font-size: 16px;
            padding: 10px;
        }
    </style>
    """
SCRIPTS = """
<script>
    function showResponse(response) {
        const container = document.getElementById(this.element)
        container.innerText = response.message
    }
    function cancelHeavyStuff() {
        pywebview.api.cancelHeavyStuff()
    }
    function retry() {
        pywebview.api.retry()
    }
    function refactor() {
        pywebview.api.refactor()
    }
    function report() {
        pywebview.api.report()
    }
    function save_refactor() {
        const expresion = document.getElementById('expresion');
        if (expresion.value != "") {
            if (document.getElementById('xpath').checked) {
                pywebview.api.save_refactor(expresion.value, 'xpath')
            }
            if (document.getElementById('id').checked) {
                pywebview.api.save_refactor(expresion.value, 'id')
            }
            if (document.getElementById('name').checked) {
                pywebview.api.save_refactor(expresion.value, 'name')
            }
        }
        expresion.focus()
    }
    function return_home() {
        pywebview.api.return_home()
    }
</script>
"""


class Debugger:
    """
        Debugger recibe como dato de entrada en su constructor un diccionario compuesto de la siguiente forma:
        metadata = {
        "FRAMEWORK":"Selenium",
        "ENTITY": "<input>_nombre_usuario asdasd asd asdasdasdas",
        "EXCEPTION": "AlgunErrorException",
        "MESSAGE" : "Paso esto, por favor arreglalo o reportalo.",
        "LOCATOR TYPE": "xpath",
        "VALUE TO FIND": "//div/div/input",
        "JSON PATH": "C:\testing-automation\projects\Fisa\src\pages\Login.json",
        "JSON STRING": {'<input>_Nombre_de_usuario': {'GetFieldBy': 'Xpath', 'ValueToFind': "//input[@id='inputEmail']"}, '<input>_Password': {'GetFieldBy': 'Xpath', 'ValueToFind': "//input[@id='inputPassword']"}},
        "CASE NAME": "test_000_alta_de_usuario_fulano"
        }
    """

    def __init__(self, metadata) -> None:
        Debugger.metadata = Debugger.normalizer_metadata(metadata)
        Debugger.api = Api()
        Debugger.api.set_code(2)
        Debugger.pages = Debugger.build_pages()
        Debugger.window = webview.create_window(f'Debugger 3.0 - {Debugger.metadata["FRAMEWORK"]}',
                                                html=Debugger.pages["HOME"], js_api=Debugger.api,
                                                height=300, width=600, resizable=False)
        Debugger.api.set_window(Debugger.window)
        Debugger.api.set_pages(Debugger.pages)
        webview.start()

    @classmethod
    def normalizer_metadata(cls, metadata):
        # agregar condicion (de validacion)
        with open(metadata["JSON PATH"], "r", encoding='utf8') as read_file:
            metadata["JSON STRING"] = json.loads(read_file.read())
            read_file.close()
        metadata["MESSAGE"] = str(metadata["MESSAGE"]).split("--")[-1].replace("<", "&lt;").replace(">", "&gt;")
        metadata["ENTITY"] = (str(metadata["ENTITY"]).replace("<", "&lt;")).replace(">", "&gt;")
        metadata["JSON"] = str(metadata["JSON PATH"]).split("\\")[-1]
        return metadata

    @classmethod
    def build_pages(cls):
        pages = {'HOME': Debugger.get_home(),
                 'REFACTOR': Debugger.get_form_refactor()
                 }
        return pages

    @classmethod
    def get_html(cls, screen):
        if screen.upper() == "HOME":
            return Debugger.get_home()
        if screen.upper() == "REFACTOR":
            return Debugger.get_form_refactor()

    @classmethod
    def get_locator(cls, locator):
        if locator.upper() == str(Debugger.metadata["LOCATOR TYPE"]).upper():
            return "checked"
        if locator.upper() == str(Debugger.metadata["LOCATOR TYPE"]).upper():
            return "checked"
        if locator.upper() == str(Debugger.metadata["LOCATOR TYPE"]).upper():
            return "checked"

    @classmethod
    def get_home(cls):
        home = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            {STYLES}
            <body>
                <div class="container">
                    <h5>Ah ocurrido un error inesperado.</h5>
                    <div class="container-icon">
                        <svg viewBox="0 0 640 683" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M427.533 1.3333C423.933 2.79996 411.133 18.1333 408.6 24C405.667 31.0666 407 43.4666 411.4 50C413.4 52.9333 415 56.2666 415 57.3333C415 58.5333 412.2 62.6666 408.867 66.6666C401 75.8666 399.8 78.9333 402.2 84.5333C404.6 90.4 411 93.2 416.333 90.5333C420.867 88.2666 431.533 76 435.267 68.8C439.133 61.3333 438.2 48.9333 433.267 41.4666C429.533 35.8666 428.733 31.4666 431 30C431.8 29.4666 434.867 26.1333 437.667 22.4C445.133 13.0666 444.733 5.86663 436.733 1.59996C433.4 -0.266704 431.4 -0.266704 427.533 1.3333Z" fill="#D71920"/>
                            <path d="M468.733 8.80003C464.067 13.6 459.4 19.2 458.333 21.3334C453.4 30.8 454.6 42.8 461.133 51.6C462.867 53.8667 464.333 56.4 464.333 57.2C464.333 57.8667 461.4 62.1334 457.667 66.5334C449.933 75.8667 448.733 79.6 451.533 85.0667C453.8 89.6 455.933 90.6667 462.467 90.6667C466.333 90.6667 467.933 89.4667 475.4 80.6667C488.333 65.4667 490.2 53.7334 481.667 41.0667C479.533 37.8667 477.667 34.6667 477.667 34C477.667 33.2 480.733 29.2 484.333 24.9334C488.067 20.6667 491.4 15.6 491.8 13.8667C493 9.46669 490.2 3.33336 486.2 1.46669C479.933 -1.33331 477.267 -0.266641 468.733 8.80003Z" fill="#D71920"/>
                            <path d="M131.533 24.4C127.267 26.8 116.333 39.8667 113.533 46C109.133 55.3333 111 66.8 118.2 76.6667C120.6 79.8667 119.933 81.4667 111.4 92C103.533 101.6 103.667 108.8 112.067 113.2C117.533 116.133 122.467 113.733 130.333 104.533C140.067 92.9333 142.067 88.8 142.067 80C142.067 72.9333 138.333 62.8 135 60.6667C132.333 58.9333 133.8 55.0667 140.2 47.4667C143.933 43.0667 147.133 38.4 147.267 36.8C148.067 32 145.533 26.6667 141.533 24.6667C137 22.2667 135.267 22.2667 131.533 24.4Z" fill="#D71920"/>
                            <path d="M173.4 30.8C162.867 42.1333 159.933 48 159.933 57.6C159.933 63.8666 160.6 66.5333 164.067 72C166.467 75.7333 168.333 79.6 168.333 80.4C168.333 81.3333 165.667 85.0666 162.333 88.9333C153 99.4666 152.2 103.733 158.067 110.267C159.933 112.4 162.333 113.333 165.8 113.333C170.2 113.333 171.667 112.4 178.333 104.933C187.4 95.0666 191 88.1333 191 80C191 74 187.267 63.8666 184.467 62.1333C181.267 60.1333 183.133 54.4 189.667 46.5333C194.733 40.4 196.333 37.4666 196.333 34.1333C196.333 28.1333 192.733 24.1333 186.6 23.0666C181.667 22.2666 181.133 22.5333 173.4 30.8Z" fill="#D71920"/>
                            <path d="M528.733 48.5333C514.867 53.0666 503.133 64.7999 499 78.2666C494.467 92.9333 496.2 104.8 504.467 117.2C510.467 126.133 518.733 132.267 529.267 135.6C537.267 138.133 536.867 137.333 539 154.667C539.8 160.933 540.733 167.733 541.133 170L541.933 174L536.2 168.533C499.667 133.733 443.133 104.533 393.667 94.7999C369 89.9999 357.533 88.9333 331.667 88.9333C249.8 89.0666 176.467 117.867 119.8 172C103.4 187.733 89.2667 204.533 77.4 222.4C72.4667 230 68.3333 236 68.2 235.733C66.6 227.467 63.6667 200.533 64.3333 200.267C69 198.533 78.7333 190.4 82.4667 185.467C89.2667 176.133 91.4 168.267 90.7333 155.467C90.0667 142.267 85.8 133.467 75.9333 124.667C66.6 116.133 57 112.933 43.6667 113.6C22.8667 114.8 7.4 127.467 2.33334 147.733C-1.4 162.267 2.6 177.6 13 189.067C18.2 194.933 32.0667 202.667 37.1333 202.667C39.2667 202.667 40.4667 203.6 41 205.6C42.7333 213.867 49.8 271.6 49.2667 274C48.8667 275.467 45.9333 284.533 42.6 294C29.9333 330.667 25.2667 359.867 25.1333 402C25.1333 437.867 27.9333 460.667 36.3333 494.133C42.7333 519.467 49 536.267 59.8 557.333C111.133 657.2 216.467 698 369 677.2C437.533 667.867 494.333 648.933 536.333 621.333C595.133 582.667 628.067 529.333 637.8 457.333C640.2 439.733 639.8 396.667 637.133 375.333C629 311.867 605.8 252.4 572.333 209.333C568.867 205.067 568.333 202.267 564.467 172.667C562.067 155.067 559.933 139.333 559.667 137.733C559.133 135.467 560.2 134.133 564.867 131.467C573 126.667 581 117.067 584.467 108.133C588.2 98.1333 587.667 82.1333 583.267 73.1999C575.533 57.4666 561.267 47.9999 543.933 47.1999C538.2 46.9333 532.067 47.4666 528.733 48.5333ZM554.867 73.7333C567.667 82.2666 567.667 101.467 554.867 111.067C551 113.867 541.133 115.467 535.667 114.133C529.933 112.667 522.2 104.667 520.333 98.2666C514.733 78.1333 537.267 62.1333 554.867 73.7333ZM382.333 115.867C401.8 119.867 418.067 124.4 432.867 130.267C527 167.333 593.4 252.4 611.667 359.733C620.6 411.733 618.333 459.733 605 499.467C578.2 579.6 504.6 631.2 388.067 651.333C249 675.2 148.733 648.4 95.4 572.933C57.8 519.733 40.0667 434.533 50.4667 358C61 281.2 100.467 212.667 159.667 168C200.067 137.6 242.333 121.067 301 112.8C303.267 112.533 319.133 112.4 336.333 112.667C362.333 112.933 370.2 113.467 382.333 115.867ZM58.7333 139.6C65.1333 144.267 68.3333 150.4 68.3333 157.867C68.3333 178.8 44.8667 188.8 30.2 174.133C19.6667 163.6 22.2 146.8 35.5333 138.4C41 135.067 53.4 135.6 58.7333 139.6Z" fill="#D71920"/>
                            <path d="M297.667 193.6C291.4 194.4 288.067 195.6 285.8 198C279.8 204 282.333 214.533 290.333 216.533C291.933 216.933 299.533 216.4 307.133 215.333C319.133 213.733 321.4 212.933 324.067 210C327.933 205.333 327.933 199.467 323.667 195.333C320.067 191.6 314.067 191.2 297.667 193.6Z" fill="#D71920"/>
                            <path d="M306.333 238.267C286.733 240.933 271.8 243.6 270.067 244.8C263.933 248.667 264.6 258.133 271.133 262.933C274.6 265.6 274.733 265.6 311 260.8C331 258.133 348.467 255.333 349.8 254.667C353.267 252.8 356.333 247.867 356.333 244.267C356.333 239.333 349.4 233.333 344.067 233.467C341.667 233.6 324.733 235.733 306.333 238.267Z" fill="#D71920"/>
                            <path d="M432.333 267.6C430.467 267.867 376.867 274.933 313 283.467C249.267 291.867 192.467 299.867 186.867 301.333C131 315.067 89 359.2 77 416.667C74.0667 430.933 74.0667 458.4 77 472.667C83.5333 504.267 97.8 529.867 121.133 552C132.867 563.2 141.667 569.333 156.333 576.667C176.867 586.933 191.4 590.667 215.667 591.6C233.933 592.267 236.867 591.867 355.4 576C440.6 564.667 479.933 558.8 488.067 556.533C528.2 545.067 563.533 514.667 581 476.933C614.467 404.533 584.2 318.267 512.6 282.133C490.467 270.933 453.267 264.133 432.333 267.6ZM477.533 293.333C520.467 303.733 554.333 336.667 567.8 380.8C571.133 391.6 571.4 394.667 571.533 414C571.533 431.867 571 437.067 568.6 446C565 459.2 556.733 476.533 549 487.333C540.2 499.6 522.467 515.733 509.533 523.067C487.8 535.333 486.467 535.6 353.4 553.333C274.2 563.867 229 569.333 221.133 569.333C162.867 569.2 112.067 527.2 100.067 469.333C96.6 452.933 97.4 427.2 101.667 412C113.667 369.467 146.333 336.4 187.933 324.667C196.067 322.4 235.267 316.667 315 306.133C378.467 297.733 432.2 290.533 434.333 290.133C442.333 288.933 466.6 290.667 477.533 293.333Z" fill="#D71920"/>
                            <path d="M502.733 338.8C501.4 339.467 494.6 347.733 487.533 357.067C480.333 366.4 473.8 374.8 472.867 375.867C471.533 377.333 468.067 375.2 452.733 363.6C442.6 355.867 433 349.2 431.4 348.8C427.267 347.467 421 351.067 419 356C416.333 362.4 419 366.267 432.6 376.667C439.4 381.867 447.8 388.267 451.267 391.067L457.667 396.133L443 415.467C427.267 436.133 426.067 439.333 431 445.733C434.2 449.733 439 451.067 443.533 449.467C445.4 448.667 452.6 440.4 461 429.333C468.733 419.067 475.533 410.667 476.067 410.667C476.6 410.667 484.867 416.8 494.333 424.133C503.933 431.6 513.133 438.133 514.867 438.8C523.667 442.267 532.467 432 528.067 423.467C527.133 421.6 518.067 413.733 507.933 406L489.533 391.733L493.267 386.933C495.267 384.133 501.933 375.467 507.933 367.467C516.467 356.4 519 352.133 519 348.8C518.867 340.4 509.667 334.667 502.733 338.8Z" fill="#D71920"/>
                            <path d="M221.667 376.4C219.8 377.333 212.067 386.133 204.467 396C196.867 405.867 190.2 414.133 189.533 414.4C189 414.667 180.2 408.533 170.067 400.8C154.6 388.933 150.733 386.667 146.867 386.667C140.6 386.667 136.333 391.067 136.333 397.467C136.333 403.333 137.4 404.533 158.067 420C167.267 426.933 174.867 433.067 175 433.6C175 434.133 169.133 442.267 161.933 451.6C147.4 470.533 145.667 473.2 145.667 477.333C145.667 480.933 152.6 488 156.2 488C161.8 488 165.4 484.667 179 466.667C186.733 456.4 193.4 448.133 193.8 448C194.333 448 202.067 453.733 211.133 460.8C233.667 478.267 236.733 479.467 244.067 472.933C247.267 470 247.933 464.267 245.667 460C244.867 458.533 236.333 451.333 226.6 444C217 436.533 208.867 430 208.6 429.467C208.467 428.933 214.6 420.133 222.333 410C230.067 399.867 236.733 390.267 237.133 388.667C238.2 384.133 234.333 377.867 229.533 376.133C227.133 375.333 225.267 374.667 225.133 374.667C225 374.667 223.533 375.467 221.667 376.4Z" fill="#D71920"/>
                            <path d="M330.733 477.333C311.8 482.8 296.2 492 284.067 505.067C276.6 513.067 275.667 518.133 281 523.333C286.733 529.2 292.2 528 302.333 518.667C313.133 508.933 322.067 503.733 334.867 500C352.333 494.667 374.6 497.867 391.133 508C398.867 512.667 403.933 513.067 408.867 509.2C413.8 505.333 413.8 497.2 408.733 492.533C403.4 487.6 387.667 480.4 375.8 477.333C362.067 473.867 343.133 473.867 330.733 477.333Z" fill="#D71920"/>
                            </svg>
                    </div>
                    <div class="container-message">
                        <p>Clave: <b class="exception">{Debugger.metadata["EXCEPTION"]}</b></p>
                        <p class="message">{Debugger.metadata["MESSAGE"]}</p>
                    </div>
                    <div class="container-buttons">   
                        <button class="btn" onClick="retry()">Reintentar</button>
                        <button class="btn" onClick="refactor()">Refactorizar</button>
                        <button class="btn btn-red" onClick="report()">Reportar</button>
                    </div>
                </div>
                {SCRIPTS}
            </body>
            </html> 
            """
        return home

    @classmethod
    def get_form_refactor(cls):
        form_refactor = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            {STYLES}
            <body>
                <div class="container byflex">
                    <div class="container-titles">
                        <p>Repositorio de objetos: </p>
                        <p class="entity"><b>{Debugger.metadata["JSON"]}</b></p>
                        <p>Nombre del objeto:</p>
                        <p class="entity"><b>{Debugger.metadata["ENTITY"]}</b></p>
                    </div>
                    <div class="container-locator">
                        <p>Tipo de identificador</p>
                        <div class="container-options">
                            <div class="option">
                                <input class="opt-radio" type="radio" id="xpath" name="radio-group"{Debugger.get_locator("xpath")}>
                                <label for="radio1">xpath</label>
                            </div>
                            <div class="option">
                                <input class="opt-radio" type="radio" id="id" name="radio-group" {Debugger.get_locator("id")}>
                                <label for="radio2">id</label>
                            </div>
                            <div class="option">
                                <input class="opt-radio" type="radio" id="name" name="radio-group" {Debugger.get_locator("name")}>
                                <label for="radio3">name</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <textarea id="expresion" placeholder="Expresion" required>{Debugger.metadata["VALUE TO FIND"]}</textarea>
                </div>
                <div class="container-buttons">   
                    <button class="btn" onClick="save_refactor()">Guardar</button>
                    <button class="btn" onClick="return_home()">Volver</button>
                </div>
            {SCRIPTS}
            </body>
            </html> 
            """
        return form_refactor

    @classmethod
    def __repr__(cls) -> str:
        return f"{str(Debugger.api.get_code())}||{Debugger.metadata['VALUE TO FIND']}||{Debugger.metadata['LOCATOR TYPE']}"


class Api:
    code = 2  # status 2: exit

    def __init__(self):
        Api.cancel_heavy_stuff_flag = False
        Api._window = None
        Api._pages = None

    def set_window(self, window):
        Api._window = window

    def set_pages(self, pages):
        Api._pages = pages

    def retry(self):
        Api.set_code(Api, 1)  # status 1: retry
        webview.windows[0].destroy()
        sys.exit(1)

    def refactor(self):
        webview.windows[0].load_html(Api._pages["REFACTOR"])

    def save_refactor(self, value_to_find, type_locator):
        entity = Api.normalizer_json(Debugger.metadata["ENTITY"])
        Debugger.metadata["JSON STRING"][entity]['GetFieldBy'] = type_locator
        Debugger.metadata["JSON STRING"][entity]['ValueToFind'] = value_to_find
        Debugger.metadata["LOCATOR TYPE"] = type_locator
        Debugger.metadata["VALUE TO FIND"] = value_to_find
        with open(Debugger.metadata["JSON PATH"], "w", encoding="utf8") as file:
            json_strings = json.dumps(Debugger.metadata["JSON STRING"], indent=4, ensure_ascii=False)
            file.write(json_strings)
            file.close()
        Api.set_code(Api, 1)  # status 3: refactor
        webview.windows[0].destroy()
        sys.exit(1)

    def return_home(self):
        webview.windows[0].load_html(Api._pages["HOME"])

    def report(self):
        self.set_code(3)
        print("Función no disponible en esta versión.")

    def get_code(self):
        return Api.code

    def set_code(self, new_code):
        Api.code = new_code

    @classmethod
    def normalizer_json(cls, entity):
        entity = entity.replace("&lt;", "<").replace("&gt;", ">")
        return entity
