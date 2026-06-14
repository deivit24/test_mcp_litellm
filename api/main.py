import random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MCP Server Test",
    description="David random facts and frequently asked questions about Japan.",
    version="1.0.0",
)

DAVID_FACTS = [
    "David Salazar Random Fact: Favorite anime is between Hunter X Hunter and Vinland Saga",
    "David Salazar Random Fact: Wanted to be a WWE Wrestler when I was around 8 or 9 years old",
    "David Salazar Random Fact: Wants to live in Montana",
    "David Salazar Random Fact: Has 76 first cousins",
    "David Salazar Random Fact: Favorite cuisine is Japanese but favorite dish is Szechuan Mala Chicken",
]


class DavidFact(BaseModel):
    fact: str


class FAQItem(BaseModel):
    question: str
    answer: str


class FAQResponse(BaseModel):
    faqs: list[FAQItem]


FAQ_DATA: list[FAQItem] = [
    FAQItem(
        question="Do I need a visa to visit Japan?",
        answer="Citizens of about 68 countries can enter Japan visa-free for short stays (typically 90 days). Check the Japanese Ministry of Foreign Affairs website for your specific country.",
    ),
    FAQItem(
        question="What is the currency in Japan?",
        answer="The Japanese Yen (JPY, ¥). Japan is still largely a cash-based society, so carry yen — ATMs at 7-Eleven and Japan Post Bank accept foreign cards.",
    ),
    FAQItem(
        question="What language is spoken in Japan?",
        answer="Japanese is the official language. English is widely understood in tourist areas, major cities, and transportation hubs, but less so in rural regions.",
    ),
    FAQItem(
        question="Is Japan safe to travel?",
        answer="Japan is consistently ranked one of the safest countries in the world. Violent crime is extremely rare and lost wallets are frequently returned.",
    ),
    FAQItem(
        question="What is the best time to visit Japan?",
        answer="Spring (March–May) for cherry blossoms and autumn (September–November) for fall foliage are the most popular. Summer is hot and humid; winter is cold but great for skiing and illuminations.",
    ),
    FAQItem(
        question="What side of the road does Japan drive on?",
        answer="Japan drives on the left side of the road, similar to the UK and Australia.",
    ),
    FAQItem(
        question="Can I use my foreign credit card in Japan?",
        answer="Major cards (Visa, Mastercard) are accepted in hotels, department stores, and many restaurants. However, smaller shops, temples, and rural areas often require cash.",
    ),
    FAQItem(
        question="What is the tipping culture in Japan?",
        answer="Tipping is not customary in Japan and can even be considered rude. Excellent service is simply part of the culture — no tip expected or required.",
    ),
    FAQItem(
        question="How do I get around Japan?",
        answer="The Shinkansen (bullet train) connects major cities. Local trains and subways are excellent in urban areas. IC cards like Suica or Pasmo work on most transit systems nationwide.",
    ),
    FAQItem(
        question="What should I not do in Japan?",
        answer="Avoid eating or drinking while walking, speaking loudly on public transport, pointing directly at people, and wearing shoes indoors at homes or traditional restaurants.",
    ),
]


@app.get("/home", response_model=DavidFact, summary="Random David fact")
def home():
    """Returns a random fact about Me."""
    return DavidFact(fact=random.choice(DAVID_FACTS))


@app.get("/faq", response_model=FAQResponse, summary="Japan FAQ")
def faq():
    """Returns a list of frequently asked questions and answers about Japan."""
    return FAQResponse(faqs=FAQ_DATA)
