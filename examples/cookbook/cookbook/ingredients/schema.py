import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient

# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.Node,)
        filter_fields = ["name", "ingredients"]


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        interfaces = (graphene.Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }


class Query(object):
    category = graphene.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = graphene.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class IngredientInput(graphene.InputObjectType):
    name = graphene.String()
    notes = graphene.String()
    category_id = graphene.Int()


class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientInput()

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientNode)

    @staticmethod
    def mutate(root, info, input):
        category = Category.objects.get(pk=input.category_id)
        ingredient = Ingredient(name=input.name, notes=input.notes, category=category)
        ingredient.save()
        ok = True
        return CreateIngredient(ok=ok, ingredient=ingredient)
