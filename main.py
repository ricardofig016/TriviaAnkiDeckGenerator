import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import genanki

url = "https://www.randomtriviagenerator.com/"
driver = webdriver.Chrome()
question = set()

try:
    while len(question) < 30000:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("md-card-content")
        subjects = soup.find_all(
            "div",
            class_="Card_category-text__1i-2p col-center padding-sm padding-left-none padding-right-none xl layout-column flex",
        )
        for i in range(0, len(subjects), 2):
            q = [
                subjects[i].get_text(),
                cards[i].get_text(),
                cards[i + 1].get_text(),
            ]
            question.add(tuple(q))

        print(f"questions scraped: {len(question)}")

except KeyboardInterrupt:
    pass

driver.quit()

guess_answer_html = """<p><b>{{Answer}}</b></p>"""

model = genanki.Model(
    model_id=20983477,
    name="Trivia Question",
    fields=[{"name": "Subject"}, {"name": "Question"}, {"name": "Answer"}],
    templates=[
        {
            "name": "Trivia",
            "qfmt": "{{Question}}",
            "qfmt": '<p class="light">{{Subject}}</p>  <p><b>{{Question}}</b></p>',
            "afmt": '{{FrontSide}} <hr id="answer"> ' + guess_answer_html,
        }
    ],
    css="""
            .card {
                font-family: arial;
                font-size: 18px;
                text-align: left;
                color: black;
                background-color: white;
                line-height:1.45;
                text-align:center;
                background-color:#f9f9f9;
            }
            .small {
                font-size:13px;
                font-weight:bold;
            }
            .light {
                color:#b0b0b5;
            }
            img {
                border:2px solid white;
            }
        """,
)

deck = genanki.Deck(29348752, "Trivia Deck")

for q in question:
    note = genanki.Note(model=model, fields=[q[0], q[1], q[2]])
    deck.add_note(note)

package = genanki.Package(deck)
package.write_to_file("my_trivia_deck.apkg")
