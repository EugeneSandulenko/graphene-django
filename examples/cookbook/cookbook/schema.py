import cookbook.ingredients.schema
import cookbook.recipes.schema
import graphene

from graphene_django.debug import DjangoDebug


class Query(
    cookbook.ingredients.schema.Query,
    cookbook.recipes.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class IngredientMutations(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")
    create_ingredient = cookbook.ingredients.schema.CreateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=IngredientMutations)
