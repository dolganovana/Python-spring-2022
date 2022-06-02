from fastapi import APIRouter
import pandas as pd

df = pd.read_csv("eda.csv")
router = APIRouter()

@router.get('/recipes/query')
def find_recipe(query: str):
    mask = df["name"].apply(lambda x: query in x)
    return df[mask].to_dict(orient="index")

@router.get('/recipes/{recipe_id}')
def id_recipe(recipe_id: str) -> dict:
    return df[df["id"] == recipe_id].ro_dict()

@router.get('/recipes/random')
def random_recipe():
    return df.sample().to_dict

@router.get('/recipes/diet/')
def recipes_calories(calories: int, top_n: int) -> dict:
    resultat = df[df['cal'] <= calories]
    top_sorted = resultat.sort_values(by='cal').head(top_n)
    logger.info(f"{top_n} recipes that have less than {calories} ")
    return top_sorted.to_dict(orient='index')

@router.get('/recipes/most_difficult')
def recipes_difficult(difficulty: str, top_n: int) -> dict:
    ascending = True if difficulty == 'simple' else False
    new_df = pd.DataFrame().assign(id = df['id'], name = df['name'], steps = df['list_resipe'])
    new_df['difficulty'] = new_df.apply(lambda row: len(row.steps), axis=1)
    new_df.drop('steps', axis=1)
    top_sorted = new_df.sort_values(by='difficulty', ascending=ascending).head(top_n)
    return top_sorted.to_dict(orient='index')

@router.post('/recipes/new', status_code=201)
def new_recipe(recipe_json):
    id = recipe_json["id"]
    name = recipe_json["name"]
    ingridient = recipe_json["ingridients"]
    image = recipe_json["img_url"]
    order_recipe = recipe_json["recipe"]
    rec_keyword = "n/a"
    cal = recipe_json["nutrition info"]["callories"]
    protein = recipe_json["nutrition info"]["proteins"]
    carb = recipe_json["nutrition info"]["carbs"]
    rec_link = recipe_json["recipe_url"]
    fats = "n/a"
    list = [id, name, ingridient, image, order_recipe, rec_keyword, cal, protein, carb, rec_link, fats]
    total = pd. Series(list, index=df.columns)
    new_df = df
    new_df = new_df.append(total, ignore_index=True)

@router.post('/recipes/search')
def search_by_ingridients(ingridients: list):
    mask = df["ingridients"].apply(lambda x: ingridients in x)
    return df[mask].head(3)["name"].values
