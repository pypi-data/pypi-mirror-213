# filtro-python

The official Python API package for [filtro.ai](https://www.filtro.ai/). Empowering your applications with AI, while safeguarding sensitive data across all third-party models, in just a few lines of Python code. 

## ⚙️ Install

```bash
pip install filtro
```

## 🗣️ Usage

```py
from filtro import mask, clear

masked, mapping = mask(
    "Hi my name is Giovanni, I work at Google. What's up?"
)

from langchain.llms import OpenAI
llm = OpenAI(temperature=0.9)
response = llm(masked)

cleared = clear(response, mapping)
```

## 🥽 Examples

```py
python examples/basic.py
````


<details> <summary> Show output </summary>

[YOUR INPUT] Hi my name is Gianmarco Rengucci! I am a Software Engineer at Apple, here in Milan. Whats up?

[FILTRO.AI] Hi my name is Terri Clark! I am a Software Engineer at Compton-Krueger, here in Lake Erin. Whats up?

[OPENAI] Hey there Terri, nice to meet you! Im doing great, but Im curious to learn more about what you do at Compton-Krueger. Could you tell me a little bit about your role at the company?

[FILTRO.AI] Hey there Gianmarco, nice to meet you! Im doing great, but Im curious to learn more about what you do at Apple. Could you tell me a little bit about your role at the company?

</details>
