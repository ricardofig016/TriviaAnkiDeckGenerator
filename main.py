import time
from bs4 import BeautifulSoup
from selenium import webdriver
import genanki

url = "https://www.randomtriviagenerator.com/"
driver = webdriver.Chrome()

answer = []

try:
    while len(answer) < 1000:
        driver.get(url)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        cards = soup.find_all("md-card-content")

        for i in range(0, len(cards), 2):
            ans = [cards[i].get_text(), cards[i + 1].get_text()]
            if not ans in answer:
                answer.append(ans)
        print(len(answer))

except KeyboardInterrupt:
    pass

print(answer)

driver.quit()

model = genanki.Model(
    model_id="Trivia_Question_Model",
    name="Trivia Question",
    fields=[{"name": "Subject"}, {"name": "Question"}, {"name": "Answer"}],
    templates=[
        {
            "name": "{{Subject}}",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        }
    ],
)

deck = genanki.Deck(29348752, "Trivia Deck")

for ans in answer:
    note = genanki.Note(model=model, fields=["Subject", ans[0], ans[1]])
    deck.add_note(note)

package = genanki.Package(deck)
package.write_to_file("my_trivia_deck.apkg")
