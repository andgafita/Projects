import psycopg2
from utils.config import config

""" create tables in the PostgreSQL database"""


def create_tables():
    commands = (
       """
       DROP TABLE IF EXISTS news;
       """,
       """
       CREATE TABLE news (
         news_id SERIAL PRIMARY KEY,
         title VARCHAR(255),
         body VARCHAR,
         author_name VARCHAR(255),
           
          category VARCHAR(255),
          inserted_time TIMESTAMP DEFAULT now()
        )
        """, """
        INSERT INTO news(title, body, author_name, category)
            VALUES(E'Campionatul European de Securitate Cibernetică, în România. Înscrierile, până pe 5 aprilie', E'Este ultimul prilej pentru ca toţi românii pasionaţi de IT să se înscrie la faza naţională a Campionatului European de Securitate Cibernetică de anul acesta din toamnă. Competiţia va avea loc pentru prima oară în România, la Palatul Parlamentului. Scopul este de la le testa tinerilor europeni aptitudinile de „hackeri”.
    
    
        În Campionatul European de Securitate Cibernetică de anul acesta, se vor întrece peste 20 de echipe din toată Europa. Acestea sunt formate din 5 juniori şi 5 seniori cu vârste între 16 şi 25 de ani care să îşi reprezinte ţara în competiţie. Organizatorii aşteaptă ca românii pasionaţi de securitate cibernetică să se înscrie într-un număr căt mai mare la faza naţională.
    
        Anton Rog – director Cyberint: „Există un site, cybersecuritychallenge.ro. Avem deja 300 de tineri. Înscrierile se pot face până pe 5 aprilie. Etapa de selecţie iniţială presupune rezolvarea unui număr de probe. Cei mai buni 30, pentru că o să avem nevoie şi de rezerve la lot, vor fi selectaţi pentru stagiile de pregătire”.
    
        Astfel, pentru a se pregăti de campionat, tinerii sunt antrenaţi intensiv de specialişti în domeniul securităţii cibernetice.
    
        Andrei Avădanei – coordonator tehnic: „Scopul este să-i învăţăm anumite tehnici de exploatare, de pivotare, de atac în infrastructură, dar şi să protejeze anumite tehnologii. Rolul activităţii este acela de a selecta cei mai buni 10 finalişti. Am pregătit o serie de probleme şi provocări care vor simula foarte mult din ce vor simula în etapa finală”.
    
        Cătălin Aramă – director CERT.RO: „Este un eveniment important pentru că implică tinerii în cadrul acestui campionat. Noi vorbim de educaţie digitală, vorbim de educaţie cibernetică şi vorbim de nevoia unei culturi a riscului de securitate cibernetică de la vârste cât se poate de fragede”.
    
        De-a lungul timpului, România a reuşit să fie vicecampioană de două ori, iar anul trecut a ieşit pe locul 9.
    
        Matei Bădănoiu – participant anul trecut în echipa României: „Am fost la etapa din 2018. (….) Faza de calificare a fost puţin grea. Ai nevoie de un pic de experienţă şi recomand oricui. Chiar dacă nu crede că are putere în el să treacă de prima etapă, totuşi, să încerce. E o experienţă unică”.
    
        A cincea ediţie a Campionatului European de Securitate Cibernetică va avea loc în în România, la Palatul Parlamentului, între 9 şi 11 octombrie, anul acesta.', E'Cretu Marian', E'MATERII');
        """
        )
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
