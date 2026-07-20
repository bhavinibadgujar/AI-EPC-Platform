from backend.core.gemini import client

models = client.models.list()

for model in models:
    print(model.name)