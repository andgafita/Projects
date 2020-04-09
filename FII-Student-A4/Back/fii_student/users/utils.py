from .models import FiiUser


def validate_user_details(data):
    email = data.get('email')
    rol = data.get('rol')
    an_studiu = data.get('an_studiu')
    grupa = data.get('grupa')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if email is None:
        return u'Completeaza campul email.'
    if email and FiiUser.objects.filter(email=email).exists():
        return u'Exista deja un user cu aceasta adresa de email.'
    elif 'info.uaic.ro' not in email:
        return u'Adresa de email introdusa nu apartine domeniului facultatii.'
    if not (email.endswith('students.info.uaic.ro') or email.endswith('profs.info.uaic.ro')):
        return u'Email-ul nu apartine facultatii.'
    if rol is not None:
        if 'Student' in rol:
            # print(email.split('@')[1])
            if not email.split('@')[1].endswith('students.info.uaic.ro'):
                return u'Adresa de email a unui student trebuie sa contina @students.info.uaic.ro'
        if 'Profesor' in rol:
            if not email.split('@')[1].endswith('profs.info.uaic.ro'):
                return u'Adresa de email a unui profesor trebuie sa contina @profs.info.uaic.ro'
            elif an_studiu is not None and an_studiu != '-':
                return u'Profesorii nu au an de studiu'
            elif grupa is not None and grupa != '-':
                return u'Profesorii nu au grupa de studiu'

        if 'Masterand' in rol:
            if an_studiu is not None and an_studiu not in ['-', 'I', 'II']:
                return u'Masteranzii pot fi doar in anul I sau II'
        if 'Doctorand' in rol:
            if grupa is not None and grupa != '-':
                return u'Doctoranzii nu au grupa de studiu'
    if last_name.lower() not in email.lower() or first_name.lower() not in email.lower().split('@')[0].split('.'):
        return u'Numele si prenumele trebuie sa corespunda cu cele din email'

    return None
