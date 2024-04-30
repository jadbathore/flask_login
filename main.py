from flask import Flask,render_template, request,redirect,url_for,session
from utilitaire import error as Uerr
from utilitaire import connect as Uconn
from utilitaire import emailCheck as Uemail
import bcrypt 
###############explication arborésance#####################
# static = dossier que l'on peux remplir avec un dossier js mais aussi img et css vu que j'utilise bootstrap et qu'il n'y a pas d'image ce n'est pas néssecaire
# templates = dossier de vu des html divisé en sous catégorie pour plus clarté
# utlitaire = un dossier comprenant plusier fichier de code python (juste pour le rangement) c'est fonction et class n'utilise pas de route 
# main.py = la ou il y a tout les fonction route nécessaire au login
###########################################################
# system de hashage bcrypt pour les mots de passe  
###########################################################
# pour tester une connection x 
# email : test@test
# mot de passe : test
###########################################################

app = Flask(__name__)
app.secret_key = "280dbeec2e777bec8de124a141dabc0057a6a38624c54c8376672660fd4dca7f"

@app.route("/")
def index():
    return render_template('home/index.html')

# redirection si une Uerr.Error et lever il y a deux cas :
# - si l'utilisateur essait trop de fois de s'inscrit depuis le login il est envoyer vers signin 
# - si l'utilisateur utilise un mail deja dans la base de donnée depuis le signin il est renvoyer vers le login
@app.route('/login', methods=['POST','GET'])
def login():   
    if "compteur" not in session:
        session['compteur'] = 0
        print(session['compteur'])
    if(request.method == "POST"):
        connect = Uconn.connect_func()
        cursor = connect.cursor()
        data = request.form
        mail = data.get("email")
        mdp = data.get("password")
        sql = "SELECT email,password FROM users WHERE email= %s"
        cursor.execute(sql,(mail,))
        result = cursor.fetchone()
        try:
            if(session['compteur'] and session['compteur'] >= 3):
                erreur = Uerr.Error("êtes vous sur d'avoir un indefiant")
                raise erreur
            else :
                if(mail != '' and mdp != ''):
                    sql = "SELECT email,password FROM users WHERE email= %s"
                    cursor.execute(sql,(mail,))
                    result = cursor.fetchone()
                    print(result)
                    if(result):
                        nom,password = result
                        encodePassword_input = mdp.encode('utf-8')
                        encode_Password = password.encode('utf-8')
                        if((bcrypt.hashpw(encodePassword_input,encode_Password)) == encode_Password):
                            session['nom_utilisateur'] = nom
                            return redirect(url_for('index'))
                        else:
                            session['compteur'] += 1
                            raise Exception("Mot de passe non valide")
                    else:
                        session['compteur'] += 1
                        raise Exception("Addresse mail non valide")
                else:
                    session['compteur'] += 1
                    raise Exception("veuiller renseigner votre mail et mots de passe")
        except Exception as err:
            message = f"{err} ,vous ne pouvez pas vous connecter"
            return render_template('login/login.html',message = message)
        except Uerr.Error:
            message = erreur.__get__()
            session.pop("compteur",None)
            return redirect(url_for('signin',messageErr_login = message,mail = mail))
    else:
        errorCheck = request.args.get("messageErr_sign")
        if(errorCheck):
            mail = request.args.get("mail")
            return render_template("login/login.html",messageErr_sign = errorCheck,mail = mail)
    return render_template('login/login.html')


@app.route('/signin',methods=['POST','GET'])
def signin():
        if(request.method == "POST"):
            connect = Uconn.connect_func()
            cursor = connect.cursor()
            data = request.form
            mail = data.get('email')
            password = data.get('password')
            sub = data.get('sub')
            if(sub == 'Envoyer'):
                try:
                    if(mail != '' and password != ''):
                            if(mail.count("@") != 0):
                                if(len(password) >= 20 or len(mail) >= 20):
                                    raise Exception("le mots de passe ou l'email est trop long")
                                else:
                                    if(Uemail.test_mail(mail) == True):
                                        error = Uerr.Error("Email deja utilisé")
                                        raise error
                                    else:
                                        strippassword = password.strip()
                                        stripemail = mail.strip()
                                        encode_password = strippassword.encode('utf-8')
                                        salt = bcrypt.gensalt()
                                        crypted = bcrypt.hashpw(encode_password,salt=salt)
                                        data = (stripemail,crypted)
                                        sql = "INSERT INTO users (email,password) VALUES (%s,%s)"
                                        cursor.execute(sql,data)
                                        connect.commit()
                                        session['nom_utilisateur'] = stripemail
                                        return redirect(url_for('index'))
                            else :
                                raise Exception("veuillez renseignez un email valide")
                    else:
                        raise Exception("veuillez renseigner votre mail et le mots de passe que vous souhaiter enregistré")
                except Exception as err:
                    message = f"{err} ,vous ne pouvez pas vous inscrire"
                    return render_template('sign/signup.html',message = message) 
                except Uerr.Error:
                    message = error.__get__()
                    return redirect(url_for('login',messageErr_sign = message,mail = mail))
        else:
            errorCheck = request.args.get("messageErr_login")
            if(errorCheck):
                emailErr_login = request.args.get("mail")
                return render_template("sign/signup.html",messageErr_login = errorCheck,mail = emailErr_login)
        return render_template('sign/signup.html')

@app.route('/logout')
def logout():
    session.pop('nom_utilisateur',None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def route404(erreur):
    return render_template(
        'erreur/erreur.html',
        code = 404,
        message = "la page web demander n'existe pas."
    )

if __name__ == '__main__':  
    app.run(debug=True)



